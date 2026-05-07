"""
Create PDB-SWE dataset from SWE-smith instances.

Loads SWE-smith instances from HuggingFace or a local .json/.jsonl file,
filters for single-file Python patches, extracts buggy file content via
Docker, recovers the clean (pre-bug) content by reverse-applying the patch,
computes gt_diff, and writes a PDB-format JSON file.

Each output entry:
  task_id          - same as instance_id
  gt_solution      - clean file content (pre-bug)
  buggy_code       - buggy file content (post-bug-patch)
  gt_diff          - file_diff(buggy_code, gt_solution)
  task_prompt      - problem_statement from SWE-smith
  target_file      - relative path of the modified .py file
  bug_count        - number of diff hunks in the patch (≥ 1)
  + all original SWE-smith fields (image_name, FAIL_TO_PASS, etc.)

Usage:
  python src/create_swesmith_data.py \\
      --instances SWE-bench/SWE-smith \\
      --output dataset/swesmith/data/pdb_swe.json \\
      --max_instances 300 \\
      --workers 2

  # Or from a local file:
  python src/create_swesmith_data.py \\
      --instances path/to/instances.jsonl \\
      --output dataset/swesmith/data/pdb_swe.json
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# SWE-smith and SWE-bench live under dataset/swesmith/install/
_INSTALL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset", "swesmith", "install")
for _p in [os.path.join(_INSTALL_DIR, "SWE-smith"), os.path.join(_INSTALL_DIR, "SWE-bench")]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import argparse
import json
import re
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import docker
import tqdm

from utils import apply_unified_patch, file_diff

DOCKER_WORKDIR = "/testbed"
DOCKER_USER = "root"


# ─── Patch helpers ────────────────────────────────────────────────────────────

_DIFF_GIT_RE = re.compile(r'^diff --git a/(.+) b/(.+)$', re.MULTILINE)


def get_changed_files(patch_str: str) -> list[str]:
    """Return list of file paths changed in a unified diff."""
    return [m.group(2) for m in _DIFF_GIT_RE.finditer(patch_str)]


def is_single_python_file(patch_str: str) -> bool:
    """True iff the patch modifies exactly one .py file (no other files)."""
    files = get_changed_files(patch_str)
    return len(files) == 1 and files[0].endswith('.py')


def count_hunks(patch_str: str) -> int:
    """Count @@ hunk headers in the patch (proxy for number of bug changes)."""
    return len(re.findall(r'^@@ ', patch_str, re.MULTILINE))


# ─── Docker helpers ───────────────────────────────────────────────────────────

def _pull_image_if_needed(client: docker.DockerClient, image_name: str) -> bool:
    """Pull Docker image if not already present. Returns True on success."""
    try:
        client.images.get(image_name)
        return True
    except docker.errors.ImageNotFound:
        pass
    try:
        print(f"  Pulling {image_name}…")
        client.images.pull(image_name, platform="linux/x86_64")
        return True
    except Exception as e:
        print(f"  WARN: could not pull {image_name}: {e}")
        return False


def get_buggy_content_from_docker(
    client: docker.DockerClient,
    image_name: str,
    file_path: str,
) -> str | None:
    """
    Start a container from image_name, read the file at HEAD (buggy state),
    stop and remove the container, and return the file content.
    """
    container = None
    try:
        container = client.containers.create(
            image=image_name,
            command="tail -f /dev/null",
            detach=True,
            platform="linux/x86_64",
            mem_limit="4g",
        )
        container.start()
        result = container.exec_run(
            f"cat {DOCKER_WORKDIR}/{file_path}",
            workdir=DOCKER_WORKDIR,
            user=DOCKER_USER,
        )
        if result.exit_code != 0:
            return None
        return result.output.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Docker error for {image_name}/{file_path}: {e}")
        return None
    finally:
        if container is not None:
            try:
                container.stop(timeout=5)
            except Exception:
                pass
            try:
                container.remove(force=True)
            except Exception:
                pass


# ─── Per-instance processing ──────────────────────────────────────────────────

def process_instance(instance: dict, client: docker.DockerClient) -> dict | None:
    """
    Convert one SWE-smith instance into a PDB data entry.

    Returns None if the instance should be skipped (not single-file Python,
    Docker failure, patch reversal failure, etc.).
    """
    iid = instance["instance_id"]
    patch_str = instance.get("patch", "")

    # Filter: must modify exactly one Python file
    if not is_single_python_file(patch_str):
        return None

    target_file = get_changed_files(patch_str)[0]
    image_name = instance["image_name"]

    # Pull image
    if not _pull_image_if_needed(client, image_name):
        print(f"  [{iid}] skipped: image pull failed")
        return None

    # Get buggy file content from Docker
    buggy_code = get_buggy_content_from_docker(client, image_name, target_file)
    if buggy_code is None:
        print(f"  [{iid}] skipped: could not read {target_file} from container")
        return None

    # Recover clean (pre-bug) content by applying the patch in reverse
    gt_solution = apply_unified_patch(buggy_code, patch_str, reverse=True)
    if gt_solution is None:
        print(f"  [{iid}] skipped: reverse patch application failed")
        return None

    # Sanity check: the clean and buggy files should differ
    if gt_solution == buggy_code:
        print(f"  [{iid}] skipped: reverse patch produced no change")
        return None

    # Compute gt_diff in PDB line-level format
    _, _, gt_diff = file_diff(buggy_code, gt_solution, cleaned=True)
    if not gt_diff:
        print(f"  [{iid}] skipped: gt_diff is empty")
        return None

    bug_count = count_hunks(patch_str)

    return {
        # PDB required fields
        "task_id": iid,
        "gt_solution": gt_solution,
        "buggy_code": buggy_code,
        "gt_diff": gt_diff,
        "task_prompt": instance.get("problem_statement", ""),
        "target_file": target_file,
        "bug_count": bug_count,
        # SWE-smith fields (needed by SWESmithHandler.verify_unit_test)
        "instance_id": iid,
        "repo": instance.get("repo", ""),
        "image_name": image_name,
        "FAIL_TO_PASS": instance.get("FAIL_TO_PASS", []),
        "PASS_TO_PASS": instance.get("PASS_TO_PASS", []),
        "patch": patch_str,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def load_instances(instances_path: str) -> list[dict]:
    """Load SWE-smith instances from HuggingFace or a local file."""
    if instances_path.endswith(".json"):
        with open(instances_path) as f:
            data = json.load(f)
        return data if isinstance(data, list) else list(data.values())
    elif instances_path.endswith(".jsonl"):
        with open(instances_path) as f:
            return [json.loads(l) for l in f if l.strip()]
    else:
        # Treat as a HuggingFace dataset path
        from datasets import load_dataset
        ds = load_dataset(instances_path, split="train")
        return list(ds)


def main(args):
    print(f"Loading instances from {args.instances}…")
    all_instances = load_instances(args.instances)
    print(f"Loaded {len(all_instances)} total instances")

    # Pre-filter without Docker (cheap)
    single_py = [inst for inst in all_instances if is_single_python_file(inst.get("patch", ""))]
    print(f"  Single-file Python patches: {len(single_py)}")

    # Cap to max_instances
    if args.max_instances and len(single_py) > args.max_instances:
        single_py = single_py[:args.max_instances]
        print(f"  Capped to {len(single_py)} instances")

    # Prepare output directory
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load checkpoint (already processed)
    processed = []
    processed_ids = set()
    if output_path.exists() and not args.overwrite:
        processed = json.load(open(output_path))
        processed_ids = {e["task_id"] for e in processed}
        print(f"  Resuming: {len(processed_ids)} already done")

    remaining = [inst for inst in single_py if inst["instance_id"] not in processed_ids]
    print(f"  Processing {len(remaining)} instances with {args.workers} worker(s)…\n")

    client = docker.from_env()
    results = list(processed)

    def _worker(inst):
        try:
            return process_instance(inst, client)
        except Exception as e:
            print(f"  [{inst['instance_id']}] error: {e}")
            traceback.print_exc()
            return None

    if args.workers <= 1:
        for inst in tqdm.tqdm(remaining, desc="Processing"):
            entry = _worker(inst)
            if entry:
                results.append(entry)
                # Checkpoint after each success
                with open(output_path, "w") as f:
                    json.dump(results, f, indent=2)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(_worker, inst): inst for inst in remaining}
            for fut in tqdm.tqdm(as_completed(futures), total=len(futures), desc="Processing"):
                entry = fut.result()
                if entry:
                    results.append(entry)
                    with open(output_path, "w") as f:
                        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results)} instances saved to {output_path}")
    print(f"  Skipped: {len(remaining) - (len(results) - len(processed))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--instances",
        default="SWE-bench/SWE-smith",
        help="HuggingFace dataset name or path to local .json/.jsonl file",
    )
    parser.add_argument(
        "--output",
        default=os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "dataset", "swesmith", "data", "pdb_swe.json",
        ),
        help="Output JSON path (default: dataset/swesmith/data/pdb_swe.json)",
    )
    parser.add_argument(
        "--max_instances",
        type=int,
        default=350,
        help="Maximum single-file Python instances to process (default: 350)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="Parallel Docker workers (default: 2)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Ignore existing output file and start fresh",
    )
    args = parser.parse_args()
    main(args)

"""
gen_swesmith_data.py — Extract Python files from a SWE-smith Docker image and
create PDB-format data items for bug injection.

Usage
-----
python src/gen_swesmith_data.py \
    --image swesmith.x86_64.pandas-dev__pandas.95280573 \
    --max_files 30 \
    --min_lines 150 \
    --max_lines 750 \
    --output dataset/swesmith/data/pdb_swe_input.json

The output JSON is consumed by bug_generation.py:

    python src/bug_generation.py \
        --dataset_name swesmith \
        --input_file pdb_swe_input.json \
        --model_name openrouter/openrouter/free \
        --bug_per_time 5 \
        --dry_run   # remove for real run
"""
import argparse
import ast
import json
import os
import random
import sys
from pathlib import Path

# Make dataset/ importable
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))


def image_to_repo_key(image_name: str) -> str:
    """
    Extract the SWE-smith registry key (repo_name) from a Docker image name.

    Docker Hub format:  "swebench/swesmith.x86_64.msiemens_1776_tinydb.10644a0e"
    Legacy/dataset fmt: "swesmith.x86_64.msiemens__tinydb.10644a0e"
    Both → registry key: "msiemens__tinydb.10644a0e"

    The registry uses "__" as org/repo separator; the Docker image uses "_1776_"
    to avoid naming issues (Docker doesn't allow "__" in some contexts).
    """
    # Strip optional "swebench/" org prefix
    name = image_name.split("/")[-1]
    # Strip "swesmith.x86_64." prefix
    name = name.removeprefix("swesmith.x86_64.")
    # Normalise separator: _1776_ → __
    name = name.replace("_1776_", "__")
    return name


def list_testbed_python_files(
    container,
    min_lines: int = 150,
    max_lines: int = 750,
    exclude_patterns: tuple[str, ...] = ("test_", "_test.py", "/tests/", "/test/",
                                          "setup.py", "conf.py", "conftest.py",
                                          "docs/", "doc/", "examples/", "benchmarks/"),
) -> list[str]:
    """
    List Python files inside a Docker container's /testbed that meet size criteria.

    Returns file paths relative to /testbed/ (e.g., "pandas/core/algorithms.py").
    """
    result = container.exec_run(
        "find /testbed -name '*.py' -type f",
        user="root",
    )
    if result.exit_code != 0:
        return []

    all_files = result.output.decode("utf-8", errors="replace").splitlines()

    candidates = []
    for full_path in all_files:
        full_path = full_path.strip()
        if not full_path.startswith("/testbed/"):
            continue
        rel_path = full_path[len("/testbed/"):]

        # Filter by exclude patterns
        if any(pat in rel_path for pat in exclude_patterns):
            continue

        # Filter by line count
        wc_result = container.exec_run(
            f"wc -l {full_path}",
            user="root",
        )
        if wc_result.exit_code != 0:
            continue
        try:
            line_count = int(wc_result.output.decode().split()[0])
        except (ValueError, IndexError):
            continue

        if min_lines <= line_count <= max_lines:
            candidates.append((rel_path, line_count))

    return candidates


def get_file_content(container, rel_path: str) -> str | None:
    """Read the content of /testbed/{rel_path} from a running Docker container."""
    result = container.exec_run(
        f"cat /testbed/{rel_path}",
        user="root",
    )
    if result.exit_code != 0:
        return None
    return result.output.decode("utf-8", errors="replace")


def extract_task_prompt(code: str, rel_path: str) -> str:
    """
    Extract a task description from a Python file.
    Uses the module docstring if present, otherwise falls back to file path.
    """
    try:
        tree = ast.parse(code)
        if (tree.body
                and isinstance(tree.body[0], ast.Expr)
                and isinstance(tree.body[0].value, ast.Constant)
                and isinstance(tree.body[0].value.value, str)):
            docstring = tree.body[0].value.value.strip()
            # Truncate to a reasonable length
            if len(docstring) > 400:
                docstring = docstring[:400].rsplit("\n", 1)[0] + "..."
            if docstring:
                return f"File: {rel_path}\n\n{docstring}"
    except SyntaxError:
        pass
    return f"Fix bugs in {rel_path}"


def create_data_item(
    image_name: str,
    repo_key: str,
    rel_path: str,
    code: str,
) -> dict:
    """
    Create one PDB-format data item from a Python file extracted from Docker.

    Fields required by bug_generation.py / SWESmithHandler.mark_editable_lines:
        task_id, gt_solution, task_prompt, repo, image_name, target_file
    """
    # Derive a stable task_id from image + file path
    safe_path = rel_path.replace("/", "__").replace(".py", "").replace(".", "_")
    task_id = f"{repo_key}.{safe_path}"

    return {
        "task_id": task_id,
        "gt_solution": code,
        "task_prompt": extract_task_prompt(code, rel_path),
        "repo": repo_key,           # registry key: "pandas-dev__pandas.95280573"
        "image_name": image_name,   # original image name for reference
        "target_file": rel_path,    # relative to /testbed/
    }


def extract_files_from_image(
    image_name: str,
    max_files: int = 30,
    min_lines: int = 150,
    max_lines: int = 750,
    seed: int = 42,
    prefer_files: list[str] | None = None,
) -> list[dict]:
    """
    Start a Docker container from image_name, extract Python files, and
    return a list of PDB data items.

    prefer_files: list of relative paths to prioritize (e.g. from SWE-smith dataset).
    These files are extracted first with a relaxed line-count window (50–3000 lines)
    so large core files aren't excluded. Random files fill any remaining slots.
    """
    try:
        import docker
    except ImportError:
        raise ImportError("docker-py not installed. Run: pip install docker")

    repo_key = image_to_repo_key(image_name)
    client = docker.from_env()

    print(f"[gen_swesmith_data] Starting container from {image_name}...")
    container = client.containers.create(
        image=image_name,
        command="tail -f /dev/null",
        detach=True,
        platform="linux/x86_64",
    )
    container.start()
    print(f"[gen_swesmith_data] Container {container.short_id} started.")

    try:
        items = []
        seen_paths = set()

        # --- Step 1: extract preferred files first (relaxed line-count window) ---
        if prefer_files:
            print(f"[gen_swesmith_data] Trying {len(prefer_files)} preferred file(s)...")
            for rel_path in prefer_files:
                if len(items) >= max_files:
                    break
                wc = container.exec_run(f"wc -l /testbed/{rel_path}", user="root")
                if wc.exit_code != 0:
                    print(f"[gen_swesmith_data]   - {rel_path} (not found, skipping)")
                    continue
                try:
                    lc = int(wc.output.decode().split()[0])
                except (ValueError, IndexError):
                    continue
                if not (50 <= lc <= 3000):
                    print(f"[gen_swesmith_data]   - {rel_path} ({lc} lines, out of relaxed range)")
                    continue
                code = get_file_content(container, rel_path)
                if code is None:
                    continue
                item = create_data_item(image_name, repo_key, rel_path, code)
                items.append(item)
                seen_paths.add(rel_path)
                print(f"[gen_swesmith_data]   + {rel_path} ({lc} lines) [preferred]")

        # --- Step 2: fill remaining slots from random candidates ---
        remaining = max_files - len(items)
        if remaining > 0:
            print("[gen_swesmith_data] Listing Python files for random fill...")
            candidates = list_testbed_python_files(
                container, min_lines=min_lines, max_lines=max_lines
            )
            candidates = [(p, lc) for p, lc in candidates if p not in seen_paths]
            print(f"[gen_swesmith_data] Found {len(candidates)} additional candidate files.")

            if len(candidates) > remaining:
                random.seed(seed)
                random.shuffle(candidates)
                candidates = candidates[:remaining]

            for rel_path, line_count in candidates:
                code = get_file_content(container, rel_path)
                if code is None:
                    print(f"[gen_swesmith_data] Could not read {rel_path}, skipping.")
                    continue
                item = create_data_item(image_name, repo_key, rel_path, code)
                items.append(item)
                print(f"[gen_swesmith_data]   + {rel_path} ({line_count} lines)")

        return items

    finally:
        print(f"[gen_swesmith_data] Stopping container {container.short_id}...")
        container.stop(timeout=5)
        container.remove(force=True)


def main():
    parser = argparse.ArgumentParser(
        description="Extract Python files from a SWE-smith Docker image for PDB bug injection."
    )
    parser.add_argument(
        "--image", required=True,
        help="SWE-smith Docker image name, e.g. swesmith.x86_64.pandas-dev__pandas.95280573",
    )
    parser.add_argument(
        "--output", default="dataset/swesmith/data/pdb_swe_input.json",
        help="Output JSON file path",
    )
    parser.add_argument(
        "--max_files", type=int, default=30,
        help="Maximum number of Python files to extract per image",
    )
    parser.add_argument(
        "--min_lines", type=int, default=150,
        help="Minimum number of lines in a file to include",
    )
    parser.add_argument(
        "--max_lines", type=int, default=750,
        help="Maximum number of lines in a file to include",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed for file selection",
    )
    parser.add_argument(
        "--append", action="store_true",
        help="Append to existing output file instead of overwriting",
    )
    parser.add_argument(
        "--prefer_files", type=str, default=None,
        help="Comma-separated list of file paths (relative to /testbed) to prioritize",
    )
    args = parser.parse_args()

    prefer = [f.strip() for f in args.prefer_files.split(",")] if args.prefer_files else None

    items = extract_files_from_image(
        image_name=args.image,
        max_files=args.max_files,
        min_lines=args.min_lines,
        max_lines=args.max_lines,
        seed=args.seed,
        prefer_files=prefer,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.append and output_path.exists():
        existing = json.load(open(output_path))
        # Deduplicate by task_id
        existing_ids = {d["task_id"] for d in existing}
        items = [d for d in items if d["task_id"] not in existing_ids]
        items = existing + items

    with open(output_path, "w") as f:
        json.dump(items, f, indent=2)

    print(f"\n[gen_swesmith_data] Saved {len(items)} items to {output_path}")


if __name__ == "__main__":
    main()

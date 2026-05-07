"""
compose_cross_file.py — Compose cross-file bug instances from single-file bugs.

Groups single-file bug instances by repo, then combines bugs from N distinct
files within the same repo into a single cross-file instance.  The result can
be fed into bug_correct.py with --cross_file.

Usage
-----
python src/compose_cross_file.py \
    --input results/swesmith/bug_data/buggy_code_XXXX.json \
    --files_per_instance 2 \
    --output results/swesmith/bug_data/cross_file_XXXX.json
"""
import argparse
import json
import itertools
from collections import defaultdict
from pathlib import Path


def _file_key(item: dict) -> str:
    """Return a key that identifies the source file (strips per-variant suffix)."""
    return item.get("target_file", item["task_id"])


def compose_cross_file(
    single_file_items: list[dict],
    files_per_instance: int = 2,
    bugs_per_file: int = 1,
) -> list[dict]:
    """
    Group single-file bugs by repo, then produce cross-file instances.

    For each repo, groups items by target_file, takes up to bugs_per_file bugs
    per file, then enumerates all combinations of files_per_instance distinct
    files to form cross-file instances.

    Returns a list of cross-file instance dicts, each with:
        task_id, cross_file, repo, image_name, bug_count, files[]
    """
    # Group by repo, then by file
    by_repo: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))
    for item in single_file_items:
        repo = item.get("repo", "")
        fkey = _file_key(item)
        by_repo[repo][fkey].append(item)

    cross_instances = []
    for repo, file_groups in by_repo.items():
        # Cap each file's pool at bugs_per_file
        capped: dict[str, list] = {
            fkey: items[:bugs_per_file] for fkey, items in file_groups.items()
        }
        file_keys = list(capped.keys())

        if len(file_keys) < files_per_instance:
            print(f"[compose_cross_file] repo {repo}: only {len(file_keys)} files, "
                  f"need {files_per_instance} — skipping")
            continue

        instance_idx = 0
        for file_combo in itertools.combinations(file_keys, files_per_instance):
            # Take first bug from each file in this combination
            files_in_instance = [capped[fk][0] for fk in file_combo]
            image_name = files_in_instance[0].get("image_name", "")
            total_bugs = sum(f.get("bug_count", 1) for f in files_in_instance)

            cross_instance = {
                "task_id": f"cross.{repo}.{instance_idx}",
                "cross_file": True,
                "repo": repo,
                "image_name": image_name,
                "bug_count": total_bugs,
                "files": [
                    {
                        "source_task_id": f["task_id"],
                        "target_file": f.get("target_file", ""),
                        "gt_solution": f.get("gt_solution", ""),
                        "buggy_code": f.get("buggy_code", ""),
                        "gt_diff": f.get("gt_diff", {}),
                        "bug_count": f.get("bug_count", 1),
                        "FAIL_TO_PASS": f.get("FAIL_TO_PASS", []),
                        "PASS_TO_PASS": f.get("PASS_TO_PASS", []),
                        "task_prompt": f.get("task_prompt", ""),
                    }
                    for f in files_in_instance
                ],
            }
            cross_instances.append(cross_instance)
            instance_idx += 1

    return cross_instances


def main():
    parser = argparse.ArgumentParser(
        description="Compose cross-file bug instances from single-file bugs."
    )
    parser.add_argument("--input", required=True,
                        help="Single-file bug JSON (output of bug_generation.py)")
    parser.add_argument("--output", required=True,
                        help="Output cross-file JSON path")
    parser.add_argument("--files_per_instance", type=int, default=2,
                        help="Number of files per cross-file instance (default 2)")
    parser.add_argument("--bugs_per_file", type=int, default=1,
                        help="Max bugs to take from each file (default 1)")
    args = parser.parse_args()

    items = json.load(open(args.input))
    cross = compose_cross_file(items, args.files_per_instance, args.bugs_per_file)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(cross, f, indent=2)

    print(f"[compose_cross_file] {len(items)} single-file bugs → {len(cross)} cross-file instances → {out}")


if __name__ == "__main__":
    main()

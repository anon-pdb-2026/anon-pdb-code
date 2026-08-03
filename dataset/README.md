# Adding a New Dataset to PDB

## Overview

Each dataset in PDB is represented by a **handler class** that implements five
dataset-specific operations. This guide walks you through adding support for a new dataset.

## Architecture

```
dataset/
    __init__.py          # Registry — maps dataset name strings to handler instances
    base.py              # DatasetHandler ABC — defines the interface all handlers share
    bigcodebench/
        README.md        # per-dataset install + usage
        handler.py       # BigCodeBenchHandler
        install/         # self-contained uv project with vendored evaluator
            pyproject.toml
            <package>/
            .venv/       # created by `uv venv` (git-ignored)
    livecodebench/
        ...
    README.md            # this file
```

Callers throughout the codebase use `get_handler(dataset_name)` to obtain a handler, then
call its methods without needing to know which dataset is active. Each handler runs its
evaluator inside `dataset/<name>/install/.venv/` via `python -m <module>` — the parent
shell's environment is never touched, and there's nothing to activate or deactivate.

## Steps to Add a New Dataset

### 1. Create the dataset directory

```bash
mkdir -p dataset/<your_dataset_name>
touch dataset/<your_dataset_name>/__init__.py
```

### 2. Implement the handler class

Create `dataset/<your_dataset_name>/handler.py`:

```python
from dataset.base import DatasetHandler


class YourDatasetHandler(DatasetHandler):

    def preprocess(self, raw_data):
        """
        Transform raw data into PDB's standardized format.

        Must return a list of dicts, each with at least:
            "task_id": str
            "gt_solution": str
            "task_prompt": str
        Optionally:
            "test": str (unit test code)
        """
        processed_data = []
        for example in raw_data:
            processed_data.append({
                "task_id": example["id"],
                "gt_solution": example["solution"],
                "task_prompt": example["prompt"],
            })
        return processed_data

    def verify_unit_test(self, verify_file, gt_file=None,
                         timeout_per_task=20, timeout=1800):
        """
        Run unit tests using your dataset's evaluation harness.

        Must return: (fail_ids, correct_ids, fail_feedback)
            - fail_ids: list[str] of task IDs that failed
            - correct_ids: list[str] of task IDs that passed
            - fail_feedback: str or list with failure details
        """
        ...

    def build_verify_unit_test(self, log_file_prefix, results,
                               sol_field="solution"):
        """
        Build verification file(s) consumed by verify_unit_test().

        Returns: file path (str) or None if nothing to verify.
        """
        ...

    def save_formatted_gt(self, log_file_prefix, data):
        """
        Save ground truth in the format your evaluator expects.

        Returns: file path (str) or None if not needed.
        """
        ...
```

### 3. Decide on `mark_editable_lines`

The base class provides a **concrete default** `mark_editable_lines` that works for
Python code with starter-code frozen lines. It uses keyword-based heuristics to determine
which lines can be edited or deleted during bug injection.

- **If this default works for your dataset**: do nothing (it's inherited automatically).
- **If your dataset needs different rules**: override `mark_editable_lines(self, data)` in
  your handler.

### 4. Register the handler

In `dataset/__init__.py`, add your import and registry entry:

```python
from dataset.your_dataset_name.handler import YourDatasetHandler

# Add to _REGISTRY:
_REGISTRY["your_dataset_name"] = YourDatasetHandler()
```

### 5. Vendor the evaluator under `install/`

Each dataset gets its own self-contained uv project so `verify_unit_test` can shell out
without depending on a globally-installed CLI or a pre-activated conda env.

```bash
mkdir -p dataset/<your_dataset_name>/install
cd dataset/<your_dataset_name>/install
```

Drop the evaluator's Python package(s) and a `pyproject.toml` here. Use hatchling for
the build backend (matches the existing datasets):

```toml
[project]
name = "<your_evaluator>"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    # pin the eval harness's runtime deps
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["<your_evaluator_package>"]
```

Then create the venv and install:

```bash
uv venv --python 3.10
uv sync
```

Inside `handler.verify_unit_test`, build subprocess commands with the inherited
`self.venv_cmd(module, *args)` helper from `DatasetHandler`. It returns a list like
`["<install>/.venv/bin/python", "-m", module, *args]` and raises a clear error if the
venv hasn't been created yet:

```python
subprocess.run(
    self.venv_cmd("your_evaluator.cli", "--samples", verify_file),
    cwd=self.install_dir,
    check=True,
    timeout=timeout,
)
```

`self.install_dir` and `self.venv_python` are also available on the base class. The
subprocess opens its own venv for its lifetime and exits cleanly — no activate /
deactivate plumbing required.

Finally, write a `dataset/<your_dataset_name>/README.md` with Overview / Install (uv) /
Layout / Verification / Troubleshooting sections (mirror `dataset/bigcodebench/README.md`
or `dataset/livecodebench/README.md`).

### 6. Add your data files

Place raw data files in `data/<your_dataset_name>/`.

### 7. Verify test-suite adequacy (before bug generation)

PDB uses your dataset's unit tests as the semantic oracle for three things: validating
injected bugs (a bug is kept only if the suite fails on it), atomicity filtering, and
precision/recall scoring. A weak suite degrades *gracefully* on the first two, bugs the
suite cannot detect are filtered out, so the benchmark shrinks but never contains
undetectable bugs. The residual risk is at **scoring time**: a model patch that passes a
weak suite while being actually incorrect (a scoring false positive).

For reference, we audited this risk on PDB-Single (LiveCodeBench) by submitting 216
test-passing, ground-truth-differing model patches to LeetCode's official online judge:
4/216 were rejected, a 1.85% false-positive rate (see
`false_positive_testset.md` and `..._batch2.md` for the full audit).
Rejected patches had markedly lower edit-level precision than accepted ones (mean 0.25
vs. 0.45), so low-precision patches are where functional scoring is least reliable.

Before running bug generation on a new dataset, check and strengthen its suites:

1. **Coverage check.** Run the suite under a coverage tool on each
   ground-truth solution and confirm the editable lines are actually executed by at
   least one test. Lines never executed cannot host a detectable bug: drop them from
   injection, or drop the task if too few covered lines remain.

2. **Strengthen weak suites.** Options in increasing order of effort: LLM test
   amplification validated against the ground truth (keep only generated tests that the
   ground-truth solution passes), human-LLM collaborative test generation, or online-judge
   validation where available. Never add a test without first confirming the ground-truth
   solution passes it, a wrong expected output flips true positives into false negatives.

4. **Patch gaps with local regression tests.** For LiveCodeBench we ship a
   `tests_override.json` mechanism at
   `dataset/livecodebench/install/tests_override.json`: a JSON map from `question_id` to
   extra test cases, merged into the private test set at load time. Every downstream
   evaluation picks the extra tests up automatically. Mirror this pattern for your own dataset's harness.
   
### 8. Test

Run preprocessing to verify everything works end to end:

```bash
python src/preprocess.py --dataset_name your_dataset_name \
    --input_file your_data.json
```

## Method Reference

| Method | Purpose | Returns |
|---|---|---|
| `preprocess(raw_data)` | Raw data -> standardized format | `list[dict]` |
| `mark_editable_lines(data)` | Annotate which lines can be edited | `None` (mutates in-place) |
| `build_verify_unit_test(prefix, results, sol_field)` | Build test harness input file | file path or `None` |
| `verify_unit_test(verify_file, gt_file, ...)` | Run unit tests | `(fail_ids, correct_ids, feedback)` |
| `save_formatted_gt(prefix, data)` | Save ground truth for evaluator | file path or `None` |

## Existing Datasets

| Dataset | Status | Evaluation Tool | Install | Used by subset |
|---|---|---|---|---|
| `bigcodebench` | Complete | `bigcodebench.evaluate` (vendored v0.2.5) | `dataset/bigcodebench/install/` — `uv sync --extra eval` | `single`, `wild` |
| `livecodebench` | Complete | `lcb_runner.runner.custom_evaluator` | `dataset/livecodebench/install/` — `uv sync` | `single`, `wild` |
| `swesmith` | Complete | `swesmith.harness.valid` (Docker; vendored under `install/SWE-{smith,bench}/`) | none — vendored source trees, Docker images pulled at runtime | `wild` |

See each dataset's own `README.md` for full install + verification instructions.

"""
Bug correction (debugging) pipeline for PDB (Precise Debugging Benchmarking).

Given buggy code + task prompts, drives an LLM debugger through one or more
rounds of fix attempts, evaluates each round, and accumulates failed-attempt
feedback for the next round.

Round structure (see `eval_main`):
    - Round 1 calls `bug_correct` on raw buggy_data (or optionally reloads a
      previous round's results via --reload_first_round).
    - After each round, the Evaluator scores every attempt. Tasks that failed
      have their solution appended to `failed_attempts` (plus optional error
      messages) and their `debug_results` stripped so the next call to
      `bug_correct` re-attempts them.
    - Starting with round 2 the debug_mode is suffixed with "_with_feedback"
      so the Debugger signature consumes the accumulated failures.

Tolerance defaults (`DEFAULT_TOLERANCE_SINGLELINE`/`_MULTILINE` in config.py)
are picked based on --mode so scoring is fair to the bug granularity used.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import argparse
import copy
import itertools
import json
import time
import dspy
import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils import file_diff, make_file_context, patch_to_pred_diff
from module import Debugger
from evaluator import Evaluator
from api_config import resolve_api_key
from config import DEFAULT_TOLERANCE_MULTILINE, DEFAULT_TOLERANCE_SINGLELINE


def _fix_one_cross(item, debugger, args, rd):
    """Call the Debugger once per file in a cross-file instance."""
    log_entry = copy.deepcopy(item)
    if "debug_results" in log_entry:
        return log_entry
    log_entry["round"] = rd

    file_results = []
    for file_item in item.get("files", []):
        try:
            response = debugger(
                task_prompt=file_item.get("task_prompt", ""),
                buggy_code=file_item.get("buggy_code", ""),
                test_cases=file_item.get("test"),
                failures=None,
                mode=args.debug_mode,
            )
            raw_output = response.solution or ""
            pred_diff = file_diff(file_item["buggy_code"], raw_output, cleaned=True)[2]
            file_results.append({
                "target_file": file_item["target_file"],
                "solution": raw_output,
                "pred_diff": pred_diff,
            })
        except Exception as e:
            print(f"Error on {file_item.get('target_file')}: {e}")
            file_results.append({
                "target_file": file_item["target_file"],
                "solution": "",
                "pred_diff": {},
            })

    log_entry["debug_results"] = {
        "model": args.model_name,
        "file_results": file_results,
    }
    return log_entry


def bug_correct_cross(data, debugger, output_file, args, rd):
    """Run one debugging round for cross-file instances."""
    if not data:
        print("No cross-file data to correct; skipping.")
        return []

    ckpt_file = output_file + ".ckpt"
    ckpt = {}
    if os.path.exists(ckpt_file):
        try:
            ckpt = {item["task_id"]: item for item in json.load(open(ckpt_file))}
            print(f"Resuming from checkpoint: {len(ckpt)}/{len(data)} items done")
        except Exception:
            ckpt = {}

    results = [None] * len(data)
    for i, item in enumerate(data):
        if item.get("task_id") in ckpt:
            results[i] = ckpt[item["task_id"]]
        else:
            results[i] = copy.deepcopy(item)

    failed_indices = [i for i in range(len(results)) if "debug_results" not in results[i]]
    max_api_retries = 3

    def _save_checkpoint():
        done = [r for r in results if r is not None and "debug_results" in r]
        with open(ckpt_file, "w") as f:
            json.dump(done, f)

    for attempt in range(max_api_retries):
        if not failed_indices:
            break
        n_workers = getattr(args, "n_workers", 1)
        if n_workers <= 1:
            for i in tqdm.tqdm(failed_indices):
                results[i] = _fix_one_cross(results[i], debugger, args, rd)
                _save_checkpoint()
        else:
            with ThreadPoolExecutor(max_workers=n_workers) as pool:
                futures = {pool.submit(_fix_one_cross, results[i], debugger, args, rd): i
                           for i in failed_indices}
                for fut in tqdm.tqdm(as_completed(futures), total=len(futures)):
                    results[futures[fut]] = fut.result()
                    _save_checkpoint()
        failed_indices = [i for i in failed_indices if "debug_results" not in results[i]]

    for i in failed_indices:
        results[i]["debug_results"] = {"model": args.model_name, "file_results": []}

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    if os.path.exists(ckpt_file):
        os.remove(ckpt_file)
    return results


def _fix_one(item, debugger, args, rd):
    """Call the Debugger on one item and return the log entry."""
    log_entry = copy.deepcopy(item)
    if "debug_results" in log_entry:
        return log_entry
    log_entry["round"] = rd
    task_id = log_entry.get("task_id")
    buggy_code = log_entry.get("buggy_code")
    task_prompt = log_entry.get("task_prompt")
    unit_tests_code = log_entry.get("test", None)
    failed_attempts = log_entry.get("failed_attempts", None)
    try:
        debug_format = getattr(args, "debug_format", "code")
        if debug_format == "patch":
            target_file = log_entry.get("target_file", "solution.py")
            buggy_file_ctx = make_file_context(buggy_code, target_file)
            response = debugger(task_prompt=task_prompt, buggy_code=buggy_file_ctx,
                                test_cases=unit_tests_code, failures=failed_attempts,
                                mode=args.debug_mode)
            patch_str = response.solution or ""
            pred_diff, corrected = patch_to_pred_diff(patch_str, buggy_code)
            log_entry["debug_results"] = {
                "model": args.model_name,
                "solution": corrected,
                "pred_diff": pred_diff,
                "raw_patch": patch_str,
            }
        else:
            response = debugger(task_prompt=task_prompt, buggy_code=buggy_code, test_cases=unit_tests_code,
                                failures=failed_attempts, mode=args.debug_mode)
            raw_output = response.solution or ""
            log_entry["debug_results"] = {
                "model": args.model_name,
                "solution": raw_output,
                "pred_diff": file_diff(buggy_code, raw_output, cleaned=True)[2]
            }
    except Exception as e:
        # Omit debug_results so the retry loop re-attempts this item.
        print(f"Error processing task_id {task_id}: {e}")
    return log_entry


def bug_correct(data, debugger, output_file, args, rd):
    """Run one debugging round: call the Debugger on each still-unsolved item.

    Supports parallel execution via --n_workers. Checkpoints after each item
    to output_file + ".ckpt"; resumes from checkpoint on restart. Retries
    API failures with exponential backoff up to max_api_retries times.
    """
    if not data:
        print("No buggy data to correct; skipping correction phase.")
        return []

    # --- checkpoint load ---
    ckpt_file = output_file + ".ckpt"
    ckpt = {}
    if os.path.exists(ckpt_file):
        try:
            ckpt = {item["task_id"]: item for item in json.load(open(ckpt_file))}
            print(f"Resuming from checkpoint: {len(ckpt)}/{len(data)} items already done")
        except Exception:
            ckpt = {}

    results = [None] * len(data)
    for i, item in enumerate(data):
        if item.get("task_id") in ckpt:
            results[i] = ckpt[item["task_id"]]

    def _save_checkpoint():
        done = [r for r in results if r is not None and "debug_results" in r]
        with open(ckpt_file, "w") as f:
            json.dump(done, f)

    # only submit items not yet checkpointed
    pending = [(i, item) for i, item in enumerate(data) if item.get("task_id") not in ckpt]

    # --- main loop ---
    n_workers = getattr(args, "n_workers", 1)
    if n_workers <= 1:
        for i, item in tqdm.tqdm(pending):
            results[i] = _fix_one(item, debugger, args, rd)
            _save_checkpoint()
    else:
        with ThreadPoolExecutor(max_workers=n_workers) as pool:
            futures = {pool.submit(_fix_one, item, debugger, args, rd): i
                       for i, item in pending}
            for fut in tqdm.tqdm(as_completed(futures), total=len(futures)):
                results[futures[fut]] = fut.result()
                _save_checkpoint()

    # Retry items that came back without debug_results (API error).
    max_api_retries = getattr(args, "max_api_retries", 3)
    failed_indices = [i for i, r in enumerate(results) if r is not None and "debug_results" not in r]
    for attempt in range(1, max_api_retries + 1):
        if not failed_indices:
            break
        wait = 30 * (2 ** (attempt - 1))  # 30s, 60s, 120s
        print(f"API retry {attempt}/{max_api_retries}: {len(failed_indices)} items failed, retrying in {wait}s...")
        time.sleep(wait)
        if n_workers <= 1:
            for i in tqdm.tqdm(failed_indices):
                results[i] = _fix_one(results[i], debugger, args, rd)
                _save_checkpoint()
        else:
            with ThreadPoolExecutor(max_workers=n_workers) as pool:
                futures = {pool.submit(_fix_one, results[i], debugger, args, rd): i
                           for i in failed_indices}
                for fut in tqdm.tqdm(as_completed(futures), total=len(futures)):
                    results[futures[fut]] = fut.result()
                    _save_checkpoint()
        failed_indices = [i for i in failed_indices if "debug_results" not in results[i]]

    # Write empty solution for items that exhausted all retries.
    for i in failed_indices:
        task_id = results[i].get("task_id")
        buggy_code = results[i].get("buggy_code", "")
        results[i]["debug_results"] = {
            "model": args.model_name,
            "solution": "",
            "pred_diff": file_diff(buggy_code, "", cleaned=True)[2]
        }
        print(f"Permanently failed after {max_api_retries} retries: {task_id}, writing empty solution")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    if os.path.exists(ckpt_file):
        os.remove(ckpt_file)

    return results


def eval_main(args):
    """Round controller: load data/model -> loop rounds -> feed failures back."""
    data_dir = os.path.join("results", args.dataset_name, "bug_data")
    output_dir = os.path.join("results", args.dataset_name, "debug_results")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    if not args.eval_set_name:
        args.eval_set_name = os.path.splitext(os.path.basename(args.input_file[0]))[0]
    output_prefix = args.model_name.split("/")[-1]
    if args.output_prefix:
        output_prefix = args.output_prefix + args.model_name.split("/")[-1]

    # Load the dataset
    if len(args.input_file) == 1:
        input_file = os.path.join(data_dir, args.input_file[0])
        buggy_data = json.load(open(input_file, "r"))
    else:
        input_files = [os.path.join(data_dir, args.input_file[i]) for i in range(len(args.input_file))]
        buggy_data = list(itertools.chain.from_iterable([json.load(open(in_file, "r")) for in_file in input_files]))
    if (args.use_tests or args.use_claude_code) and not args.debug_mode.startswith("patch_"):
        args.debug_mode += "_unit"
        for d in buggy_data:
            assert "test" in d, "Not having test in data but using unit-test-based debug mode!"

    # Load the model (skipped when --skip_generation is set)
    debugger = None
    if not getattr(args, 'skip_generation', False):
        assert args.use_claude_code or args.model_name
        if args.use_claude_code:
            print("Using Claude Code autonomous agent mode")
            from claude_code_wrapper import ClaudeCodeGenerator
            generator_cor = ClaudeCodeGenerator(
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                timeout=args.timeout
            )
            debugger = Debugger(model=generator_cor)
        else:
            print(f"Using model: {args.model_name}")
            api_key = resolve_api_key(args.model_name, args.model_api_file)
            if args.model_name.split("/")[0] == "together_ai":
                generator_cor = dspy.LM(args.model_name, api_key=api_key, api_base='https://api.together.xyz/v1',
                                        temperature=args.temperature, max_tokens=args.max_tokens, num_retries=3)
            else:
                lm_kwargs = dict(temperature=args.temperature, max_tokens=args.max_tokens, num_retries=3)
                if api_key is not None:  # None means ADC (e.g. vertex_ai/)
                    lm_kwargs["api_key"] = api_key
                if getattr(args, 'reasoning_effort', None):
                    lm_kwargs["reasoning_effort"] = args.reasoning_effort
                generator_cor = dspy.LM(args.model_name, **lm_kwargs)
            dspy.settings.configure(lm=generator_cor)
            debugger = Debugger()

        # Dry-run: replace the LM with a mock so no API credit is consumed
        if getattr(args, 'dry_run', False):
            from unittest.mock import MagicMock
            mock_lm = MagicMock()
            mock_lm.return_value = ["```python\n# mock dry-run response\npass\n```"]
            dspy.settings.configure(lm=mock_lm)
            debugger = Debugger()
            print("DRY RUN: using mock LM, no API calls will be made")

    # init evaluator
    print(f"Init evaluator")
    if not args.eval_model_name:
        args.eval_model_name = args.model_name.split("/")[-1] if args.model_name else "claude_code"
    if not args.eval_set_name:
        args.eval_set_name = os.path.splitext(args.input_file)[0]
    evaluator = Evaluator(args)

    print(f"Enter debugging process")
    for rd in range(1, args.max_rounds + 1):
        print(f"Round {rd}")

        if getattr(args, 'skip_generation', False):
            existing_file = os.path.join(output_dir, output_prefix) + f"_on_{args.eval_set_name}_round_{rd}.json"
            if not os.path.exists(existing_file):
                raise FileNotFoundError(
                    f"No saved results found at {existing_file}. "
                    f"Run without --skip_generation first to generate them."
                )
            results = json.load(open(existing_file))
            print(f"Loaded {len(results)} saved results from {existing_file} (skipping generation)")
            if not args.no_eval:
                evaluator.run_evaluation(results=results, round=rd)

        elif rd == 1 and args.reload_first_round:
            results = json.load(open(args.reload_result_file))
            scores = json.load(open(args.reload_score_file))
            buggy_dict = {d["task_id"]: d for d in buggy_data}
            filtered_results = []
            for item in results:
                if item["task_id"] in buggy_dict:
                    if args.use_tests or args.use_claude_code:
                        item["test"] = buggy_dict[d["task_id"]]["test"]
                    filtered_results.append(item)
            results = filtered_results
            scores = {metric: {task_id: v for task_id, v in metric_dict.items() if task_id in buggy_dict} for
                      metric, metric_dict in scores.items()}
            evaluator.result_formatting(results)
            evaluator.scores = scores
            if args.error_msg:
                evaluator.unit_score("Unit score")
        else:
            # Run debugging process
            output_file = os.path.join(output_dir, output_prefix) + f"_on_{args.eval_set_name}_round_{rd}.json"
            if getattr(args, "cross_file", False):
                results = bug_correct_cross(buggy_data, debugger, output_file, args, rd)
            else:
                results = bug_correct(buggy_data, debugger, output_file, args, rd)

            # Run evaluation and save outputs
            if not args.no_eval:
                if getattr(args, "cross_file", False):
                    evaluator.run_cross_file_evaluation(results=results, round=rd)
                else:
                    evaluator.run_evaluation(results=results, round=rd)
            else:
                return

        if getattr(args, "cross_file", False):
            continue

        buggy_data = results
        for d in buggy_data:
            if not evaluator.success_unit(d["task_id"]):
                failed_attempt = d["debug_results"]["solution"]
                if args.error_msg and evaluator.error_msg and evaluator.error_msg[d["task_id"]]:
                    failed_attempt = f"{failed_attempt}\nWith error message:\n{evaluator.error_msg[d['task_id']]}"
                if "failed_attempts" in d:
                    d["failed_attempts"] += "\nFailed attempt {}\n{}\n".format(rd, failed_attempt)
                else:
                    d["failed_attempts"] = "Failed attempt {}\n{}\n".format(rd, failed_attempt)
                del d["debug_results"]

        if not args.debug_mode.endswith("_with_feedback"):
            args.debug_mode += "_with_feedback"
            print(f"Switching debug mode to {args.debug_mode}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_name", type=str, help="Dataset name", required=True)
    parser.add_argument("--input_file", nargs='+', help="Input buggy file path, under output/{dataset_name}",
                        required=True)
    parser.add_argument("--debug_mode", choices=["free", "minimal", "patch_free", "patch_minimal"],
                        default="minimal", type=str)
    parser.add_argument("--debug_format", choices=["code", "patch"], default="code",
                        help="Output format: 'code' (full corrected file) or 'patch' (unified diff).")
    parser.add_argument("--use_tests", action="store_true", help="Whether to use test cases")
    parser.add_argument("--cross_file", action="store_true",
                        help="Cross-file mode: input is a cross-file instance JSON produced "
                             "by compose_cross_file.py. Model is called once per file; "
                             "P/R numerators/denominators are summed across files.")
    parser.add_argument("--output_prefix", type=str, help="Output file path, under eval/{dataset_name}", default="")

    # Model arguments
    parser.add_argument("--model_name", type=str, help="Evaluation model name", default=None)
    parser.add_argument("--model_api_file", type=str, default=None,
                        help="Model API file under keys/ (optional, auto-resolved from model name)")
    parser.add_argument("--max_tokens", type=int, default=8000, help="Maximum number of tokens")
    parser.add_argument("--temperature", type=float, default=1.0, help="Temperature for the generator")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout for model execution (seconds)")
    parser.add_argument("--n_workers", type=int, default=4,
                        help="Parallel workers for the Debugger fix-loop. "
                             "Only the LLM step is parallelized; evaluation still runs serially.")

    # Eval results arguments
    parser.add_argument("--no_eval", action="store_true", help="No evaluation after correction if on")
    parser.add_argument("--eval_result_dir", type=str, default="results")
    parser.add_argument("--eval_model_name", type=str, default=None)
    parser.add_argument("--eval_set_name", type=str, default=None)
    parser.add_argument("--stride", type=int, default=2, help="Minimum stride between bug diffs")
    parser.add_argument("--mode", choices=["single", "multi"], default="single",
                        help="Bug mode. Controls the --tolerance default when not set explicitly.")
    parser.add_argument("--tolerance", type=int, default=None,
                        help=f"Per-block tolerance: extra predicted lines per matched GT block. "
                             f"0=strict. If unset, defaults to {DEFAULT_TOLERANCE_SINGLELINE} in "
                             f"--mode single and {DEFAULT_TOLERANCE_MULTILINE} in --mode multi.")

    # Iterative arguments
    parser.add_argument("--max_rounds", type=int, default=1, help="Maximum number of debugging rounds")
    parser.add_argument("--reload_first_round", action="store_true", help="Whether to reload first round results")
    parser.add_argument("--reload_result_file", type=str, default=1, help="The result file to reload")
    parser.add_argument("--reload_score_file", type=str, default=1, help="The score file to reload")
    parser.add_argument("--error_msg", action="store_true", help="Whether to provide error message")

    # Claude Code specific arguments
    parser.add_argument("--use_claude_code", action="store_true", help="Use Claude Code agent")
    parser.add_argument("--reasoning_effort", type=str, default=None,
                        choices=["low", "medium", "high", "xhigh", "max"],
                        help="Enable extended thinking for Claude 4+ models (e.g. high, xhigh, max)."
                             " Has no effect on models that do not support reasoning.")

    # Testing
    parser.add_argument("--dry_run", action="store_true",
                        help="Replace LLM with a mock that returns dummy output (no API credit used)")
    parser.add_argument("--skip_generation", action="store_true",
                        help="Skip LLM queries; load the previously saved debug_results file and re-run "
                             "evaluation only. Use this to re-evaluate after fixing a sandbox issue "
                             "without spending API credits again.")

    args = parser.parse_args()
    if args.tolerance is None:
        args.tolerance = (DEFAULT_TOLERANCE_MULTILINE if args.mode == "multi"
                          else DEFAULT_TOLERANCE_SINGLELINE)
    eval_main(args)

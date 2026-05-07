"""
Core diff utilities for PDB (Precise Debugging Benchmarking).

Provides line-level diff computation, diff application, block parsing, and
verification functions used throughout the pipeline.
"""
import json
import re
import tokenize
from io import StringIO
from tokenize import TokenError
import numpy as np
import difflib
DIFF_STR_PATTERN = re.compile(r"^(\d+): (.*) --> (.*)$")


def remove_comment_from_line(code_line: str):
    """
    Detect and remove comments from a single line of Python code. No used in the code.

    Returns:
        have_comment (bool)
        removed_comment_code_line (str)
    """
    try:
        tokens = tokenize.generate_tokens(StringIO(code_line).readline)
        for tok in tokens:
            if tok.type == tokenize.COMMENT:
                idx = tok.start[1]
                return True, code_line[:idx].rstrip()
        return False, code_line.rstrip()

    except TokenError:
        # Fallback for incomplete / invalid lines
        if " # " in code_line:
            idx = code_line.find("#")
            return True, code_line[:idx].rstrip()
        return False, code_line.rstrip()


def single_diff_to_str(diff):
    assert len(diff) == 1
    k, v = list(diff.items())[0]
    return f"{k}: {v['original']} --> {v['modified']}"


def str_to_single_diff(s):
    m = DIFF_STR_PATTERN.match(s)
    if not m:
        raise ValueError(f"String not in expected format: {s}")
    k, original, modified = m.groups()
    if original == "":
        tp = "Add"
    elif modified == "":
        tp = "Delete"
    else:
        tp = "Modify"
    return {str(k): {"type": tp, "original": original, "modified": modified}}


def get_indentation(s):
    """
    Returns the leading whitespace of a string.
    """
    indent = ""
    for char in s:
        if char == ' ' or char == '\t':
            indent += char
        else:
            break
    return indent


def rstrip_lines(code_str):
    """
    Format code to remove right indentation

    :param code_str: original code string
    :return: formatted_code with right indentation removed
    """
    return "\n".join([l.rstrip() for l in code_str.splitlines()])


def file_diff(str1, str2, cleaned=False):
    """
    Compare two file contents line by line, and construct a file diff, such that applying the line_diff_dict (using apply_diff function) on str1 in a reversed order, we get str2.

    :param str1: initial file contents as strings
    :param str2: goal file contents as strings
    :param cleaned: whether to clean the new empty line diff or not
    :return: (delete list, add list, line_diff_dict)
    the line_diff_dict is in format: {"line_number": ("type": xxx, "original": xxx, "modified": xxx)}
    """
    lines1 = [d.rstrip() for d in str1.splitlines()]
    lines2 = [d.rstrip() for d in str2.splitlines()]

    diff = list(difflib.ndiff(lines1, lines2))

    delete_list = []
    add_list = []

    line_num1 = 0
    line_num2 = 0

    for d in diff:
        code = d[0]
        text = d[2:]

        if code == " ":  # unchanged
            line_num1 += 1
            line_num2 += 1
        elif code == "-":  # deletion
            line_num1 += 1
            delete_list.append((line_num1, text))
        elif code == "+":  # addition
            line_num2 += 1
            add_list.append((line_num2, text))

    # Post-process for modifications:
    # If a deletion and an addition at the same line, treat it as "Modify".
    # Build a line_diff_dict without mutating while iterating.
    line_diff_dict = {}
    delete_ptr = 0
    add_ptr = 0
    while delete_ptr < len(delete_list) or add_ptr < len(add_list):
        # Add delta to compute the delta of add and delete operations before
        delete_add_delta = add_ptr - delete_ptr
        if delete_ptr >= len(delete_list):
            tp = "Add"
            original_text = ""
            line_no, modified_text = add_list[add_ptr]
            line_no -= delete_add_delta
            add_ptr += 1
        elif add_ptr >= len(add_list):
            tp = "Delete"
            modified_text = ""
            line_no, original_text = delete_list[delete_ptr]
            delete_ptr += 1
        else:
            delete_line_no = delete_list[delete_ptr][0]
            add_line_no = add_list[add_ptr][0]
            if delete_line_no + delete_add_delta < add_line_no:
                tp = "Delete"
                modified_text = ""
                line_no, original_text = delete_list[delete_ptr]
                delete_ptr += 1
            elif delete_line_no + delete_add_delta > add_line_no:
                tp = "Add"
                original_text = ""
                line_no, modified_text = add_list[add_ptr]
                line_no -= delete_add_delta
                add_ptr += 1
            else:
                tp = "Modify"
                line_no, original_text = delete_list[delete_ptr]
                _, modified_text = add_list[add_ptr]
                delete_ptr += 1
                add_ptr += 1
        while str(line_no) in line_diff_dict:
            line_no = f"{line_no} "
        line_diff_dict[str(line_no)] = {
            "type": tp,
            "original": original_text,
            "modified": modified_text
        }

    # Remove new line diff (optional, but should be used in evaluation)
    if cleaned:
        keys_to_delete = []
        for k, v in line_diff_dict.items():
            if v["original"].strip() == v["modified"].strip() == "":
                keys_to_delete.append(k)
        for k in keys_to_delete:
            del line_diff_dict[k]

    line_diff_dict = dict(sorted(line_diff_dict.items(), key=lambda item: (int(item[0]), item[1]["type"])))
    return delete_list, add_list, line_diff_dict


def apply_diff(original_code, diff, with_delta=False):
    """
    Apply diff on original code to get a modified code.

    :param original_code: original code string to apply diff
    :param diff: the diff in format {"line_number": ("type": xxx, "original": xxx, "modified": xxx)}
    :param with_delta: boolean variable
        when it is False, we apply diff_dict reversely as-is to the original code, normally used when building composition from a set of single bugs;
            For example, with the following diff
            {
                "24": {
                    "type": "Add",
                    "original": "",
                    "modified": "a=1"
                },
                "24 ": {
                    "type": "Add",
                    "original": "",
                    "modified": "a=2"
                },
            }
            when applying reversely, we will add to line 24 two times, first a=2 and then a=1.
            Note that we DO assume the input diff is sorted in this format.
        when it is True, we apply diff_dict reversely with some delta, normally used when constructing fixes to the buggy code, especially when there are multiple adds and deletes.
            For example, with the following diff
            {
                "24": {
                    "type": "Add",
                    "original": "",
                    "modified": "a=1"
                },
                "25": {
                    "type": "Add",
                    "original": "",
                    "modified": "a=2"
                },
            }
            when applying reversely, similarly, we have to add to line 24 (pushing the original content to line 25) two times, first a=2 and then a=1.
            Note that we DO NOT assume the input diff is sorted in this format.
    :return: modified code string
    """
    diffs = []
    for line_no, v in diff.items():
        diffs.append((int(line_no), v["type"], v["original"], v["modified"]))
    if with_delta:
        # We do not assume diffs are sorted when with_delta=True
        diffs.sort(key=lambda x: (x[0], x[1]))

    # Apply modifications
    code_lines = original_code.splitlines()
    delete_add_delta = 0
    for _, tp, orig, mod in diffs:
        if tp == "Add":
            delete_add_delta += 1
        elif tp == "Delete":  # Deletion
            delete_add_delta -= 1

    # Process from bottom to top to avoid messing up indices, put Delete first than Add if line number is the same
    for line_no, tp, orig, mod in diffs[::-1]:
        idx = line_no - 1  # 1-based to 0-based

        if tp == "Modify":
            if 0 <= idx < len(code_lines):
                code_lines[idx] = mod

        elif tp == "Add":
            delete_add_delta -= 1
            if with_delta and 0 <= idx - delete_add_delta <= len(code_lines):
                code_lines.insert(idx - delete_add_delta, mod)
            elif 0 <= idx <= len(code_lines):
                code_lines.insert(idx, mod)

        elif tp == "Delete":
            delete_add_delta += 1
            if 0 <= idx < len(code_lines):
                del code_lines[idx]

    mod_code = "\n".join([l.rstrip() for l in code_lines])
    return mod_code


def parse_diff_to_blocks(diffs, ordered=True):
    """
    Parse diffs into edit blocks, merging consecutive edits into one block of edits.

    :param diffs: the diff in format {"line_number": ("type": xxx, "original": xxx, "modified": xxx)}
    :param ordered: the diff is sorted by line number or not
    :return: a list of block diffs in order, each element in format {
        "block_start": start line number,
        "block_end": end line number,
        "diff": the block diff,
        "block_id": block numbering
    }
    """
    if not ordered:
        orig_diffs = list(sorted(diffs.items(), key=lambda x: (int(x[0]), x[1]["type"])))
    else:
        orig_diffs = list(diffs.items())

    set_del_mod = {"Delete", "Modify"}
    set_add = {"Add"}
    current_block = []
    all_blocks = []
    consecutive = True
    prev_tp, prev_line_no = None, None
    for line_no_str, edit in orig_diffs[::-1]:
        line_no = int(line_no_str)
        tp = edit["type"]

        # starting from the second last, check if consecutive edits
        # NOTE: [design] also merge Add(N) adjacent to Delete/Modify(N-1) since
        # file_diff represents code moves as Add+Delete at adjacent line positions.
        if prev_tp is not None:
            if tp in set_del_mod and line_no == prev_line_no - 1:
                consecutive = True
            elif tp in set_add and (line_no == prev_line_no or line_no == prev_line_no - 1):
                consecutive = True
            else:
                consecutive = False

        if consecutive:
            current_block.insert(0, (line_no_str, edit))
        else:
            all_blocks.insert(0, {
                "block_start": int(current_block[0][0]),
                "block_end": int(current_block[-1][0]),
                "diff": dict(current_block)
            })
            current_block = [(line_no_str, edit)]
        prev_tp = tp
        prev_line_no = line_no

    # add the remaining block if non-empty
    if len(current_block):
        all_blocks.insert(0, {
            "block_start": int(current_block[0][0]),
            "block_end": int(current_block[-1][0]),
            "diff": dict(current_block)
        })

    # numbering blocks
    for i, block in enumerate(all_blocks):
        if i == 0:
            stride_before = block['block_start'] - 1
        else:
            prev_block = all_blocks[i - 1]
            prev_block_end = prev_block['block_end']
            prev_type = list(prev_block['diff'].values())[0]['type']
            if prev_type == 'Add':
                stride_before = block['block_start'] - prev_block_end
            else:
                stride_before = block['block_start'] - prev_block_end - 1

        if i == len(all_blocks) - 1:
            stride_after = None
        else:
            next_block = all_blocks[i + 1]
            next_block_start = next_block['block_start']
            curr_type = list(block['diff'].values())[0]['type']

            if curr_type == 'Add':
                stride_after = next_block_start - block['block_end']
            else:
                stride_after = next_block_start - block['block_end'] - 1

        block['stride_before'] = stride_before
        block['stride_after'] = stride_after
        block["block_id"] = i

    return all_blocks


def expand_blocks_to_diff(blocks, ordered=True):
    """
    Expand code blocks into diffs.

    :param blocks: a list of block diffs in reverse order, each element in format {
        "block_start": start line number,
        "block_end": end line number,
        "diff": the block diff,
        "block_id": block numbering
    }
    :param ordered: the blocks are sorted by block number or not
    :return: a diff in format {"line_number": ("type": xxx, "original": xxx, "modified": xxx)}
    """
    if not ordered:
        ordered_blocks = sorted(blocks, key=lambda x: x["block_start"])
    else:
        ordered_blocks = blocks

    merged_diff = {}
    for block in ordered_blocks:
        merged_diff |= block["diff"]

    return merged_diff


def verify_block_diff(diff, block_count=-1, stride=0, max_lines_per_block=1, min_lines_per_block=1):
    """
    Verify each block has between min and max lines_per_block line diffs.

    :param diff: the diff dict
    :param block_count: expected number of blocks (-1 to skip check)
    :param stride: minimum gap between blocks
    :param max_lines_per_block: maximum edits per block
    :param min_lines_per_block: minimum edits per block (use 2 to enforce true multiline)
    :return: (passed, reason_string)
    """
    blocks = parse_diff_to_blocks(diff)
    if block_count >= 0 and len(blocks) != block_count:
        return False, f"Blocks count {len(blocks)} not equals to expected number {block_count}."
    block_end = -np.inf
    for i, b in enumerate(blocks):
        if b["block_start"] - block_end < stride:
            return False, (f"Block {i} starts at line {b['block_start']}, while previous one ends at line {block_end}, "
                           f"smaller than expected stride {stride}.")
        if len(b["diff"]) > max_lines_per_block:
            return False, f"Block {i} has {len(b['diff'])} line diffs, more than max {max_lines_per_block}."
        if len(b["diff"]) < min_lines_per_block:
            return False, f"Block {i} has {len(b['diff'])} line diffs, less than min {min_lines_per_block}."
        block_end = b["block_end"]
    return True, ""


def verify_block_single_diff(diff, block_count=-1, stride=0):
    """
    Verify each block has only a single line diff. Original single-line version.
    """
    return verify_block_diff(diff, block_count=block_count, stride=stride, max_lines_per_block=1)


def verify_span_diff(diff, max_span=30, min_changes=2, max_changes=30):
    """
    Span-based validation for multi-line bugs: all changed lines within a max_span
    line window, and total changed entries within [min_changes, max_changes].

    Unlike verify_block_diff, this allows non-contiguous blocks inside the span —
    capturing code-reorder bugs (Add + Delete at nearby positions) that file_diff
    represents as disjoint blocks.

    :param diff: the diff dict from file_diff
    :param max_span: max physical line range (max_line - min_line + 1)
    :param min_changes: minimum total changed entries (dict size)
    :param max_changes: maximum total changed entries
    :return: (passed, reason_string)
    """
    if not diff:
        return False, "Empty diff."
    line_nos = [int(str(k).strip()) for k in diff.keys()]
    span = max(line_nos) - min(line_nos) + 1
    total = len(diff)
    if span > max_span:
        return False, f"Span {span} exceeds max_span {max_span}."
    if total < min_changes:
        return False, f"Total changes {total} < min_changes {min_changes}."
    if total > max_changes:
        return False, f"Total changes {total} > max_changes {max_changes}."
    return True, ""


def make_file_context(code: str, file_path: str = "solution.py") -> str:
    """
    Format code with line numbers in SWE-bench style for LLM patch prompts.

    Example output:
        [start of solution.py]
        1 def foo(x):
        2     return x + 1
        [end of solution.py]
    """
    numbered = "\n".join(f"{i + 1} {line}" for i, line in enumerate(code.splitlines()))
    return f"[start of {file_path}]\n{numbered}\n[end of {file_path}]"


def _extract_patch_from_llm_output(text: str) -> str:
    """
    Extract a unified diff from LLM output, handling markdown code fences.

    Tries, in order:
      1. ```diff ... ``` or ```patch ... ``` fenced block
      2. Plain ``` ... ``` block that contains @@ markers
      3. Raw text if it already looks like a diff
    """
    import re
    fence = re.compile(r'```(?:diff|patch)?\n(.*?)```', re.DOTALL)
    for m in fence.finditer(text):
        candidate = m.group(1).strip()
        if '@@' in candidate:
            return candidate

    # Any fenced block that contains @@ (LLM may omit language tag)
    any_fence = re.compile(r'```[^\n]*\n(.*?)```', re.DOTALL)
    for m in any_fence.finditer(text):
        candidate = m.group(1).strip()
        if '@@' in candidate:
            return candidate

    # Raw text looks like a diff
    if '@@' in text:
        return text.strip()

    return ""


def apply_unified_patch(buggy_code: str, patch_str: str, reverse: bool = False) -> str | None:
    """
    Apply a unified diff patch string to buggy_code (pure Python, no external tools).

    When reverse=True the patch is applied backwards: '+' lines are treated as
    consumed (removed) and '-' lines as inserted (added), and hunk positions are
    taken from the dst (+) side of the @@ header instead of the src (-) side.
    This lets us recover the original clean file from a buggy one given the bug
    patch (as used by SWE-smith, where `patch` introduces the bug).

    Returns the patched code string, or None if the patch cannot be parsed/applied.
    Hunks are applied in reverse order to preserve line indices during multi-hunk patches.
    """
    import re

    hunk_re = re.compile(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@')
    patch_lines = patch_str.splitlines()

    # Locate hunk start positions
    hunk_starts = [i for i, l in enumerate(patch_lines) if hunk_re.match(l)]
    if not hunk_starts:
        return None

    # Parse each hunk
    hunks = []
    for idx, start in enumerate(hunk_starts):
        m = hunk_re.match(patch_lines[start])
        src_start = int(m.group(1))
        dst_start = int(m.group(2))
        apply_start = dst_start if reverse else src_start
        end = hunk_starts[idx + 1] if idx + 1 < len(hunk_starts) else len(patch_lines)
        body = [l for l in patch_lines[start + 1:end] if not l.startswith('\\')]
        hunks.append((apply_start, body))

    result = buggy_code.splitlines()

    # Apply in reverse so earlier hunks don't shift later line numbers
    for apply_start, body in reversed(hunks):
        removed = []   # lines consumed from source (context + deleted)
        added = []     # lines written to target (context + inserted)
        for line in body:
            if line.startswith('-'):
                if reverse:
                    added.append(line[1:])
                else:
                    removed.append(line[1:])
            elif line.startswith('+'):
                if reverse:
                    removed.append(line[1:])
                else:
                    added.append(line[1:])
            else:
                # space = context line; empty line in body treated as context too
                content = line[1:] if line.startswith(' ') else ''
                removed.append(content)
                added.append(content)

        start_idx = apply_start - 1            # convert to 0-based
        end_idx = start_idx + len(removed)
        end_idx = min(end_idx, len(result))    # clamp to actual file length

        result[start_idx:end_idx] = added

    return '\n'.join(result)


def patch_to_pred_diff(patch_str: str, buggy_code: str) -> tuple[dict, str]:
    """
    Convert an LLM-output unified diff into (pred_diff, corrected_code).

    pred_diff uses PDB's line-level format:
        {"line_no": {"type": "Modify"|"Add"|"Delete", "original": str, "modified": str}}

    Returns ({}, buggy_code) if the patch is empty, malformed, or cannot be applied.
    Internally applies the patch to buggy_code and runs file_diff() on the result,
    so coord system is consistent with gt_diff throughout the pipeline.
    """
    raw = _extract_patch_from_llm_output(patch_str)
    if not raw:
        return {}, buggy_code

    corrected = apply_unified_patch(buggy_code, raw)
    if corrected is None:
        return {}, buggy_code

    _, _, pred_diff = file_diff(buggy_code, corrected, cleaned=True)
    return pred_diff, corrected


if __name__ == "__main__":
    str1 = """def fc(n, target):
  R = len(n)
  L = 0
  while L <= R:
    mid = (R + L) // 2
    if n[mid] > target:
      R = mid
    else:
      R = L
      L = mid + 1"""
    str2 = """def fc(n, target):
  R = len(n) - 1
  L = 0
  while L < R:
    mid = R + L // 2
    if n[mid] > target:
      R = mid
    else:
      L = (R + L) // 2 + 1"""
    delete, add, json_diff = file_diff(str1, str2)
    print(json.dumps(json_diff, indent=2))
    print(apply_diff(str1, json_diff, True) == str2)

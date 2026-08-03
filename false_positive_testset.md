# False-Positive Testing Set — PDB-Single (LiveCodeBench)

108 patches: 12 per Table-3b model (seed=0), drawn from
a pool of 17496 test-passing, ground-truth-differing patches.
Submit each code block to the linked LeetCode problem; a rejection by
LeetCode's hidden tests marks a scoring false positive in PDB.

## 1. `3426_45` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/minimum-number-of-chairs-in-a-waiting-room/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minimumChairs(self, s: str) -> int:
        cnt, max_cnt = 0, 0
        for c in s:
            if c == "E":
                cnt += 1
                max_cnt = max(max_cnt, cnt)
            else:
                cnt -= 1
        return max_cnt
```

## 2. `3700_31` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/subsequences-with-a-unique-middle-mode-i/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
  def __init__(self):
    self.MOD = 1_000_000_007

  def subsequencesWithMiddleMode(self, nums: list[int]) -> int:
    n = len(nums)
    ans = 0
    left = collections.Counter()
    right = collections.Counter()

    for i in range(2):
      left[nums[i]] += 1

    for i in range(2, n):
      right[nums[i]] += 1

    for i in range(2, n - 2):
      num = nums[i]
      right[num] -= 1
      if right[num] == 0:
        del right[num]

      leftCount = left[num]
      rightCount = right[num]
      leftOther = i - leftCount
      rightOther = n - i - 1 - rightCount

      # count[mode] = 5 -- [a a] a [a a]
      ans += math.comb(leftCount, 2) * math.comb(rightCount, 2)

      # count[mode] = 4 -- [a a] a [a ?]
      ans += math.comb(leftCount, 2) * rightCount * rightOther

      # count[mode] = 4 -- [a ?] a [a a]
      ans += leftCount * leftOther * math.comb(rightCount, 2)

      # count[mode] = 3 -- [a a] a [? ?]
      ans += math.comb(leftCount, 2) * math.comb(rightOther, 2)

      # count[mode] = 3 -- [? ?] a [a a]
      ans += math.comb(leftOther, 2) * math.comb(rightCount, 2)

      # count[mode] = 3 -- [a ?] a [a ?]
      ans += leftCount * leftOther * rightCount * rightOther

      # count[mode] = 2 -- [a ?] a [? ?]
      ans += leftCount * self._calc(num, leftOther, rightOther, left, right)

      # count[mode] = 2 -- [? ?] a [a ?]
      ans += rightCount * self._calc(num, rightOther, leftOther, right, left)

      ans %= self.MOD
      left[num] += 1

    return ans

  def _calc(
      self,
      a: int,
      other1: int,
      other2: int,
      count1: dict[int, int],
      count2: dict[int, int]
  ) -> int:
    """
    Returns the count of subsequences that have `a` as the middle number, where
    invalid subsequences are excluded.
    """
    # [a ?] a [? ?]
    res = (other1 * math.comb(other2, 2)) % self.MOD

    for b, b1 in count1.items():
      if b == a:
        continue
      b2 = count2[b]
      # Exclude triples -- [a b] a [b b].
      res = (res - b1 * math.comb(b2, 2)) % self.MOD
      # Exclude doubles -- [a b] a [b ?].
      res = (res - b1 * b2 * (other2 - b2)) % self.MOD

    for b, b2 in count2.items():
      if b == a:
        continue
      b1 = count1[b]
      # Exclude doubles -- [a ?] a [b b].
      res = (res - (other1 - b1) * math.comb(b2, 2)) % self.MOD

    return (res + self.MOD) % self.MOD
```

## 3. `3461_47` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-i/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
    def minimumArea(self, grid: List[List[int]]) -> int:
        x1 = y1 = float('inf')
        x2 = y2 = -float('inf')
        for i, row in enumerate(grid):
            for j, x in enumerate(row):
                if x == 1:
                    x1 = min(x1, i)
                    y1 = min(y1, j)
                    x2 = max(x2, i)
                    y2 = max(y2, j)
        return (x2 - x1 + 1) * (y2 - y1 + 1)
```

## 4. `2832_55` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/find-the-longest-equal-subarray/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def longestEqualSubarray(self, nums: List[int], k: int) -> int:
        from collections import defaultdict
        pos = defaultdict(list)
        for i, x in enumerate(nums):
            pos[x].append(i)
        
        mx = 0
        for indices in pos.values():
            l = 0
            for r in range(len(indices)):
                while indices[r] - indices[l] - (r - l) > k:
                    l += 1
                mx = max(mx, r - l + 1)
        return mx
```

## 5. `3245_16` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/find-beautiful-indices-in-the-given-array-i/
- Precision: 0.125
- Test pass: [Y ]

```python
class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        def build_prefix_function(pattern):
            prefix_function = [0] * len(pattern)
            j = 0
            for i in range(1, len(pattern)):
                while j > 0 and pattern[i] != pattern[j]:
                    j = prefix_function[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                prefix_function[i] = j
            return prefix_function

        def kmp_search(pattern, text, prefix_function):
            occurrences = []
            j = 0
            for i in range(len(text)):
                while j > 0 and text[i] != pattern[j]:
                    j = prefix_function[j - 1]
                if text[i] == pattern[j]:
                    j += 1
                if j == len(pattern):
                    occurrences.append(i - len(pattern) + 1)
                    j = prefix_function[j - 1]
            return occurrences

        prefix_a = build_prefix_function(a)
        prefix_b = build_prefix_function(b)

        resa = kmp_search(a, s, prefix_a)
        resb = kmp_search(b, s, prefix_b)

        res = []
        j = 0
        for i in range(len(resa)):
            while j < len(resb) and resb[j] < resa[i] - k:
                j += 1
            if j < len(resb) and abs(resb[j] - resa[i]) <= k:
                res.append(resa[i])
        return res
```

## 6. `3299_20` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/find-the-maximum-number-of-elements-in-subset/
- Precision: 0.200
- Test pass: [Y ]

```python
class Solution:
    def maximumLength(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = cnt[1] - (cnt[1] % 2 ^ 1)
        del cnt[1]
        for x in cnt:
            t = 0
            curr = x
            while cnt[curr] > 1:
                curr = curr * curr
                t += 2
            t += 1 if cnt[curr] else -1
            ans = max(ans, t)
        return ans
```

## 7. `3345_19` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/find-the-sum-of-the-power-of-all-subsequences/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        mod = 10**9 + 7
        n = len(nums)
        f = [[0] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i, x in enumerate(nums, start=1):
            for j in range(k + 1):
                f[i][j] = f[i - 1][j] * 2 % mod
                if j >= x:
                    f[i][j] = (f[i][j] + f[i - 1][j - x]) % mod
        return f[n][k]
```

## 8. `3451_23` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/string-compression-iii/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def compressedString(self, word: str) -> str:
        from itertools import groupby
        g = groupby(word)
        ans = []
        for c, v in g:
            k = len(list(v))
            while k:
                x = min(9, k)
                ans.append(str(x) + c)
                k -= x
        return "".join(ans)
```

## 9. `3346_29` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/lexicographically-smallest-string-after-operations-with-constraint/
- Precision: 0.750
- Test pass: [Y ]

```python
from string import ascii_lowercase

class Solution:
    def getSmallestString(self, s: str, k: int) -> str:
        cs = list(s)
        for i, c1 in enumerate(s):
            for c2 in ascii_lowercase:
                if c2 >= c1:
                    break
                d = min(ord(c1) - ord(c2), 26 - ord(c1) + ord(c2))
                if d <= k:
                    cs[i] = c2
                    k -= d
                    break
        return "".join(cs)
```

## 10. `3510_31` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/maximize-the-total-height-of-unique-towers/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight.sort()
        ans, mx = 0, float('inf')
        for x in maximumHeight[::-1]:
            x = min(x, mx - 1)
            if x <= 0:
                return -1
            ans += x
            mx = x
        return ans
```

## 11. `3403_34` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minimumSubstringsInPartition(self, s: str) -> int:
        @cache
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            cnt = defaultdict(int)
            freq = defaultdict(int)
            ans = n - i
            for j in range(i, n):
                if cnt[s[j]]:
                    freq[cnt[s[j]]] -= 1
                    if freq[cnt[s[j]]] == 0:
                        freq.pop(cnt[s[j]])
                cnt[s[j]] += 1
                freq[cnt[s[j]]] += 1
                if len(freq) == 1 and (t := 1 + dfs(j + 1)) < ans:
                    ans = t
            return ans

        n = len(s)
        return dfs(0)
```

## 12. `3696_6` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/count-substrings-divisible-by-last-digit/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
  def countSubstrings(self, s: str) -> int:
    ans = 0
    # dp[i][num][rem] := the number of first `i` digits of s that have a
    # remainder of `rem` when divided by `num`
    dp = [[[0] * 10 for _ in range(10)] for _ in range(len(s) + 1)]

    for i in range(1, len(s) + 1):
      digit = int(s[i - 1])
      for num in range(1, 10):
        for rem in range(num):
          dp[i][num][(rem * 10 + digit) % num] += dp[i - 1][num][rem]
        dp[i][num][digit % num] += 1
      if digit != 0:
        ans += dp[i][digit][0]

    return ans
```

## 13. `3199_35` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/distribute-candies-among-children-i/
- Precision: 0.750
- Test pass: [Y ]

```python
from math import comb

class Solution:
    def distributeCandies(self, n: int, limit: int) -> int:
        if n > 3 * limit:
            return 0
        ans = comb(n + 2, 2)
        if n > limit:
            ans -= 3 * comb(n - limit + 1, 2)
        if n - 2 >= 2 * limit:
            ans += 3 * comb(n - 2 * limit, 2)
        return ans
```

## 14. `3532_28` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/time-taken-to-mark-all-nodes/
- Precision: 0.667
- Test pass: [Y ]

```python
from dataclasses import dataclass


@dataclass
class Node:
  node: int = 0  # the node number
  time: int = 0  # the time taken to mark the entire subtree rooted at the node


class Top2:
  def __init__(self, top1: Node = Node(), top2: Node = Node()):
    # the direct child node, where the time taken to mark the entire subtree
    # rooted at the node is the maximum
    self.top1 = top1
    # the direct child node, where the time taken to mark the entire subtree
    # rooted at the node is the second maximum
    self.top2 = top2


class Solution:
  def timeTaken(self, edges: list[list[int]]) -> list[int]:
    n = len(edges) + 1
    ans = [0] * n
    tree = [[] for _ in range(n)]
    # dp[i] := the top two direct child nodes for subtree rooted at node i,
    # where each node contains the time taken to mark the entire subtree rooted
    # at the node itself
    dp = [Top2() for _ in range(n)]

    for u, v in edges:
      tree[u].append(v)
      tree[v].append(u)

    self._dfs(tree, 0, -1, dp)
    self._reroot(tree, 0, -1, 0, dp, ans)
    return ans

  def _getTime(self, u: int) -> int:
    """Returns the time taken to mark node u."""
    return 2 if u % 2 == 0 else 1

  def _dfs(
      self,
      tree: list[list[int]],
      u: int,
      prev: int,
      dp: list[Top2]
  ) -> int:
    """
    Performs a DFS traversal of the subtree rooted at node `u`, computes the
    time taken to mark all nodes in the subtree, records the top two direct
    child nodes, where the time taken to mark the subtree rooted at each of the
    child nodes is maximized, and returns the top child node.

    These values are used later in the rerooting process.
    """
    top1 = Node()
    top2 = Node()
    for v in tree[u]:
      if v == prev:
        continue
      time = self._dfs(tree, v, u, dp) + self._getTime(v)
      if time >= top1.time:
        top2 = top1
        top1 = Node(v, time)
      elif time > top2.time:
        top2 = Node(v, time)
    dp[u] = Top2(top1, top2)
    return top1.time

  def _reroot(
      self,
      tree: list[list[int]],
      u: int,
      prev: int,
      maxTime: int,
      dp: list[Top2],
      ans: list[int]
  ) -> None:
    """
    Reroots the tree at node `u` and updates the answer array, where `maxTime`
    is the longest path that doesn't go through `u`'s subtree.
    """
    ans[u] = max(maxTime, dp[u].top1.time)

    for v in tree[u]:
      if v == prev:
        continue
      newMaxTime = self._getTime(u) + max(
          maxTime,
          dp[u].top2.time if dp[u].top1.node == v else dp[u].top1.time
      )
      self._reroot(tree, v, u, newMaxTime, dp, ans)
```

## 15. `3025_71` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/minimum-operations-to-form-subsequence-with-target-sum/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        if s < target:
            return -1
        cnt = [0] * 33
        for x in nums:
            for i in range(32):
                if x >> i & 1:
                    cnt[i] += 1
        i = j = 0
        ans = 0
        while 1:
            while i < 32 and (target >> i & 1) == 0:
                i += 1
            if i == 32:
                break
            while j < i:
                cnt[j + 1] += cnt[j] // 2
                cnt[j] %= 2
                j += 1
            while cnt[j] == 0:
                cnt[j] = 1
                j += 1
            ans += j - i
            cnt[j] -= 1
            j = i
            i += 1
        return ans
```

## 16. `3243_47` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/count-the-number-of-powerful-integers/
- Precision: 0.800
- Test pass: [Y ]

```python
import functools

class Solution:
    def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
        @functools.cache
        def dfs(pos: int, lim: int):
            if len(t) < n:
                return 0
            if len(t) - pos == n:
                return int(s <= t[pos:]) if lim else 1
            up = min(int(t[pos]) if lim else 9, limit)
            ans = 0
            for i in range(up + 1):
                ans += dfs(pos + 1, lim and i == int(t[pos]))
            return ans

        n = len(s)
        t = str(start - 1)
        a = dfs(0, True)
        dfs.cache_clear()
        t = str(finish)
        b = dfs(0, True)
        return b - a
```

## 17. `3025_73` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/minimum-operations-to-form-subsequence-with-target-sum/
- Precision: 0.304
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        if s < target:
            return -1
        cnt = [0] * 32
        for x in nums:
            cnt[x.bit_length() - 1] += 1

        ans = 0
        i = 0
        while i < 31:
            if (target >> i) & 1:
                if cnt[i] > 0:
                    cnt[i] -= 1
                else:
                    j = i + 1
                    while j < 32 and cnt[j] == 0:
                        j += 1
                    
                    ans += j - i
                    cnt[j] -= 1
                    for k in range(i, j):
                        cnt[k] += 1
                    cnt[i] -= 1
            
            cnt[i+1] += cnt[i] // 2
            i += 1
        
        if (target >> 31) & 1 and cnt[31] == 0:
            return -1
            
        return ans
```

## 18. `3770_7` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/lexicographically-smallest-generated-string/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
  def generateString(self, str1: str, str2: str) -> str:
    n = len(str1)
    m = len(str2)
    sz = n + m - 1
    ans = [None] * sz
    modifiable = [True] * sz

    # 1. Handle all 'T' positions first.
    for i, tf in enumerate(str1):
      if tf == 'T':
        for j, c in enumerate(str2):
          pos = i + j
          if ans[pos] and ans[pos] != c:
            return ''
          ans[pos] = c
          modifiable[pos] = False

    # 2. Fill all remaining positions with 'a'.
    for i in range(sz):
      if ans[i] is None:
        ans[i] = 'a'

    # 3. Handle all 'F' positions.
    for i in range(n):
      if str1[i] == 'F' and self._match(ans, i, str2):
        modifiablePos = self._lastModifiablePosition(i, m, modifiable)
        if modifiablePos == -1:
          return ''
        ans[modifiablePos] = 'b'
        modifiable[modifiablePos] = False

    return ''.join(ans)

  def _match(self, ans: list, i: int, s: str) -> bool:
    """Returns True if the substring of ans starting at `i` matches `s`."""
    for j, c in enumerate(s):
      if ans[i + j] != c:
        return False
    return True

  def _lastModifiablePosition(self, i: int, m: int, modifiable: list) -> int:
    """
    Finds the last modifiable position in the substring of ans starting at `i`.
    """
    modifiablePos = -1
    for j in range(m):
      pos = i + j
      if modifiable[pos]:
        modifiablePos = pos
    return modifiablePos
```

## 19. `2916_50` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/check-if-it-is-possible-to-split-array/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def canSplitArray(self, nums: List[int], m: int) -> bool:
        @lru_cache(None)
        def dfs(i: int, j: int) -> bool:
            if i == j:
                return True
            for k in range(i, j):
                a = k == i or s[k + 1] - s[i] >= m
                b = k == j - 1 or s[j + 1] - s[k + 1] >= m
                if a and b and dfs(i, k) and dfs(k + 1, j):
                    return True
            return False

        s = list(accumulate(nums, initial=0))
        return dfs(0, len(nums) - 1)
```

## 20. `3620_24` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/maximum-number-of-distinct-elements-after-operations/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def maxDistinctElements(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = 0
        pre = -inf
        for x in nums:
            cur = max(x - k, pre + 1)
            if cur <= x + k:
                ans += 1
                pre = cur
        return ans
```

## 21. `3634_1` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/find-mirror-score-of-a-string/
- Precision: 0.500
- Test pass: [Y ]

```python
from collections import defaultdict

class Solution:
    def calculateScore(self, s: str) -> int:
        d = defaultdict(list)
        ans = 0
        for i, x in enumerate(s):
            y = chr(ord('a') + ord('z') - ord(x))
            if d[y]:
                j = d[y].pop()
                ans += i - j
            else:
                d[x].append(i)
        return ans
```

## 22. `3203_35` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/palindrome-rearrangement-queries/
- Precision: 0.091
- Test pass: [N ]

```python
class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        def count(pre: List[List[int]], i: int, j: int) -> List[int]:
            if i > j:
                return [0] * 26
            return [x - y for x, y in zip(pre[j + 1], pre[i])]

        def sub(cnt1: List[int], cnt2: List[int]) -> List[int]:
            res = []
            for x, y in zip(cnt1, cnt2):
                if x - y < 0:
                    return []
                res.append(x - y)
            return res

        def check(
            pre1: List[List[int]], pre2: List[List[int]], a: int, b: int, c: int, d: int
        ) -> bool:
            if diff[a] > 0 or diff[m] - diff[max(b, d) + 1] > 0:
                return False
            if d <= b:
                return count(pre1, a, b) == count(pre2, a, b)
            if b < c:
                return (
                    diff[c] - diff[b + 1] == 0
                    and [x + y for x, y in zip(count(pre1, a, b), count(pre1, c, d))] == [x + y for x, y in zip(count(pre2, a, b), count(pre2, c, d))]
                )
            cnt1 = sub(count(pre2, a, b), count(pre1, a, c - 1))
            cnt2 = sub(count(pre1, c, d), count(pre2, b + 1, d))
            return cnt1 == cnt2 and cnt1 != []

        n = len(s)
        m = n // 2
        s_rev = s[::-1]
        t = s_rev[m:][::-1]
        s = s_rev[:m]
        pre1 = [[0] * 26 for _ in range(m + 1)]
        pre2 = [[0] * 26 for _ in range(m + 1)]
        diff = [0] * (m + 1)
        for i, (c1, c2) in enumerate(zip(s, t), 1):
            pre1[i] = pre1[i - 1][:]
            pre2[i] = pre2[i - 1][:]
            pre1[i][ord(c1) - ord("a")] += 1
            pre2[i][ord(c2) - ord("a")] += 1
            diff[i] = diff[i - 1] + int(c1 != c2)
        ans = []
        for a, b, c, d in queries:
            c, d = n - 1 - d, n - 1 - c
            ok = (
                check(pre1, pre2, a, b, c, d)
                if a <= c
                else check(pre2, pre1, c, d, a, b)
            )
            ans.append(ok)
        return ans
```

## 23. `3510_12` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/maximize-the-total-height-of-unique-towers/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight.sort()
        ans, mx = 0, float('inf')
        for x in maximumHeight[::-1]:
            x = min(x, mx - 1)
            if x <= 0:
                return -1
            ans += x
            mx = x
        return ans
```

## 24. `3717_53` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/
- Precision: 0.273
- Test pass: [Y ]

```python
from collections import defaultdict
from heapq import heappop, heappush, heappushpop
from math import inf
from typing import List


class LazyHeap:
    def __init__(self):
        self.heap = []
        self.remove_cnt = defaultdict(int)  # 每个元素剩余需要删除的次数
        self.size = 0  # 实际大小
        self.sum = 0  # 堆中元素总和

    # 删除
    def remove(self, x: int) -> None:
        self.remove_cnt[x] += 1  # 懒删除
        self.size -= 1
        self.sum -= x

    # 正式执行删除操作
    def apply_remove(self) -> None:
        while self.heap and self.remove_cnt[self.heap[0]] > 0:
            self.remove_cnt[self.heap[0]] -= 1
            heappop(self.heap)

    # 查看堆顶
    def top(self) -> int:
        self.apply_remove()
        return self.heap[0]

    # 出堆
    def pop(self) -> int:
        self.apply_remove()
        self.size -= 1
        self.sum -= self.heap[0]
        return heappop(self.heap)

    # 入堆
    def push(self, x: int) -> None:
        if self.remove_cnt[x] > 0:
            self.remove_cnt[x] -= 1  # 抵消之前的删除
        else:
            heappush(self.heap, x)
        self.size += 1
        self.sum += x

    # push(x) 然后 pop()
    def pushpop(self, x: int) -> int:
        self.apply_remove()
        if not self.heap or x <= self.heap[0]:
            return x
        self.sum += x - self.heap[0]
        return heappushpop(self.heap, x)


class Solution:
    # 480. 滑动窗口中位数（有改动）
    # 返回 nums 的所有长为 k 的子数组的（到子数组中位数的）距离和
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        ans = [0] * (len(nums) - k + 1)
        left = LazyHeap()  # 最大堆（元素取反）
        right = LazyHeap()  # 最小堆

        for i, x in enumerate(nums):
            # 1. 进入窗口
            if left.size == right.size:
                left.push(-right.pushpop(x))
            else:
                right.push(-left.pushpop(-x))

            l = i + 1 - k
            if l < 0:  # 窗口大小不足 k
                continue

            # 2. 计算答案
            v = -left.top()
            s1 = v * left.size + left.sum  # sum 取反
            s2 = right.sum - v * right.size
            ans[l] = s1 + s2

            # 3. 离开窗口
            x = nums[l]
            if x <= -left.top():
                left.remove(-x)
                if left.size < right.size:
                    left.push(-right.pop())  # 平衡两个堆的大小
            else:
                right.remove(x)
                if left.size > right.size + 1:
                    right.push(-left.pop())  # 平衡两个堆的大小

        return ans

    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        dis = self.medianSlidingWindow(nums, x)
        f = [[inf] * (n + 1) for _ in range(k + 1)]
        for j in range(n + 1):
            f[0][j] = 0
        for i in range(1, k + 1):
            for j in range(i * x, n - (k - i) * x + 1):  # 左右留出足够空间给其他子数组
                f[i][j] = min(f[i][j - 1], f[i - 1][j - x] + dis[j - x])  # j-x 为子数组左端点
        return f[k][n]
```

## 25. `3682_16` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
    MOD = 10**9 + 7
    _fact = None  # Class variable for precomputed factorials
    _inv_fact = None  # Class variable for precomputed inverse factorials

    @classmethod
    def precompute(cls, max_n):
        """Precompute factorial and inverse factorial arrays up to max_n."""
        if cls._fact is not None and len(cls._fact) > max_n:
            return  # Already precomputed sufficiently

        cls._fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            cls._fact[i] = cls._fact[i-1] * i % cls.MOD

        cls._inv_fact = [1] * (max_n + 1)
        cls._inv_fact[max_n] = pow(cls._fact[max_n], cls.MOD - 2, cls.MOD)
        for i in range(max_n - 1, -1, -1):
            cls._inv_fact[i] = cls._inv_fact[i + 1] * (i + 1) % cls.MOD

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if k < 0 or k > n - 1:
            return 0

        max_needed = n
        Solution.precompute(max_needed)

        a = n - 1
        b = k
        # Compute combination C(a, b)
        comb = Solution._fact[a] * Solution._inv_fact[b] % self.MOD
        comb = comb * Solution._inv_fact[a - b] % self.MOD

        exponent = (n - k - 1)
        term = pow(m - 1, exponent, self.MOD)

        ans = comb * m % self.MOD
        ans = ans * term % self.MOD
        return ans
```

## 26. `3114_45` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/beautiful-towers-i/
- Precision: 0.000
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def maximumSumOfHeights(self, maxHeights: List[int]) -> int:
        n = len(maxHeights)
        max_total = 0

        for i in range(n):
            # Calculate left part
            left = [0] * (i + 1)
            left[i] = maxHeights[i]
            for j in range(i - 1, -1, -1):
                left[j] = min(maxHeights[j], left[j + 1])
            left_sum = sum(left)

            # Calculate right part
            right_length = n - i
            right = [0] * right_length
            right[0] = maxHeights[i]
            for j in range(i + 1, n):
                pos_in_right = j - i
                right[pos_in_right] = min(maxHeights[j], right[pos_in_right - 1])
            right_sum = sum(right)

            # Update the maximum total
            current_total = left_sum + right_sum - maxHeights[i]
            if current_total > max_total:
                max_total = current_total

        return max_total
```

## 27. `3403_21` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minimumSubstringsInPartition(self, s: str) -> int:
        @cache
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            cnt = defaultdict(int)
            freq = defaultdict(int)
            ans = n - i
            for j in range(i, n):
                if cnt[s[j]]:
                    freq[cnt[s[j]]] -= 1
                    if freq[cnt[s[j]]] == 0:
                        freq.pop(cnt[s[j]])
                cnt[s[j]] += 1
                freq[cnt[s[j]]] += 1
                if len(freq) == 1 and (t := 1 + dfs(j + 1)) < ans:
                    ans = t
            return ans

        n = len(s)
        return dfs(0)
```

## 28. `2921_58` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/count-stepping-numbers-in-range/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def countSteppingNumbers(self, low: str, high: str) -> int:
        @cache
        def dfs(pos: int, pre: int, lead: bool, limit: bool) -> int:
            if pos == len(num):
                return int(not lead)
            up = int(num[pos]) if limit else 9
            ans = 0
            for i in range(up + 1):
                if i == 0 and lead:
                    ans += dfs(pos + 1, pre, True, limit and i == up)
                elif pre == -1 or abs(i - pre) == 1:
                    ans += dfs(pos + 1, i, False, limit and i == up)
            return ans % mod

        mod = 10**9 + 7
        num = high
        a = dfs(0, -1, True, True)
        dfs.cache_clear()
        num = str(int(low) - 1)
        b = dfs(0, -1, True, True)
        return (a - b) % mod
```

## 29. `2879_9` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        inf = float('inf')
        g = [[inf] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                m = j - i + 1
                for d in range(1, m):
                    if m % d == 0:
                        cnt = 0
                        for l in range(m):
                            r = (m // d - 1 - l // d) * d + l % d
                            if l >= r:
                                break
                            if s[i - 1 + l] != s[i - 1 + r]:
                                cnt += 1
                        g[i][j] = min(g[i][j], cnt)

        f = [[inf] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                for h in range(i - 1):
                    f[i][j] = min(f[i][j], f[h][j - 1] + g[h + 1][i])
        return f[n][k]
```

## 30. `3436_11` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/find-subarray-with-bitwise-or-closest-to-k/
- Precision: 0.667
- Test pass: [N ]

```python
class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        m = max(nums).bit_length()
        cnt = [0] * m
        s = i = 0
        ans = inf
        for j, x in enumerate(nums):
            s |= x
            ans = min(ans, abs(s - k))
            for h in range(m):
                if x >> h & 1:
                    cnt[h] += 1
            while i <= j and s > k:
                y = nums[i]
                for h in range(m):
                    if y >> h & 1:
                        cnt[h] -= 1
                        if cnt[h] == 0:
                            s ^= 1 << h
                i += 1
                ans = min(ans, abs(s - k))
        return ans
```

## 31. `3646_10` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/sum-of-good-subsequences/
- Precision: 0.200
- Test pass: [Y ]

```python
class Solution:
    def sumOfGoodSubsequences(self, nums: List[int]) -> int:
        mod = 10**9 + 7
        f = defaultdict(int)
        g = defaultdict(int)
        for x in nums:
            f[x] += x
            g[x] += 1
            f[x] = (f[x] + f[x - 1] + g[x - 1] * x) % mod
            g[x] = (g[x] + g[x - 1]) % mod
            f[x] = (f[x] + f[x + 1] + g[x + 1] * x) % mod
            g[x] = (g[x] + g[x + 1]) % mod
        return sum(f.values()) % mod
```

## 32. `3781_8` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/maximize-the-distance-between-points-on-a-square/
- Precision: 0.333
- Test pass: [Y ]

```python
import collections
from dataclasses import dataclass


@dataclass(frozen=True)
class Sequence:
  startX: int
  startY: int
  endX: int
  endY: int
  length: int

  def __iter__(self):
    yield self.startX
    yield self.startY
    yield self.endX
    yield self.endY
    yield self.length


class Solution:
  def maxDistance(self, side: int, points: list[list[int]], k: int) -> int:
    ordered = self._getOrderedPoints(side, points)

    def isValidDistance(m: int) -> bool:
      """
      Returns True if we can select `k` points such that the minimum Manhattan
      distance between any two consecutive chosen points is at least `m`.
      """
      dq = collections.deque([Sequence(*ordered[0], *ordered[0], 1)])
      maxLength = 1

      for i in range(1, len(ordered)):
        x, y = ordered[i]
        startX, startY = ordered[i]
        length = 1
        while dq and abs(x - dq[0].endX) + abs(y - dq[0].endY) >= m:
          if (abs(x - dq[0].startX) + abs(y - dq[0].startY) >= m
                  and dq[0].length + 1 >= length):
            startX = dq[0].startX
            startY = dq[0].startY
            length = dq[0].length + 1
            maxLength = max(maxLength, length)
          dq.popleft()
        dq.append(Sequence(startX, startY, x, y, length))

      return maxLength >= k

    l = 0
    r = side * 2

    while l < r:
      m = (l + r + 1) // 2
      if isValidDistance(m):
        l = m
      else:
        r = m - 1

    return l

  def _getOrderedPoints(self, side: int, points: list[list[int]]) -> list[list[int]]:
    """
    Returns the ordered points on the perimeter of a square of side length
    `side`, starting from left, top, right, and bottom boundaries.
    """
    left = sorted([(x, y) for x, y in points if x == 0 and y > 0])
    top = sorted([(x, y) for x, y in points if x > 0 and y == side])
    right = sorted([(x, y) for x, y in points if x == side and y < side],
                   reverse=True)
    bottom = sorted([(x, y) for x, y in points if y == 0], reverse=True)
    return left + top + right + bottom
```

## 33. `2952_30` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/minimum-time-to-make-array-sum-at-most-x/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minimumTime(self, nums1: List[int], nums2: List[int], x: int) -> int:
        n = len(nums1)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (a, b) in enumerate(sorted(zip(nums1, nums2), key=lambda z: z[1]), 1):
            for j in range(n + 1):
                f[i][j] = f[i - 1][j]
                if j > 0:
                    f[i][j] = max(f[i][j], f[i - 1][j - 1] + a + b * j)
        s1 = sum(nums1)
        s2 = sum(nums2)
        for j in range(0, n + 1):
            if s1 + s2 * j - f[n][j] <= x:
                return j
        return -1
```

## 34. `3460_0` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/count-the-number-of-inversions/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        req = [-1] * n
        for end, cnt in requirements:
            req[end] = cnt
        if req[0] > 0:
            return 0
        req[0] = 0
        mod = 10**9 + 7
        m = max(req)
        f = [[0] * (m + 1) for _ in range(n)]
        f[0][0] = 1

        for i in range(1, n):
            l, r = 0, m
            if req[i] >= 0:
                l = r = req[i]
            for j in range(l, r + 1):
                for k in range(min(i, j) + 1):
                    f[i][j] = (f[i][j] + f[i - 1][j - k]) % mod
        return f[n - 1][req[n - 1]]
```

## 35. `3560_11` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/maximum-number-of-moves-to-kill-all-pawns/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        @lru_cache(None)
        def dfs(last: int, state: int, k: int) -> int:
            if state == 0:
                return 0
            if k:
                res = 0
                for i, (x, y) in enumerate(positions):
                    if state >> i & 1:
                        t = dfs(i, state ^ (1 << i), k ^ 1) + dist[last][x][y]
                        if res < t:
                            res = t
                return res
            else:
                res = inf
                for i, (x, y) in enumerate(positions):
                    if state >> i & 1:
                        t = dfs(i, state ^ (1 << i), k ^ 1) + dist[last][x][y]
                        if res > t:
                            res = t
                return res

        n = len(positions)
        m = 50
        dist = [[[-1] * m for _ in range(m)] for _ in range(n + 1)]
        dx = [1, 1, 2, 2, -1, -1, -2, -2]
        dy = [2, -2, 1, -1, 2, -2, 1, -1]
        positions.append([kx, ky])
        for i, (x, y) in enumerate(positions):
            dist[i][x][y] = 0
            q = deque([(x, y)])
            step = 0
            while q:
                step += 1
                for _ in range(len(q)):
                    x1, y1 = q.popleft()
                    for j in range(8):
                        x2, y2 = x1 + dx[j], y1 + dy[j]
                        if 0 <= x2 < m and 0 <= y2 < m and dist[i][x2][y2] == -1:
                            dist[i][x2][y2] = step
                            q.append((x2, y2))

        ans = dfs(n, (1 << n) - 1, 1)
        dfs.cache_clear()
        return ans
```

## 36. `3416_6` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/sum-of-digit-differences-of-all-pairs/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def sumDigitDifferences(self, nums: List[int]) -> int:
        n = len(nums)
        m = len(str(nums[0]))
        ans = 0
        for _ in range(m):
            cnt = Counter()
            for i, x in enumerate(nums):
                x, y = divmod(x, 10)
                cnt[y] += 1
                nums[i] = x
            ans += sum(v * (n - v) for v in cnt.values()) // 2
        return ans
```

## 37. `3748_26` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/sort-matrix-by-diagonals/
- Precision: 0.125
- Test pass: [Y ]

```python
class Solution:
    def sortMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        n = len(grid)
        for k in range(n - 1, -1, -1):
            i, j = k, 0
            t = []
            while i < n and j < n:
                t.append(grid[i][j])
                i += 1
                j += 1
            t.sort(reverse=True)
            i, j = k, 0
            for v in t:
                grid[i][j] = v
                i += 1
                j += 1
        for k in range(n - 1, 0, -1):
            i, j = 0, k
            t = []
            while i < n and j < n:
                t.append(grid[i][j])
                i += 1
                j += 1
            t.sort()
            i, j = 0, k
            for v in t:
                grid[i][j] = v
                i += 1
                j += 1
        return grid
```

## 38. `3778_16` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/transform-array-by-parity/
- Precision: 0.286
- Test pass: [Y ]

```python
class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        for i in range(len(nums)):
            if nums[i] % 2 == 0:
                nums[i] = 0
            else:
                nums[i] = 1
        nums.sort()
        return nums
```

## 39. `3190_45` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/minimum-operations-to-maximize-last-elements-in-arrays/
- Precision: 0.100
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        def f(x: int, y: int) -> int:
            cnt = 0
            for a, b in zip(nums1, nums2):
                if a <= x and b <= y:
                    continue
                if not (a <= y and b <= x):
                    return -1
                cnt += 1
            return cnt

        a = f(nums1[-1], nums2[-1])
        b = f(nums2[-1], nums1[-1])
        if a == -1 and b == -1:
            return -1
        if a == -1:
            return b
        if b == -1:
            return a
        return min(a, b)
```

## 40. `3657_19` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/check-if-grid-can-be-cut-into-sections/
- Precision: 0.125
- Test pass: [Y ]

```python
class Solution:
    def countLineIntersections(self, coordinates: List[tuple[int, int]]) -> bool:
        lines = 0
        overlap = 0
        for value, marker in sorted(coordinates):
            if marker == 1:
                overlap += 1
            else:
                overlap -= 1

            if overlap == 0:
                lines += 1

        return lines >= 3

    def checkValidCuts(self, n: int, rectangles: List[List[int]]) -> bool:
        y_coordinates = []
        x_coordinates = []

        for rect in rectangles:
            x1, y1, x2, y2 = rect
            y_coordinates.append((y1, 1))  # start
            y_coordinates.append((y2, 0))  # end

            x_coordinates.append((x1, 1))  # start
            x_coordinates.append((x2, 0))  # end

        # Sort by coordinate value, and for tie, put end (0) before start (1)
        y_coordinates.sort(key=lambda x: (x[0], x[1]))
        x_coordinates.sort(key=lambda x: (x[0], x[1]))

        return self.countLineIntersections(
            y_coordinates
        ) or self.countLineIntersections(x_coordinates)
```

## 41. `3345_34` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/find-the-sum-of-the-power-of-all-subsequences/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        mod = 10**9 + 7
        n = len(nums)
        f = [[0] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 1
        for i, x in enumerate(nums, start=1):
            for j in range(k + 1):
                f[i][j] = f[i - 1][j] * 2 % mod
                if j >= x:
                    f[i][j] = (f[i][j] + f[i - 1][j - x]) % mod
        return f[n][k]
```

## 42. `3517_20` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
    def shortestDistanceAfterQueries(
        self, n: int, queries: List[List[int]]
    ) -> List[int]:
        def bfs(i: int) -> int:
            q = deque([i])
            vis = [False] * n
            vis[i] = True
            d = 0
            while 1:
                for _ in range(len(q)):
                    u = q.popleft()
                    if u == n - 1:
                        return d
                    for v in g[u]:
                        if not vis[v]:
                            vis[v] = True
                            q.append(v)
                d += 1

        g = [[] for _ in range(n)]
        for i in range(n - 1):
            g[i].append(i + 1)
        ans = []
        for u, v in queries:
            g[u].append(v)
            ans.append(bfs(0))
        return ans
```

## 43. `3594_17` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/identify-the-largest-outlier-in-an-array/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def getLargestOutlier(self, nums: List[int]) -> int:
        from collections import Counter
        s = sum(nums)
        cnt = Counter(nums)
        max_outlier = -float('inf')
        for x in nums:
            t = s - x
            if t % 2:
                continue
            target = t // 2
            if cnt.get(target, 0) > 0:
                if x != target or cnt[target] > 1:
                    max_outlier = max(max_outlier, x)
        return max_outlier
```

## 44. `3235_69` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/minimum-cost-to-convert-string-i/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minimumCost(
        self,
        source: str,
        target: str,
        original: List[str],
        changed: List[str],
        cost: List[int],
    ) -> int:
        g = [[float('inf')] * 26 for _ in range(26)]
        for i in range(26):
            g[i][i] = 0
        for x, y, z in zip(original, changed, cost):
            x = ord(x) - ord('a')
            y = ord(y) - ord('a')
            g[x][y] = min(g[x][y], z)
        for k in range(26):
            for i in range(26):
                for j in range(26):
                    g[i][j] = min(g[i][j], g[i][k] + g[k][j])
        ans = 0
        for a, b in zip(source, target):
            if a != b:
                x, y = ord(a) - ord('a'), ord(b) - ord('a')
                if g[x][y] == float('inf'):
                    return -1
                ans += g[x][y]
        return ans
```

## 45. `2873_17` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/prime-pairs-with-target-sum/
- Precision: 0.400
- Test pass: [Y ]

```python
class Solution:
    def findPrimePairs(self, n: int) -> List[List[int]]:
        if n < 2:
            return []
        primes = [True] * n
        for i in range(2, n):
            if primes[i]:
                for j in range(i + i, n, i):
                    primes[j] = False
        ans = []
        for x in range(2, n // 2 + 1):
            y = n - x
            if y < n and primes[x] and primes[y]:
                ans.append([x, y])
        return ans
```

## 46. `3656_14` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/minimum-number-of-operations-to-make-elements-in-array-distinct/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        s = set()
        for i in reversed(range(len(nums))):
            if nums[i] in s:
                return i // 3 + 1
            s.add(nums[i])
        return 0
```

## 47. `2784_26` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/power-of-heroes/
- Precision: 0.400
- Test pass: [Y ]

```python
class Solution:
    def sumOfPower(self, nums: List[int]) -> int:
        mod = 10**9 + 7
        nums.sort()
        ans = 0
        p = 0
        for x in nums:
            ans = (ans + (x * x % mod) * x) % mod
            ans = (ans + x * x % mod * p) % mod
            p = (p * 2 + x) % mod
        return ans
```

## 48. `2891_14` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/maximum-beauty-of-an-array-after-applying-operation/
- Precision: 0.286
- Test pass: [Y ]

```python
class Solution:
    def maximumBeauty(self, nums: List[int], k: int) -> int:
        nums.sort()
        l, max_beauty = 0, 0
        for r in range(len(nums)):
            while nums[r] - nums[l] > 2 * k:
                l += 1
            max_beauty = max(max_beauty, r - l + 1)
        return max_beauty
```

## 49. `3498_49` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-array-changes-to-make-differences-equal/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minChanges(self, nums: List[int], k: int) -> int:
        from collections import Counter
        n = len(nums)
        freq = Counter()
        mp = [0] * (k + 1)
        for i in range(n // 2):
            p = nums[i]
            q = nums[n - i - 1]
            d = abs(p - q)
            freq[d] += 1
            max_val = max(p, q, k - p, k - q)
            if max_val <= k:
                mp[max_val] += 1
        suffix = [0] * (k + 2)
        for i in range(k, -1, -1):
            suffix[i] = suffix[i + 1] + mp[i]
        ans = float('inf')
        for x in range(k + 1):
            can1 = suffix[x]
            cost = 2 * (n // 2) - freq[x] - can1
            ans = min(ans, cost)
        return ans
```

## 50. `3680_26` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/count-connected-components-in-lcm-graph/
- Precision: 0.158
- Test pass: [Y ]

```python
class DSU:
    def __init__(self, n):
        self.parent = {i: i for i in range(n)}
        self.rank = {i: 0 for i in range(n)}

    def make_set(self, v):
        self.parent[v] = v
        self.rank[v] = 1

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union_set(self, u, v):
        u = self.find(u)
        v = self.find(v)
        if u != v:
            if self.rank[u] < self.rank[v]:
                u, v = v, u
            self.parent[v] = u
            if self.rank[u] == self.rank[v]:
                self.rank[u] += 1


class Solution:
    def countComponents(self, nums, threshold):
        import math
        dsu = DSU(len(nums))
        num_to_idx = {nums[i]: i for i in range(len(nums))}
        for m in range(1, threshold + 1):
            divs = []
            for d in range(1, int(math.sqrt(m)) + 1):
                if m % d == 0:
                    if d in num_to_idx:
                        divs.append(num_to_idx[d])
                    other = m // d
                    if other != d and other in num_to_idx:
                        divs.append(num_to_idx[other])
            if len(divs) > 1:
                for j in range(1, len(divs)):
                    dsu.union_set(divs[0], divs[j])
        components = set()
        for i in range(len(nums)):
            components.add(dsu.find(i))
        return len(components)
```

## 51. `3626_16` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/smallest-divisible-digit-product-i/
- Precision: 0.667
- Test pass: [Y ]

```python
from itertools import count
class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        for i in count(n):
            p = 1
            x = i
            while x:
                p *= x % 10
                x //= 10
            if p % t == 0:
                return i
```

## 52. `2754_6` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/maximum-strength-of-a-group/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def maxStrength(self, nums: List[int]) -> int:
        ans = -inf
        for i in range(1 << len(nums)):
            t = 1
            for j, x in enumerate(nums):
                if i >> j & 1:
                    t *= x
            if i != 0:
                ans = max(ans, t)
        return ans
```

## 53. `3573_0` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/count-substrings-that-can-be-rearranged-to-contain-a-string-i/
- Precision: 0.500
- Test pass: [Y ]

```python
from collections import Counter

class Solution:
    def validSubstringCount(self, word1: str, word2: str) -> int:
        if len(word1) < len(word2):
            return 0
        cnt = Counter(word2)
        need = len(cnt)
        ans = l = 0
        win = Counter()
        for c in word1:
            win[c] += 1
            if win[c] == cnt[c]:
                need -= 1
            while need == 0:
                if win[word1[l]] == cnt[word1[l]]:
                    need += 1
                win[word1[l]] -= 1
                l += 1
            ans += l
        return ans
```

## 54. `3621_1` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-array-values-equal-to-k/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        s = set()
        mi = inf
        for x in nums:
            if x < k:
                return -1
            if x > k:
                s.add(x)
            mi = min(mi, x)
        return len(s)
```

## 55. `3403_11` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/
- Precision: 0.333
- Test pass: [Y ]

```python
from collections import defaultdict
from functools import lru_cache

class Solution:
    def minimumSubstringsInPartition(self, s: str) -> int:
        @lru_cache(None)
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            cnt = defaultdict(int)
            freq = defaultdict(int)
            ans = n - i
            for j in range(i, n):
                if cnt[s[j]]:
                    freq[cnt[s[j]]] -= 1
                    if not freq[cnt[s[j]]]:
                        freq.pop(cnt[s[j]])
                cnt[s[j]] += 1
                freq[cnt[s[j]]] += 1
                if len(freq) == 1 and (t := 1 + dfs(j + 1)) < ans:
                    ans = t
            return ans

        n = len(s)
        return dfs(0)
```

## 56. `3264_13` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/maximum-points-after-enemy-battles/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def maximumPoints(self, enemyEnergies: List[int], currentEnergy: int) -> int:
        enemyEnergies = sorted(enemyEnergies)
        if currentEnergy < enemyEnergies[0]:
            return 0
        ans = 0
        for i in range(len(enemyEnergies) - 1, -1, -1):
            ans += currentEnergy // enemyEnergies[0]
            currentEnergy %= enemyEnergies[0]
            currentEnergy += enemyEnergies[i]
        return ans
```

## 57. `3394_32` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-array-end/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minEnd(self, n: int, x: int) -> int:
        ans = x
        val = n - 1
        i = 0
        while val:
            if not (x & (1 << i)):
                ans |= (val & 1) << i
                val >>= 1
            i += 1
        return ans
```

## 58. `2879_0` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/
- Precision: 0.250
- Test pass: [Y ]

```python
class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        import math
        n = len(s)
        inf = math.inf
        g = [[inf] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i, n + 1):
                m = j - i + 1
                for d in range(1, m):
                    if m % d == 0:
                        cnt = 0
                        for l in range(m):
                            r = (m // d - 1 - l // d) * d + l % d
                            if l >= r:
                                break
                            if s[i - 1 + l] != s[i - 1 + r]:
                                cnt += 1
                        g[i][j] = min(g[i][j], cnt)

        f = [[inf] * (k + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, k + 1):
                for h in range(i):
                    f[i][j] = min(f[i][j], f[h][j - 1] + g[h + 1][i])
        return f[n][k]
```

## 59. `3213_42` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/
- Precision: 0.818
- Test pass: [Y ]

```python
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        mx = max(nums)
        n = len(nums)
        total = n * (n + 1) // 2
        bad = 0
        i = 0
        cnt = 0
        for j in range(n):
            cnt += (nums[j] == mx)
            while cnt > k - 1:
                cnt -= (nums[i] == mx)
                i += 1
            bad += j - i + 1
        ans = total - bad
        return ans
```

## 60. `3736_3` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/find-valid-pair-of-adjacent-digits-in-string/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def findValidPair(self, s: str) -> str:
        cnt = [0] * 10
        for x in map(int, s):
            cnt[x] += 1
        for x, y in zip(map(int, s[:-1]), map(int, s[1:])):
            if x != y and cnt[x] == x and cnt[y] == y:
                return f"{x}{y}"
        return ""
```

## 61. `3327_70` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/minimum-moves-to-pick-k-ones/
- Precision: 0.024
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        n = len(nums)
        cnt = [0] * (n + 1)
        s = [0] * (n + 1)
        for i, x in enumerate(nums, 1):
            cnt[i] = cnt[i - 1] + x
            s[i] = s[i - 1] + i * x
        
        ans = float('inf')
        
        for i, x in enumerate(nums, 1):
            t = 0
            need = k - x
            
            # Count and take from immediate neighbors (distance 1)
            neighbor_ones = 0
            for j in (i - 1, i + 1):
                if 1 <= j <= n and nums[j - 1] == 1:
                    neighbor_ones += 1
            
            take = min(neighbor_ones, need)
            t += take
            need -= take
            
            # Use maxChanges operations (cost 2 each)
            take = min(need, maxChanges)
            need -= take
            t += take * 2
            
            if need <= 0:
                ans = min(ans, t)
                continue
            
            # Binary search for remaining ones at distance >= 2
            left, right = 2, max(i - 1, n - i)
            while left <= right:
                mid = (left + right) // 2
                
                # Calculate ranges for ones at distance >= 2
                l1 = max(1, i - mid)
                r1 = max(0, i - 2)
                l2 = min(n + 1, i + 2)
                r2 = min(n, i + mid)
                
                # Count ones in ranges with validation
                count_left = cnt[r1] - cnt[l1 - 1] if l1 <= r1 else 0
                count_right = cnt[r2] - cnt[l2 - 1] if l2 <= r2 else 0
                total_count = count_left + count_right
                
                if total_count >= need:
                    # Calculate cost for ones in ranges
                    sum_left = s[r1] - s[l1 - 1] if l1 <= r1 else 0
                    sum_right = s[r2] - s[l2 - 1] if l2 <= r2 else 0
                    
                    cost_left = count_left * i - sum_left
                    cost_right = sum_right - count_right * i
                    
                    ans = min(ans, t + cost_left + cost_right)
                    right = mid - 1
                else:
                    left = mid + 1
        
        return ans
```

## 62. `3367_0` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/find-the-sum-of-encrypted-integers/
- Precision: 0.000
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        def encrypt(x: int) -> int:
            mx = 0
            d = 0
            while x:
                x, v = divmod(x, 10)
                mx = max(mx, v)
                d += 1
            return mx * (10**d - 1) // 9

        return sum(encrypt(x) for x in nums)
```

## 63. `3190_12` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/minimum-operations-to-maximize-last-elements-in-arrays/
- Precision: 0.222
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        def f(x: int, y: int) -> int:
            cnt = 0
            for a, b in zip(nums1[:-1], nums2[:-1]):
                if a <= x and b <= y:
                    continue
                if not (a <= y and b <= x):
                    return -1
                cnt += 1
            return cnt

        a, b = f(nums1[-1], nums2[-1]), f(nums2[-1], nums1[-1])
        if a == -1 and b == -1:
            return -1
        if a == -1:
            return b + 1
        if b == -1:
            return a
        return min(a, b + 1)
```

## 64. `3682_27` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    MOD = 10**9 + 7
    _fact = None  # Class variable for precomputed factorials
    _inv_fact = None  # Class variable for precomputed inverse factorials

    @classmethod
    def precompute(cls, max_n):
        """Precompute factorial and inverse factorial arrays up to max_n."""
        if cls._fact is not None and len(cls._fact) >= max_n + 1:
            return  # Already precomputed sufficiently

        cls._fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            cls._fact[i] = cls._fact[i-1] * i % cls.MOD

        cls._inv_fact = [1] * (max_n + 1)
        cls._inv_fact[max_n] = pow(cls._fact[max_n], cls.MOD - 2, cls.MOD)
        for i in range(max_n - 1, -1, -1):
            cls._inv_fact[i] = cls._inv_fact[i + 1] * (i + 1) % cls.MOD

    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        if k < 0 or k > n - 1:
            return 0

        Solution.precompute(n)

        a = n - 1
        b = k
        # Compute combination C(a, b)
        comb = Solution._fact[a] * Solution._inv_fact[b] % self.MOD
        comb = comb * Solution._inv_fact[a - b] % self.MOD

        exponent = n - k - 1
        term = pow(m - 1, exponent, self.MOD)

        ans = comb * m % self.MOD
        ans = ans * term % self.MOD
        return ans
```

## 65. `3681_0` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/maximum-area-rectangle-with-point-constraints-i/
- Precision: 0.250
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def maxRectangleArea(self, points: List[List[int]]) -> int:
        def check(x1: int, y1: int, x2: int, y2: int) -> bool:
            cnt = 0
            for x, y in points:
                if x < x1 or x > x2 or y < y1 or y > y2:
                    continue
                if (x == x1 or x == x2) and (y == y1 or y == y2):
                    cnt += 1
                    continue
                return False
            return cnt == 4

        ans = -1
        for i, (x1, y1) in enumerate(points):
            for x2, y2 in points[:i]:
                x3, y3 = min(x1, x2), min(y1, y2)
                x4, y4 = max(x1, x2), max(y1, y2)
                if x3 == x4 or y3 == y4:
                    continue
                if check(x3, y3, x4, y4):
                    ans = max(ans, (x4 - x3) * (y4 - y3))
        return ans
```

## 66. `3025_34` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/minimum-operations-to-form-subsequence-with-target-sum/
- Precision: 0.105
- Test pass: [N ]

```python
class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        if s < target:
            return -1
        cnt = [0] * 32
        for x in nums:
            for i in range(32):
                if x >> i & 1:
                    cnt[i] += 1
        
        ops = 0
        for i in range(32):
            if target & (1 << i):
                if cnt[i] == 0:
                    j = i
                    while j < 32 and cnt[j] == 0:
                        j += 1
                    ops += j - i
                    cnt[j] -= 1
                    for k in range(j, i, -1):
                        cnt[k-1] += 2
                cnt[i] -= 1
            if i < 31:
                cnt[i+1] += cnt[i] // 2
        
        return ops
```

## 67. `2954_22` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/maximum-sum-of-almost-unique-subarray/
- Precision: 0.500
- Test pass: [Y ]

```python
from typing import List
from collections import Counter

class Solution:
    def maxSum(self, nums: List[int], m: int, k: int) -> int:
        cnt = Counter(nums[:k])
        s = sum(nums[:k])
        ans = s if len(cnt) >= m else 0
        for i in range(k, len(nums)):
            cnt[nums[i]] += 1
            cnt[nums[i - k]] -= 1
            s += nums[i] - nums[i - k]
            if cnt[nums[i - k]] == 0:
                cnt.pop(nums[i - k])
            if len(cnt) >= m:
                ans = max(ans, s)
        return ans
```

## 68. `3492_14` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/count-submatrices-with-equal-frequency-of-x-and-y/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def numberOfSubmatrices(self, grid: List[List[str]]) -> int:
        m, n = len(grid), len(grid[0])
        s = [[[0] * 2 for _ in range(n + 1)] for _ in range(m + 1)]
        ans = 0
        for i, row in enumerate(grid, 1):
            for j, x in enumerate(row, 1):
                s[i][j][0] = s[i - 1][j][0] + s[i][j - 1][0] - s[i - 1][j - 1][0]
                s[i][j][1] = s[i - 1][j][1] + s[i][j - 1][1] - s[i - 1][j - 1][1]
                if x != '.':
                    s[i][j][ord(x) & 1] += 1
                if s[i][j][0] > 0 and s[i][j][0] == s[i][j][1]:
                    ans += 1
        return ans
```

## 69. `3778_8` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/transform-array-by-parity/
- Precision: 0.250
- Test pass: [Y ]

```python
class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        even = sum(x % 2 == 0 for x in nums)
        result = []
        for i in range(even):
            result.append(0)
        for i in range(even, len(nums)):
            result.append(1)
        return sorted(result)
```

## 70. `3750_25` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/closest-equal-element-queries/
- Precision: 0.667
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def solveQueries(self, nums: List[int], queries: List[int]) -> List[int]:
        n = len(nums)
        m = n << 1
        d = [m] * m
        left = {}
        for i in range(m):
            x = nums[i % n]
            if x in left:
                d[i] = min(d[i], i - left[x])
            left[x] = i
        right = {}
        for i in range(m - 1, -1, -1):
            x = nums[i % n]
            if x in right:
                d[i] = min(d[i], right[x] - i)
            right[x] = i
        for i in range(n):
            d[i] = min(d[i], d[i + n])
        return [-1 if d[i] >= n else d[i] for i in queries]
```

## 71. `3081_42` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/minimum-array-length-after-pair-removals/
- Precision: 0.500
- Test pass: [Y ]

```python
from typing import List
from collections import Counter
from heapq import heapify, heappop, heappush

class Solution:
    def minLengthAfterRemovals(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        pq = [-x for x in cnt.values()]
        heapify(pq)
        ans = len(nums)
        while len(pq) > 1:
            x, y = -heappop(pq), -heappop(pq)
            x -= 1
            y -= 1
            if x > 0:
                heappush(pq, -x)
            if y > 0:
                heappush(pq, -y)
            ans -= 2
        return ans
```

## 72. `3454_37` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-array-equal-to-target/
- Precision: 0.750
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def minimumOperations(self, nums: List[int], target: List[int]) -> int:
        total = 0
        prev = 0
        for i in range(len(nums)):
            cur = target[i] - nums[i]
            total += abs(cur - prev)
            prev = cur
        total += abs(prev)
        return total // 2
```

## 73. `3460_64` — deepseek-chat

- LeetCode: https://leetcode.com/problems/count-the-number-of-inversions/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        req = [-1] * n
        for end, cnt in requirements:
            req[end] = cnt
        if req[0] not in (0, -1):
            return 0
        req[0] = 0
        mod = 10**9 + 7
        m = max(req)
        f = [[0] * (m + 1) for _ in range(n)]
        f[0][0] = 1
        for i in range(1, n):
            l, r = 0, m
            if req[i] >= 0:
                l = r = req[i]
            for j in range(l, r + 1):
                for k in range(min(i, j) + 1):
                    f[i][j] = (f[i][j] + f[i - 1][j - k]) % mod
        return f[n - 1][req[n - 1]]
```

## 74. `3106_39` — deepseek-chat

- LeetCode: https://leetcode.com/problems/length-of-the-longest-subsequence-that-sums-to-target/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def lengthOfLongestSubsequence(self, nums: List[int], target: int) -> int:
        n = len(nums)
        f = [[-float('inf')] * (target + 1) for _ in range(n + 1)]
        f[0][0] = 0
        for i, x in enumerate(nums, 1):
            for j in range(target + 1):
                f[i][j] = f[i - 1][j]
                if j >= x:
                    f[i][j] = max(f[i][j], f[i - 1][j - x] + 1)
        return -1 if f[n][target] <= 0 else f[n][target]
```

## 75. `3362_12` — deepseek-chat

- LeetCode: https://leetcode.com/problems/find-the-median-of-the-uniqueness-array/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def medianOfUniquenessArray(self, nums: List[int]) -> int:
        def check(mx: int) -> bool:
            cnt = defaultdict(int)
            k = l = 0
            for r, x in enumerate(nums):
                cnt[x] += 1
                while len(cnt) > mx:
                    y = nums[l]
                    cnt[y] -= 1
                    if cnt[y] == 0:
                        cnt.pop(y)
                    l += 1
                k += r - l + 1
                if k >= target:
                    return True
            return False

        n = len(nums)
        total = n * (n + 1) // 2
        target = (total + 1) // 2
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if check(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
```

## 76. `3292_29` — deepseek-chat

- LeetCode: https://leetcode.com/problems/earliest-second-to-mark-indices-i/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
    def earliestSecondToMarkIndices(
        self, nums: List[int], changeIndices: List[int]
    ) -> int:
        def check(t: int) -> bool:
            decrement = 0
            marked = 0
            last = {}
            for s, i in enumerate(changeIndices[:t], 1):
                last[i] = s
            for s, i in enumerate(changeIndices[:t], 1):
                if last[i] == s:
                    if decrement < nums[i - 1]:
                        return False
                    decrement -= nums[i - 1]
                    marked += 1
                else:
                    decrement += 1
            return marked == len(nums)
        
        m = len(changeIndices)
        l = bisect_left(range(1, m + 2), True, key=check) + 1
        return -1 if l > m else l
```

## 77. `3460_0` — deepseek-chat

- LeetCode: https://leetcode.com/problems/count-the-number-of-inversions/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        req = [-1] * n
        for end, cnt in requirements:
            req[end] = cnt
        if req[0] > 0:
            return 0
        req[0] = 0
        mod = 10**9 + 7
        m = max(req)
        f = [[0] * (m + 1) for _ in range(n)]
        f[0][0] = 1

        for i in range(1, n):
            l, r = 0, m
            if req[i] >= 0:
                l = r = req[i]
            for j in range(l, r + 1):
                for k in range(min(i, j) + 1):
                    f[i][j] = (f[i][j] + f[i - 1][j - k]) % mod
        return f[n - 1][req[n - 1]]
```

## 78. `3764_32` — deepseek-chat

- LeetCode: https://leetcode.com/problems/maximum-sum-with-at-most-k-elements/
- Precision: 0.600
- Test pass: [Y ]

```python
class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        pq = []
        for nums, limit in zip(grid, limits):
            nums.sort(reverse=True)
            for i in range(min(limit, len(nums))):
                heappush(pq, nums[i])
                if len(pq) > k:
                    heappop(pq)
        return sum(pq)
```

## 79. `3017_31` — deepseek-chat

- LeetCode: https://leetcode.com/problems/number-of-beautiful-integers-in-the-range/
- Precision: 0.032
- Test pass: [Y ]

```python
class Solution:
    def numberOfBeautifulIntegers(self, low: int, high: int, k: int) -> int:
        from functools import cache
        
        def solve(x: int) -> int:
            s = str(x)
            
            @cache
            def dfs(pos: int, mod: int, diff: int, lead: int, limit: int) -> int:
                if pos >= len(s):
                    return 1 if mod == 0 and diff == 0 and not lead else 0
                up = int(s[pos]) if limit else 9
                ans = 0
                for i in range(up + 1):
                    if i == 0 and lead:
                        ans += dfs(pos + 1, mod, diff, 1, limit and i == up)
                    else:
                        nxt = diff + (1 if i % 2 == 1 else -1)
                        ans += dfs(pos + 1, (mod * 10 + i) % k, nxt, 0, limit and i == up)
                return ans
            
            return dfs(0, 0, 0, 1, 1)
        
        return solve(high) - solve(low - 1)
```

## 80. `3649_4` — deepseek-chat

- LeetCode: https://leetcode.com/problems/minimum-time-to-break-locks-i/
- Precision: 0.200
- Test pass: [Y ]

```python
import itertools
from typing import List

class Solution:
    def findMinimumTime(self, strength: List[int], K: int) -> int:
        min_time = float('inf')
        for perm in itertools.permutations(strength):
            x = 1
            current_time = 0
            for s in perm:
                t = (s + x - 1) // x
                current_time += t
                x += K
            if current_time < min_time:
                min_time = current_time
        return min_time
```

## 81. `3485_10` — deepseek-chat

- LeetCode: https://leetcode.com/problems/maximize-score-of-numbers-in-ranges/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def maxPossibleScore(self, start: List[int], d: int) -> int:
        def check(mi: int) -> bool:
            last = -float('inf')
            for st in start:
                if last + mi > st + d:
                    return False
                last = max(st, last + mi)
            return True

        start.sort()
        l, r = 0, start[-1] + d - start[0]
        while l < r:
            mid = (l + r + 1) >> 1
            if check(mid):
                l = mid
            else:
                r = mid - 1
        return l
```

## 82. `3382_12` — deepseek-chat

- LeetCode: https://leetcode.com/problems/find-the-number-of-subarrays-where-boundary-elements-are-maximum/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def numberOfSubarrays(self, nums: List[int]) -> int:
        stk = []
        ans = 0
        for x in nums:
            while stk and stk[-1][0] < x:
                stk.pop()
            if not stk or stk[-1][0] != x:
                stk.append([x, 1])
            else:
                stk[-1][1] += 1
            ans += stk[-1][1]
        return ans
```

## 83. `3460_50` — deepseek-chat

- LeetCode: https://leetcode.com/problems/count-the-number-of-inversions/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        req = [-1] * n
        for end, cnt in requirements:
            req[end] = cnt
        if req[0] not in (0, -1):
            return 0
        req[0] = 0
        mod = 10**9 + 7
        m = max(req)
        f = [[0] * (m + 1) for _ in range(n)]
        f[0][0] = 1
        for i in range(1, n):
            l, r = 0, m
            if req[i] != -1:
                l = r = req[i]
            for j in range(l, r + 1):
                for k in range(min(i, j) + 1):
                    f[i][j] = (f[i][j] + f[i - 1][j - k]) % mod
        return f[n - 1][req[n - 1]]
```

## 84. `3240_17` — deepseek-chat

- LeetCode: https://leetcode.com/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        from functools import lru_cache
        
        @lru_cache(None)
        def dfs(pos, limit, cnt):
            if pos == 0:
                return cnt
            ans = 0
            up = (self.num >> (pos - 1)) & 1 if limit else 1
            for i in range(up + 1):
                ans += dfs(pos - 1, limit and i == up, cnt + (i == 1 and pos % x == 0))
            return ans

        l, r = 1, 10**18
        while l < r:
            mid = (l + r + 1) >> 1
            self.num = mid
            v = dfs(mid.bit_length(), True, 0)
            dfs.cache_clear()
            if v <= k:
                l = mid
            else:
                r = mid - 1
        return l
```

## 85. `3226_26` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-number-game/
- Precision: 0.333
- Test pass: [Y ]

```python
from typing import List
from heapq import heapify, heappop

class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        heapify(nums)
        ans = []
        while nums:
            a = heappop(nums)
            b = heappop(nums)
            ans.append(b)
            ans.append(a)
        return ans
```

## 86. `3219_25` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/make-lexicographically-smallest-array-by-swapping-elements/
- Precision: 0.667
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def lexicographicallySmallestArray(self, nums: List[int], limit: int) -> List[int]:
        n = len(nums)
        arr = sorted(zip(nums, range(n)))
        i = 0
        ans = [0] * n
        while i < n:
            j = i + 1
            while j < n and arr[j][0] - arr[j - 1][0] <= limit:
                j += 1
            idx = sorted(k for x, k in arr[i:j])
            for k, (x, _) in zip(idx, arr[i:j]):
                ans[k] = x
            i = j
        return ans
```

## 87. `2837_12` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-the-integer-zero/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def makeTheIntegerZero(self, num1: int, num2: int) -> int:
        for k in range(1, 61):
            x = num1 - k * num2
            if x < 0:
                break
            if x.bit_count() <= k <= x:
                return k
        return -1
```

## 88. `3720_15` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimize-the-maximum-edge-weight-of-graph/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minMaxWeight(self, n: int, edges: List[List[int]], threshold: int) -> int:
        MAX = 1000000
        reversedGraph = [[] for _ in range(n)]
        for u, v, w in edges:
            reversedGraph[v].append((u, w))
        l = 0
        r = MAX + 1
        while l < r:
            m = (l + r) // 2
            if self._dfs(reversedGraph, 0, m) == n:
                r = m
            else:
                l = m + 1
        return -1 if l == MAX + 1 else l

    def _dfs(self, reversedGraph, start, maxWeight):
        seen = set()
        stack = [start]
        seen.add(start)
        while stack:
            node = stack.pop()
            for v, w in reversedGraph[node]:
                if w <= maxWeight and v not in seen:
                    seen.add(v)
                    stack.append(v)
        return len(seen)
```

## 89. `3327_70` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-moves-to-pick-k-ones/
- Precision: 0.176
- Test pass: [Y ]

```python
class Solution:
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        n = len(nums)
        cnt = [0] * (n + 1)
        s = [0] * (n + 1)
        for i, x in enumerate(nums, 1):
            cnt[i] = cnt[i - 1] + x
            s[i] = s[i - 1] + i * x
        inf = float('inf')
        ans = inf
        for i, x in enumerate(nums, 1):
            t = 0
            need = k - x
            # Count immediate neighbors that are ones
            b = 0
            for j in (i - 1, i + 1):
                if 1 <= j <= n and nums[j - 1] == 1:
                    b += 1
            use_neighbors = min(need, b)
            t += use_neighbors
            need -= use_neighbors
            c = min(need, maxChanges)
            need -= c
            t += c * 2
            if need <= 0:
                ans = min(ans, t)
                continue
            l, r = 2, max(i - 1, n - i)
            while l <= r:
                mid = (l + r) >> 1
                l1 = max(1, i - mid)
                r1 = max(0, i - 2)
                l2 = min(n + 1, i + 2)
                r2 = min(n, i + mid)
                c1 = max(0, cnt[r1] - cnt[l1 - 1])
                c2 = max(0, cnt[r2] - cnt[l2 - 1])
                if c1 + c2 >= need:
                    t1 = c1 * i - (s[r1] - s[l1 - 1])
                    t2 = s[r2] - s[l2 - 1] - c2 * i
                    ans = min(ans, t + t1 + t2)
                    r = mid - 1
                else:
                    l = mid + 1
        return ans
```

## 90. `3638_37` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-character-frequencies-equal/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def makeStringGood(self, s: str) -> int:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        return min(self._getMinOperations(count, target) for target in range(1, max(count) + 1))

    def _getMinOperations(self, count: list[int], target: int) -> int:
        dp = [0] * 27

        for i in range(25, -1, -1):
            deleteAllToZero = count[i]
            deleteOrInsertToTarget = abs(target - count[i])
            dp[i] = min(deleteAllToZero, deleteOrInsertToTarget) + dp[i + 1]

            if i + 1 < 26:
                c1 = count[i]
                c2 = count[i + 1]
                T = target
                cost00 = c1 + c2
                cand0T = {0, c1}
                if T >= c2:
                    cand0T.add(T - c2)
                cost0T = min(k + abs(c1 - k) + abs(c2 + k - T) for k in cand0T)
                costT0 = abs(c1 - T) + c2
                candTT = {0}
                if c1 >= T:
                    candTT.add(c1 - T)
                if T >= c2:
                    candTT.add(T - c2)
                costTT = min(k + abs(c1 - k - T) + abs(c2 + k - T) for k in candTT)
                pair_cost = min(cost00, cost0T, costT0, costTT)
                dp[i] = min(dp[i], pair_cost + dp[i + 2])

        return dp[0]
```

## 91. `2883_45` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/partition-string-into-minimum-beautiful-substrings/
- Precision: 0.154
- Test pass: [Y ]

```python
class Solution:
    def minimumBeautifulSubstrings(self, s: str) -> int:
        from functools import lru_cache
        
        @lru_cache(None)
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            if s[i] == "0":
                return float('inf')
            x = 0
            ans = float('inf')
            for j in range(i, n):
                x = x << 1 | int(s[j])
                if x in powers:
                    ans = min(ans, 1 + dfs(j + 1))
            return ans

        n = len(s)
        max_val = (1 << n) - 1
        powers = set()
        p = 1
        while p <= max_val:
            powers.add(p)
            p *= 5
        ans = dfs(0)
        return -1 if ans == float('inf') else ans
```

## 92. `2921_51` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/count-stepping-numbers-in-range/
- Precision: 0.238
- Test pass: [Y ]

```python
from functools import lru_cache

class Solution:
    def countSteppingNumbers(self, low: str, high: str) -> int:
        mod = 10**9 + 7
        
        def dec_string(s: str) -> str:
            if s == "1":
                return "0"
            digits = list(s)
            i = len(digits) - 1
            while i >= 0 and digits[i] == '0':
                digits[i] = '9'
                i -= 1
            digits[i] = chr(ord(digits[i]) - 1)
            result = ''.join(digits).lstrip('0')
            if not result:
                return "0"
            return result
        
        @lru_cache(maxsize=None)
        def dfs(pos: int, pre: int, lead: bool, limit: bool) -> int:
            if pos >= len(num):
                return int(not lead)
            up = int(num[pos]) if limit else 9
            ans = 0
            for i in range(up + 1):
                if i == 0 and lead:
                    ans += dfs(pos + 1, pre, True, limit and i == up)
                elif pre == -1 or abs(i - pre) == 1:
                    ans += dfs(pos + 1, i, False, limit and i == up)
            return ans % mod
        
        num = high
        a = dfs(0, -1, True, True)
        dfs.cache_clear()
        low_minus_one = dec_string(low)
        num = low_minus_one
        b = dfs(0, -1, True, True)
        return (a - b) % mod
```

## 93. `3081_5` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-array-length-after-pair-removals/
- Precision: 0.250
- Test pass: [Y ]

```python
from collections import Counter
from heapq import heapify, heappop, heappush
from typing import List

class Solution:
    def minLengthAfterRemovals(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        pq = [-x for x in cnt.values()]
        heapify(pq)
        ans = len(nums)
        while len(pq) > 1:
            x, y = -heappop(pq), -heappop(pq)
            x -= 1
            y -= 1
            if x > 0:
                heappush(pq, -x)
            if y > 0:
                heappush(pq, -y)
            ans -= 2
        return ans
```

## 94. `3141_28` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-size-subarray-in-infinite-array/
- Precision: 0.069
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def minSizeSubarray(self, nums: List[int], target: int) -> int:
        s = sum(nums)
        n = len(nums)
        k = target // s
        ans = float('inf')
        # Try m = k and m = k-1 (if k > 0)
        for m in (k, k - 1):
            if m < 0:
                continue
            full_len = m * n
            t = target - m * s
            if t == 0:
                ans = min(ans, full_len)
                continue
            # Find shortest subarray summing to t within two copies of nums
            pos = {0: -1}
            pre = 0
            best = float('inf')
            # Iterate over two copies
            for i in range(2 * n):
                x = nums[i % n]
                pre += x
                need = pre - t
                if need in pos:
                    best = min(best, i - pos[need])
                if pre not in pos:
                    pos[pre] = i
            if best != float('inf'):
                ans = min(ans, full_len + best)
        return -1 if ans == float('inf') else ans
```

## 95. `2847_1` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/find-maximum-number-of-string-pairs/
- Precision: 0.333
- Test pass: [Y ]

```python
from collections import Counter
from typing import List

class Solution:
    def maximumNumberOfStringPairs(self, words: List[str]) -> int:
        cnt = Counter()
        ans = 0
        for w in words:
            ans += cnt[w[::-1]]
            cnt[w] += 1
        return ans
```

## 96. `2916_50` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/check-if-it-is-possible-to-split-array/
- Precision: 0.333
- Test pass: [Y ]

```python
from typing import List
from itertools import accumulate
from functools import lru_cache

class Solution:
    def canSplitArray(self, nums: List[int], m: int) -> bool:
        s = list(accumulate(nums, initial=0))
        
        @lru_cache(None)
        def dfs(i: int, j: int) -> bool:
            if i == j:
                return True
            for k in range(i, j):
                a = k == i or s[k + 1] - s[i] >= m
                b = k == j - 1 or s[j + 1] - s[k + 1] >= m
                if a and b and dfs(i, k) and dfs(k + 1, j):
                    return True
            return False
        
        return dfs(0, len(nums) - 1)
```

## 97. `3754_39` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-manhattan-distance-after-k-changes/
- Precision: 0.077
- Test pass: [Y ]

```python
class Solution:
    def maxDistance(self, s: str, k: int) -> int:
        def calc(a: str, b: str) -> int:
            pos = {a, b}
            neg = best = length = 0
            for c in s:
                length += 1
                if c not in pos:
                    neg += 1
                val = length
                if neg > k:
                    val -= 2 * (neg - k)
                if val > best:
                    best = val
            return best

        a = calc("S", "E")
        b = calc("S", "W")
        c = calc("N", "E")
        d = calc("N", "W")
        return max(a, b, c, d)
```

## 98. `3510_37` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximize-the-total-height-of-unique-towers/
- Precision: 0.800
- Test pass: [Y ]

```python
class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight = maximumHeight[:]
        maximumHeight.sort()
        ans, mx = 0, float('inf')
        for x in maximumHeight[::-1]:
            if mx != float('inf'):
                x = min(x, mx - 1)
            if x <= 0:
                return -1
            ans += x
            mx = x
        return ans
```

## 99. `3737_4` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/paint-house-iv/
- Precision: 0.167
- Test pass: [Y ]

```python
from typing import List
from collections import defaultdict

class Solution:
    def minCost(self, n: int, cost: List[List[int]]) -> int:
        prev_dp = {}
        
        first_left = 0
        first_right = n - 1
        for L in [1, 2, 3]:
            for R in [1, 2, 3]:
                if L != R:
                    total = cost[0][L-1] + cost[first_right][R-1]
                    prev_dp[(L, R)] = total
        
        for i in range(1, n//2):
            current_right_pos = n - 1 - i
            curr_dp = defaultdict(lambda: float('inf'))
            for (prev_L, prev_R), prev_cost in prev_dp.items():
                for L in [1, 2, 3]:
                    if L == prev_L:
                        continue
                    for R in [1, 2, 3]:
                        if R == L or R == prev_R:
                            continue
                        new_cost = prev_cost + cost[i][L-1] + cost[current_right_pos][R-1]
                        key = (L, R)
                        if new_cost < curr_dp[key]:
                            curr_dp[key] = new_cost
            prev_dp = {}
            for k, v in curr_dp.items():
                if v < float('inf'):
                    prev_dp[k] = v
            if not prev_dp:
                return -1
        
        return min(prev_dp.values()) if prev_dp else 0
```

## 100. `3372_57` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        ans = inc = dec = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                inc += 1
            else:
                inc = 1
            if nums[i] < nums[i - 1]:
                dec += 1
            else:
                dec = 1
            ans = max(ans, inc, dec)
        return ans
```

## 101. `3736_1` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/find-valid-pair-of-adjacent-digits-in-string/
- Precision: 0.500
- Test pass: [Y ]

```python
from itertools import pairwise

class Solution:
    def findValidPair(self, s: str) -> str:
        cnt = [0] * 10
        for x in map(int, s):
            cnt[x] += 1
        for x, y in pairwise(map(int, s)):
            if x != y and cnt[x] == x and cnt[y] == y:
                return f"{x}{y}"
        return ""
```

## 102. `3267_39` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/find-longest-special-substring-that-occurs-thrice-i/
- Precision: 0.200
- Test pass: [Y ]

```python
from collections import defaultdict

class Solution:
    def maximumLength(self, s: str) -> int:
        def check(x: int) -> bool:
            cnt = defaultdict(int)
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                cnt[s[i]] += max(0, j - i - x + 1)
                i = j
            return any(v >= 3 for v in cnt.values())

        n = len(s)
        l, r = 1, n
        ans = 0
        while l <= r:
            mid = (l + r) >> 1
            if check(mid):
                ans = mid
                l = mid + 1
            else:
                r = mid - 1
        return -1 if ans == 0 else ans
```

## 103. `3240_40` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/
- Precision: 0.750
- Test pass: [Y ]

```python
from functools import lru_cache

class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        @lru_cache(None)
        def dfs(pos, limit, cnt):
            if pos == 0:
                return cnt
            ans = 0
            up = (self.num >> (pos - 1) & 1) if limit else 1
            for i in range(up + 1):
                ans += dfs(pos - 1, limit and i == up, cnt + (i == 1 and pos % x == 0))
            return ans

        l, r = 1, 10**18
        while l < r:
            mid = (l + r + 1) >> 1
            self.num = mid
            v = dfs(mid.bit_length(), True, 0)
            dfs.cache_clear()
            if v <= k:
                l = mid
            else:
                r = mid - 1
        return l
```

## 104. `3648_17` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/find-the-maximum-number-of-fruits-collected/
- Precision: 0.030
- Test pass: [Y ]

```python
from typing import List

class Solution:
  def maxCollectedFruits(self, fruits: List[List[int]]) -> int:
    n = len(fruits)

    def getTopLeft() -> int:
      return sum(fruits[i][i] for i in range(n))

    def getTopRight() -> int:
      NEG = -10**18
      dp = [[NEG] * n for _ in range(n)]
      dp[0][-1] = fruits[0][-1]
      for x in range(n):
        for y in range(n):
          if (x, y) == (0, n - 1):
            continue
          if x >= y and (x, y) != (n - 1, n - 1):
            continue
          best = NEG
          for px, py in [(x - 1, y + 1), (x - 1, y), (x - 1, y - 1)]:
            if px < 0 or px == n or py < 0 or py == n:
              continue
            if px >= py and (px, py) != (n - 1, n - 1):
              continue
            if dp[px][py] == NEG:
              continue
            best = max(best, dp[px][py])
          if best == NEG:
            continue
          dp[x][y] = best + fruits[x][y]
      return dp[-1][-1]

    def getBottomLeft() -> int:
      NEG = -10**18
      dp = [[NEG] * n for _ in range(n)]
      dp[-1][0] = fruits[-1][0]
      for y in range(n):
        for x in range(n):
          if (x, y) == (n - 1, 0):
            continue
          if x <= y and (x, y) != (n - 1, n - 1):
            continue
          best = NEG
          for px, py in [(x + 1, y - 1), (x, y - 1), (x - 1, y - 1)]:
            if px < 0 or px == n or py < 0 or py == n:
              continue
            if px <= py and (px, py) != (n - 1, n - 1):
              continue
            if dp[px][py] == NEG:
              continue
            best = max(best, dp[px][py])
          if best == NEG:
            continue
          dp[x][y] = best + fruits[x][y]
      return dp[-1][-1]

    return getTopLeft() + getTopRight() + getBottomLeft() - 2 * fruits[-1][-1]
```

## 105. `3559_53` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-i/
- Precision: 0.235
- Test pass: [Y ]

```python
from functools import lru_cache
from typing import List, Optional


def min(a: int, b: int) -> int:
    return a if a < b else b


class Trie:
    def __init__(self):
        self.children: List[Optional["Trie"]] = [None] * 26

    def insert(self, w: str):
        node = self
        for i in map(lambda c: ord(c) - 97, w):
            if node.children[i] is None:
                node.children[i] = Trie()
            node = node.children[i]


class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        trie = Trie()
        for w in words:
            trie.insert(w)
        n = len(target)
        inf = float('inf')

        @lru_cache(None)
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            node = trie
            ans = inf
            for j in range(i, n):
                k = ord(target[j]) - 97
                if node.children[k] is None:
                    break
                node = node.children[k]
                candidate = 1 + dfs(j + 1)
                if candidate < ans:
                    ans = candidate
            return ans

        ans = dfs(0)
        return ans if ans < inf else -1
```

## 106. `3612_5` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/adjacent-increasing-subarrays-detection-i/
- Precision: 0.062
- Test pass: [Y ]

```python
class Solution:
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        for start in range(n - 2 * k + 1):
            valid = True
            for i in range(start + 1, start + k):
                if nums[i - 1] >= nums[i]:
                    valid = False
                    break
            if not valid:
                continue
            for i in range(start + k + 1, start + 2 * k):
                if nums[i - 1] >= nums[i]:
                    valid = False
                    break
            if valid:
                return True
        return False
```

## 107. `3372_55` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/longest-strictly-increasing-or-strictly-decreasing-subarray/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def longestMonotonicSubarray(self, nums: List[int]) -> int:
        inc = dec = ans = 1
        for i in range(1, len(nums)):
            if nums[i] > nums[i - 1]:
                inc += 1
            else:
                inc = 1
            if nums[i] < nums[i - 1]:
                dec += 1
            else:
                dec = 1
            ans = max(ans, inc, dec)
        return ans
```

## 108. `3620_11` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-number-of-distinct-elements-after-operations/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def maxDistinctElements(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = 0
        pre = float('-inf')
        for x in nums:
            cur = min(x + k, max(x - k, pre + 1))
            if cur > pre:
                ans += 1
                pre = cur
        return ans
```

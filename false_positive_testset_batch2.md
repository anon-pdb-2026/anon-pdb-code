# False-Positive Testing Set — PDB-Single (LiveCodeBench)

108 patches: 12 per Table-3b model (seed=1, disjoint from batch 1), drawn from
a pool of 17496 test-passing, ground-truth-differing patches.
Submit each code block to the linked LeetCode problem; a rejection by
LeetCode's hidden tests marks a scoring false positive in PDB.

## 1. `3025_14` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/minimum-operations-to-form-subsequence-with-target-sum/
- Precision: 0.500
- Test pass: [Y ]

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
                ans += 1
            cnt[j] -= 1
            j = i
            i += 1
        return ans
```

## 2. `3657_34` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/check-if-grid-can-be-cut-into-sections/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def countLineIntersections(self, coordinates: List[tuple[int, int]]) -> bool:
        overlap = 0
        lines = 0
        for value, marker in coordinates:
            if marker == 0:
                overlap -= 1
            else:
                overlap += 1

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

## 3. `2855_32` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/maximum-number-of-jumps-to-reach-the-last-index/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def maximumJumps(self, nums: List[int], target: int) -> int:
        @cache
        def dfs(i: int) -> int:
            if i == n - 1:
                return 0
            ans = float('-inf')
            for j in range(i + 1, n):
                if abs(nums[j] - nums[i]) <= target:
                    ans = max(ans, 1 + dfs(j))
            return ans

        n = len(nums)
        ans = dfs(0)
        return ans if ans >= 0 else -1
```

## 4. `3243_47` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/count-the-number-of-powerful-integers/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def numberOfPowerfulInt(self, start: int, finish: int, limit: int, s: str) -> int:
        from functools import cache
        
        def count(num_str: str) -> int:
            @cache
            def dfs(pos: int, lim: int):
                if len(num_str) < n:
                    return 0
                if len(num_str) - pos == n:
                    return int(s <= num_str[pos:]) if lim else 1
                up = min(int(num_str[pos]) if lim else 9, limit)
                ans = 0
                for i in range(up + 1):
                    ans += dfs(pos + 1, lim and i == int(num_str[pos]))
                return ans
            
            return dfs(0, True)
        
        n = len(s)
        a = count(str(start - 1))
        b = count(str(finish))
        return b - a
```

## 5. `2952_43` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/minimum-time-to-make-array-sum-at-most-x/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def minimumTime(self, nums1: List[int], nums2: List[int], x: int) -> int:
        n = len(nums1)
        f = [[0] * (n + 1) for _ in range(n + 1)]
        for i, (a, b) in enumerate(sorted(zip(nums1, nums2), key=lambda z: z[1]), 1):
            for j in range(n + 1):
                if j > 0:
                    f[i][j] = max(f[i][j], f[i - 1][j - 1] + a + b * j)
                f[i][j] = max(f[i][j], f[i - 1][j])
        s1 = sum(nums1)
        s2 = sum(nums2)
        for j in range(n + 1):
            if s1 + s2 * j - f[n][j] <= x:
                return j
        return -1
```

## 6. `3354_42` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/replace-question-marks-in-string-to-minimize-its-value/
- Precision: 0.600
- Test pass: [Y ]

```python
class Solution:
    def minimizeStringValue(self, s: str) -> str:
        from collections import Counter
        from heapq import heapify, heapreplace
        
        cnt = Counter(s)
        pq = [(cnt[c], c) for c in 'abcdefghijklmnopqrstuvwxyz']
        heapify(pq)
        t = []
        for _ in range(s.count("?")):
            v, c = pq[0]
            t.append(c)
            heapreplace(pq, (v + 1, c))
        t.sort()
        cs = list(s)
        j = 0
        for i, c in enumerate(s):
            if c == "?":
                cs[i] = t[j]
                j += 1
        return "".join(cs)
```

## 7. `3532_33` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/time-taken-to-mark-all-nodes/
- Precision: 0.750
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
    return 1 if u % 2 != 0 else 2

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

## 8. `3510_18` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/maximize-the-total-height-of-unique-towers/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight.sort()
        ans, mx = 0, inf
        for x in maximumHeight[::-1]:
            x = min(x, mx)
            if x <= 0:
                return -1
            ans += x
            mx = x - 1
        return ans
```

## 9. `3770_29` — claude-sonnet-4-5-20250929

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

## 10. `3423_27` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/
- Precision: 0.500
- Test pass: [Y ]

```python
def max(a: int, b: int) -> int:
    return a if a > b else b


class Node:
    __slots__ = "l", "r", "s00", "s01", "s10", "s11"

    def __init__(self, l: int, r: int):
        self.l = l
        self.r = r
        self.s00 = self.s01 = self.s10 = self.s11 = 0


class SegmentTree:
    __slots__ = "tr"

    def __init__(self, n: int):
        self.tr: List[Node | None] = [None] * (n << 2)
        self.build(1, 1, n)

    def build(self, u: int, l: int, r: int):
        self.tr[u] = Node(l, r)
        if l == r:
            return
        mid = (l + r) >> 1
        self.build(u << 1, l, mid)
        self.build(u << 1 | 1, mid + 1, r)

    def query(self, u: int, l: int, r: int) -> int:
        if self.tr[u].l >= l and self.tr[u].r <= r:
            return self.tr[u].s11
        mid = (self.tr[u].l + self.tr[u].r) >> 1
        ans = 0
        if r <= mid:
            ans = self.query(u << 1, l, r)
        if l > mid:
            ans = max(ans, self.query(u << 1 | 1, l, r))
        return ans

    def pushup(self, u: int):
        left, right = self.tr[u << 1], self.tr[u << 1 | 1]
        self.tr[u].s00 = max(left.s00 + right.s10, left.s01 + right.s00)
        self.tr[u].s01 = max(left.s00 + right.s11, left.s01 + right.s01)
        self.tr[u].s10 = max(left.s10 + right.s10, left.s11 + right.s00)
        self.tr[u].s11 = max(left.s10 + right.s11, left.s11 + right.s01)

    def modify(self, u: int, x: int, v: int):
        if self.tr[u].l == self.tr[u].r:
            self.tr[u].s11 = max(0, v)
            self.tr[u].s00 = 0
            self.tr[u].s01 = 0
            self.tr[u].s10 = 0
            return
        mid = (self.tr[u].l + self.tr[u].r) >> 1
        if x <= mid:
            self.modify(u << 1, x, v)
        else:
            self.modify(u << 1 | 1, x, v)
        self.pushup(u)


class Solution:
    def maximumSumSubsequence(self, nums: List[int], queries: List[List[int]]) -> int:
        n = len(nums)
        tree = SegmentTree(n)
        for i, x in enumerate(nums, 1):
            tree.modify(1, i, x)
        ans = 0
        mod = 10**9 + 7
        for i, x in queries:
            tree.modify(1, i + 1, x)
            ans = (ans + tree.query(1, 1, n)) % mod
        return ans
```

## 11. `3213_0` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        mx = max(nums)
        n = len(nums)
        ans = cnt = j = 0
        for i, x in enumerate(nums):
            while j < n and cnt < k:
                cnt += nums[j] == mx
                j += 1
            if cnt < k:
                break
            ans += n - j + 1
            cnt -= x == mx
        return ans
```

## 12. `2882_64` — claude-sonnet-4-5-20250929

- LeetCode: https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/
- Precision: 0.800
- Test pass: [Y ]

```python
class Solution:
    def numberOfWays(self, n: int, x: int) -> int:
        MOD = 10**9 + 7
        candidates = []
        i = 1
        while True:
            current = i ** x
            if current > n:
                break
            candidates.append(current)
            i += 1

        dp = [0] * (n + 1)
        dp[0] = 1

        for num in candidates:
            for s in range(n, num - 1, -1):
                dp[s] = (dp[s] + dp[s - num]) % MOD

        return dp[n]
```

## 13. `3507_52` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/find-the-count-of-numbers-which-are-not-special/
- Precision: 0.800
- Test pass: [Y ]

```python
from math import sqrt, floor, ceil

m = 31623
primes = [True] * (m + 1)
primes[0] = primes[1] = False
for i in range(2, m + 1):
    if primes[i]:
        for j in range(i + i, m + 1, i):
            primes[j] = False


class Solution:
    def nonSpecialCount(self, l: int, r: int) -> int:
        lo = ceil(sqrt(l))
        hi = floor(sqrt(r))
        cnt = sum(primes[i] for i in range(lo, hi + 1))
        return (r - l + 1) - cnt
```

## 14. `2827_61` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/greatest-common-divisor-traversal/
- Precision: 0.069
- Test pass: [Y ]

```python
from collections import defaultdict
from typing import List

class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb:
            return False
        if self.size[pa] > self.size[pb]:
            self.p[pb] = pa
            self.size[pa] += self.size[pb]
        else:
            self.p[pa] = pb
            self.size[pb] += self.size[pa]
        return True


mx = 100001
p = defaultdict(list)
for x in range(1, mx):
    v = x
    i = 2
    while i <= v // i:
        if v % i == 0:
            p[x].append(i)
            while v % i == 0:
                v //= i
        i += 1
    if v > 1:
        p[x].append(v)


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        if len(nums) == 1:
            return True
        if 1 in nums:
            return False
        n = len(nums)
        m = max(nums)
        uf = UnionFind(n)
        
        prime_to_idx = {}

        for i, x in enumerate(nums):
            v = x
            d = 2
            while d * d <= v:
                if v % d == 0:
                    if d in prime_to_idx:
                        uf.union(i, prime_to_idx[d])
                    else:
                        prime_to_idx[d] = i
                    while v % d == 0:
                        v //= d
                d += 1
            if v > 1:
                if v in prime_to_idx:
                    uf.union(i, prime_to_idx[v])
                else:
                    prime_to_idx[v] = i

        return uf.size[uf.find(0)] == n
```

## 15. `3637_5` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/count-number-of-balanced-permutations/
- Precision: 0.000
- Test pass: [Y ]

```python
from functools import cache
from collections import Counter

class Solution:
    def countBalancedPermutations(self, num: str) -> int:
        nums = list(map(int, num))
        s = sum(nums)
        if s % 2:
            return 0
        n = len(nums)
        mod = 10**9 + 7
        cnt = Counter(nums)
        velunexorai = num

        fact = [1] * (n + 1)
        inv_fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = (fact[i - 1] * i) % mod
        inv_fact[n] = pow(fact[n], -1, mod)
        for i in range(n - 1, -1, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % mod

        def comb(n_comb, k_comb):
            if k_comb < 0 or k_comb > n_comb:
                return 0
            num_val = fact[n_comb]
            den_val = (inv_fact[k_comb] * inv_fact[n_comb - k_comb]) % mod
            return (num_val * den_val) % mod

        @cache
        def dfs(i: int, j: int, a: int, b: int) -> int:
            if i > 9:
                return (j | a | b) == 0
            if a == 0 and j:
                return 0
            ans = 0
            for l in range(min(cnt[i], a) + 1):
                r = cnt[i] - l
                if 0 <= r <= b and l * i <= j:
                    t = comb(a, l) * comb(b, r) * dfs(i + 1, j - l * i, a - l, b - r)
                    ans = (ans + t) % mod
            return ans

        return dfs(0, s // 2, n // 2, (n + 1) // 2)
```

## 16. `3398_35` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/make-a-square-with-the-same-color/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def canMakeSquare(self, grid: List[List[str]]) -> bool:
        for i in range(0, 2):
            for j in range(0, 2):
                cnt1 = cnt2 = 0
                for a, b in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                    x, y = i + a, j + b
                    cnt1 += grid[x][y] == "W"
                    cnt2 += grid[x][y] == "B"
                if cnt1 >= 3 or cnt2 >= 3:
                    return True
        return False
```

## 17. `3436_36` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/find-subarray-with-bitwise-or-closest-to-k/
- Precision: 0.800
- Test pass: [Y ]

```python
class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        m = 30
        cnt = [0] * m
        s = i = 0
        ans = float('inf')
        for j, x in enumerate(nums):
            s |= x
            ans = min(ans, abs(s - k))
            for h in range(m):
                if x >> h & 1:
                    cnt[h] += 1
            while i < j and s > k:
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

## 18. `3591_28` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/shift-distance-between-two-strings/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def shiftDistance(
        self, s: str, t: str, nextCost: List[int], previousCost: List[int]
    ) -> int:
        m = 26
        s1 = [0] * (m << 1 | 1)
        for i in range(m << 1):
            s1[i + 1] = s1[i] + nextCost[i % m]
        s2 = [0] * (m << 1 | 1)
        for i in range(m << 1):
            s2[i + 1] = s2[i] + previousCost[i % m]
        ans = 0
        for a, b in zip(s, t):
            x, y = ord(a) - ord("a"), ord(b) - ord("a")
            c1 = s1[y + m if y < x else y] - s1[x]
            c2 = s2[x + 1 + m if x < y else x + 1] - s2[y + 1]
            ans += min(c1, c2)
        return ans
```

## 19. `3786_23` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/longest-palindromic-subsequence-after-at-most-k-operations/
- Precision: 0.667
- Test pass: [Y ]

```python
from functools import lru_cache

class Solution:
    def longestPalindromicSubsequence(self, s: str, k: int) -> int:
        @lru_cache(None)
        def dfs(i: int, j: int, k: int) -> int:
            if i > j:
                return 0
            if i == j:
                return 1
            res = max(dfs(i + 1, j, k), dfs(i, j - 1, k))
            t = min(abs(s[i] - s[j]), 26 - abs(s[i] - s[j]))
            if t <= k:
                res = max(res, dfs(i + 1, j - 1, k - t) + 2)
            return res

        s = list(map(ord, s))
        n = len(s)
        ans = dfs(0, n - 1, k)
        dfs.cache_clear()
        return ans
```

## 20. `3788_14` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/maximum-unique-subarray-sum-after-deletion/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def maxSum(self, nums: List[int]) -> int:
        mx = max(nums)
        if mx <= 0:
            return mx
        ans = 0
        s = []
        for x in nums:
            if x < 0 or x in s:
                continue
            ans += x
            s.append(x)
        return ans
```

## 21. `2755_24` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/extra-characters-in-a-string/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        n = len(s)
        ss = set(dictionary)
        f = [0] * (n + 1)
        for i in range(1, n + 1):
            f[i] = f[i-1] + 1
            for j in range(i):
                if s[j:i] in ss and f[j] < f[i]:
                    f[i] = f[j]
        return f[n]
```

## 22. `3716_47` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/longest-subsequence-with-decreasing-adjacent-difference/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
  def longestSubsequence(self, nums: list[int]) -> int:
    # dp[num][diff] := the length of the longest subsequence ending in `num`
    # s.t. the last absolute difference between consecutive elements is `diff`
    mx = 300
    dp = [[0] * (mx + 1) for _ in range(mx + 1)]

    for num in nums:
      for prev in range(1, mx + 1):
        diff = abs(num - prev)
        dp[num][diff] = max(dp[num][diff], dp[prev][diff] + 1)
      # dp[num][diff] := max(dp[num][j]) for j >= diff
      for j in range(mx - 1, -1, -1):
        dp[num][j] = max(dp[num][j], dp[num][j + 1])

    return max(map(max, dp))
```

## 23. `3453_47` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/generate-binary-strings-without-adjacent-zeros/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
    def validStrings(self, n: int) -> List[str]:
        def dfs(i: int):
            if i == n:
                ans.append("".join(t))
                return
            for j in range(2):
                if (j == 0 and (i == 0 or t[i - 1] == "1")) or j == 1:
                    t.append(str(j))
                    dfs(i + 1)
                    t.pop()

        ans = []
        t = []
        dfs(0)
        return ans
```

## 24. `3239_15` — gemini-2.5-pro

- LeetCode: https://leetcode.com/problems/minimum-number-of-operations-to-make-x-and-y-equal/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def minimumOperationsToMakeEqual(self, x: int, y: int) -> int:
        @cache
        def dfs(x: int) -> int:
            if y >= x:
                return y - x
            ans = x - y
            ans = min(ans, x % 5 + 1 + dfs(x // 5))
            ans = min(ans, (5 - x % 5) % 5 + 1 + dfs((x + 4) // 5))
            ans = min(ans, x % 11 + 1 + dfs(x // 11))
            ans = min(ans, 11 - x % 11 + 1 + dfs((x + 10) // 11))
            return ans

        return dfs(x)
```

## 25. `3263_5` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        a, b, c = nums[0], float('inf'), float('inf')
        for x in nums[1:]:
            if x < b:
                c, b = b, x
            elif x < c:
                c = x
        return a + b + c
```

## 26. `3634_28` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/find-mirror-score-of-a-string/
- Precision: 0.200
- Test pass: [Y ]

```python
class Solution:
    def calculateScore(self, s: str) -> int:
        d = {}
        ans = 0
        marked = set()
        for i, x in enumerate(s):
            y = chr(ord("z") + ord("a") - ord(x))
            if y in d and d[y]:
                j = d[y].pop()
                marked.add(i)
                marked.add(j)
                ans += i - j
            else:
                if x not in d:
                    d[x] = []
                d[x].append(i)
        return ans
```

## 27. `2979_21` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/maximize-the-profit-as-the-salesman/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def maximizeTheProfit(self, n: int, offers: List[List[int]]) -> int:
        offers.sort(key=lambda x: x[1])
        f = [0] * (len(offers) + 1)
        g = [x[1] for x in offers]
        for i, (s, e, v) in enumerate(offers, 1):
            j = bisect_left(g, s)
            f[i] = max(f[i - 1], f[j] + v)
        return f[-1]
```

## 28. `3416_41` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/sum-of-digit-differences-of-all-pairs/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
    def sumDigitDifferences(self, nums: List[int]) -> int:
        n = len(nums)
        m = len(str(nums[0]))
        ans = 0
        for _ in range(m):
            cnt = [0] * 10
            for i, x in enumerate(nums):
                nums[i], y = divmod(x, 10)
                cnt[y] += 1
            ans += sum(v * (n - v) for v in cnt) // 2
        return ans
```

## 29. `2831_48` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/number-of-beautiful-pairs/
- Precision: 0.182
- Test pass: [Y ]

```python
class Solution:
    def countBeautifulPairs(self, nums: List[int]) -> int:
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
            
        cnt = [0] * 10
        ans = 0
        for x in nums:
            first_digit = int(str(x)[0])
            last_digit = x % 10
            for y in range(1, 10):
                if cnt[y] and gcd(y, last_digit) == 1:
                    ans += cnt[y]
            cnt[first_digit] += 1
        return ans
```

## 30. `2816_28` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/lexicographically-smallest-palindrome/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def makeSmallestPalindrome(self, s: str) -> str:
        cs = list(s)
        i, j = 0, len(s) - 1
        while i < j:
            cs[i] = cs[j] = min(cs[i], cs[j])
            i += 1
            j -= 1
        return "".join(cs)
```

## 31. `2827_26` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/greatest-common-divisor-traversal/
- Precision: 0.500
- Test pass: [Y ]

```python
class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, a, b):
        pa, pb = self.find(a), self.find(b)
        if pa == pb:
            return False
        if self.size[pa] > self.size[pb]:
            self.p[pb] = pa
            self.size[pa] += self.size[pb]
        else:
            self.p[pa] = pb
            self.size[pb] += self.size[pa]
        return True


mx = 100010
p = defaultdict(list)
for x in range(1, mx + 1):
    v = x
    i = 2
    while i <= v // i:
        if v % i == 0:
            p[x].append(i)
            while v % i == 0:
                v //= i
        i += 1
    if v > 1:
        p[x].append(v)


class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        n = len(nums)
        if n == 1:
            return True
        m = max(nums)
        uf = UnionFind(n + m + 1)
        for i, x in enumerate(nums):
            for j in p[x]:
                uf.union(i, j + n)
        return len(set(uf.find(i) for i in range(n))) == 1
```

## 32. `3700_2` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/subsequences-with-a-unique-middle-mode-i/
- Precision: 0.000
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
            rightOther = n - 1 - i - rightCount

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
            b2 = count2.get(b, 0)
            # Exclude triples -- [a b] a [b b].
            res = (res - b1 * math.comb(b2, 2)) % self.MOD
            # Exclude doubles -- [a b] a [b ?].
            res = (res - b1 * b2 * (other2 - b2)) % self.MOD

        for b, b2 in count2.items():
            if b == a:
                continue
            b1 = count1.get(b, 0)
            # Exclude doubles -- [a ?] a [b b].
            res = (res - (other1 - b1) * math.comb(b2, 2)) % self.MOD

        return (res + self.MOD) % self.MOD
```

## 33. `3764_5` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/maximum-sum-with-at-most-k-elements/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        pq = []
        for nums, limit in zip(grid, limits):
            nums.sort()
            for _ in range(limit):
                if nums:
                    heappush(pq, nums.pop())
                if len(pq) > k:
                    heappop(pq)
        return sum(pq)
```

## 34. `2779_22` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/number-of-adjacent-elements-with-the-same-color/
- Precision: 0.250
- Test pass: [Y ]

```python
class Solution:
    def colorTheArray(self, n: int, queries: List[List[int]]) -> List[int]:
        nums = [0] * n
        ans = [0] * len(queries)
        x = 0
        for k, (i, c) in enumerate(queries):
            if i > 0 and nums[i] and nums[i - 1] == nums[i]:
                x -= 1
            if i < n - 1 and nums[i] and nums[i + 1] == nums[i]:
                x -= 1
            nums[i] = c
            if i > 0 and nums[i - 1] == nums[i]:
                x += 1
            if i < n - 1 and nums[i + 1] == nums[i]:
                x += 1
            ans[k] = x
        return ans
```

## 35. `3532_50` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/time-taken-to-mark-all-nodes/
- Precision: 0.750
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
          dp[u].top1.time if dp[u].top1.node != v else dp[u].top2.time
      )
      self._reroot(tree, v, u, newMaxTime, dp, ans)
```

## 36. `3240_9` — Qwen3-Coder-480B-A35B-Instruct-FP8

- LeetCode: https://leetcode.com/problems/maximum-number-that-sum-of-the-prices-is-less-than-or-equal-to-k/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def findMaximumNumber(self, k: int, x: int) -> int:
        @cache
        def dfs(pos, limit, cnt):
            if pos == 0:
                return cnt
            ans = 0
            up = (self.num >> (pos - 1) & 1) if limit else 1
            for i in range(up + 1):
                ans += dfs(pos - 1, limit and i == up, cnt + (i == 1 and (pos) % x == 0))
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

## 37. `3475_34` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-binary-array-elements-equal-to-one-i/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums: List[int]) -> int:
        ans = 0
        n = len(nums)
        nums = list(nums)
        for i in range(n - 2):
            if nums[i] == 0:
                nums[i] ^= 1
                nums[i + 1] ^= 1
                nums[i + 2] ^= 1
                ans += 1
        for x in nums:
            if x == 0:
                return -1
        return ans
```

## 38. `3605_3` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/construct-the-minimum-bitwise-array-i/
- Precision: 0.400
- Test pass: [Y ]

```python
class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        ans = []
        for x in nums:
            if x == 2:
                ans.append(-1)
            else:
                found = False
                for i in range(1, 32):
                    if x >> i & 1 ^ 1:
                        ans.append(x ^ (1 << (i - 1)))
                        found = True
                        break
                if not found:
                    ans.append(-1)
        return ans
```

## 39. `2831_11` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/number-of-beautiful-pairs/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def countBeautifulPairs(self, nums: List[int]) -> int:
        from math import gcd
        cnt = [0] * 10
        ans = 0
        for x in nums:
            for y in range(10):
                if cnt[y] and gcd(x % 10, y) == 1:
                    ans += cnt[y]
            cnt[int(str(x)[0])] += 1
        return ans
```

## 40. `3629_14` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/total-characters-in-string-after-transformations-i/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def lengthAfterTransformations(self, s: str, t: int) -> int:
        MOD = 1_000_000_007
        count = [0] * 26

        for c in s:
            count[ord(c) - ord('a')] += 1

        for _ in range(t):
            newCount = [0] * 26
            # 'a' -> 'b', 'b' -> 'c', ..., 'y' -> 'z'
            for i in range(25):
                newCount[i + 1] = count[i]
            # 'z' -> 'ab'
            newCount[0] = count[25]
            newCount[1] = (newCount[1] + count[25]) % MOD
            count = newCount

        return sum(count) % MOD
```

## 41. `3213_42` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/
- Precision: 0.200
- Test pass: [Y ]

```python
class Solution:
    def countSubarrays(self, nums: List[int], k: int) -> int:
        mx = max(nums)
        n = len(nums)
        ans = cnt = 0
        j = 0
        for i in range(n):
            while j < n and cnt < k:
                cnt += nums[j] == mx
                j += 1
            if cnt < k:
                break
            ans += n - j + 1
            cnt -= nums[i] == mx
        return ans
```

## 42. `3507_52` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/find-the-count-of-numbers-which-are-not-special/
- Precision: 0.667
- Test pass: [Y ]

```python
import math

m = 31623
primes = [True] * (m + 1)
primes[0] = primes[1] = False
for i in range(2, m + 1):
    if primes[i]:
        for j in range(i + i, m + 1, i):
            primes[j] = False


class Solution:
    def nonSpecialCount(self, l: int, r: int) -> int:
        lo = math.isqrt(l - 1) + 1
        hi = math.isqrt(r)
        cnt = sum(primes[i] for i in range(lo, hi + 1))
        return (r - l + 1) - cnt
```

## 43. `3559_48` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-i/
- Precision: 0.500
- Test pass: [Y ]

```python
from functools import lru_cache
from typing import List
from math import inf

def min(a: int, b: int) -> int:
    return a if a < b else b


class Trie:
    def __init__(self):
        self.children: List['Trie'] = [None] * 26

    def insert(self, w: str):
        node = self
        for i in map(lambda c: ord(c) - 97, w):
            if node.children[i] is None:
                node.children[i] = Trie()
            node = node.children[i]


class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
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
                ans = min(ans, 1 + dfs(j + 1))
            return ans

        trie = Trie()
        for w in words:
            trie.insert(w)
        n = len(target)
        ans = dfs(0)
        return ans if ans < inf else -1
```

## 44. `3659_30` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/count-paths-with-the-given-xor-value/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
  def countPathsWithXorValue(self, grid: list[list[int]], k: int) -> int:
    MOD = 1_000_000_007
    m = len(grid)
    n = len(grid[0])

    @functools.lru_cache(maxsize=None)
    def count(i: int, j: int, xors: int) -> int:
      """
      Return the number of paths from (i, j) to (m - 1, n - 1) with XOR value
      `xors`.
      """
      if i == m or j == n:
        return 0
      xors ^= grid[i][j]
      if i == m - 1 and j == n - 1:
        return int(xors == k)
      right = count(i, j + 1, xors)
      down = count(i + 1, j, xors)
      return (right + down) % MOD

    return count(0, 0, 0)

class Solution:
  def countPathsWithXorValue(self, grid: list[list[int]], k: int) -> int:
    MOD = 1_000_000_007
    m = len(grid)
    n = len(grid[0])

    @functools.lru_cache(None)
    def count(i: int, j: int, xors: int) -> int:
      """
      Return the number of paths from (i, j) to (m - 1, n - 1) with XOR value
      `xors`.
      """
      if i == m or j == n:
        return 0
      xors ^= grid[i][j]
      if i == m - 1 and j == n - 1:
        return int(xors == k)
      right = count(i, j + 1, xors)
      down = count(i + 1, j, xors)
      return (right + down) % MOD

    return count(0, 0, 0)
```

## 45. `2810_31` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/collecting-chocolates/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def minCost(self, nums: List[int], x: int) -> int:
        n = len(nums)
        f = [[0] * n for _ in range(n)]
        for i in range(n):
            f[i][0] = nums[i]
            for j in range(1, n):
                f[i][j] = min(f[i][j - 1], nums[(i - j) % n])
        return min(sum(f[i][j] for i in range(n)) + x * j for j in range(n))
```

## 46. `3381_38` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/shortest-subarray-with-or-at-least-k-i/
- Precision: 0.529
- Test pass: [Y ]

```python
class Solution:
    def minimumSubarrayLength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = n + 1
        for i in range(n):
            current_or = 0
            for j in range(i, n):
                current_or |= nums[j]
                if current_or >= k:
                    ans = min(ans, j - i + 1)
                    break
        return -1 if ans > n else ans
```

## 47. `3226_43` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/minimum-number-game/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def numberGame(self, nums: List[int]) -> List[int]:
        from heapq import heapify, heappop
        nums = nums.copy()
        heapify(nums)
        ans = []
        while nums:
            a = heappop(nums)
            b = heappop(nums)
            ans.append(b)
            ans.append(a)
        return ans
```

## 48. `3709_4` — Kimi-K2-Instruct

- LeetCode: https://leetcode.com/problems/find-special-substring-of-length-k/
- Precision: 0.200
- Test pass: [Y ]

```python
class Solution:
    def hasSpecialSubstring(self, s: str, k: int) -> bool:
        l, n = 0, len(s)
        while l < n:
            r = l
            while r < n and s[r] == s[l]:
                r += 1
            if r - l == k:
                left_ok  = (l == 0) or (s[l - 1] != s[l])
                right_ok = (r == n) or (s[r] != s[l])
                if left_ok and right_ok:
                    return True
            l = r
        return False
```

## 49. `3235_42` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-cost-to-convert-string-i/
- Precision: 0.667
- Test pass: [Y ]

```python
from typing import List
from math import inf

class Solution:
    def minimumCost(
        self,
        source: str,
        target: str,
        original: List[str],
        changed: List[str],
        cost: List[int],
    ) -> int:
        g = [[inf] * 26 for _ in range(26)]
        for i in range(26):
            g[i][i] = 0
        for x, y, z in zip(original, changed, cost):
            a = ord(x) - ord('a')
            b = ord(y) - ord('a')
            g[a][b] = min(g[a][b], z)
        for k in range(26):
            for i in range(26):
                for j in range(26):
                    if g[i][k] + g[k][j] < g[i][j]:
                        g[i][j] = g[i][k] + g[k][j]
        ans = 0
        for a, b in zip(source, target):
            if a != b:
                x, y = ord(a) - ord('a'), ord(b) - ord('a')
                if g[x][y] == inf:
                    return -1
                ans += g[x][y]
        return ans
```

## 50. `3559_12` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-number-of-valid-strings-to-form-target-i/
- Precision: 0.667
- Test pass: [Y ]

```python
def min(a: int, b: int) -> int:
    return a if a < b else b


class Trie:
    def __init__(self):
        self.children: List[Optional[Trie]] = [None] * 26

    def insert(self, w: str):
        node = self
        for i in map(lambda c: ord(c) - 97, w):
            if node.children[i] is None:
                node.children[i] = Trie()
            node = node.children[i]


class Solution:
    def minValidStrings(self, words: List[str], target: str) -> int:
        @cache
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
                ans = min(ans, 1 + dfs(j + 1))
            return ans

        trie = Trie()
        for w in words:
            trie.insert(w)
        n = len(target)
        inf = float('inf')
        ans = dfs(0)
        return ans if ans < inf else -1
```

## 51. `3360_26` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/minimum-deletions-to-make-string-k-special/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minimumDeletions(self, word: str, k: int) -> int:
        def f(v: int) -> int:
            ans = 0
            for x in nums:
                if x < v:
                    ans += x
                elif x > v + k:
                    ans += x - v - k
            return ans

        nums = Counter(word).values()
        nums = list(nums)
        return min(f(v) for v in range(len(word) + 1))
```

## 52. `2811_34` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/determine-the-minimum-sum-of-a-k-avoiding-array/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
    def minimumSum(self, n: int, k: int) -> int:
        s, i = 0, 1
        vis = []
        for _ in range(n):
            while k - i in vis:
                i += 1
            s += i
            vis.append(i)
            i += 1
        return s
```

## 53. `3535_43` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/find-the-count-of-monotonic-pairs-i/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def countOfPairs(self, nums: List[int]) -> int:
        mod = 10**9 + 7
        n = len(nums)
        m = max(nums) + 1
        dp = [[0] * m for _ in range(n)]
        for val in range(nums[0] + 1):
            dp[0][val] = 1
        for i in range(1, n):
            for prev in range(nums[i-1] + 1):
                if dp[i-1][prev] > 0:
                    lower = max(prev, max(0, prev + nums[i] - nums[i-1]))
                    for val in range(lower, nums[i] + 1):
                        dp[i][val] = (dp[i][val] + dp[i-1][prev]) % mod
        return sum(dp[-1][:nums[-1] + 1]) % mod
```

## 54. `3721_8` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/count-mentions-per-user/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def countMentions(self, numberOfUsers: int, events: List[List[str]]) -> List[int]:
        events.sort(key=lambda e: (int(e[1]), e[0][2]))
        online_t = [0] * numberOfUsers
        ans = [0] * numberOfUsers
        lazy = 0
        for etype, ts, s in events:
            cur = int(ts)
            if etype[0] == "O":
                online_t[int(s)] = cur + 60
            elif s[0] == "A":
                lazy += 1
            elif s[0] == "H":
                for i, t in enumerate(online_t):
                    if t <= cur:
                        ans[i] += 1
            else:
                for a in s.split():
                    ans[int(a[2:])] += 1
        if lazy:
            for i in range(numberOfUsers):
                ans[i] += lazy
        return ans
```

## 55. `3714_48` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
  def minMaxSums(self, nums: list[int], k: int) -> int:
    # In a sorted array, nums[i] will be
    #   1. The maximum for subsequences formed by nums[0..i].
    #   2. The minimum for subsequences formed by nums[i..n - 1].
    #
    # The number of times nums[i] is the maximum is the same as the number of
    # times nums[n - 1 - i] is the minimum, due to the symmetry in subsequences
    # derived from the sorted order.
    #
    # To calculate the contribution of nums[i], we need to find the number of
    # ways to select at most (k - 1) elements from the range of indices where
    # nums[i] is the smallest or nums[n - 1 - i] is the largest.
    MOD = 1_000_000_007

    def getComb(n: int, r: int) -> list[list[int]]:
      """C(n, k) = C(n - 1, k) + C(n - 1, k - 1)"""
      comb = [[0] * (r + 1) for _ in range(n + 1)]
      for i in range(n + 1):
        comb[i][0] = 1
      for i in range(1, n + 1):
        for j in range(1, r + 1):
          comb[i][j] = (comb[i - 1][j] + comb[i - 1][j - 1]) % MOD
      return comb

    n = len(nums)
    comb = getComb(n, k - 1)
    ans = 0

    nums.sort()

    for i in range(n):
      count = 0
      m = min(i, k - 1)
      for j in range(m + 1):
        count = (count + comb[i][j]) % MOD
      ans = (ans + nums[i] * count) % MOD
      ans = (ans + nums[-1 - i] * count) % MOD

    return ans
```

## 56. `2955_9` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/account-balance-after-rounded-purchase/
- Precision: 0.111
- Test pass: [Y ]

```python
class Solution:
    def accountBalanceAfterPurchase(self, purchaseAmount: int) -> int:
        floor = (purchaseAmount // 10) * 10
        ceil = floor + 10
        if purchaseAmount - floor < ceil - purchaseAmount:
            rounded = floor
        elif ceil - purchaseAmount < purchaseAmount - floor:
            rounded = ceil
        else:
            rounded = ceil
        return 100 - rounded
```

## 57. `3211_35` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/find-maximum-non-decreasing-array-length/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def findMaximumLength(self, nums: List[int]) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [0] * (n + 1)
        pre = [0] * (n + 2)
        for i in range(1, n + 1):
            pre[i] = max(pre[i], pre[i - 1])
            j = bisect_left(s, s[i] * 2 - s[pre[i]])
            f[i] = f[pre[i]] + 1
            pre[j] = i
        return f[n]
```

## 58. `3682_4` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/count-the-number-of-arrays-with-k-matching-adjacent-elements/
- Precision: 0.500
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
        
        max_needed = n - 1
        Solution.precompute(max_needed)
        
        a = n - 1
        b = n - k - 1
        # Compute combination C(a, b)
        comb = Solution._fact[a] * Solution._inv_fact[b] % self.MOD
        comb = comb * Solution._inv_fact[a - b] % self.MOD
        
        exponent = (n - k - 1)
        term = pow(m - 1, exponent, self.MOD)
        
        ans = comb * m % self.MOD
        ans = ans * term % self.MOD
        return ans
```

## 59. `3367_35` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/find-the-sum-of-encrypted-integers/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
    def sumOfEncryptedInt(self, nums: List[int]) -> int:
        def encrypt(x: int) -> int:
            mx = 0
            p = 0
            while x:
                x, v = divmod(x, 10)
                mx = max(mx, v)
                p = p * 10 + 1
            return mx * p

        return sum([encrypt(x) for x in nums])
```

## 60. `3034_7` — grok-code-fast-1

- LeetCode: https://leetcode.com/problems/points-that-intersect-with-cars/
- Precision: 0.111
- Test pass: [Y ]

```python
class Solution:
    def numberOfPoints(self, nums: List[List[int]]) -> int:
        m = 102
        d = [0] * m
        for start, end in nums:
            d[start] += 1
            if end + 1 < m:
                d[end + 1] -= 1
        count = 0
        current = 0
        for i in range(1, 101):
            current += d[i]
            if current > 0:
                count += 1
        return count
```

## 61. `3517_67` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/
- Precision: 0.500
- Test pass: [Y ]

```python
from collections import deque
from typing import List

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
        g = [[i + 1] for i in range(n - 1)] + [[]]
        ans = []
        for u, v in queries:
            g[u].append(v)
            ans.append(bfs(0))
        return ans
```

## 62. `3768_14` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/check-if-digits-are-equal-in-string-after-operations-i/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def hasSameDigits(self, s: str) -> bool:
        t = [int(c) for c in s]
        n = len(t)
        for k in range(n, 2, -1):
            for i in range(k - 1):
                t[i] = (t[i] + t[i + 1]) % 10
        return t[0] == t[1]
```

## 63. `3631_45` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/count-k-reducible-numbers-less-than-n/
- Precision: 0.000
- Test pass: [Y ]

```python
import functools

class Solution:
    MOD = 1_000_000_007
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        ops = self._getOps(s)
        @functools.lru_cache(None)
        def dp(i: int, setBits: int, tight: bool) -> int:
            """
            Returns the number of positive integers less than n that are k-reducible,
            considering the i-th digit, where `setBits` is the number of set bits in
            the current number, and `tight` indicates if the current digit is
            tightly bound.
            """
            if i == len(s):
                if setBits == 0:
                    return 0
                return int(not tight and ops[setBits] < k)
            res = 0
            maxDigit = int(s[i]) if tight else 1
            for d in range(maxDigit + 1):
                nextTight = tight and (d == maxDigit)
                nextSetBits = setBits + d
                res += dp(i + 1, nextSetBits, nextTight)
                res %= self.MOD
            return res
        return dp(0, 0, True) % self.MOD

    def _getOps(self, s: str) -> int:
        """Returns the number of operations to reduce a number to 0."""
        ops = [0] * (len(s) + 1)
        for num in range(2, len(s) + 1):
            ops[num] = 1 + ops[num.bit_count()]
        return ops
```

## 64. `3781_51` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/maximize-the-distance-between-points-on-a-square/
- Precision: 0.600
- Test pass: [Y ]

```python
from dataclasses import dataclass
import collections


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
    r = 2 * side

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

## 65. `3245_7` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/find-beautiful-indices-in-the-given-array-i/
- Precision: 0.200
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
                    occurrences.append(i - j + 1)
                    j = prefix_function[j - 1]
            return occurrences

        prefix_a = build_prefix_function(a)
        prefix_b = build_prefix_function(b)

        resa = kmp_search(a, s, prefix_a)
        resb = kmp_search(b, s, prefix_b)

        res = []
        i = 0
        j = 0
        while i < len(resa):
            while j < len(resb):
                if abs(resb[j] - resa[i]) <= k:
                    res.append(resa[i])
                    break
                elif j + 1 < len(resb) and abs(resb[j + 1] - resa[i]) < abs(resb[j] - resa[i]):
                    j += 1
                else:
                    break
            i += 1
        return res
```

## 66. `3460_58` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/count-the-number-of-inversions/
- Precision: 0.429
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def numberOfPermutations(self, n: int, requirements: List[List[int]]) -> int:
        req = [-1] * n
        for end, cnt in requirements:
            req[end] = cnt
        # prefix of length 1 must have 0 inversions
        if req[0] > 0:
            return 0
        req[0] = 0

        mod = 10**9 + 7
        m = max(req)                     # largest inversion count that we need to keep
        f = [[0] * (m + 1) for _ in range(n)]
        f[0][0] = 1

        for i in range(1, n):
            # if there is a requirement for this prefix we only keep that exact count
            if req[i] >= 0:
                l = r = req[i]
            else:
                l, r = 0, m

            for j in range(l, r + 1):
                max_k = min(i, j)
                total = 0
                for k in range(max_k + 1):
                    total += f[i - 1][j - k]
                f[i][j] = total % mod

        return f[n - 1][req[n - 1]]
```

## 67. `3436_0` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/find-subarray-with-bitwise-or-closest-to-k/
- Precision: 0.250
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        m = max(nums).bit_length()
        cnt = [0] * m
        s = i = 0
        ans = float('inf')
        for j, x in enumerate(nums):
            s |= x
            ans = min(ans, abs(s - k))
            for h in range(m):
                if x >> h & 1:
                    cnt[h] += 1
            while i < j and s > k:
                y = nums[i]
                for h in range(m):
                    if y >> h & 1:
                        cnt[h] -= 1
                        if cnt[h] == 0:
                            s ^= 1 << h
                i += 1
                ans = min(ans, abs(s - k))
            ans = min(ans, abs(s - k))
        return ans
```

## 68. `3764_31` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/maximum-sum-with-at-most-k-elements/
- Precision: 0.600
- Test pass: [Y ]

```python
from typing import List
from heapq import heappush, heappop

class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        pq = []
        for nums, limit in zip(grid, limits):
            nums.sort()
            for _ in range(min(limit, len(nums))):
                heappush(pq, nums.pop())
                if len(pq) > k:
                    heappop(pq)
        return sum(pq)
```

## 69. `3778_7` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/transform-array-by-parity/
- Precision: 0.500
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def transformArray(self, nums: List[int]) -> List[int]:
        even = sum(x % 2 == 0 for x in nums)
        for i in range(even):
            nums[i] = 0
        for i in range(even, len(nums)):
            nums[i] = 1
        return nums
```

## 70. `3583_9` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/sorted-gcd-pair-queries/
- Precision: 0.167
- Test pass: [Y ]

```python
from typing import List
from collections import Counter
from itertools import accumulate
from bisect import bisect_right

class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        mx = max(nums)
        cnt = Counter(nums)
        cnt_g = [0] * (mx + 1)          # allocate index up to mx
        for i in range(mx, 0, -1):
            v = 0
            for j in range(i, mx + 1, i):
                v += cnt[j]
                cnt_g[i] -= cnt_g[j]
            cnt_g[i] += v * (v - 1) // 2   # fix syntax
        s = list(accumulate(cnt_g))
        return [bisect_right(s, q) for q in queries]
```

## 71. `2854_40` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/decremental-string-concatenation/
- Precision: 0.375
- Test pass: [Y ]

```python
from functools import cache
from typing import List

class Solution:
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        @cache
        def dfs(i: int, a: str, b: str) -> int:
            if i >= len(words):
                return 0
            s = words[i]
            # Option 1: attach current string first
            x = dfs(i + 1, a, s[-1]) - (s[0] == b)
            # Option 2: attach word first
            y = dfs(i + 1, s[0], b) - (s[-1] == a)
            return len(s) + min(x, y)

        return len(words[0]) + dfs(1, words[0][0], words[0][-1])
```

## 72. `3744_8` — Kimi-K2-Thinking

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-array-elements-zero/
- Precision: 0.333
- Test pass: [Y ]

```python
from typing import List

class Solution:
  def minOperations(self, queries: List[List[int]]) -> int:
    return sum((self._getOperations(r) - self._getOperations(l - 1) + 1) // 2
               for l, r in queries)

  def _getOperations(self, n: int) -> int:
    """Returns the number of operations required for [1, n]."""
    res = 0
    ops = 0
    powerOfFour = 1
    while powerOfFour <= n:
      r = min(n, powerOfFour * 4 - 1)
      ops += 1
      res += (r - powerOfFour + 1) * ops
      powerOfFour *= 4
    return res
```

## 73. `3383_14` — deepseek-chat

- LeetCode: https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/
- Precision: 0.667
- Test pass: [Y ]

```python
class Solution:
    def maximumEnergy(self, energy: List[int], k: int) -> int:
        ans = -inf
        n = len(energy)
        for i in range(n - 1, n - k - 1, -1):
            j, s = i, 0
            while j >= 0:
                s += energy[j]
                ans = max(ans, s)
                j -= k
        return ans
```

## 74. `3704_15` — deepseek-chat

- LeetCode: https://leetcode.com/problems/count-partitions-with-even-sum-difference/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def countPartitions(self, nums: List[int]) -> int:
        l, r = 0, sum(nums)
        ans = 0
        for x in nums[:-1]:
            l += x
            r -= x
            if (l - r) % 2 == 0:
                ans += 1
        return ans
```

## 75. `3733_7` — deepseek-chat

- LeetCode: https://leetcode.com/problems/length-of-longest-v-shaped-diagonal-segment/
- Precision: 0.167
- Test pass: [Y ]

```python
class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        next_digit = {1: 2, 2: 0, 0: 2}

        def within_bounds(i, j):
            return 0 <= i < m and 0 <= j < n

        from functools import lru_cache
        
        @lru_cache(None)
        def f(i, j, di, dj, turned):
            result = 1
            successor = next_digit[grid[i][j]]

            if within_bounds(i + di, j + dj) and grid[i + di][j + dj] == successor:
                result = 1 + f(i + di, j + dj, di, dj, turned)

            if not turned:
                ndi, ndj = dj, -di
                if within_bounds(i + ndi, j + ndj) and grid[i + ndi][j + ndj] == successor:
                    result = max(result, 1 + f(i + ndi, j + ndj, ndi, ndj, True))

            return result

        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        result = 0

        for i in range(m):
            for j in range(n):
                if grid[i][j] != 1:
                    continue
                for di, dj in directions:
                    result = max(result, f(i, j, di, dj, False))

        return result
```

## 76. `3231_43` — deepseek-chat

- LeetCode: https://leetcode.com/problems/minimum-number-of-coins-to-be-added/
- Precision: 0.750
- Test pass: [Y ]

```python
class Solution:
    def minimumAddedCoins(self, coins: List[int], target: int) -> int:
        coins.sort()
        s = 1
        ans = i = 0
        while s <= target:
            if i < len(coins) and coins[i] <= s:
                s += coins[i]
                i += 1
            else:
                s += s
                ans += 1
        return ans
```

## 77. `3621_2` — deepseek-chat

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-array-values-equal-to-k/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        if any(x < k for x in nums):
            return -1
        s = set()
        for x in nums:
            if x > k:
                s.add(x)
        return len(s)
```

## 78. `3638_5` — deepseek-chat

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-character-frequencies-equal/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def makeStringGood(self, s: str) -> int:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        max_count = max(count)
        if max_count == 0:
            return 0
        return min(self._getMinOperations(count, target)
                   for target in range(1, max_count + 1))

    def _getMinOperations(self, count: list[int], target: int) -> int:
        dp = [0] * 27

        for i in range(25, -1, -1):
            deleteAllToZero = count[i]
            deleteOrInsertToTarget = abs(target - count[i])
            dp[i] = min(deleteAllToZero, deleteOrInsertToTarget) + dp[i + 1]
            if i + 1 < 26 and count[i + 1] < target:
                nextDeficit = target - count[i + 1]
                needToChange = count[i] if count[i] <= target else count[i] - target
                if nextDeficit > needToChange:
                    changeToTarget = needToChange + (nextDeficit - needToChange)
                else:
                    changeToTarget = nextDeficit + (needToChange - nextDeficit)
                dp[i] = min(dp[i], changeToTarget + dp[i + 2])

        return dp[0]
```

## 79. `2954_46` — deepseek-chat

- LeetCode: https://leetcode.com/problems/maximum-sum-of-almost-unique-subarray/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def maxSum(self, nums: List[int], m: int, k: int) -> int:
        from collections import Counter
        cnt = Counter(nums[:k])
        s = sum(nums[:k])
        ans = s if len(cnt) >= m else 0
        for i in range(k, len(nums)):
            cnt[nums[i]] = cnt.get(nums[i], 0) + 1
            cnt[nums[i - k]] -= 1
            s += nums[i] - nums[i - k]
            if cnt[nums[i - k]] == 0:
                cnt.pop(nums[i - k])
            if len(cnt) >= m:
                ans = max(ans, s)
        return ans
```

## 80. `3762_18` — deepseek-chat

- LeetCode: https://leetcode.com/problems/maximize-the-minimum-game-score/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def maxScore(self, points: list[int], m: int) -> int:
        def isPossible(minVal: int, m: int) -> bool:
            moves = 0
            prevMoves = 0
            for i, point in enumerate(points):
                required = (minVal + point - 1) // point
                required = max(0, required - prevMoves)
                if required > 0:
                    moves += 2 * required - 1
                    prevMoves = required - 1
                elif i + 1 < len(points):
                    moves += 1
                    prevMoves = 0
                if moves > m:
                    return False
            return True

        l = 0
        r = (m + 1) // 2 * max(points) + 1

        while l < r:
            mid = (l + r + 1) // 2
            if isPossible(mid, m):
                l = mid
            else:
                r = mid - 1

        return l
```

## 81. `3605_4` — deepseek-chat

- LeetCode: https://leetcode.com/problems/construct-the-minimum-bitwise-array-i/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        ans = []
        for x in nums:
            found = False
            for i in range(1, 32):
                if (x >> i) & 1 == 0:
                    candidate = x ^ (1 << (i - 1))
                    if candidate | (candidate + 1) == x:
                        ans.append(candidate)
                        found = True
                        break
            if not found:
                ans.append(-1)
        return ans
```

## 82. `3045_17` — deepseek-chat

- LeetCode: https://leetcode.com/problems/minimum-right-shifts-to-sort-the-array/
- Precision: 0.143
- Test pass: [N ]

```python
class Solution:
    def minimumRightShifts(self, nums: List[int]) -> int:
        n = len(nums)
        i = 1
        while i < n and nums[i - 1] < nums[i]:
            i += 1
        if i == n:
            return 0
        k = i + 1
        while k < n and nums[k - 1] < nums[k] and nums[k] < nums[0]:
            k += 1
        if k != n:
            return -1
        return n - i
```

## 83. `3046_16` — deepseek-chat

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-a-special-number/
- Precision: 0.200
- Test pass: [Y ]

```python
class Solution:
    def minimumOperations(self, num: str) -> int:
        from functools import lru_cache
        
        n = len(num)
        
        @lru_cache(None)
        def dfs(i: int, k: int) -> int:
            if i == n:
                return 0 if k == 0 else n
            ans = dfs(i + 1, k) + 1
            ans = min(ans, dfs(i + 1, (k * 10 + int(num[i])) % 25))
            return ans

        return dfs(0, 0)
```

## 84. `3677_7` — deepseek-chat

- LeetCode: https://leetcode.com/problems/maximum-amount-of-money-robot-can-earn/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
    def maximumAmount(self, coins: List[List[int]]) -> int:
        from functools import lru_cache
        
        m, n = len(coins), len(coins[0])
        
        @lru_cache(None)
        def dfs(i: int, j: int, k: int) -> int:
            if i >= m or j >= n:
                return -float('inf')
            if i == m - 1 and j == n - 1:
                return max(coins[i][j], 0) if k else coins[i][j]
            ans = coins[i][j] + max(dfs(i + 1, j, k), dfs(i, j + 1, k))
            if coins[i][j] < 0 and k:
                ans = max(ans, dfs(i + 1, j, k - 1), dfs(i, j + 1, k - 1))
            return ans
        
        return dfs(0, 0, 2)
```

## 85. `3517_20` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/shortest-distance-after-road-addition-queries-i/
- Precision: 0.500
- Test pass: [Y ]

```python
from collections import deque
from typing import List

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

## 86. `3659_3` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/count-paths-with-the-given-xor-value/
- Precision: 0.000
- Test pass: [Y ]

```python
import functools

class Solution:
    def countPathsWithXorValue(self, grid: list[list[int]], k: int) -> int:
        MOD = 1_000_000_007
        m = len(grid)
        n = len(grid[0])

        @functools.lru_cache(None)
        def count(i: int, j: int, xors: int) -> int:
            if i == m or j == n:
                return 0
            xors ^= grid[i][j]
            if i == m - 1 and j == n - 1:
                return int(xors == k)
            right = count(i, j + 1, xors)
            down = count(i + 1, j, xors)
            return (right + down) % MOD

        return count(0, 0, 0)
```

## 87. `2833_22` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/count-zero-request-servers/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def countServers(
        self, n: int, logs: List[List[int]], x: int, queries: List[int]
    ) -> List[int]:
        from collections import Counter
        from itertools import count
        cnt = Counter()
        logs.sort(key=lambda x: x[1])
        ans = [0] * len(queries)
        j = k = 0
        for r, i in sorted(zip(queries, count())):
            l = r - x
            while k < len(logs) and logs[k][1] <= r:
                cnt[logs[k][0]] += 1
                k += 1
            while j < len(logs) and logs[j][1] < l:
                cnt[logs[j][0]] -= 1
                if cnt[logs[j][0]] == 0:
                    cnt.pop(logs[j][0])
                j += 1
            ans[i] = n - len(cnt)
        return ans
```

## 88. `3631_32` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/count-k-reducible-numbers-less-than-n/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        import functools
        MOD = 1_000_000_007
        ops = self._getOps(s)

        @functools.lru_cache(None)
        def dp(i: int, setBits: int, tight: bool) -> int:
            if i == len(s):
                return 1 if (ops[setBits] < k and not tight) else 0
            res = 0
            maxDigit = int(s[i]) if tight else 1
            for d in range(maxDigit + 1):
                nextTight = tight and (d == maxDigit)
                res = (res + dp(i + 1, setBits + d, nextTight)) % MOD
            return res

        ans = dp(0, 0, True)
        ans = (ans - 1) % MOD
        return ans

    def _getOps(self, s: str):
        n = len(s)
        ops = [0] * (n + 1)
        for num in range(2, n + 1):
            ops[num] = 1 + ops[num.bit_count()]
        return ops
```

## 89. `2854_38` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/decremental-string-concatenation/
- Precision: 1.000
- Test pass: [Y ]

```python
class Solution:
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        @cache
        def dfs(i: int, a: str, b: str) -> int:
            if i == len(words):
                return 0
            s = words[i]
            x = dfs(i + 1, a, s[-1]) - int(s[0] == b)
            y = dfs(i + 1, s[0], b) - int(s[-1] == a)
            return len(s) + min(x, y)

        return len(words[0]) + dfs(1, words[0][0], words[0][-1])
```

## 90. `3403_70` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/
- Precision: 0.158
- Test pass: [Y ]

```python
class Solution:
    def minimumSubstringsInPartition(self, s: str) -> int:
        from collections import defaultdict
        n = len(s)
        memo = {}
        def dfs(i: int) -> int:
            if i >= n:
                return 0
            if i in memo:
                return memo[i]
            cnt = defaultdict(int)
            freq = defaultdict(int)
            ans = n - i
            for j in range(i, n):
                old = cnt[s[j]]
                if old > 0:
                    freq[old] -= 1
                    if freq[old] == 0:
                        del freq[old]
                cnt[s[j]] += 1
                new = cnt[s[j]]
                freq[new] += 1
                if len(freq) == 1:
                    t = 1 + dfs(j + 1)
                    if t < ans:
                        ans = t
            memo[i] = ans
            return ans
        return dfs(0)
```

## 91. `3765_7` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/minimum-cost-to-divide-array-into-subarrays/
- Precision: 0.500
- Test pass: [Y ]

```python
from typing import List
from itertools import accumulate

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        s = list(accumulate(cost, initial=0))  # cost 的前缀和
        f = [0] * (n + 1)
        for i, sum_num in enumerate(accumulate(nums), 1):
            f[i] = min(f[j] + sum_num * (s[i] - s[j]) + k * (s[n] - s[j])
                       for j in range(i))
        return f[n]
```

## 92. `3648_9` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/find-the-maximum-number-of-fruits-collected/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
  def maxCollectedFruits(self, fruits: list[list[int]]) -> int:
    n = len(fruits)

    def getTopLeft() -> int:
      return sum(fruits[i][i] for i in range(n))

    def getTopRight() -> int:
      dp = [[-10**9] * n for _ in range(n)]
      dp[0][n - 1] = fruits[0][n - 1]
      for i in range(n - 1):
        for j in range(n):
          if dp[i][j] < 0:
            continue
          for dj in (-1, 0, 1):
            j2 = j + dj
            if 0 <= j2 < n:
              add = fruits[i + 1][j2] if j2 != i + 1 else 0
              new_val = dp[i][j] + add
              if new_val > dp[i + 1][j2]:
                dp[i + 1][j2] = new_val
      return dp[n - 1][n - 1]

    def getBottomLeft() -> int:
      dp = [[-10**9] * n for _ in range(n)]
      dp[n - 1][0] = fruits[n - 1][0]
      for j in range(n - 1):
        for i in range(n):
          if dp[i][j] < 0:
            continue
          for di in (-1, 0, 1):
            i2 = i + di
            if 0 <= i2 < n:
              add = fruits[i2][j + 1] if i2 != j + 1 else 0
              new_val = dp[i][j] + add
              if new_val > dp[i2][j + 1]:
                dp[i2][j + 1] = new_val
      return dp[n - 1][n - 1]

    return getTopLeft() + getTopRight() + getBottomLeft()
```

## 93. `3593_4` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/find-the-maximum-factor-score-of-array/
- Precision: 0.333
- Test pass: [Y ]

```python
from typing import List
from math import gcd, lcm

class Solution:
    def maxScore(self, nums: List[int]) -> int:
        n = len(nums)
        suf_gcd = [0] * (n + 1)
        suf_lcm = [0] * n + [1]
        for i in range(n - 1, -1, -1):
            suf_gcd[i] = gcd(suf_gcd[i + 1], nums[i])
            suf_lcm[i] = lcm(suf_lcm[i + 1], nums[i])
        ans = suf_gcd[0] * suf_lcm[0]
        pre_gcd, pre_lcm = 0, 1
        for i, x in enumerate(nums):
            ans = max(ans, gcd(pre_gcd, suf_gcd[i + 1]) * lcm(pre_lcm, suf_lcm[i + 1]))
            pre_gcd = gcd(pre_gcd, x)
            pre_lcm = lcm(pre_lcm, x)
        return ans
```

## 94. `3510_18` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/maximize-the-total-height-of-unique-towers/
- Precision: 0.000
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def maximumTotalSum(self, maximumHeight: List[int]) -> int:
        maximumHeight.sort()
        ans, mx = 0, float('inf')
        for x in maximumHeight[::-1]:
            x = min(x, mx)
            if x <= 0:
                return -1
            ans += x
            mx = x - 1
        return ans
```

## 95. `3700_10` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/subsequences-with-a-unique-middle-mode-i/
- Precision: 0.000
- Test pass: [Y ]

```python
import math
import collections
from typing import List

class Solution:
    def __init__(self):
        self.MOD = 1_000_000_007

    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
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
            rightOther = n - 1 - i - rightCount

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
            b2 = count2.get(b, 0)
            # Exclude triples -- [a b] a [b b].
            res = (res - b1 * math.comb(b2, 2)) % self.MOD
            # Exclude doubles -- [a b] a [b ?].
            res = (res - b1 * b2 * (other2 - b2)) % self.MOD

        for b, b2 in count2.items():
            if b == a:
                continue
            b1 = count1.get(b, 0)
            # Exclude doubles -- [a ?] a [b b].
            res = (res - (other1 - b1) * math.comb(b2, 2)) % self.MOD

        return (res + self.MOD) % self.MOD
```

## 96. `3195_27` — deepseek-reasoner

- LeetCode: https://leetcode.com/problems/separate-black-and-white-balls/
- Precision: 0.000
- Test pass: [Y ]

```python
class Solution:
    def minimumSteps(self, s: str) -> int:
        n = len(s) - 1
        ans = cnt = 0
        for i in range(n, -1, -1):
            cnt += s[i] == '0'
            if s[i] == '1':
                ans += cnt
        return ans
```

## 97. `3192_59` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-xor-product/
- Precision: 0.333
- Test pass: [Y ]

```python
class Solution:
    def maximumXorProduct(self, a: int, b: int, n: int) -> int:
        mod = 10**9 + 7
        ax, bx = (a >> n) << n, (b >> n) << n
        for i in range(n - 1, -1, -1):
            x = a >> i & 1
            y = b >> i & 1
            if x == y:
                ax |= 1 << i
                bx |= 1 << i
            else:
                if ax > bx:
                    bx |= 1 << i
                else:
                    ax |= 1 << i
        return (ax % mod) * (bx % mod) % mod
```

## 98. `3702_28` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-subarray-with-equal-products/
- Precision: 0.364
- Test pass: [Y ]

```python
from typing import List
from math import gcd

def lcm(*args):
    res = 1
    for num in args:
        res = res * num // gcd(res, num)
    return res

class Solution:
    def maxLength(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        max_p = lcm(*nums) * max(nums)
        for i in range(n):
            p, g, l = 1, 0, 1
            for j in range(i, n):
                p *= nums[j]
                g = gcd(g, nums[j])
                l = lcm(l, nums[j])
                if p == g * l:
                    ans = max(ans, j - i + 1)
                if p > max_p:
                    break
        return ans
```

## 99. `3263_11` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-i/
- Precision: 0.333
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        inf = float('inf')
        a, b, c = nums[0], inf, inf
        for x in nums[1:]:
            if x < b:
                c, b = b, x
            elif x < c:
                c = x
        return a + b + c
```

## 100. `2779_55` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/number-of-adjacent-elements-with-the-same-color/
- Precision: 0.176
- Test pass: [Y ]

```python
class Solution:
    def colorTheArray(self, n: int, queries: List[List[int]]) -> List[int]:
        nums = [0] * n
        ans = [0] * len(queries)
        x = 0
        for k, (i, c) in enumerate(queries):
            if nums[i] == c:
                ans[k] = x
                continue
            prev = nums[i]
            if prev:
                if i > 0 and nums[i - 1] == prev:
                    x -= 1
                if i < n - 1 and nums[i + 1] == prev:
                    x -= 1
            nums[i] = c
            if c:
                if i > 0 and nums[i - 1] == c:
                    x += 1
                if i < n - 1 and nums[i + 1] == c:
                    x += 1
            ans[k] = x
        return ans
```

## 101. `3229_6` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/minimum-cost-to-make-array-equalindromic/
- Precision: 0.182
- Test pass: [Y ]

```python
from bisect import bisect_left
from typing import List

ps = []
limit = 10**9
for i in range(1, 10**5 + 1):
    s = str(i)
    t1 = s[::-1]
    t2 = s[:-1][::-1]
    val = int(s + t1)
    if val < limit:
        ps.append(val)
    val = int(s + t2)
    if val < limit:
        ps.append(val)
ps.sort()


class Solution:
    def minimumCost(self, nums: List[int]) -> int:
        def f(x: int) -> int:
            return sum(abs(v - x) for v in nums)

        arr = sorted(nums)
        i = bisect_left(ps, arr[len(arr) // 2])
        return min(f(ps[j]) for j in range(i - 1, i + 2) if 0 <= j < len(ps))
```

## 102. `3759_14` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/choose-k-elements-with-maximum-sum/
- Precision: 0.500
- Test pass: [Y ]

```python
from heapq import heappush, heappop

class Solution:
    def findMaxSum(self, nums1: List[int], nums2: List[int], k: int) -> List[int]:
        arr = [(x, i) for i, x in enumerate(nums1)]
        arr.sort()
        pq = []
        s = j = 0
        n = len(arr)
        ans = [0] * n
        for h, (x, i) in enumerate(arr):
            while j < h and arr[j][0] < x:
                y = nums2[arr[j][1]]
                heappush(pq, y)
                s += y
                if len(pq) > k:
                    s -= heappop(pq)
                j += 1
            ans[i] = s
        return ans
```

## 103. `3764_35` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-sum-with-at-most-k-elements/
- Precision: 0.750
- Test pass: [Y ]

```python
from heapq import heappush, heappop

class Solution:
    def maxSum(self, grid: List[List[int]], limits: List[int], k: int) -> int:
        pq = []
        for nums, limit in zip(grid, limits):
            nums.sort()
            for _ in range(min(limit, len(nums))):
                heappush(pq, nums.pop())
                if len(pq) > k:
                    heappop(pq)
        return sum(pq)
```

## 104. `3265_33` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/maximum-good-subarray-sum/
- Precision: 0.500
- Test pass: [Y ]

```python
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        p = {nums[0]: 0}
        s, n = 0, len(nums)
        ans = float('-inf')
        for i, x in enumerate(nums):
            s += x
            if x - k in p:
                ans = max(ans, s - p[x - k])
            if x + k in p:
                ans = max(ans, s - p[x + k])
            if i + 1 < n and (nums[i + 1] not in p or p[nums[i + 1]] > s):
                p[nums[i + 1]] = s
        return 0 if ans == float('-inf') else ans
```

## 105. `3456_57` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/find-the-maximum-length-of-a-good-subsequence-i/
- Precision: 0.182
- Test pass: [Y ]

```python
from typing import List

class Solution:
    def maximumLength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        f = [[1] * (k + 1) for _ in range(n)]
        ans = 1
        for i in range(n):
            for j in range(i):
                if nums[i] == nums[j]:
                    for h in range(k + 1):
                        f[i][h] = max(f[i][h], f[j][h] + 1)
                else:
                    for h in range(1, k + 1):
                        f[i][h] = max(f[i][h], f[j][h - 1] + 1)
            ans = max(ans, max(f[i]))
        return ans
```

## 106. `3717_54` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/
- Precision: 0.114
- Test pass: [Y ]

```python
from typing import List
from collections import defaultdict
from heapq import heappush, heappop, heappushpop


class LazyHeap:
    def __init__(self):
        self.heap = []
        self.remove_cnt = defaultdict(int)
        self.size = 0
        self.sum = 0

    def remove(self, x: int) -> None:
        self.remove_cnt[x] += 1
        self.size -= 1
        self.sum -= x

    def apply_remove(self) -> None:
        while self.heap and self.remove_cnt[self.heap[0]] > 0:
            self.remove_cnt[self.heap[0]] -= 1
            heappop(self.heap)

    def top(self) -> int:
        self.apply_remove()
        return self.heap[0]

    def pop(self) -> int:
        self.apply_remove()
        val = heappop(self.heap)
        self.size -= 1
        self.sum -= val
        return val

    def push(self, x: int) -> None:
        if self.remove_cnt[x] > 0:
            self.remove_cnt[x] -= 1
        else:
            heappush(self.heap, x)
        self.size += 1
        self.sum += x

    def pushpop(self, x: int) -> int:
        self.apply_remove()
        if not self.heap or x <= self.heap[0]:
            return x
        self.sum += x - self.heap[0]
        return heappushpop(self.heap, x)


class Solution:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[int]:
        ans = [0] * (len(nums) - k + 1)
        left = LazyHeap()
        right = LazyHeap()

        for i, x in enumerate(nums):
            if left.size == right.size:
                left.push(-right.pushpop(x))
            else:
                right.push(-left.pushpop(-x))

            l = i + 1 - k
            if l < 0:
                continue

            v = -left.top()
            s1 = v * left.size + left.sum
            s2 = right.sum - v * right.size
            ans[l] = s1 + s2

            x = nums[l]
            if x <= -left.top():
                left.remove(-x)
                if left.size < right.size:
                    left.push(-right.pop())
            else:
                right.remove(x)
                if left.size > right.size + 1:
                    right.push(-left.pop())

        return ans

    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        dis = self.medianSlidingWindow(nums, x)
        f = [[0] * (n + 1) for _ in range(k + 1)]
        inf = float('inf')
        for i in range(1, k + 1):
            f[i][i * x - 1] = inf
            for j in range(i * x, n - (k - i) * x + 1):
                f[i][j] = min(f[i][j - 1], f[i - 1][j - x] + dis[j - x])
        return f[k][n]
```

## 107. `3463_23` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/alternating-groups-i/
- Precision: 0.375
- Test pass: [Y ]

```python
class Solution:
    def numberOfAlternatingGroups(self, colors: List[int]) -> int:
        n = len(colors)
        ans = 0
        for i in range(n):
            if colors[i] != colors[(i + 1) % n] and colors[i] == colors[(i + 2) % n]:
                ans += 1
        return ans
```

## 108. `3612_15` — gpt-5.1-codex

- LeetCode: https://leetcode.com/problems/adjacent-increasing-subarrays-detection-i/
- Precision: 0.118
- Test pass: [Y ]

```python
class Solution:
    def hasIncreasingSubarrays(self, nums: List[int], k: int) -> bool:
        n = len(nums)
        for start in range(n - 2 * k + 1):
            first = True
            for i in range(start + 1, start + k):
                if nums[i] <= nums[i - 1]:
                    first = False
                    break
            if not first:
                continue
            second = True
            for i in range(start + k + 1, start + 2 * k):
                if nums[i] <= nums[i - 1]:
                    second = False
                    break
            if first and second:
                return True
        return False
```

import timeit
from typing import List, Callable, Tuple


# -------------------------
# KMP (Knuth–Morris–Pratt)
# -------------------------
def kmp_prefix(pattern: str) -> List[int]:
    pi = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j
    return pi


def kmp_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    pi = kmp_prefix(pattern)
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
            if j == len(pattern):
                return i - j + 1
    return -1


# -------------------------
# Rabin–Karp
# -------------------------
def rabin_karp_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    base = 256
    mod = 1_000_000_007

    pat_hash = 0
    win_hash = 0
    h = 1

    for _ in range(m - 1):
        h = (h * base) % mod

    for i in range(m):
        pat_hash = (pat_hash * base + ord(pattern[i])) % mod
        win_hash = (win_hash * base + ord(text[i])) % mod

    for i in range(n - m + 1):
        if pat_hash == win_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            win_hash = (win_hash - ord(text[i]) * h) % mod
            win_hash = (win_hash * base + ord(text[i + m])) % mod
            win_hash = (win_hash + mod) % mod

    return -1


# -------------------------
# Boyer–Moore (bad character rule)
# -------------------------
def bm_bad_char_table(pattern: str) -> dict:
    table = {}
    for i, ch in enumerate(pattern):
        table[ch] = i
    return table


def boyer_moore_search(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    n, m = len(text), len(pattern)
    if m > n:
        return -1

    bad = bm_bad_char_table(pattern)
    shift = 0

    while shift <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        if j < 0:
            return shift
        else:
            last = bad.get(text[shift + j], -1)
            shift += max(1, j - last)

    return -1


# -------------------------
# Benchmark
# -------------------------
def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()



def bench(fn: Callable[[str, str], int], text: str, pattern: str, number: int) -> float:
    t = timeit.Timer(lambda: fn(text, pattern))
    return t.timeit(number=number)


def pick_existing_substring(text: str, length: int = 30) -> str:
    if len(text) < length + 1:
        return text
    start = len(text) // 2
    return text[start:start + length]


def run_for_text(label: str, text: str) -> None:
    algorithms: List[Tuple[str, Callable[[str, str], int]]] = [
        ("Boyer–Moore", boyer_moore_search),
        ("KMP", kmp_search),
        ("Rabin–Karp", rabin_karp_search),
    ]

    existing = pick_existing_substring(text, 30)
    fake = "THIS_SUBSTRING_SHOULD_NOT_EXIST_123456789"

    number = 30

    print(f"\n=== {label} ===")
    print(f"Text length: {len(text)}")
    print(f"Existing pattern: {repr(existing[:30])}...")
    print(f"Fake pattern: {repr(fake)}")

    results = {}

    for alg_name, fn in algorithms:
        t_exist = bench(fn, text, existing, number)
        t_fake = bench(fn, text, fake, number)
        results[alg_name] = (t_exist, t_fake)
        print(f"{alg_name:12} | exist: {t_exist:.6f}s | fake: {t_fake:.6f}s (number={number})")

    best_exist = min(results.items(), key=lambda x: x[1][0])[0]
    best_fake = min(results.items(), key=lambda x: x[1][1])[0]
    print(f"→ Fastest for existing: {best_exist}")
    print(f"→ Fastest for fake:     {best_fake}")

    return results


def main():
    text1_path = "text1.txt"
    text2_path = "text2.txt"

    text1 = load_text(text1_path)
    text2 = load_text(text2_path)

    run_for_text("TEXT 1", text1)
    run_for_text("TEXT 2", text2)


if __name__ == "__main__":
    main()

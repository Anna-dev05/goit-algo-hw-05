from typing import List, Tuple, Optional


def binary_search_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    """
    arr — відсортований список float (за зростанням).
    Повертає (кількість ітерацій, upper_bound).
    upper_bound = найменший елемент >= target, або None якщо не існує.
    """
    left, right = 0, len(arr) - 1
    iterations = 0
    answer_index = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2

        if arr[mid] >= target:
            answer_index = mid
            right = mid - 1  # шукаємо ще менший, але все ще >= target
        else:
            left = mid + 1

    return iterations, (arr[answer_index] if answer_index is not None else None)


if __name__ == "__main__":
    data = [0.5, 1.1, 1.1, 2.3, 3.14, 4.0, 4.01]
    for x in [1.1, 1.12, 0.1, 4.01, 10.0]:
        iters, ub = binary_search_upper_bound(data, x)
        print(f"target={x} -> iterations={iters}, upper_bound={ub}")

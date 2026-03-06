from pl_tiny_clients.constants import PYTEST_NONDETERMINISTIC_MARKER
from pl_tiny_clients.random_int import random_int

pytestmark = [
    PYTEST_NONDETERMINISTIC_MARKER,
]


def test_returns_correct_distribution() -> None:
    # Note: This test is non-deterministic

    results: list[float] = []
    sample_count = 100000

    results = [random_int(1, 10) for _ in range(sample_count)]

    actual_count_of_threes = len([x for x in results if x == 3])
    expected_count_of_threes = sample_count / 10
    difference = abs(actual_count_of_threes - expected_count_of_threes)
    assert difference < sample_count / 100, (
        f"Expected approximately {expected_count_of_threes} threes but found {actual_count_of_threes} (difference of {difference})"
    )
    threshold = sample_count / 100
    assert abs(actual_count_of_threes - expected_count_of_threes) < threshold, (
        f"Expected number of threes to be within {threshold} of {expected_count_of_threes}, but got {actual_count_of_threes}"
    )
    assert (
        abs(len([x for x in results if x == 7]) - sample_count / 10)
        < sample_count / 100
    )


def test_all_values_greater_than_or_equal_to_min_value() -> None:
    sample_count = 10000
    results = [random_int(1, 10) for _ in range(sample_count)]

    assert min(results) == 1


def test_all_values_less_than_or_equal_to_max_value() -> None:
    sample_count = 10000
    results = [random_int(1, 10) for _ in range(sample_count)]

    assert max(results) == 10
    assert max(results) == 10

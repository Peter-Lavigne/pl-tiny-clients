import string

from pl_tiny_clients.constants import PYTEST_NONDETERMINISTIC_MARKER
from pl_tiny_clients.random_str import random_str

pytestmark = [PYTEST_NONDETERMINISTIC_MARKER]


def test_returns_correct_length() -> None:
    result = random_str(10)
    assert len(result) == 10

    result = random_str(5)
    assert len(result) == 5

    result = random_str(20)
    assert len(result) == 20


def test_all_characters_are_valid() -> None:
    # Test that all characters are letters or digits
    valid_chars = set(string.ascii_letters + string.digits)
    sample_count = 1000

    for _ in range(sample_count):
        result = random_str(10)
        for char in result:
            assert char in valid_chars, (
                f"Invalid character '{char}' found in '{result}'"
            )


def test_generates_different_values() -> None:
    # Test that the function produces random results (not always the same)
    results: set[str] = set()
    sample_count = 1000

    for _ in range(sample_count):
        results.add(random_str(10))

    # With 1000 samples of 10-character strings, we should get many unique values
    # If we get less than 900 unique values, something is likely wrong with randomness
    assert len(results) > 900, (
        f"Expected at least 900 unique strings but got {len(results)}"
    )


def test_character_distribution() -> None:
    # Note: This test is non-deterministic
    # Test that characters are roughly evenly distributed
    all_results = ""
    sample_count = 10000

    for _ in range(sample_count):
        all_results += random_str(10)

    # Count how many times 'a' appears
    count_of_a = all_results.count("a")
    total_chars = len(all_results)
    valid_chars_count = len(string.ascii_letters + string.digits)

    # Expected frequency for any single character
    expected_frequency = total_chars / valid_chars_count

    # Allow for 50% variance (statistical test)
    assert abs(count_of_a - expected_frequency) < expected_frequency * 0.5, (
        f"Character 'a' appeared {count_of_a} times, expected around {expected_frequency}"
    )

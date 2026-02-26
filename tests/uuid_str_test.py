import re

from pl_tiny_clients.constants import PYTEST_NONDETERMINISTIC_MARKER
from pl_tiny_clients.uuid_str import uuid_str

pytestmark = [PYTEST_NONDETERMINISTIC_MARKER]


def test_return_value_is_formatted_as_uuid() -> None:
    """Test that the UUID is formatted correctly according to RFC 4122."""
    result = uuid_str()

    # UUID format: 8-4-4-4-12 (hexadecimal characters separated by hyphens)
    # Example: 550e8400-e29b-41d4-a716-446655440000
    uuid_pattern = re.compile(
        r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
    )

    assert isinstance(result, str), f"UUID must be a string, got {type(result)}"
    assert uuid_pattern.match(result), f"UUID format is invalid: {result}"
    assert len(result) == 36, (
        f"UUID must be exactly 36 characters long, got {len(result)}"
    )


def test_return_value_is_unique() -> None:
    """Test that multiple calls to uuid() generate unique values."""
    num_iterations = 1000
    generated_uuids = [uuid_str() for _ in range(num_iterations)]

    # Check that all UUIDs are unique
    unique_uuids = set(generated_uuids)
    assert len(unique_uuids) == num_iterations, (
        f"Expected {num_iterations} unique UUIDs, but got {len(unique_uuids)}. "
        f"Duplicates found: {num_iterations - len(unique_uuids)}"
    )

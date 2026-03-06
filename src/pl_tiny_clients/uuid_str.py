import uuid as uuid_module

from pl_mocks_and_fakes import MockInUnitTests, MockReason

UUIDReturnValue = str


@MockInUnitTests(MockReason.NONDETERMINISTIC)
def uuid_str() -> UUIDReturnValue:
    """
    Generate and returns a UUID string.

    Returns:
        str: A UUID string in the format 8-4-4-4-12 (e.g., "550e8400-e29b-41d4-a716-446655440000")

    """
    return str(uuid_module.uuid4())

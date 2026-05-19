from secrets import randbelow

from pl_mocks_and_fakes import MockInUnitTests, MockReason

type RandomIntResponse = int


@MockInUnitTests(MockReason.UNINVESTIGATED)
def random_int(min_value: int, max_value: int) -> RandomIntResponse:
    """Return a value N in the range min_value <= N <= max_value."""
    return min_value + randbelow(max_value - min_value + 1)

from time import time

from pl_mocks_and_fakes import MockInUnitTests, MockReason


@MockInUnitTests(MockReason.NONDETERMINISTIC)
def current_time() -> float:
    """Return the current time as a Unix timestamp, in seconds."""
    return time()

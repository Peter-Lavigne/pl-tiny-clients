from datetime import timedelta
from time import sleep

from pl_mocks_and_fakes import MockInUnitTests, MockReason


@MockInUnitTests(MockReason.UNINVESTIGATED)
def delay(t: timedelta) -> None:
    """
    Pauses thread execution.

    This should be used instead of `time.sleep` because the behavior is documented better.

    Computer sleep interferes with this function, extending it by the amount of time the computer was asleep. For this reason it is recommended to pass small t values.
    """
    seconds = t.total_seconds()
    sleep(seconds)

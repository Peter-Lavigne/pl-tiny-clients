from datetime import timedelta
from time import sleep
from typing import NamedTuple

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.current_datetime import current_datetime


class DelayResponse(NamedTuple):
    clock_time_passed: timedelta
    computer_asleep_time: timedelta | None


@MockInUnitTests(MockReason.UNINVESTIGATED)
def delay(t: timedelta) -> DelayResponse:
    """
    Pauses thread execution.

    This should be used instead of `time.sleep` because the behavior is documented better.

    Computer sleep interferes with this function, extending it by the amount of time the computer was asleep. For this reason it is recommended to pass small t values.

    Returns a tuple containing:
     - The actual time passed ("clock time"). This may be less or greater than t.
     - The time the computer was asleep. This value is imperfect and may be off by 45 seconds or so.
    """
    seconds = t.total_seconds()
    t1 = current_datetime()
    sleep(seconds)
    t2 = current_datetime()
    clock_time = t2 - t1

    diff = clock_time - t
    error_bound = timedelta(seconds=0.01)
    computer_asleep_time = diff if diff > error_bound else None

    return DelayResponse(clock_time, computer_asleep_time)

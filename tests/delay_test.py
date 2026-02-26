from datetime import timedelta

from pl_user_io.assert_yes import assert_yes
from pl_user_io.display import display
from pl_user_io.task import task

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.current_datetime import current_datetime
from pl_tiny_clients.delay import delay

pytestmark = PYTEST_INTEGRATION_MARKER


def test_pauses_execution() -> None:
    task("After pressing enter, start counting from 0 until `Done.` is printed.")
    delay(timedelta(seconds=5))
    display("Done.")
    assert_yes("Did it take 5 seconds to print `Done.`?")


def test_smaller_clock_times_sometimes_returned() -> None:
    # Interestingly, I was unable to get this to pass with smaller t values,
    # such as one second.
    t = timedelta(minutes=1)
    attempts = 60
    for _ in range(attempts):
        clock_time, _ = delay(t)
        if clock_time < t:
            return
    msg = "Expected a smaller clock time than passed to appear."
    raise AssertionError(msg)


def test_computer_sleep_adds_to_delay() -> None:
    task(
        "After pressing enter, put the computer to sleep for two minutes. The test will resume about one minute later."
    )

    t1 = current_datetime()
    delay(timedelta(minutes=1))
    t2 = current_datetime()
    total_minutes = (t2 - t1).total_seconds() / 60

    assert abs(total_minutes - (1 + 2)) < 0.75  # assert almost equal


def test_returns_computer_asleep_time_if_asleep() -> None:
    task(
        "After pressing enter, put the computer to sleep for two minutes. The test will resume about one minute later."
    )

    _, asleep_time = delay(timedelta(minutes=1))

    assert asleep_time is not None
    minutes_asleep_manual = 2
    minutes_asleep_reported = asleep_time.total_seconds() / 60
    assert (
        abs(minutes_asleep_manual - minutes_asleep_reported) < 0.75
    )  # assert almost equal


def test_returns_none_for_computer_asleep_time_if_not_asleep() -> None:
    for _ in range(10000):
        _, asleep_time = delay(timedelta(milliseconds=1))
        assert asleep_time is None

    for _ in range(1000):
        _, asleep_time = delay(timedelta(milliseconds=10))
        assert asleep_time is None

    for _ in range(100):
        _, asleep_time = delay(timedelta(milliseconds=100))
        assert asleep_time is None

    for _ in range(10):
        _, asleep_time = delay(timedelta(seconds=1))
        assert asleep_time is None

    for _ in range(10):
        _, asleep_time = delay(timedelta(seconds=10))
        assert asleep_time is None

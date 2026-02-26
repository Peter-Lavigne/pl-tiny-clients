from pl_user_io.int_input import int_input
from pl_user_io.task_with_url import task_with_url

from pl_tiny_clients.constants import PYTEST_MANUAL_MARKERS
from pl_tiny_clients.current_time import current_time
from tests.conftest import with_pytestmarks


@with_pytestmarks(*PYTEST_MANUAL_MARKERS)
def test_current_time() -> None:
    task_with_url(
        "Check the current Unix timestamp.", "https://www.epochconverter.com/"
    )
    human_verified_timestamp = int_input(
        "Enter the current Unix timestamp (in seconds):"
    )

    now = current_time()

    assert abs(human_verified_timestamp - now) < 60, (
        "The human-verified timestamp should be close to the actual current time."
    )

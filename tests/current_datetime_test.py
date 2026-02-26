from pl_mocks_and_fakes import fake_for

from pl_tiny_clients.current_datetime import current_datetime
from pl_tiny_clients.testing.time_fake import TimeFake


def test_current_datetime() -> None:
    one_year_in_seconds = 60 * 60 * 24 * 365
    timezone_offset_seconds = (
        60 * 60 * 5
    )  # My timezone is UTC-5, so the offset is 5 hours in seconds
    fake_for(TimeFake).set_current_time(one_year_in_seconds + timezone_offset_seconds)

    result = current_datetime()

    assert result.year == 1971

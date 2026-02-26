from datetime import datetime

from pl_tiny_clients.constants import SYSTEM_TIMEZONE
from pl_tiny_clients.current_time import current_time


def current_datetime() -> datetime:
    """Return the current datetime in the system timezone."""
    return datetime.fromtimestamp(current_time(), tz=SYSTEM_TIMEZONE)

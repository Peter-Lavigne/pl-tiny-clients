from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.get_volume_on_mac import get_volume_on_mac
from pl_tiny_clients.get_volume_on_ubuntu import get_volume_on_ubuntu


def get_volume() -> int:
    """Return the volume as a value between 0 and 100."""
    return by_platform(
        mac=get_volume_on_mac,
        ubuntu=get_volume_on_ubuntu,
    )()

from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.set_volume_on_mac import set_volume_on_mac
from pl_tiny_clients.set_volume_on_ubuntu import set_volume_on_ubuntu


def set_volume(volume: int) -> None:
    """Set the volume to a value between 0 and 100."""
    by_platform(
        mac=set_volume_on_mac,
        ubuntu=set_volume_on_ubuntu,
    )(volume)

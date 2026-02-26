from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.put_mac_to_sleep import put_mac_to_sleep
from pl_tiny_clients.put_ubuntu_to_sleep import put_ubuntu_to_sleep


def put_computer_to_sleep() -> None:
    by_platform(
        mac=put_mac_to_sleep,
        ubuntu=put_ubuntu_to_sleep,
    )()

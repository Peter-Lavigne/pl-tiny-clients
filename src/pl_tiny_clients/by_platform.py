from typing import TypeVar

from pl_tiny_clients.constants import PLATFORM_MAC, PLATFORM_UBUNTU
from pl_tiny_clients.settings import get_settings

T = TypeVar("T")


def by_platform(mac: T, ubuntu: T) -> T:
    platform = get_settings().platform
    if platform == PLATFORM_MAC:
        return mac
    if platform == PLATFORM_UBUNTU:
        return ubuntu
    msg = f"Unsupported platform: {platform}"
    raise ValueError(msg)

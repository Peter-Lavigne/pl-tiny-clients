from pl_tiny_clients.by_platform import by_platform
from pl_tiny_clients.notify_on_mac import notify_on_mac
from pl_tiny_clients.notify_on_ubuntu import notify_on_ubuntu


def notify(text: str, title: str | None = None) -> None:
    if title is None:
        title = "Notifier"

    by_platform(
        mac=notify_on_mac,
        ubuntu=notify_on_ubuntu,
    )(text, title)

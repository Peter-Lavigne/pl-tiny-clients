from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.fetch_chat_completion_baseten_deepseek import (
    fetch_chat_completion_baseten_deepseek,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_fetch_chat_completion_baseten_deepseek_returns_text() -> None:
    result = fetch_chat_completion_baseten_deepseek(
        "Say 'Hello, world!' and nothing else."
    )

    assert result.text == "Hello, world!"


def test_fetch_chat_completion_baseten_deepseek_returns_cost() -> None:
    result = fetch_chat_completion_baseten_deepseek(
        "Say 'Hello, world!' and nothing else."
    )

    assert result.cost_in_dollars > 0  # Should cost something
    assert result.cost_in_dollars < 0.01  # Should be very cheap

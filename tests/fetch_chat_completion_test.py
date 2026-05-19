from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.current_time import current_time
from pl_tiny_clients.fetch_chat_completion import (
    MODEL_HAIKU_4_5,
    MODEL_OPUS_4_5,
    fetch_chat_completion,
)

pytestmark = PYTEST_INTEGRATION_MARKER


def test_generates_text() -> None:
    result = fetch_chat_completion("Say 'Hello, world!'")

    assert result.text == "Hello, world!"


def test_chooses_tool() -> None:
    prompt = "Read the contents of the file at path '/tmp/test.txt' and return it."

    result = fetch_chat_completion(
        prompt,
        tools=[
            {
                "name": "read_file",
                "description": "Returns the content of a file.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to be read.",
                        }
                    },
                    "required": ["file_path"],
                },
            }
        ],
    )

    assert result.tool_choice == "read_file"


def test_generates_text_and_chooses_tool() -> None:
    prompt = (
        "First, say 'Hello!'. Then, read the contents of the file at path "
        "'/tmp/test.txt' and return it."
    )

    result = fetch_chat_completion(
        prompt,
        tools=[
            {
                "name": "read_file",
                "description": "Returns the content of a file.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The path to the file to be read.",
                        }
                    },
                    "required": ["file_path"],
                },
            }
        ],
    )

    assert "Hello!" in result.text
    assert result.tool_choice == "read_file"


def test_can_select_model() -> None:
    time_haiku_start = current_time()
    fetch_chat_completion(
        "Count to 500 by fours.",
        model=MODEL_HAIKU_4_5,
    )
    time_haiku_end = current_time()
    total_haiku_time = time_haiku_end - time_haiku_start

    time_opus_start = current_time()
    fetch_chat_completion(
        "Count to 500 by fours.",
        model=MODEL_OPUS_4_5,
    )
    time_opus_end = current_time()
    total_opus_time = time_opus_end - time_opus_start

    # Haiku is unaware of it's model, so I'm using time taken as a proxy for capability.
    assert total_opus_time > total_haiku_time * 1.1


def test_cost_is_reported_for_haiku_chat_completions() -> None:
    result = fetch_chat_completion(
        "Say 'Hello, world!'",
        model=MODEL_HAIKU_4_5,
    )

    assert result.cost is not None
    assert result.cost > 0.0

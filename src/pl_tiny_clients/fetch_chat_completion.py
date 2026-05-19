from typing import NamedTuple, TypedDict, cast

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.fetch_chat_completion_baseten_deepseek import (
    fetch_chat_completion_baseten_deepseek,
)
from pl_tiny_clients.fetch_chat_completion_deepseek import (
    fetch_chat_completion_deepseek,
)
from pl_tiny_clients.requests_wrapper import BodyParamItem, BodyParams, requests_wrapper
from pl_tiny_clients.settings import get_settings

INPUT_PRICE_PER_MILLION = 1.0
OUTPUT_PRICE_PER_MILLION = 5.0


class FetchChatCompletionResponse(NamedTuple):
    text: str
    tool_choice: str | None
    cost: float | None = None


class _UsageDict(TypedDict):
    # Note: Does not include cache or tool usage costs
    input_tokens: int
    output_tokens: int


class _ChatCompletionApiResponseContentText(TypedDict):
    type: str
    text: str


class _ChatCompletionApiResponseContentToolUse(TypedDict):
    type: str
    name: str
    input: dict[str, str]


MODEL_HAIKU_4_5 = "claude-haiku-4-5"
MODEL_SONNET_4_5 = "claude-sonnet-4-5"
MODEL_OPUS_4_5 = "claude-opus-4-5"

MODEL_DEEPSEEK_V3_2 = "deepseek-ai/DeepSeek-V3.2"

PROVIDER_ANTHROPIC = "anthropic"
PROVIDER_BASETEN = "baseten"
PROVIDER_DEEPSEEK = "deepseek"

ToolsType = BodyParamItem


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_chat_completion(
    prompt: str,
    model: str = MODEL_HAIKU_4_5,
    provider: str = PROVIDER_ANTHROPIC,
    tools: BodyParamItem | None = None,
) -> FetchChatCompletionResponse:
    if provider == PROVIDER_ANTHROPIC:
        # Docs: https://platform.claude.com/docs/en/api/messages/create
        # Prompt testing: https://console.anthropic.com/workbench

        assert model in {MODEL_HAIKU_4_5, MODEL_SONNET_4_5, MODEL_OPUS_4_5}, (
            f"Unsupported model for Anthropic provider: {model}"
        )

        class _FetchChatCompletionApiResponse(TypedDict):
            content: list[
                _ChatCompletionApiResponseContentText
                | _ChatCompletionApiResponseContentToolUse
            ]
            stop_reason: str
            usage: _UsageDict

        body_params: BodyParams = {
            "model": model,
            "max_tokens": 10000,
            "messages": [{"role": "user", "content": prompt}],
        }

        if tools is not None:
            body_params["tools"] = tools  # type: ignore[assignment]

        response = requests_wrapper(
            "https://api.anthropic.com/v1/messages",
            _FetchChatCompletionApiResponse,
            method="POST",
            headers={
                # https://console.anthropic.com/settings/keys
                "x-api-key": get_settings().anthropic_api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01",
            },
            body_params=body_params,
            timeout=30,
        )

        if len(response["content"]) == 1:
            if response["content"][0]["type"] == "text":
                assert response["stop_reason"] == "end_turn"
                text_content = cast(
                    "_ChatCompletionApiResponseContentText", response["content"][0]
                )
                usage: float | None = None
                if model == MODEL_HAIKU_4_5:
                    usage_content = response["usage"]
                    input_cost = (
                        usage_content["input_tokens"]
                        / 1000000
                        * INPUT_PRICE_PER_MILLION
                    )
                    output_cost = (
                        usage_content["output_tokens"]
                        / 1000000
                        * OUTPUT_PRICE_PER_MILLION
                    )
                    usage = input_cost + output_cost
                return FetchChatCompletionResponse(
                    text=text_content["text"],
                    tool_choice=None,
                    cost=usage,
                )
            if response["content"][0]["type"] == "tool_use":
                assert response["stop_reason"] == "tool_use"
                tool_use_content = cast(
                    "_ChatCompletionApiResponseContentToolUse", response["content"][0]
                )
                return FetchChatCompletionResponse(
                    text="",
                    tool_choice=tool_use_content["name"],
                )
        elif len(response["content"]) == 2:
            assert response["content"][0]["type"] == "text"
            assert response["content"][1]["type"] == "tool_use"
            assert response["stop_reason"] == "tool_use"
            text_content = cast(
                "_ChatCompletionApiResponseContentText", response["content"][0]
            )
            tool_use_content = cast(
                "_ChatCompletionApiResponseContentToolUse", response["content"][1]
            )
            return FetchChatCompletionResponse(
                text=text_content["text"],
                tool_choice=tool_use_content["name"],
            )
        msg = "Unexpected response format from chat completion API."
        raise Exception(msg)
    if provider == PROVIDER_BASETEN:
        # This section is untested; I'm still trying to decide on the API design.
        assert model == MODEL_DEEPSEEK_V3_2, (
            f"Unsupported model for Baseten provider: {model}"
        )
        result = fetch_chat_completion_baseten_deepseek(prompt)
        return FetchChatCompletionResponse(
            text=result.text,
            tool_choice=None,
            cost=result.cost_in_dollars,
        )
    if provider == PROVIDER_DEEPSEEK:
        # This section is untested; I'm still trying to decide on the API design.
        assert model == MODEL_DEEPSEEK_V3_2, (
            f"Unsupported model for Deepseek provider: {model}"
        )
        result = fetch_chat_completion_deepseek(prompt)
        return FetchChatCompletionResponse(
            text=result.text,
            tool_choice=None,
            cost=result.cost_in_dollars,
        )
    msg = f"Unsupported model: {model}"
    raise Exception(msg)

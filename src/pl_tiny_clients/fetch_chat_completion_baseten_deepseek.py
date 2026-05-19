from typing import NamedTuple, TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings


class FetchChatCompletionBasetenDeepseekResponseChoiceMessage(TypedDict):
    content: str
    role: str


class FetchChatCompletionBasetenDeepseekResponseChoice(TypedDict):
    index: int
    message: FetchChatCompletionBasetenDeepseekResponseChoiceMessage
    finish_reason: str


class FetchChatCompletionBasetenDeepseekResponseUsagePromptTokensDetails(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_tokens_details: dict[str, int]
    completion_tokens_details: dict[str, int]


class FetchChatCompletionBasetenDeepseekAPIResponse(TypedDict):
    choices: list[FetchChatCompletionBasetenDeepseekResponseChoice]
    usage: FetchChatCompletionBasetenDeepseekResponseUsagePromptTokensDetails


class FetchChatCompletionBasetenDeepseekResponse(NamedTuple):
    text: str
    cost_in_dollars: float


INPUT_COST_PER_MILLION_TOKENS_IN_CENTS = 30
OUTPUT_COST_PER_MILLION_TOKENS_IN_CENTS = 45


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_chat_completion_baseten_deepseek(
    prompt: str,
) -> FetchChatCompletionBasetenDeepseekResponse:
    # Docs: https://www.baseten.co/library/deepseek-v3-2/
    # The rate limit for this endpoint is relatively low, at 15 requests per minute for "unverified" accounts and 120 requests per minute for "verified" accounts. There's no documentation on how to check whether the account is verified or not. For reference, Anthropic's rate limit is 1000 requests per minute and Deepseek's is unlimited.

    result = requests_wrapper(
        "https://inference.baseten.co/v1/chat/completions",
        FetchChatCompletionBasetenDeepseekAPIResponse,
        method="POST",
        headers={
            "Content-Type": "application/json",
            # https://baseten.co/account/api-keys
            "Authorization": f"Api-Key {get_settings().baseten_api_key}",
        },
        body_params={
            "model": "deepseek-ai/DeepSeek-V3.2",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )

    for value in result["usage"]["prompt_tokens_details"].values():
        assert value == 0, f"Unexpected prompt tokens details value: {value}"
    for value in result["usage"]["completion_tokens_details"].values():
        assert value == 0, f"Unexpected completion tokens details value: {value}"

    input_cost_per_token_in_dollars = (
        INPUT_COST_PER_MILLION_TOKENS_IN_CENTS / 1_000_000 / 100
    )
    output_cost_per_token_in_dollars = (
        OUTPUT_COST_PER_MILLION_TOKENS_IN_CENTS / 1_000_000 / 100
    )

    return FetchChatCompletionBasetenDeepseekResponse(
        text=result["choices"][0]["message"]["content"],
        cost_in_dollars=(
            result["usage"]["prompt_tokens"] * input_cost_per_token_in_dollars
            + result["usage"]["completion_tokens"] * output_cost_per_token_in_dollars
        ),
    )

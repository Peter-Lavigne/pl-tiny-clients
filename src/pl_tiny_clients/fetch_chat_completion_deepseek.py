from typing import NamedTuple, TypedDict

from pl_mocks_and_fakes import MockInUnitTests, MockReason

from pl_tiny_clients.requests_wrapper import requests_wrapper
from pl_tiny_clients.settings import get_settings


class FetchChatCompletionDeepseekAPIResponseChoiceMessage(TypedDict):
    role: str
    content: str


class FetchChatCompletionDeepseekAPIResponseChoice(TypedDict):
    index: int
    message: FetchChatCompletionDeepseekAPIResponseChoiceMessage
    finish_reason: str


class FetchChatCompletionDeepseekAPIResponseUsagePromptTokensDetails(TypedDict):
    cached_tokens: int


class FetchChatCompletionDeepseekAPIResponseUsage(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    prompt_tokens_details: (
        FetchChatCompletionDeepseekAPIResponseUsagePromptTokensDetails
    )
    prompt_cache_hit_tokens: int
    prompt_cache_miss_tokens: int


class FetchChatCompletionDeepseekAPIResponse(TypedDict):
    choices: list[FetchChatCompletionDeepseekAPIResponseChoice]
    usage: FetchChatCompletionDeepseekAPIResponseUsage


class FetchChatCompletionDeepseekResponse(NamedTuple):
    text: str
    cost_in_dollars: float


PRICE_PER_MILLION_INPUT_TOKENS_CACHE_HIT_IN_DOLLARS = 0.028
PRICE_PER_MILLION_INPUT_TOKENS_CACHE_MISS_IN_DOLLARS = 0.28
PRICE_PER_MILLION_OUTPUT_TOKENS_IN_DOLLARS = 0.42


@MockInUnitTests(MockReason.UNINVESTIGATED)
def fetch_chat_completion_deepseek(prompt: str) -> FetchChatCompletionDeepseekResponse:
    # Docs: https://api-docs.deepseek.com/
    result = requests_wrapper(
        "https://api.deepseek.com/chat/completions",
        FetchChatCompletionDeepseekAPIResponse,
        method="POST",
        headers={
            "Content-Type": "application/json",
            # https://platform.deepseek.com/account/api-keys
            "Authorization": f"Bearer {get_settings().deepseek_api_key}",
        },
        body_params={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )

    usage = result["usage"]
    assert (
        usage["prompt_tokens"] + usage["completion_tokens"] == usage["total_tokens"]
    ), "Inconsistent token usage counts"
    assert (
        usage["prompt_cache_hit_tokens"] + usage["prompt_cache_miss_tokens"]
        == usage["prompt_tokens"]
    ), "Inconsistent prompt token cache counts"

    price_per_input_token_cache_hit_in_dollars = (
        PRICE_PER_MILLION_INPUT_TOKENS_CACHE_HIT_IN_DOLLARS / 1_000_000
    )
    price_per_input_token_cache_miss_in_dollars = (
        PRICE_PER_MILLION_INPUT_TOKENS_CACHE_MISS_IN_DOLLARS / 1_000_000
    )
    price_per_output_token_in_dollars = (
        PRICE_PER_MILLION_OUTPUT_TOKENS_IN_DOLLARS / 1_000_000
    )

    return FetchChatCompletionDeepseekResponse(
        text=result["choices"][0]["message"]["content"],
        cost_in_dollars=(
            usage["prompt_cache_hit_tokens"]
            * price_per_input_token_cache_hit_in_dollars
            + usage["prompt_cache_miss_tokens"]
            * price_per_input_token_cache_miss_in_dollars
            + usage["completion_tokens"] * price_per_output_token_in_dollars
        ),
    )

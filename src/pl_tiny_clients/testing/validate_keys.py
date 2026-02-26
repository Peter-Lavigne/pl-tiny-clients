from typing import TypedDict, TypeVar, get_type_hints

MOCKS_FILE_PATH = "/Users/peter/bin/src/test_utils.py"

# I don't know why this type bound is failing checks. It seems to work fine.
U = TypeVar("U", bound=TypedDict)  # type: ignore[type-arg]


# Deprecated: Use Pydantic instead
def validate_keys(data: U, data_type: type[U]) -> None:  # noqa: UP047, RUF100
    actual_keys = set(data.keys())
    for expected_key in get_type_hints(data_type):
        assert expected_key in actual_keys, (
            f"Key `{expected_key}` is missing from the data."
        )

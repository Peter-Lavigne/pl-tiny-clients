import os
from collections.abc import Callable
from typing import Any, TypeVar

import pytest
from dotenv.main import load_dotenv
from pl_mocks_and_fakes import create_fakes, initialize_mocks
from pl_user_io.display import display
from pl_user_io.testing import UserIOFake

from pl_tiny_clients.constants import (
    PYTEST_INTEGRATION_TEST_MARKERS,
)
from pl_tiny_clients.testing.settings_fake import SettingsFake
from pl_tiny_clients.testing.time_fake import TimeFake

F = TypeVar("F", bound=Callable[..., Any])


def with_pytestmarks(*marks: pytest.MarkDecorator) -> Callable[[F], F]:
    """Apply the given pytest marks to a test function."""

    def decorator(func: F) -> F:
        func.__setattr__("pytestmark", list(marks))
        return func

    return decorator


def pytest_runtest_setup(item: pytest.Item) -> None:
    def _add_newline_before_tests() -> None:
        display()

    def _is_integration_test() -> bool:
        return any(
            marker.name in [m.name for m in PYTEST_INTEGRATION_TEST_MARKERS]
            for marker in item.iter_markers()
        )

    def _load_env_for_integration_tests() -> None:
        if _is_integration_test():
            load_dotenv()

    def _clear_env_for_unit_tests() -> None:
        if not _is_integration_test():
            os.environ.clear()

    def _mock_code_for_unit_tests() -> None:
        if not _is_integration_test():
            initialize_mocks()
            create_fakes(
                TimeFake,
                SettingsFake,
                UserIOFake,
            )

    _add_newline_before_tests()
    _load_env_for_integration_tests()
    _clear_env_for_unit_tests()
    _mock_code_for_unit_tests()

from pl_user_io.assert_yes import assert_yes

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.execute_shell_command import CommandError, execute_shell_command

pytestmark = PYTEST_INTEGRATION_MARKER


def test_returns_output() -> None:
    output = execute_shell_command("echo hello")
    assert output == "hello"


def test_supports_brace_expansion() -> None:
    output = execute_shell_command("for i in {1..3}; do echo $i; done")
    assert output == "1\n2\n3"


def test_raises_exception() -> None:
    # Source for writing to stderr syntax: https://stackoverflow.com/q/2990414
    command = "echo ERROR 1>&2 && exit 1"
    try:
        execute_shell_command(command)
        msg = "Expected exception to be raised."
        raise AssertionError(msg)
    except CommandError as e:
        assert (
            str(e)
            == f"Error: command `{command}` returned code `1` with output `` and error: `ERROR`"
        )


def test_logs_output() -> None:
    command = "echo hello"
    output = execute_shell_command(command)
    assert_yes(f"Was the command '{command}' logged to the test logs?")
    assert_yes(f"Was the output '{output}' logged? to the test logs?")


def test_logs_output__newlines_display_on_one_line() -> None:
    command = "for i in {1..5}; do echo $i; done"

    execute_shell_command(command)

    assert_yes(
        "Do the test logs contain output without newlines, such as `1\\n2\\n3\\n4\\n5`?"
    )


def test_passes_env_variables() -> None:
    env = {"TEST_ENV_VAR": "test value"}
    output = execute_shell_command("echo $TEST_ENV_VAR", env=env)
    assert output == "test value"


def test_execute_shell_command_can_stream_output() -> None:
    execute_shell_command(
        "for i in 1 2 3 4 5; do echo $i; sleep 1; done", stream_output=True
    )

    assert_yes("Did you see the numbers 1-5 printed one at a time?")

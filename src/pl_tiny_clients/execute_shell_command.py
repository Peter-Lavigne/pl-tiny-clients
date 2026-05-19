import logging
import subprocess

from pl_mocks_and_fakes import MockInUnitTests, MockReason
from pl_user_io.display import display


class CommandError(Exception):
    pass


@MockInUnitTests(MockReason.UNINVESTIGATED)
def execute_shell_command(
    command: str, env: dict[str, str] | None = None, stream_output: bool = False
) -> str:
    """
    I'M CONSIDERING DEPRECATING THIS: Consider migrating to run_program, which has a simpler interface and is more secure.

    Runs a shell command and returns its output. Raises an exception if the command fails.

    For interactive commands, capturing output can lead to issues, such as not seeing prompts.
    For those commands, use subprocess.run() directly instead.

    If using external input, beware shell injection attacks.
    """

    def _log_shell_command_output(output: str) -> None:
        """Log the output of a shell command."""
        # The output for `display_power_events` is thousands of lines long so I had been truncating it. However, debugging it was made harder with partial output. I'm now trying a one-line approach which could be better. If that doesn't work, consider allowing turning off or customizing (i.e. regex, passed str->str function) output for a given command.

        def _oneline_output(o: str) -> str:
            return o.replace("\n", "\\n")

        logging.debug(f"Shell command out/err: `{_oneline_output(output)}`")

    logging.debug(f"Executing shell command: `{command}`")

    if stream_output:
        # Stream mode: print output line by line as it arrives
        process = subprocess.Popen(  # noqa: S602 (deprecated function)
            command,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            executable="/bin/bash",
        )

        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        # Read stdout line by line
        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                if not line:
                    break
                # Remove trailing newline for callback
                line_stripped = line.rstrip("\n")
                stdout_lines.append(line_stripped)
                display(line_stripped)

        # Wait for process to complete and get stderr
        process.wait()
        if process.stderr:
            stderr_content = process.stderr.read()
            stderr_lines = stderr_content.split("\n")[:-1] if stderr_content else []
        out = "\n".join(stdout_lines)
        err = "\n".join(stderr_lines)
        return_code = process.returncode
    else:
        result = subprocess.run(  # noqa: S602 (deprecated function)
            command,
            shell=True,
            text=True,
            capture_output=True,
            env=env,
            executable="/bin/bash",
            check=False,
        )
        out, err = result.stdout[:-1], result.stderr[:-1]  # Remove trailing newline
        return_code = result.returncode

    if return_code != 0:
        logging.debug(f"Shell command returned error code {return_code}")
        _log_shell_command_output(err)
        msg = f"Error: command `{command}` returned code `{return_code}` with output `{out}` and error: `{err}`"
        raise CommandError(msg)
    _log_shell_command_output(out)
    return out

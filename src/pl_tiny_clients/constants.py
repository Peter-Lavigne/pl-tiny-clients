from pathlib import Path

from pl_run_program import program_at_path

UV_PROGRAM = program_at_path(Path.home() / ".local/bin/uv")

SPOTIFY_CLIENT_ID = "5dac1d5933fb4c89bc85a3067adb6af0"
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_DESKTOP_DEVICE_NAME = "Peter’s iMac"  # noqa: RUF001
SPOTIFY_PHONE_DEVICE_NAME = "KB2005"

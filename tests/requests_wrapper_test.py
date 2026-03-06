from pprint import pprint
from types import NoneType
from typing import Any, cast

from pl_user_io.display import display
from pl_user_io.task import task
from pl_user_io.yes_no import yes_no

from pl_tiny_clients.constants import PYTEST_INTEGRATION_MARKER
from pl_tiny_clients.requests_wrapper import requests_wrapper

# Tests in this file make real API and system calls and use a combination of
# automated and manual verification techniques.

pytestmark = PYTEST_INTEGRATION_MARKER


def start_test_server() -> None:
    task("Start a basic Python server by running `cd ~/bin && python -m http.server`")


def stop_test_server() -> None:
    task("Stop the server")


def _setup_custom_server(test_server_code: str) -> None:
    task(
        "Copy and paste into your terminal, but do not run, the following command: pbpaste | python"
    )
    task(f"Copy the following python code:\n```\n{test_server_code}\n```")
    task("Run the command.")
    task("Wait for the server to start.")


def _setup_log_everything_server() -> None:
    _setup_custom_server("""from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Extract query parameters
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        # Read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Print the details
        print("----- Incoming POST Request -----")
        print("Query Parameters:")
        print(query_params)
        print()
        print("Body:")
        print(post_data.decode('utf-8'))
        print()
        print("Headers:")
        print(self.headers)
        print("---------------------------------")

        self.send_response(204)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
        """)


def _setup_204_test_server() -> None:
    _setup_custom_server("""from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(204)
        self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
        """)


def test_fetches_json_data() -> None:
    start_test_server()
    json_file = ".vscode/settings.json"  # This will fail if the file moves. If so, point to another json file.
    data = requests_wrapper(f"http://localhost:8000/{json_file}", dict[Any, Any])
    display("Output of {json_file}:")
    pprint(data)
    assert yes_no(f"Does the above match {json_file}?")
    stop_test_server()


def test_posts_json_data() -> None:
    _setup_log_everything_server()
    requests_wrapper(
        "http://localhost:8000/",
        NoneType,
        method="POST",
        body_params={"TestKey": "TestValue"},
        json=True,
    )
    assert yes_no(
        'Do the server logs indicate that the data {"TestKey": "TestValue"} has been sent with a Content-Type header of \'application/json\'?'
    )
    stop_test_server()


def test_posts_non_json_data() -> None:
    _setup_log_everything_server()
    requests_wrapper(
        "http://localhost:8000/",
        NoneType,
        method="POST",
        body_params={"TestKey": "TestValue"},
        json=False,
        headers={"Content-Type": "FakeContentType"},
    )
    assert yes_no(
        "Do the server logs indicate that the data \"TestKey=TestValue\" has been sent with a Content-Type header of 'FakeContentType'?"
    )
    stop_test_server()


def test_indicates_error_for_failed_requests() -> None:
    start_test_server()
    unexpected_pass = False
    try:
        requests_wrapper("http://localhost:8000/fake.json", dict)
        unexpected_pass = True
    except Exception as e:
        assert yes_no("Were you asked to investgate a failure?")
        assert yes_no("Was more information available in the logs?")
        assert yes_no("Did the logs indicate that the file could not be found?")
        display(f"Error raised: `{e}`")
        assert yes_no(
            "Does the raised error above match the one from the investigation step?"
        )
    if unexpected_pass:
        msg = "Expected an error to be thrown"
        raise AssertionError(msg)
    stop_test_server()


def test_throws_error_for_non_json_data() -> None:
    start_test_server()
    unexpected_pass = False
    this_file_path = "src/requests_wrapper_test.py"
    try:
        requests_wrapper(f"http://localhost:8000/{this_file_path}", NoneType)
        unexpected_pass = True
    except Exception as e:
        assert yes_no("Were you asked to investgate a failure?")
        assert yes_no("Was more information available in the logs?")
        assert yes_no("Did the logs indicate that the file was not JSON data?")
        display(f"Error raised: `{e}`")
        assert yes_no(
            "Does the raised error above match the one from the investigation step?"
        )
    if unexpected_pass:
        msg = "Expected an error to be thrown"
        raise AssertionError(msg)
    stop_test_server()


def test_allows_no_content_for_204() -> None:
    _setup_204_test_server()
    requests_wrapper("http://localhost:8000", method="POST")


def test_allows_possibly_no_content_for_204() -> None:
    _setup_204_test_server()
    result = cast(
        "int | None",
        requests_wrapper(
            "http://localhost:8000", int, method="POST", possibly_none_expected=True
        ),
    )
    assert result is None


def test_raises_exception_if_204_and_content_expected() -> None:
    _setup_204_test_server()

    unexpected_pass = False
    try:
        requests_wrapper("http://localhost:8000", method="POST")
        unexpected_pass = True
    except Exception as e:
        assert yes_no("Were you asked to investgate a failure?")
        assert yes_no("Was more information available in the logs?")
        assert yes_no(
            "Did the logs indicate that a type other than NoneType was requested?"
        )
        display(f"Error raised: `{e}`")
        assert yes_no(
            "Does the raised error above match the one from the investigation step?"
        )
    if unexpected_pass:
        msg = "Expected an error to be thrown"
        raise AssertionError(msg)

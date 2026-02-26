import secrets
import string

from pl_mocks_and_fakes import MockInUnitTests, MockReason


@MockInUnitTests(MockReason.UNINVESTIGATED)
def random_str(length: int) -> str:
    """
    Return a random string of the specified length containing letters (a-z, A-Z) and digits (0-9).

    Example output: "abcABC123".
    """
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))

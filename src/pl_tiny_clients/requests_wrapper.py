import logging
from collections.abc import Mapping, Sequence
from types import NoneType
from typing import Literal, cast

import requests
from pl_mocks_and_fakes import MockInUnitTests, MockReason

# If needed, authorization schemes other than basic auth could be used:
# https://requests.readthedocs.io/en/latest/user/authentication/
BasicAuth = tuple[str, str] | None

_ParamPrimitive = str | int | float | bool | None
BodyParamItem = (
    _ParamPrimitive
    | Mapping[str, "BodyParamItem"]
    | Sequence[Mapping[str, "BodyParamItem"]]
    | Sequence[_ParamPrimitive]
)
BodyParams = Mapping[str, BodyParamItem] | None
QueryParams = Mapping[str, _ParamPrimitive] | None

RequestMethod = Literal["GET", "POST", "PUT", "DELETE"]

Headers = Mapping[str, str] | None


@MockInUnitTests(MockReason.UNINVESTIGATED)
def requests_wrapper[T](
    url: str,
    response_type: type[T] = NoneType,
    method: RequestMethod = "GET",
    query_params: QueryParams = None,
    body_params: BodyParams = None,
    json: bool = True,
    headers: Headers | None = None,
    auth: BasicAuth = None,
    timeout: int = 5,
    possibly_none_expected: bool = False,
    temp_override_for_spotify_204_bug: bool = False,
) -> T:
    """
    Make an HTTP request using the requests library.

    `response_type` does not need to be set for requests where you do not use the output, such as POST requests where you don't use the response data

    When using `possibly_none_expected`, pass the non-None type to response_type and manually cast the result to a Union. Passing a union directly may be possible someday with https://github.com/python/mypy/issues/9773
    """
    logging.debug(f"Making a {method} request to URL `{url}`.")
    json_argument = body_params if json else None
    data_argument = body_params if not json else None
    response = requests.request(
        method,
        url,
        params=query_params,
        headers=headers,
        json=json_argument,
        data=data_argument,
        timeout=timeout,
        auth=auth,
    )
    response.raise_for_status()
    if response.status_code == 204:
        exactly_none_expected = response_type is NoneType
        if not exactly_none_expected and not possibly_none_expected:
            msg = f"Expected a {response_type} response, but got a 204 response."
            raise Exception(msg)
        logging.debug(f"API response for URL `{url}`: None")
        return cast("T", None)
    if temp_override_for_spotify_204_bug:
        # Remove this when https://community.spotify.com/t5/Spotify-for-Developers/200-returned-instead-of-advertised-204/td-p/6269784 is addressed
        return cast("response_type", None)  # type: ignore[return-value]
    valid_content_types = ["application/json", "application/vnd.api+json"]
    content_type = response.headers["Content-Type"]
    # We check for content type substrings because encoding may be included in the content type
    if all(vct not in content_type for vct in valid_content_types):
        msg = f"Invalid non-JSON response content type `{content_type}` for URL: {url}"
        raise Exception(msg)
    response_data = response.json()
    logging.debug(f"API response for URL `{url}`: {response_data}")
    # Adding a TypeGuard would be nice but requires either significant boilerplate
    # or an additional dependency.
    return cast("response_type", response_data)  # type: ignore[return-value]

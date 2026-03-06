from pl_tiny_clients.requests_wrapper import Headers


def spotify_api_authorization_headers(access_token: str) -> Headers:
    return {"Authorization": f"Bearer {access_token}"}

from pl_tiny_clients.constants import TRELLO_API_KEY
from pl_tiny_clients.settings import get_settings


def trello_api_authorization_headers() -> dict[str, str]:
    # Docs: https://developer.atlassian.com/cloud/trello/rest
    #
    # Obtaining an API key and token:
    # https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/
    # - Visit https://trello.com/power-ups/admin
    # - If I don't have a Power Up, create one: https://trello.com/power-ups/64a2b5a96d78a331dfd96300
    # - Go to the API Key page for that power up
    # - Copy the key to the TRELLO_API_KEY constant
    # - Click "manually generate a Token" (note: This is different from the "secret")
    # - Copy the resulting token to .env (TRELLO_TOKEN)
    api_key = TRELLO_API_KEY
    api_token = get_settings().trello_token

    return {
        "Authorization": f'OAuth oauth_consumer_key="{api_key}", oauth_token="{api_token}"'
    }

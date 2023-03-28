import logging
from typing import Any, Mapping
from airbyte_cdk.sources.streams.http.requests_native_auth import Oauth2Authenticator

logger = logging.getLogger("airbyte")


class MicrosoftSentinelOauth2Authenticator(Oauth2Authenticator):
    def __init__(
        self, url: str, client_id: str, client_secret: str, grant_type: str, resource: str, refresh_token: str = "", *args, **kwargs
    ):
        super().__init__(url, client_id, client_secret, refresh_token, *args, **kwargs)
        self.grant_type = grant_type
        self.resource = resource

    def build_refresh_request_body(self) -> Mapping[str, Any]:
        if not self.get_refresh_token():
            return {
                "client_id": self.get_client_id(),
                "client_secret": self.get_client_secret(),
                "grant_type": self.grant_type,
                "resource": self.resource
            }
        else:
            return super().build_refresh_request_body()

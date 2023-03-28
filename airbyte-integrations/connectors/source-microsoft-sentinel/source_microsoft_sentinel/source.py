#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
from urllib import parse

import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator

from .utils import initialize_authenticator


class MicrosoftSentinelStream(HttpStream, ABC):
    API_VERSION = "2022-07-01-preview"

    def __init__(self, authenticator, base_url: str, subscription_id: str, resource_group_name: str, workspace_name: str):
        super().__init__(authenticator)
        self.base_url = base_url
        self.subscription_id = subscription_id
        self.resource_group_name = resource_group_name
        self.workspace_name = workspace_name

    @property
    def url_base(self):
        return f"{self.base_url}/subscriptions/{self.subscription_id}/resourceGroups/{self.resource_group_name}/providers/Microsoft.OperationalInsights/workspaces/{self.workspace_name}/providers/Microsoft.SecurityInsights/"

    def request_params(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    ) -> MutableMapping[str, Any]:
        return {"api-version": self.API_VERSION}

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield response.json()

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None


class Incidents(MicrosoftSentinelStream):
    primary_key = None

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return "incidents"

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield response.json()["value"]



# Source
class SourceMicrosoftSentinel(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        url = parse.urljoin(config["auth_url"], f"{config['tenant_id']}/oauth2/token")
        payload = {
            "client_id": config["client_id"],
            "client_secret": config["client_secret"],
            "resource": config["resource"],
            "grant_type": config["grant_type"],
        }
        response = requests.post(url=url, data=payload)

        if response.status_code == 200:
            return True, None

        return False, "MS Sentinel account is not valid. Please make sure the credentials are valid."

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        auth = initialize_authenticator(config)
        initialization_params = {
            "authenticator": auth,
            "base_url": config["base_url"],
            "subscription_id": config["subscription_id"],
            "resource_group_name": config["resource_group_name"],
            "workspace_name": config["workspace_name"],
        }
        return [Incidents(**initialization_params)]

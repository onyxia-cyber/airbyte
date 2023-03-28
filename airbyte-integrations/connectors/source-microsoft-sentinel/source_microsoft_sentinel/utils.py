import logging
from typing import Dict

from requests.auth import AuthBase
from urllib import parse

from .authenticator import MicrosoftSentinelOauth2Authenticator


def initialize_authenticator(config: Dict) -> AuthBase:
    auth_url = parse.urljoin(config["auth_url"], f"{config['tenant_id']}/oauth2/token")
    return MicrosoftSentinelOauth2Authenticator(
        url=auth_url,
        client_secret=config["client_secret"],
        client_id=config["client_id"],
        grant_type=config["grant_type"],
        resource=config["resource"],
    )

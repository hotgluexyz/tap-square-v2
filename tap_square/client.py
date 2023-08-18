"""REST client handling, including squareStream base class."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable, Iterable, Optional

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_square.auth import squareAuthenticator
from pendulum import parse

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
from singer_sdk.authenticators import BearerTokenAuthenticator


class squareStream(RESTStream):
    """square stream class."""

   
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.cursor"  # Or override `get_next_page_token`.

    
    @cached_property
    def authenticator(self) -> squareAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        if self.config.get('is_sandbox'):
            base_endpoint = 'https://connect.squareupsandbox.com'
        else: 
            base_endpoint = "https://connect.squareup.com"
        return squareAuthenticator(self, f"{base_endpoint}/oauth2/token")

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Any:
        
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            if first_match == previous_token:
                return None
            next_page_token = first_match
        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context)
        return rep_key or start_date
    
    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        ## PAGINATION
        if next_page_token and self.rest_method == 'GET':
            params["cursor"] = next_page_token
        
        start_date = self.get_starting_time(context)
        if self.replication_key and start_date:
            start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
            params["begin_time"] = start_date
        return params

    def prepare_request_payload(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict | None:
        """Prepare the data payload for the REST API request
        """
        payload = None
        if self.rest_method == 'POST':
            payload = dict()
            if next_page_token:
                payload['cursor'] = next_page_token
        return payload

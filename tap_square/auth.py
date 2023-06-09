"""square Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from datetime import datetime, timedelta
from singer_sdk.helpers._util import utc_now
import requests
from typing import Optional
import json
from singer_sdk.authenticators import APIAuthenticatorBase
from singer_sdk.streams import Stream as RESTStreamBase

# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class squareAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for square."""
    def __init__(
        self,
        stream: RESTStreamBase,
        config_file: Optional[str] = None,
        auth_endpoint: Optional[str] = None,
    ) -> None:
        super().__init__(stream=stream)
        self._auth_endpoint = auth_endpoint
        self._config_file = config_file
        self._tap = stream._tap
    @property
    def oauth_request_body(self) -> dict:
        """Define the OAuth request body for the AutomaticTestTap API.

        Returns:
            A dict with the request body
        """
        # TODO: Define the request body needed for the API.
        return {
            'resource': 'https://connect.squareupsandbox.com/oauth2/token',
            'scope': self.oauth_scopes,
            'client_id': self.config["client_id"],
            'client_secret': self.config['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': self.config['refresh_token'],
            'short_lived':self.config['short_lived'],
        }


    def is_token_valid(self) -> bool:
        access_token = self._tap._config.get("access_token")
        now = round(datetime.utcnow().timestamp())
        expires_in = self._tap._config.get("expires_at",0)
        if expires_in:
            expires_in = self.calculate_expires_in(expires_in)

        return not bool(
            (not access_token) or (not expires_in) or ((expires_in) < 120)
        )


    
    @classmethod
    def create_for_stream(cls, stream) -> "squareAuthenticator":
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        if stream.config.get('is_sandbox'):
            base_endpoint = 'https://connect.squareupsandbox.com'
        else: 
            base_endpoint = "https://connect.squareup.com"
        
        return cls(
            stream=stream,
            auth_endpoint=f"{base_endpoint}/oauth2/token",
            oauth_scopes=["INVOICES_READ","SUBSCRIPTIONS_READ","PAYMENTS_READ"],
        )
    
    def calculate_expires_in(self,expires_at):
        given_datetime = datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ")
        current_datetime = datetime.utcnow()

        time_difference = given_datetime - current_datetime
        seconds_left = int(time_difference.total_seconds())
        return seconds_left
    
    # Authentication and refresh
    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time = utc_now()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(
            self.auth_endpoint,
            data=auth_request_payload,
            timeout=60,
        )
        try:
            token_response.raise_for_status()
        except requests.HTTPError as ex:
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.json()}'. {ex}",
            ) from ex

        self.logger.info("OAuth authorization attempt was successful.")

        token_json = token_response.json()
        self.access_token = token_json["access_token"]
        
        self.expires_in = self.calculate_expires_in(token_json.get("expires_at"))
        if self.expires_in is None:
            self.logger.debug(
                "No expires_in receied in OAuth response and no "
                "default_expiration set. Token will be treated as if it never "
                "expires.",
            )
        self.last_refreshed = request_time
        self._tap._config["access_token"] = token_json["access_token"]
        self._tap._config["expires_at"] = token_json.get("expires_at")
        self._tap._config["refresh_token"] = token_json["refresh_token"]
        with open(self._tap.config_file, "w") as outfile:
            json.dump(self._tap._config, outfile, indent=4)

    @property
    def auth_headers(self) -> dict:
        """Return a dictionary of auth headers to be applied.

        These will be merged with any `http_headers` specified in the stream.

        Returns:
            HTTP headers for authentication.
        """
        if not self.is_token_valid():
            self.update_access_token()
        result = super().auth_headers
        result["Authorization"] = f"Bearer {self._tap._config.get('access_token')}"
        return result    

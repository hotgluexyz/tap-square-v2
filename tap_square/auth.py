"""square Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import OAuthAuthenticator, SingletonMeta
from datetime import datetime, timedelta

# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class squareAuthenticator(OAuthAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for square."""
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


    def is_token_valid(self):
        access_token = self.config.get("access_token")
        now = round(datetime.utcnow().timestamp())
        day_hours = timedelta(hours=24)
        
        return not bool(
            (not access_token) or (not self.config['short_lived']) or ((self.last_refreshed - now) < day_hours)
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

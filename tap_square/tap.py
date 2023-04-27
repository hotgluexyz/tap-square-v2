"""square tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_square import streams
import inspect 


class Tapsquare(Tap):
    """square tap class."""

    name = "tap-square"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://connect.squareupsandbox.com",
            description="The url for the API service",
        ),
        th.Property(
            'client_id',
            th.StringType,
            required='true',
            description="Square application client id"

        ),
        th.Property(
            'client_secret',
            th.StringType,
            required='true',
            description="Square application client secret"

        ),
        th.Property(
            'refresh_token',
            th.StringType, 
            required=True, 
            description= "Square account OAuth refresh token"
        ),
        th.Property(
            'short_lived',
            th.BooleanType, 
            required=True, 
            description= "Square account OAuth refresh token",
            default=True
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.squareStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
           cls(self) for name, cls in inspect.getmembers(streams,inspect.isclass) if cls.__module__ == 'tap_square.streams'
        ]

if __name__ == "__main__":
    Tapsquare.cli()

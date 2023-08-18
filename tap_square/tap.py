"""square tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_square import streams
from typing import TYPE_CHECKING, Any, Callable, Iterable, Sequence, cast
from singer_sdk._singerlib import Catalog
import inspect 
if TYPE_CHECKING:
    from pathlib import PurePath

    from singer_sdk.streams import SQLStream, Stream

class Tapsquare(Tap):
    """square tap class."""
    def __init__(
        self,
        *,
        config: dict | PurePath | str | list[PurePath | str] | None = None,
        catalog: PurePath | str | dict | Catalog | None = None,
        state: PurePath | str | dict | None = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
    ) -> None:
        super().__init__(
            config=config,
            catalog=catalog,
            state=state,
            parse_env_config=parse_env_config,
            validate_config=validate_config,
        )
        self.config_file = config[0]

    name = "tap-square"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
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
            required=True,
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
        ),
        th.Property(
            'is_sandbox', 
            th.BooleanType,
            default=False
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

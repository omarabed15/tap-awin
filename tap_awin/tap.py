"""AWin tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_awin.streams import (
    AccountsStream,
    TransactionsStream,
    PublishersStream,
    ReportByPublisherStream,
)

STREAM_TYPES = [
    AccountsStream,
    TransactionsStream,
    PublishersStream,
    ReportByPublisherStream,
]


class TapAwin(Tap):

    name = "tap-awin"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "api_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service"
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            default="2016-01-01T00:00:00Z",
            description="The earliest transaction date to sync"
        ),
        th.Property(
            "timezone",
            th.StringType,
            default="Europe/London",
            description="Timezone to use"
        ),
        th.Property(
            "lookback_days",
            th.IntegerType,
            default=30,
            description="Number of days to lookback to re-sync transactions"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]

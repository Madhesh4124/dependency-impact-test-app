"""Command-line entry point for the sample application."""

import argparse
import json

from app.client import ApiClient
from app.models import EndpointConfig, FetchSummary


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch an endpoint and print response metadata.")
    parser.add_argument("url", help="Base URL to fetch")
    parser.add_argument("--name", default="default", help="Friendly endpoint name")
    args = parser.parse_args()

    config = EndpointConfig(name=args.name, url=args.url)
    result = ApiClient(config.url).fetch()
    summary = FetchSummary(
        endpoint=config.name,
        status_code=result.status_code,
        content_type=result.content_type,
    )
    print(json.dumps(summary.as_dict(), sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Datadog CLI for querying metrics, listing monitors, and searching logs."""
import argparse
import json
import os
import sys
import time
import requests


class DatadogClient:
    """Client for Datadog API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("DATADOG_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "DATADOG_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.app_key = os.environ.get("DATADOG_APP_KEY", "")
        if not self.app_key:
            print(
                '{"error": "DATADOG_APP_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        site = os.environ.get("DATADOG_SITE", "datadoghq.com")
        self.base_url_v1 = f"https://api.{site}/api/v1"
        self.base_url_v2 = f"https://api.{site}/api/v2"
        self.headers = {
            "DD-API-KEY": self.api_key,
            "DD-APPLICATION-KEY": self.app_key,
            "Content-Type": "application/json",
        }

    def query_metrics(self, query, from_ts, to_ts):
        """Query time series metrics."""
        try:
            response = requests.get(
                f"{self.base_url_v1}/query",
                headers=self.headers,
                params={
                    "query": query,
                    "from": from_ts,
                    "to": to_ts,
                },
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_monitors(self):
        """List all monitors."""
        try:
            response = requests.get(
                f"{self.base_url_v1}/monitor",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def search_logs(self, query, from_ts, to_ts):
        """Search logs using the Datadog v2 logs API."""
        payload = {
            "filter": {
                "query": query,
                "from": from_ts,
                "to": to_ts,
            },
            "sort": "-timestamp",
            "page": {"limit": 50},
        }

        try:
            response = requests.post(
                f"{self.base_url_v2}/logs/events/search",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Datadog CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    metrics_parser = subparsers.add_parser("query-metrics", help="Query time series metrics")
    metrics_parser.add_argument(
        "--query", required=True, help="Datadog metrics query (e.g., 'avg:system.cpu.user{*}')"
    )
    metrics_parser.add_argument(
        "--from", dest="from_ts", required=True,
        help="Start time as UNIX timestamp",
    )
    metrics_parser.add_argument(
        "--to", dest="to_ts", required=True,
        help="End time as UNIX timestamp",
    )

    subparsers.add_parser("list-monitors", help="List all monitors")

    logs_parser = subparsers.add_parser("search-logs", help="Search logs")
    logs_parser.add_argument("--query", required=True, help="Log search query")
    logs_parser.add_argument(
        "--from", dest="from_ts", required=True,
        help="Start time as ISO 8601 string (e.g., 2024-01-01T00:00:00Z)",
    )
    logs_parser.add_argument(
        "--to", dest="to_ts", required=True,
        help="End time as ISO 8601 string",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = DatadogClient()

    if args.command == "query-metrics":
        result = client.query_metrics(args.query, args.from_ts, args.to_ts)
    elif args.command == "list-monitors":
        result = client.list_monitors()
    elif args.command == "search-logs":
        result = client.search_logs(args.query, args.from_ts, args.to_ts)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

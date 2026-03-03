#!/usr/bin/env python3
"""PostHog CLI for capturing events, running queries, and listing feature flags."""
import argparse
import json
import os
import sys
import requests


class PostHogClient:
    """Client for PostHog API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("POSTHOG_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "POSTHOG_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.host = os.environ.get("POSTHOG_HOST", "https://app.posthog.com").rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get_project_id(self):
        """Get the first project ID for the current user."""
        try:
            response = requests.get(
                f"{self.host}/api/projects/",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results", data) if isinstance(data, dict) else data
            if results:
                return results[0].get("id")
            return None
        except requests.exceptions.RequestException:
            return None

    def capture(self, event, distinct_id, properties_json=None):
        """Capture an event."""
        payload = {
            "event": event,
            "distinct_id": distinct_id,
            "properties": {},
        }
        if properties_json:
            try:
                payload["properties"] = json.loads(properties_json)
            except json.JSONDecodeError as e:
                return {"error": f"Invalid properties JSON: {e}"}

        try:
            response = requests.post(
                f"{self.host}/capture/",
                headers={"Content-Type": "application/json"},
                json={
                    "api_key": self.api_key,
                    "event": event,
                    "distinct_id": distinct_id,
                    "properties": payload["properties"],
                },
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "status_code": response.status_code}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def query(self, query_json):
        """Run a HogQL or insights query."""
        try:
            query_obj = json.loads(query_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid query JSON: {e}"}

        project_id = self._get_project_id()
        if not project_id:
            return {"error": "Could not determine project ID"}

        try:
            response = requests.post(
                f"{self.host}/api/projects/{project_id}/query/",
                headers=self.headers,
                json={"query": query_obj},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_feature_flags(self):
        """List all feature flags."""
        project_id = self._get_project_id()
        if not project_id:
            return {"error": "Could not determine project ID"}

        try:
            response = requests.get(
                f"{self.host}/api/projects/{project_id}/feature_flags/",
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


def main():
    parser = argparse.ArgumentParser(description="PostHog CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    capture_parser = subparsers.add_parser("capture", help="Capture an event")
    capture_parser.add_argument("--event", required=True, help="Event name")
    capture_parser.add_argument(
        "--distinct-id", required=True, help="Distinct user ID"
    )
    capture_parser.add_argument(
        "--properties-json", help="JSON string of event properties"
    )

    query_parser = subparsers.add_parser("query", help="Run a query")
    query_parser.add_argument(
        "--query-json", required=True,
        help='JSON query object (e.g., \'{"kind":"HogQLQuery","query":"SELECT ..."}\')',
    )

    subparsers.add_parser("list-feature-flags", help="List feature flags")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = PostHogClient()

    if args.command == "capture":
        result = client.capture(
            args.event, args.distinct_id,
            properties_json=getattr(args, "properties_json", None),
        )
    elif args.command == "query":
        result = client.query(args.query_json)
    elif args.command == "list-feature-flags":
        result = client.list_feature_flags()

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

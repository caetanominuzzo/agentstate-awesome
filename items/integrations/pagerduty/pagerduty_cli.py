#!/usr/bin/env python3
"""PagerDuty CLI for managing incidents."""
import argparse
import json
import os
import sys
import requests


class PagerDutyClient:
    """Client for PagerDuty REST API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("PAGERDUTY_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "PAGERDUTY_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.pagerduty.com"
        self.headers = {
            "Authorization": f"Token token={self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.pagerduty+json;version=2",
        }

    def list_incidents(self, status=None):
        """List incidents, optionally filtered by status."""
        params = {"limit": 100, "sort_by": "created_at:desc"}
        if status:
            params["statuses[]"] = status

        try:
            response = requests.get(
                f"{self.base_url}/incidents",
                headers=self.headers,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_incident(self, service_id, title):
        """Create a new incident."""
        payload = {
            "incident": {
                "type": "incident",
                "title": title,
                "service": {
                    "id": service_id,
                    "type": "service_reference",
                },
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/incidents",
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

    def acknowledge(self, incident_id):
        """Acknowledge an incident."""
        payload = {
            "incident": {
                "type": "incident_reference",
                "status": "acknowledged",
            }
        }

        try:
            response = requests.put(
                f"{self.base_url}/incidents/{incident_id}",
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

    def resolve(self, incident_id):
        """Resolve an incident."""
        payload = {
            "incident": {
                "type": "incident_reference",
                "status": "resolved",
            }
        }

        try:
            response = requests.put(
                f"{self.base_url}/incidents/{incident_id}",
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
    parser = argparse.ArgumentParser(description="PagerDuty CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    list_parser = subparsers.add_parser("list-incidents", help="List incidents")
    list_parser.add_argument(
        "--status",
        choices=["triggered", "acknowledged", "resolved"],
        help="Filter by status",
    )

    create_parser = subparsers.add_parser("create-incident", help="Create an incident")
    create_parser.add_argument("--service-id", required=True, help="PagerDuty service ID")
    create_parser.add_argument("--title", required=True, help="Incident title")

    ack_parser = subparsers.add_parser("acknowledge", help="Acknowledge an incident")
    ack_parser.add_argument("--incident-id", required=True, help="Incident ID")

    resolve_parser = subparsers.add_parser("resolve", help="Resolve an incident")
    resolve_parser.add_argument("--incident-id", required=True, help="Incident ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = PagerDutyClient()

    if args.command == "list-incidents":
        result = client.list_incidents(status=getattr(args, "status", None))
    elif args.command == "create-incident":
        result = client.create_incident(args.service_id, args.title)
    elif args.command == "acknowledge":
        result = client.acknowledge(args.incident_id)
    elif args.command == "resolve":
        result = client.resolve(args.incident_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

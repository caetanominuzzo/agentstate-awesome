#!/usr/bin/env python3
"""Grafana CLI for managing dashboards, alerts, and datasource queries."""
import argparse
import json
import os
import sys
import requests


class GrafanaClient:
    """Client for Grafana API interactions."""

    def __init__(self):
        self.grafana_url = os.environ.get("GRAFANA_URL", "").rstrip("/")
        self.api_key = os.environ.get("GRAFANA_API_KEY", "")
        if not self.grafana_url or not self.api_key:
            print(
                '{"error": "GRAFANA_URL and GRAFANA_API_KEY environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"{self.grafana_url}/api"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_dashboards(self):
        """List all dashboards."""
        try:
            response = requests.get(
                f"{self.base_url}/search",
                headers=self.headers,
                params={"type": "dash-db"},
                timeout=30,
            )
            response.raise_for_status()
            return {"dashboards": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_dashboard(self, uid):
        """Get a dashboard by UID."""
        try:
            response = requests.get(
                f"{self.base_url}/dashboards/uid/{uid}",
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

    def list_alerts(self):
        """List all alert rules."""
        try:
            response = requests.get(
                f"{self.base_url}/alertmanager/grafana/api/v2/alerts",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return {"alerts": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def query_datasource(self, datasource_id, query_json):
        """Query a datasource with a raw query."""
        try:
            query_data = json.loads(query_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --query-json: {str(e)}"}

        payload = {
            "queries": [
                {
                    "datasourceId": int(datasource_id),
                    **query_data,
                }
            ],
            "from": "now-1h",
            "to": "now",
        }

        try:
            response = requests.post(
                f"{self.base_url}/ds/query",
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
    parser = argparse.ArgumentParser(description="Grafana CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-dashboards", help="List dashboards")

    get_parser = subparsers.add_parser("get-dashboard", help="Get dashboard by UID")
    get_parser.add_argument("--uid", required=True, help="Dashboard UID")

    subparsers.add_parser("list-alerts", help="List alert rules")

    query_parser = subparsers.add_parser(
        "query-datasource", help="Query a datasource"
    )
    query_parser.add_argument(
        "--datasource-id", required=True, help="Datasource ID"
    )
    query_parser.add_argument(
        "--query-json", required=True, help="Query payload as JSON string"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GrafanaClient()

    if args.command == "list-dashboards":
        result = client.list_dashboards()
    elif args.command == "get-dashboard":
        result = client.get_dashboard(args.uid)
    elif args.command == "list-alerts":
        result = client.list_alerts()
    elif args.command == "query-datasource":
        result = client.query_datasource(args.datasource_id, args.query_json)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

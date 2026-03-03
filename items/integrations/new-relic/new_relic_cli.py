#!/usr/bin/env python3
"""New Relic CLI for querying NRQL, listing applications, and managing alerts."""
import argparse
import json
import os
import sys
import requests


class NewRelicClient:
    """Client for New Relic API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("NEW_RELIC_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "NEW_RELIC_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.account_id = os.environ.get("NEW_RELIC_ACCOUNT_ID", "")
        if not self.account_id:
            print(
                '{"error": "NEW_RELIC_ACCOUNT_ID environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.rest_url = "https://api.newrelic.com/v2"
        self.graphql_url = "https://api.newrelic.com/graphql"
        self.headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def query_nrql(self, nrql):
        """Execute a NRQL query via NerdGraph."""
        query = """
        {
          actor {
            account(id: %s) {
              nrql(query: "%s") {
                results
              }
            }
          }
        }
        """ % (self.account_id, nrql.replace('"', '\\"'))

        try:
            response = requests.post(
                self.graphql_url,
                headers=self.headers,
                json={"query": query},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_applications(self):
        """List all APM applications."""
        try:
            response = requests.get(
                f"{self.rest_url}/applications.json",
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

    def get_application(self, app_id):
        """Get details of an application."""
        try:
            response = requests.get(
                f"{self.rest_url}/applications/{app_id}.json",
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

    def list_alert_policies(self):
        """List all alert policies."""
        try:
            response = requests.get(
                f"{self.rest_url}/alerts_policies.json",
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
    parser = argparse.ArgumentParser(description="New Relic CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    nrql_parser = subparsers.add_parser("query-nrql", help="Execute a NRQL query")
    nrql_parser.add_argument("--nrql", required=True, help="NRQL query string")

    subparsers.add_parser("list-applications", help="List all APM applications")

    app_parser = subparsers.add_parser(
        "get-application", help="Get application details"
    )
    app_parser.add_argument("--app-id", required=True, help="Application ID")

    subparsers.add_parser("list-alert-policies", help="List all alert policies")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = NewRelicClient()

    if args.command == "query-nrql":
        result = client.query_nrql(args.nrql)
    elif args.command == "list-applications":
        result = client.list_applications()
    elif args.command == "get-application":
        result = client.get_application(args.app_id)
    elif args.command == "list-alert-policies":
        result = client.list_alert_policies()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

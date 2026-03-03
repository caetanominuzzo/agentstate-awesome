#!/usr/bin/env python3
"""Salesforce CLI for querying and managing records via SOQL and REST API."""
import argparse
import json
import os
import sys
import requests


class SalesforceClient:
    """Client for Salesforce API interactions."""

    def __init__(self):
        self.instance_url = os.environ.get("SALESFORCE_INSTANCE_URL", "").rstrip("/")
        self.access_token = os.environ.get("SALESFORCE_ACCESS_TOKEN", "")
        if not self.instance_url or not self.access_token:
            print(
                '{"error": "SALESFORCE_INSTANCE_URL and SALESFORCE_ACCESS_TOKEN environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"{self.instance_url}/services/data/v59.0"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def query(self, soql):
        """Execute a SOQL query."""
        try:
            response = requests.get(
                f"{self.base_url}/query",
                headers=self.headers,
                params={"q": soql},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_record(self, sobject, record_id):
        """Get a specific record by sObject type and ID."""
        try:
            response = requests.get(
                f"{self.base_url}/sobjects/{sobject}/{record_id}",
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

    def create_record(self, sobject, data_json):
        """Create a new record."""
        try:
            data = json.loads(data_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --data-json: {str(e)}"}

        try:
            response = requests.post(
                f"{self.base_url}/sobjects/{sobject}",
                headers=self.headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def update_record(self, sobject, record_id, data_json):
        """Update an existing record."""
        try:
            data = json.loads(data_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in --data-json: {str(e)}"}

        try:
            response = requests.patch(
                f"{self.base_url}/sobjects/{sobject}/{record_id}",
                headers=self.headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "sobject": sobject, "id": record_id}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def describe(self, sobject):
        """Describe an sObject's metadata."""
        try:
            response = requests.get(
                f"{self.base_url}/sobjects/{sobject}/describe",
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
    parser = argparse.ArgumentParser(description="Salesforce CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    query_parser = subparsers.add_parser("query", help="Execute a SOQL query")
    query_parser.add_argument("--soql", required=True, help="SOQL query string")

    get_parser = subparsers.add_parser("get-record", help="Get a record")
    get_parser.add_argument("--sobject", required=True, help="sObject type (e.g., Account)")
    get_parser.add_argument("--id", required=True, help="Record ID")

    create_parser = subparsers.add_parser("create-record", help="Create a record")
    create_parser.add_argument("--sobject", required=True, help="sObject type")
    create_parser.add_argument(
        "--data-json", required=True, help="Record data as JSON string"
    )

    update_parser = subparsers.add_parser("update-record", help="Update a record")
    update_parser.add_argument("--sobject", required=True, help="sObject type")
    update_parser.add_argument("--id", required=True, help="Record ID")
    update_parser.add_argument(
        "--data-json", required=True, help="Fields to update as JSON string"
    )

    desc_parser = subparsers.add_parser("describe", help="Describe an sObject")
    desc_parser.add_argument("--sobject", required=True, help="sObject type")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SalesforceClient()

    if args.command == "query":
        result = client.query(args.soql)
    elif args.command == "get-record":
        result = client.get_record(args.sobject, args.id)
    elif args.command == "create-record":
        result = client.create_record(args.sobject, args.data_json)
    elif args.command == "update-record":
        result = client.update_record(args.sobject, args.id, args.data_json)
    elif args.command == "describe":
        result = client.describe(args.sobject)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

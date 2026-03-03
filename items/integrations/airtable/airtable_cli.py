#!/usr/bin/env python3
"""Airtable CLI for listing, creating, updating, and retrieving records."""
import argparse
import json
import os
import sys
import requests


class AirtableClient:
    """Client for Airtable API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("AIRTABLE_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "AIRTABLE_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_id = os.environ.get("AIRTABLE_BASE_ID", "")
        if not self.base_id:
            print(
                '{"error": "AIRTABLE_BASE_ID environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list_records(self, table):
        """List records from a table."""
        try:
            response = requests.get(
                f"{self.base_url}/{table}",
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

    def get_record(self, table, record_id):
        """Get a single record by ID."""
        try:
            response = requests.get(
                f"{self.base_url}/{table}/{record_id}",
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

    def create_record(self, table, fields):
        """Create a new record in a table."""
        payload = {"fields": fields}
        try:
            response = requests.post(
                f"{self.base_url}/{table}",
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

    def update_record(self, table, record_id, fields):
        """Update an existing record."""
        payload = {"fields": fields}
        try:
            response = requests.patch(
                f"{self.base_url}/{table}/{record_id}",
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
    parser = argparse.ArgumentParser(description="Airtable CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    list_parser = subparsers.add_parser("list-records", help="List records from a table")
    list_parser.add_argument("--table", required=True, help="Table name")

    get_parser = subparsers.add_parser("get-record", help="Get a single record")
    get_parser.add_argument("--table", required=True, help="Table name")
    get_parser.add_argument("--record-id", required=True, help="Record ID")

    create_parser = subparsers.add_parser("create-record", help="Create a new record")
    create_parser.add_argument("--table", required=True, help="Table name")
    create_parser.add_argument(
        "--fields-json", required=True, help="JSON string of field values"
    )

    update_parser = subparsers.add_parser("update-record", help="Update a record")
    update_parser.add_argument("--table", required=True, help="Table name")
    update_parser.add_argument("--record-id", required=True, help="Record ID")
    update_parser.add_argument(
        "--fields-json", required=True, help="JSON string of field values"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = AirtableClient()

    if args.command == "list-records":
        result = client.list_records(args.table)
    elif args.command == "get-record":
        result = client.get_record(args.table, args.record_id)
    elif args.command == "create-record":
        fields = json.loads(args.fields_json)
        result = client.create_record(args.table, fields)
    elif args.command == "update-record":
        fields = json.loads(args.fields_json)
        result = client.update_record(args.table, args.record_id, fields)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

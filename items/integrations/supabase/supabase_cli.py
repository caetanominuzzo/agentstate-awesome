#!/usr/bin/env python3
"""Supabase CLI for querying, inserting, and updating data via PostgREST."""
import argparse
import json
import os
import sys
import requests


class SupabaseClient:
    """Client for Supabase PostgREST API interactions."""

    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL", "").rstrip("/")
        if not self.url:
            print(
                '{"error": "SUPABASE_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.key = os.environ.get("SUPABASE_KEY", "")
        if not self.key:
            print(
                '{"error": "SUPABASE_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.rest_url = f"{self.url}/rest/v1"
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def query(self, table, select="*", filter_str=None):
        """Query rows from a table."""
        params = {"select": select}
        if filter_str:
            # Parse filter in format "column=eq.value"
            parts = filter_str.split("=", 1)
            if len(parts) == 2:
                params[parts[0]] = parts[1]

        try:
            response = requests.get(
                f"{self.rest_url}/{table}",
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

    def insert(self, table, data_json):
        """Insert a row into a table."""
        try:
            data = json.loads(data_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid data JSON: {e}"}

        try:
            response = requests.post(
                f"{self.rest_url}/{table}",
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

    def update(self, table, data_json, filter_str):
        """Update rows in a table matching a filter."""
        try:
            data = json.loads(data_json)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid data JSON: {e}"}

        params = {}
        if filter_str:
            parts = filter_str.split("=", 1)
            if len(parts) == 2:
                params[parts[0]] = parts[1]

        try:
            response = requests.patch(
                f"{self.rest_url}/{table}",
                headers=self.headers,
                json=data,
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

    def list_tables(self):
        """List all tables by querying the pg_tables or information_schema via RPC."""
        # Use Supabase's RPC or a direct query to list tables
        # We query the information_schema via a PostgREST endpoint if available
        try:
            # Try the Supabase REST introspection endpoint
            response = requests.get(
                f"{self.rest_url}/",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            # The root endpoint returns the OpenAPI schema with table definitions
            data = response.json()
            if "definitions" in data:
                tables = list(data["definitions"].keys())
                return {"tables": tables}
            if "paths" in data:
                tables = [
                    path.lstrip("/")
                    for path in data["paths"].keys()
                    if path != "/"
                ]
                return {"tables": tables}
            return data
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="Supabase CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    query_parser = subparsers.add_parser("query", help="Query rows from a table")
    query_parser.add_argument("--table", required=True, help="Table name")
    query_parser.add_argument(
        "--select", default="*", help="Columns to select (default: *)"
    )
    query_parser.add_argument(
        "--filter",
        help="Filter in PostgREST format (e.g., 'id=eq.5' or 'name=ilike.*john*')",
    )

    insert_parser = subparsers.add_parser("insert", help="Insert a row")
    insert_parser.add_argument("--table", required=True, help="Table name")
    insert_parser.add_argument(
        "--data-json", required=True, help="JSON object to insert"
    )

    update_parser = subparsers.add_parser("update", help="Update rows")
    update_parser.add_argument("--table", required=True, help="Table name")
    update_parser.add_argument(
        "--data-json", required=True, help="JSON object with fields to update"
    )
    update_parser.add_argument(
        "--filter", required=True,
        help="Filter in PostgREST format (e.g., 'id=eq.5')",
    )

    subparsers.add_parser("list-tables", help="List all tables")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SupabaseClient()

    if args.command == "query":
        result = client.query(
            args.table, select=args.select,
            filter_str=getattr(args, "filter", None),
        )
    elif args.command == "insert":
        result = client.insert(args.table, args.data_json)
    elif args.command == "update":
        result = client.update(args.table, args.data_json, args.filter)
    elif args.command == "list-tables":
        result = client.list_tables()

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

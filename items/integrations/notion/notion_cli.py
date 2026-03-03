#!/usr/bin/env python3
"""Notion CLI for querying and managing pages and databases."""
import argparse
import json
import os
import sys
import requests


class NotionClient:
    """Client for Notion API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("NOTION_KEY")
        if not self.api_key:
            print(
                '{"error": "NOTION_KEY environment variable not set"}',
                file=sys.stderr,
            )
            sys.exit(1)

        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def search(self, query, filter_type=None, page_size=20):
        """Search across all pages and databases the integration has access to.

        Args:
            query: Search query string.
            filter_type: Optional filter - "page" or "database".
            page_size: Number of results to return (default: 20, max: 100).

        Returns:
            dict with search results or error.
        """
        payload = {
            "query": query,
            "page_size": page_size,
        }
        if filter_type:
            payload["filter"] = {"value": filter_type, "property": "object"}

        try:
            response = requests.post(
                f"{self.base_url}/search",
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

    def get_page(self, page_id):
        """Retrieve a Notion page by ID.

        Args:
            page_id: The Notion page ID (UUID, with or without dashes).

        Returns:
            dict with page properties or error.
        """
        try:
            response = requests.get(
                f"{self.base_url}/pages/{page_id}",
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

    def get_database(self, database_id):
        """Retrieve a Notion database schema by ID.

        Args:
            database_id: The Notion database ID (UUID, with or without dashes).

        Returns:
            dict with database schema/properties or error.
        """
        try:
            response = requests.get(
                f"{self.base_url}/databases/{database_id}",
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

    def query_database(self, database_id, filter_dict=None, page_size=100):
        """Query a Notion database with optional filters.

        Args:
            database_id: The Notion database ID.
            filter_dict: Optional Notion filter object (see Notion API docs).
            page_size: Number of results to return (default: 100, max: 100).

        Returns:
            dict with query results or error.
        """
        payload = {"page_size": page_size}
        if filter_dict:
            payload["filter"] = filter_dict

        try:
            response = requests.post(
                f"{self.base_url}/databases/{database_id}/query",
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
    parser = argparse.ArgumentParser(description="Notion CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # search command
    search_parser = subparsers.add_parser(
        "search", help="Search pages and databases"
    )
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument(
        "--filter-type",
        choices=["page", "database"],
        default=None,
        help="Filter results by type",
    )
    search_parser.add_argument(
        "--page-size",
        type=int,
        default=20,
        help="Number of results (default: 20, max: 100)",
    )

    # get-page command
    page_parser = subparsers.add_parser("get-page", help="Get a page by ID")
    page_parser.add_argument("--page-id", required=True, help="Notion page ID")

    # get-database command
    db_parser = subparsers.add_parser(
        "get-database", help="Get a database schema by ID"
    )
    db_parser.add_argument(
        "--database-id", required=True, help="Notion database ID"
    )

    # query-database command
    query_parser = subparsers.add_parser(
        "query-database", help="Query a database with optional filters"
    )
    query_parser.add_argument(
        "--database-id", required=True, help="Notion database ID"
    )
    query_parser.add_argument(
        "--filter",
        default=None,
        help="Notion filter as JSON string (see Notion API docs for filter format)",
    )
    query_parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Number of results (default: 100, max: 100)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = NotionClient()

    if args.command == "search":
        result = client.search(
            args.query, filter_type=args.filter_type, page_size=args.page_size
        )
    elif args.command == "get-page":
        result = client.get_page(args.page_id)
    elif args.command == "get-database":
        result = client.get_database(args.database_id)
    elif args.command == "query-database":
        filter_dict = None
        if args.filter:
            try:
                filter_dict = json.loads(args.filter)
            except json.JSONDecodeError as e:
                print(
                    json.dumps({"error": f"Invalid JSON for --filter: {e}"}),
                    file=sys.stderr,
                )
                sys.exit(1)
        result = client.query_database(
            args.database_id, filter_dict=filter_dict, page_size=args.page_size
        )

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

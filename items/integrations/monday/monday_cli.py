#!/usr/bin/env python3
"""Monday.com CLI for managing boards, items, and groups."""
import argparse
import json
import os
import sys
import requests


class MondayClient:
    """Client for Monday.com GraphQL API interactions."""

    def __init__(self):
        self.api_token = os.environ.get("MONDAY_API_TOKEN", "")
        if not self.api_token:
            print(
                '{"error": "MONDAY_API_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json",
        }

    def _graphql(self, query, variables=None):
        """Execute a GraphQL query."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        try:
            response = requests.post(
                self.base_url,
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

    def list_boards(self):
        """List all boards."""
        query = """
        query {
          boards(limit: 50) {
            id
            name
            state
            board_kind
            description
          }
        }
        """
        return self._graphql(query)

    def get_board(self, board_id):
        """Get board details."""
        query = """
        query ($boardId: [ID!]!) {
          boards(ids: $boardId) {
            id
            name
            state
            board_kind
            description
            columns {
              id
              title
              type
            }
            groups {
              id
              title
            }
          }
        }
        """
        return self._graphql(query, {"boardId": [board_id]})

    def list_items(self, board_id):
        """List items on a board."""
        query = """
        query ($boardId: [ID!]!) {
          boards(ids: $boardId) {
            items_page(limit: 50) {
              items {
                id
                name
                state
                group {
                  id
                  title
                }
                column_values {
                  id
                  text
                  value
                }
              }
            }
          }
        }
        """
        return self._graphql(query, {"boardId": [board_id]})

    def create_item(self, board_id, group_id, name):
        """Create a new item on a board."""
        query = """
        mutation ($boardId: ID!, $groupId: String!, $itemName: String!) {
          create_item(board_id: $boardId, group_id: $groupId, item_name: $itemName) {
            id
            name
          }
        }
        """
        return self._graphql(
            query,
            {"boardId": board_id, "groupId": group_id, "itemName": name},
        )

    def update_item(self, item_id, board_id, column_values):
        """Update an item's column values."""
        query = """
        mutation ($boardId: ID!, $itemId: ID!, $columnValues: JSON!) {
          change_multiple_column_values(
            board_id: $boardId,
            item_id: $itemId,
            column_values: $columnValues
          ) {
            id
            name
          }
        }
        """
        return self._graphql(
            query,
            {
                "boardId": board_id,
                "itemId": item_id,
                "columnValues": json.dumps(column_values),
            },
        )


def main():
    parser = argparse.ArgumentParser(description="Monday.com CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-boards", help="List all boards")

    board_parser = subparsers.add_parser("get-board", help="Get board details")
    board_parser.add_argument("--board-id", required=True, help="Board ID")

    items_parser = subparsers.add_parser("list-items", help="List items on a board")
    items_parser.add_argument("--board-id", required=True, help="Board ID")

    create_parser = subparsers.add_parser("create-item", help="Create a new item")
    create_parser.add_argument("--board-id", required=True, help="Board ID")
    create_parser.add_argument("--group-id", required=True, help="Group ID")
    create_parser.add_argument("--name", required=True, help="Item name")

    update_parser = subparsers.add_parser("update-item", help="Update an item")
    update_parser.add_argument("--item-id", required=True, help="Item ID")
    update_parser.add_argument("--board-id", required=True, help="Board ID")
    update_parser.add_argument(
        "--column-values-json",
        required=True,
        help='JSON object of column values (e.g., \'{"status": {"label": "Done"}}\')',
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = MondayClient()

    if args.command == "list-boards":
        result = client.list_boards()
    elif args.command == "get-board":
        result = client.get_board(args.board_id)
    elif args.command == "list-items":
        result = client.list_items(args.board_id)
    elif args.command == "create-item":
        result = client.create_item(args.board_id, args.group_id, args.name)
    elif args.command == "update-item":
        column_values = json.loads(args.column_values_json)
        result = client.update_item(args.item_id, args.board_id, column_values)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

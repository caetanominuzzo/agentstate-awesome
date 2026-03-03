#!/usr/bin/env python3
"""Trello CLI for managing boards, lists, and cards."""
import argparse
import json
import os
import sys
import requests


class TrelloClient:
    """Client for Trello API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("TRELLO_API_KEY", "")
        self.token = os.environ.get("TRELLO_TOKEN", "")
        if not self.api_key or not self.token:
            print(
                '{"error": "TRELLO_API_KEY and TRELLO_TOKEN environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.trello.com/1"
        self.auth_params = {"key": self.api_key, "token": self.token}

    def list_boards(self):
        """List all boards for the authenticated user."""
        try:
            response = requests.get(
                f"{self.base_url}/members/me/boards",
                params=self.auth_params,
                timeout=30,
            )
            response.raise_for_status()
            return {"boards": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_lists(self, board_id):
        """List all lists on a board."""
        try:
            response = requests.get(
                f"{self.base_url}/boards/{board_id}/lists",
                params=self.auth_params,
                timeout=30,
            )
            response.raise_for_status()
            return {"lists": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_cards(self, list_id):
        """List all cards in a list."""
        try:
            response = requests.get(
                f"{self.base_url}/lists/{list_id}/cards",
                params=self.auth_params,
                timeout=30,
            )
            response.raise_for_status()
            return {"cards": response.json()}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_card(self, list_id, name, desc=""):
        """Create a new card in a list."""
        params = {**self.auth_params, "idList": list_id, "name": name, "desc": desc}

        try:
            response = requests.post(
                f"{self.base_url}/cards",
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

    def update_card(self, card_id, name=None, desc=None, closed=None):
        """Update an existing card."""
        params = {**self.auth_params}
        if name is not None:
            params["name"] = name
        if desc is not None:
            params["desc"] = desc
        if closed is not None:
            params["closed"] = closed

        try:
            response = requests.put(
                f"{self.base_url}/cards/{card_id}",
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


def main():
    parser = argparse.ArgumentParser(description="Trello CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-boards", help="List boards")

    lists_parser = subparsers.add_parser("list-lists", help="List lists on a board")
    lists_parser.add_argument("--board-id", required=True, help="Board ID")

    cards_parser = subparsers.add_parser("list-cards", help="List cards in a list")
    cards_parser.add_argument("--list-id", required=True, help="List ID")

    create_parser = subparsers.add_parser("create-card", help="Create a card")
    create_parser.add_argument("--list-id", required=True, help="List ID")
    create_parser.add_argument("--name", required=True, help="Card name")
    create_parser.add_argument("--desc", default="", help="Card description")

    update_parser = subparsers.add_parser("update-card", help="Update a card")
    update_parser.add_argument("--card-id", required=True, help="Card ID")
    update_parser.add_argument("--name", help="New card name")
    update_parser.add_argument("--desc", help="New card description")
    update_parser.add_argument(
        "--closed", choices=["true", "false"], help="Archive or unarchive card"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = TrelloClient()

    if args.command == "list-boards":
        result = client.list_boards()
    elif args.command == "list-lists":
        result = client.list_lists(args.board_id)
    elif args.command == "list-cards":
        result = client.list_cards(args.list_id)
    elif args.command == "create-card":
        result = client.create_card(args.list_id, args.name, args.desc)
    elif args.command == "update-card":
        closed = None
        if args.closed is not None:
            closed = args.closed
        result = client.update_card(args.card_id, args.name, args.desc, closed)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

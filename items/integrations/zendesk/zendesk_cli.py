#!/usr/bin/env python3
"""Zendesk CLI for managing tickets and searching support data."""
import argparse
import json
import os
import sys
import requests


class ZendeskClient:
    """Client for Zendesk API interactions."""

    def __init__(self):
        self.subdomain = os.environ.get("ZENDESK_SUBDOMAIN", "")
        self.email = os.environ.get("ZENDESK_EMAIL", "")
        self.api_token = os.environ.get("ZENDESK_API_TOKEN", "")
        if not self.subdomain or not self.email or not self.api_token:
            print(
                '{"error": "ZENDESK_SUBDOMAIN, ZENDESK_EMAIL, and ZENDESK_API_TOKEN environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"https://{self.subdomain}.zendesk.com/api/v2"
        self.auth = (f"{self.email}/token", self.api_token)

    def list_tickets(self, status=None):
        """List tickets, optionally filtered by status."""
        try:
            params = {}
            if status:
                params["status"] = status
            response = requests.get(
                f"{self.base_url}/tickets.json",
                auth=self.auth,
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

    def create_ticket(self, subject, description, priority="normal"):
        """Create a new ticket."""
        payload = {
            "ticket": {
                "subject": subject,
                "description": description,
                "priority": priority,
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/tickets.json",
                auth=self.auth,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def update_ticket(self, ticket_id, status=None, comment=None):
        """Update a ticket's status or add a comment."""
        ticket_data = {}
        if status:
            ticket_data["status"] = status
        if comment:
            ticket_data["comment"] = {"body": comment, "public": True}
        payload = {"ticket": ticket_data}

        try:
            response = requests.put(
                f"{self.base_url}/tickets/{ticket_id}.json",
                auth=self.auth,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_ticket(self, ticket_id):
        """Get a ticket by ID."""
        try:
            response = requests.get(
                f"{self.base_url}/tickets/{ticket_id}.json",
                auth=self.auth,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def search(self, query):
        """Search Zendesk."""
        try:
            response = requests.get(
                f"{self.base_url}/search.json",
                auth=self.auth,
                params={"query": query},
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
    parser = argparse.ArgumentParser(description="Zendesk CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    list_parser = subparsers.add_parser("list-tickets", help="List tickets")
    list_parser.add_argument(
        "--status",
        help="Filter by status: new, open, pending, hold, solved, closed",
    )

    create_parser = subparsers.add_parser("create-ticket", help="Create a ticket")
    create_parser.add_argument("--subject", required=True, help="Ticket subject")
    create_parser.add_argument(
        "--description", required=True, help="Ticket description"
    )
    create_parser.add_argument(
        "--priority",
        default="normal",
        choices=["low", "normal", "high", "urgent"],
        help="Ticket priority (default: normal)",
    )

    update_parser = subparsers.add_parser("update-ticket", help="Update a ticket")
    update_parser.add_argument("--ticket-id", required=True, help="Ticket ID")
    update_parser.add_argument("--status", help="New ticket status")
    update_parser.add_argument("--comment", help="Comment to add")

    get_parser = subparsers.add_parser("get-ticket", help="Get ticket details")
    get_parser.add_argument("--ticket-id", required=True, help="Ticket ID")

    search_parser = subparsers.add_parser("search", help="Search Zendesk")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = ZendeskClient()

    if args.command == "list-tickets":
        result = client.list_tickets(args.status)
    elif args.command == "create-ticket":
        result = client.create_ticket(args.subject, args.description, args.priority)
    elif args.command == "update-ticket":
        result = client.update_ticket(args.ticket_id, args.status, args.comment)
    elif args.command == "get-ticket":
        result = client.get_ticket(args.ticket_id)
    elif args.command == "search":
        result = client.search(args.query)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

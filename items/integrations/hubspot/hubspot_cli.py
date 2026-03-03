#!/usr/bin/env python3
"""HubSpot CLI for managing contacts and deals."""
import argparse
import json
import os
import sys
import requests


class HubSpotClient:
    """Client for HubSpot API interactions."""

    def __init__(self):
        self.token = os.environ.get("HUBSPOT_ACCESS_TOKEN", "")
        if not self.token:
            print(
                '{"error": "HUBSPOT_ACCESS_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.hubapi.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def list_contacts(self, limit=10):
        """List contacts."""
        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/contacts",
                headers=self.headers,
                params={"limit": limit},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_contact(self, contact_id):
        """Get a contact by ID."""
        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/contacts/{contact_id}",
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

    def create_contact(self, email, firstname="", lastname=""):
        """Create a new contact."""
        payload = {
            "properties": {
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/crm/v3/objects/contacts",
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

    def list_deals(self, limit=10):
        """List deals."""
        try:
            response = requests.get(
                f"{self.base_url}/crm/v3/objects/deals",
                headers=self.headers,
                params={"limit": limit},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_deal(self, name, pipeline="default", stage=""):
        """Create a new deal."""
        properties = {"dealname": name, "pipeline": pipeline}
        if stage:
            properties["dealstage"] = stage
        payload = {"properties": properties}

        try:
            response = requests.post(
                f"{self.base_url}/crm/v3/objects/deals",
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
    parser = argparse.ArgumentParser(description="HubSpot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    contacts_parser = subparsers.add_parser("list-contacts", help="List contacts")
    contacts_parser.add_argument(
        "--limit", type=int, default=10, help="Max results (default: 10)"
    )

    get_parser = subparsers.add_parser("get-contact", help="Get contact details")
    get_parser.add_argument("--contact-id", required=True, help="Contact ID")

    create_contact_parser = subparsers.add_parser(
        "create-contact", help="Create a contact"
    )
    create_contact_parser.add_argument("--email", required=True, help="Email address")
    create_contact_parser.add_argument("--firstname", default="", help="First name")
    create_contact_parser.add_argument("--lastname", default="", help="Last name")

    deals_parser = subparsers.add_parser("list-deals", help="List deals")
    deals_parser.add_argument(
        "--limit", type=int, default=10, help="Max results (default: 10)"
    )

    create_deal_parser = subparsers.add_parser("create-deal", help="Create a deal")
    create_deal_parser.add_argument("--name", required=True, help="Deal name")
    create_deal_parser.add_argument(
        "--pipeline", default="default", help="Pipeline ID (default: default)"
    )
    create_deal_parser.add_argument("--stage", default="", help="Deal stage ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = HubSpotClient()

    if args.command == "list-contacts":
        result = client.list_contacts(args.limit)
    elif args.command == "get-contact":
        result = client.get_contact(args.contact_id)
    elif args.command == "create-contact":
        result = client.create_contact(args.email, args.firstname, args.lastname)
    elif args.command == "list-deals":
        result = client.list_deals(args.limit)
    elif args.command == "create-deal":
        result = client.create_deal(args.name, args.pipeline, args.stage)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

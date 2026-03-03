#!/usr/bin/env python3
"""Cloudflare CLI for managing zones, DNS records, and Workers."""
import argparse
import json
import os
import sys
import requests


class CloudflareClient:
    """Client for Cloudflare v4 API interactions."""

    def __init__(self):
        self.token = os.environ.get("CLOUDFLARE_API_TOKEN", "")
        if not self.token:
            print(
                '{"error": "CLOUDFLARE_API_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def list_zones(self):
        """List all zones (domains)."""
        try:
            response = requests.get(
                f"{self.base_url}/zones",
                headers=self.headers,
                params={"per_page": 50},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_dns_records(self, zone_id):
        """List DNS records for a zone."""
        try:
            response = requests.get(
                f"{self.base_url}/zones/{zone_id}/dns_records",
                headers=self.headers,
                params={"per_page": 100},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def create_dns_record(self, zone_id, record_type, name, content):
        """Create a DNS record in a zone."""
        payload = {
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": 1,  # Auto TTL
        }

        try:
            response = requests.post(
                f"{self.base_url}/zones/{zone_id}/dns_records",
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

    def list_workers(self):
        """List all Workers scripts."""
        # First get the account ID
        try:
            accounts_resp = requests.get(
                f"{self.base_url}/accounts",
                headers=self.headers,
                params={"per_page": 1},
                timeout=30,
            )
            accounts_resp.raise_for_status()
            accounts_data = accounts_resp.json()
            accounts = accounts_data.get("result", [])
            if not accounts:
                return {"error": "No accounts found for this token"}

            account_id = accounts[0]["id"]

            response = requests.get(
                f"{self.base_url}/accounts/{account_id}/workers/scripts",
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
    parser = argparse.ArgumentParser(description="Cloudflare CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-zones", help="List all zones")

    dns_list_parser = subparsers.add_parser(
        "list-dns-records", help="List DNS records for a zone"
    )
    dns_list_parser.add_argument("--zone-id", required=True, help="Zone ID")

    dns_create_parser = subparsers.add_parser(
        "create-dns-record", help="Create a DNS record"
    )
    dns_create_parser.add_argument("--zone-id", required=True, help="Zone ID")
    dns_create_parser.add_argument(
        "--type", required=True, help="Record type (A, AAAA, CNAME, TXT, etc.)"
    )
    dns_create_parser.add_argument("--name", required=True, help="Record name")
    dns_create_parser.add_argument("--content", required=True, help="Record content")

    subparsers.add_parser("list-workers", help="List Workers scripts")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = CloudflareClient()

    if args.command == "list-zones":
        result = client.list_zones()
    elif args.command == "list-dns-records":
        result = client.list_dns_records(args.zone_id)
    elif args.command == "create-dns-record":
        result = client.create_dns_record(
            args.zone_id, args.type, args.name, args.content
        )
    elif args.command == "list-workers":
        result = client.list_workers()

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Netlify CLI for managing sites and deploys."""
import argparse
import json
import os
import sys
import requests


class NetlifyClient:
    """Client for Netlify REST API interactions."""

    def __init__(self):
        self.token = os.environ.get("NETLIFY_AUTH_TOKEN", "")
        if not self.token:
            print(
                '{"error": "NETLIFY_AUTH_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.netlify.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def list_sites(self):
        """List all sites."""
        try:
            response = requests.get(
                f"{self.base_url}/sites",
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

    def get_site(self, site_id):
        """Get details of a specific site."""
        try:
            response = requests.get(
                f"{self.base_url}/sites/{site_id}",
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

    def list_deploys(self, site_id):
        """List deploys for a site."""
        try:
            response = requests.get(
                f"{self.base_url}/sites/{site_id}/deploys",
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

    def trigger_deploy(self, site_id):
        """Trigger a new deploy for a site via build hook."""
        try:
            response = requests.post(
                f"{self.base_url}/sites/{site_id}/builds",
                headers=self.headers,
                json={},
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
    parser = argparse.ArgumentParser(description="Netlify CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-sites", help="List all sites")

    get_parser = subparsers.add_parser("get-site", help="Get site details")
    get_parser.add_argument("--site-id", required=True, help="Netlify site ID or name")

    deploys_parser = subparsers.add_parser("list-deploys", help="List site deploys")
    deploys_parser.add_argument(
        "--site-id", required=True, help="Netlify site ID or name"
    )

    trigger_parser = subparsers.add_parser(
        "trigger-deploy", help="Trigger a new deploy"
    )
    trigger_parser.add_argument(
        "--site-id", required=True, help="Netlify site ID or name"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = NetlifyClient()

    if args.command == "list-sites":
        result = client.list_sites()
    elif args.command == "get-site":
        result = client.get_site(args.site_id)
    elif args.command == "list-deploys":
        result = client.list_deploys(args.site_id)
    elif args.command == "trigger-deploy":
        result = client.trigger_deploy(args.site_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

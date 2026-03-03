#!/usr/bin/env python3
"""Fly.io CLI for managing apps and machines."""
import argparse
import json
import os
import sys
import requests


class FlyIoClient:
    """Client for Fly.io Machines API interactions."""

    def __init__(self):
        self.token = os.environ.get("FLY_API_TOKEN", "")
        if not self.token:
            print(
                '{"error": "FLY_API_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.machines.dev/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def list_apps(self):
        """List all apps."""
        try:
            response = requests.get(
                f"{self.base_url}/apps",
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

    def get_app(self, app_name):
        """Get app details."""
        try:
            response = requests.get(
                f"{self.base_url}/apps/{app_name}",
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

    def list_machines(self, app_name):
        """List machines for an app."""
        try:
            response = requests.get(
                f"{self.base_url}/apps/{app_name}/machines",
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

    def get_machine(self, app_name, machine_id):
        """Get machine details."""
        try:
            response = requests.get(
                f"{self.base_url}/apps/{app_name}/machines/{machine_id}",
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
    parser = argparse.ArgumentParser(description="Fly.io CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-apps", help="List all apps")

    app_parser = subparsers.add_parser("get-app", help="Get app details")
    app_parser.add_argument("--app-name", required=True, help="App name")

    machines_parser = subparsers.add_parser(
        "list-machines", help="List machines for an app"
    )
    machines_parser.add_argument("--app-name", required=True, help="App name")

    machine_parser = subparsers.add_parser(
        "get-machine", help="Get machine details"
    )
    machine_parser.add_argument("--app-name", required=True, help="App name")
    machine_parser.add_argument("--machine-id", required=True, help="Machine ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = FlyIoClient()

    if args.command == "list-apps":
        result = client.list_apps()
    elif args.command == "get-app":
        result = client.get_app(args.app_name)
    elif args.command == "list-machines":
        result = client.list_machines(args.app_name)
    elif args.command == "get-machine":
        result = client.get_machine(args.app_name, args.machine_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

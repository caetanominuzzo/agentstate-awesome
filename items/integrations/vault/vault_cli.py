#!/usr/bin/env python3
"""HashiCorp Vault CLI for reading, writing, listing, and deleting secrets."""
import argparse
import json
import os
import sys
import requests


class VaultClient:
    """Client for HashiCorp Vault API interactions."""

    def __init__(self):
        self.vault_addr = os.environ.get("VAULT_ADDR", "").rstrip("/")
        if not self.vault_addr:
            print(
                '{"error": "VAULT_ADDR environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.vault_token = os.environ.get("VAULT_TOKEN", "")
        if not self.vault_token:
            print(
                '{"error": "VAULT_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = f"{self.vault_addr}/v1"
        self.headers = {
            "X-Vault-Token": self.vault_token,
            "Content-Type": "application/json",
        }

    def read(self, path):
        """Read a secret at the given path."""
        try:
            response = requests.get(
                f"{self.base_url}/{path}",
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

    def write(self, path, data):
        """Write a secret at the given path."""
        try:
            response = requests.post(
                f"{self.base_url}/{path}",
                headers=self.headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()
            if response.text:
                return response.json()
            return {"success": True, "path": path}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_secrets(self, path):
        """List secrets at the given path."""
        try:
            response = requests.request(
                "LIST",
                f"{self.base_url}/{path}",
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

    def delete(self, path):
        """Delete a secret at the given path."""
        try:
            response = requests.delete(
                f"{self.base_url}/{path}",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return {"success": True, "path": path}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }


def main():
    parser = argparse.ArgumentParser(description="HashiCorp Vault CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    read_parser = subparsers.add_parser("read", help="Read a secret")
    read_parser.add_argument("--path", required=True, help="Secret path")

    write_parser = subparsers.add_parser("write", help="Write a secret")
    write_parser.add_argument("--path", required=True, help="Secret path")
    write_parser.add_argument(
        "--data-json", required=True, help="JSON object of data to write"
    )

    list_parser = subparsers.add_parser("list", help="List secrets")
    list_parser.add_argument("--path", required=True, help="Secret path")

    delete_parser = subparsers.add_parser("delete", help="Delete a secret")
    delete_parser.add_argument("--path", required=True, help="Secret path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = VaultClient()

    if args.command == "read":
        result = client.read(args.path)
    elif args.command == "write":
        data = json.loads(args.data_json)
        result = client.write(args.path, data)
    elif args.command == "list":
        result = client.list_secrets(args.path)
    elif args.command == "delete":
        result = client.delete(args.path)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

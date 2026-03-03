#!/usr/bin/env python3
"""Upstash CLI for interacting with Upstash Redis via the REST API."""
import argparse
import json
import os
import sys
import requests


class UpstashClient:
    """Client for Upstash Redis REST API interactions."""

    def __init__(self):
        self.url = os.environ.get("UPSTASH_REDIS_REST_URL", "").rstrip("/")
        if not self.url:
            print(
                '{"error": "UPSTASH_REDIS_REST_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.token = os.environ.get("UPSTASH_REDIS_REST_TOKEN", "")
        if not self.token:
            print(
                '{"error": "UPSTASH_REDIS_REST_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _execute(self, command):
        """Execute a Redis command via Upstash REST API."""
        try:
            response = requests.post(
                self.url,
                headers=self.headers,
                json=command,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get(self, key):
        """Get the value of a key."""
        return self._execute(["GET", key])

    def set(self, key, value, ex=None):
        """Set a key-value pair with optional expiry."""
        command = ["SET", key, value]
        if ex is not None:
            command.extend(["EX", str(ex)])
        return self._execute(command)

    def delete(self, key):
        """Delete a key."""
        return self._execute(["DEL", key])

    def keys(self, pattern="*"):
        """List keys matching a pattern."""
        return self._execute(["KEYS", pattern])

    def incr(self, key):
        """Increment a key's integer value."""
        return self._execute(["INCR", key])


def main():
    parser = argparse.ArgumentParser(description="Upstash CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    get_parser = subparsers.add_parser("get", help="Get a key's value")
    get_parser.add_argument("--key", required=True, help="Key name")

    set_parser = subparsers.add_parser("set", help="Set a key-value pair")
    set_parser.add_argument("--key", required=True, help="Key name")
    set_parser.add_argument("--value", required=True, help="Value to set")
    set_parser.add_argument(
        "--ex", type=int, help="Expiry time in seconds"
    )

    del_parser = subparsers.add_parser("del", help="Delete a key")
    del_parser.add_argument("--key", required=True, help="Key name")

    keys_parser = subparsers.add_parser("keys", help="List keys matching a pattern")
    keys_parser.add_argument(
        "--pattern", default="*", help="Glob pattern (default: *)"
    )

    incr_parser = subparsers.add_parser("incr", help="Increment a key")
    incr_parser.add_argument("--key", required=True, help="Key name")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = UpstashClient()

    if args.command == "get":
        result = client.get(args.key)
    elif args.command == "set":
        result = client.set(args.key, args.value, ex=getattr(args, "ex", None))
    elif args.command == "del":
        result = client.delete(args.key)
    elif args.command == "keys":
        result = client.keys(args.pattern)
    elif args.command == "incr":
        result = client.incr(args.key)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

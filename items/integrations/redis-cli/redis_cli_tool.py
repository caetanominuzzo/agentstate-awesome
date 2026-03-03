#!/usr/bin/env python3
"""Redis CLI for interacting with Redis key-value store."""
import argparse
import json
import os
import sys

try:
    import redis
except ImportError:
    print(
        '{"error": "redis package required. Install with: pip install redis>=5.0.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class RedisClient:
    """Client for Redis interactions."""

    def __init__(self):
        self.redis_url = os.environ.get("REDIS_URL", "")
        if not self.redis_url:
            print(
                '{"error": "REDIS_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            self.client = redis.from_url(self.redis_url, decode_responses=True)
        except Exception as e:
            print(
                json.dumps({"error": f"Failed to connect to Redis: {str(e)}"}),
                file=sys.stderr,
            )
            sys.exit(1)

    def get(self, key):
        """Get value by key."""
        try:
            value = self.client.get(key)
            if value is None:
                return {"key": key, "value": None, "exists": False}
            return {"key": key, "value": value, "exists": True}
        except redis.RedisError as e:
            return {"error": str(e)}

    def set(self, key, value, ttl=None):
        """Set a key-value pair with optional TTL."""
        try:
            if ttl:
                self.client.setex(key, int(ttl), value)
            else:
                self.client.set(key, value)
            return {"success": True, "key": key, "ttl": ttl}
        except redis.RedisError as e:
            return {"error": str(e)}

    def delete(self, key):
        """Delete a key."""
        try:
            deleted = self.client.delete(key)
            return {"success": True, "key": key, "deleted": deleted}
        except redis.RedisError as e:
            return {"error": str(e)}

    def keys(self, pattern="*"):
        """List keys matching a pattern."""
        try:
            matched_keys = self.client.keys(pattern)
            return {"pattern": pattern, "keys": matched_keys, "count": len(matched_keys)}
        except redis.RedisError as e:
            return {"error": str(e)}

    def info(self):
        """Get Redis server info."""
        try:
            server_info = self.client.info()
            return {"info": server_info}
        except redis.RedisError as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Redis CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    get_parser = subparsers.add_parser("get", help="Get value by key")
    get_parser.add_argument("--key", required=True, help="Redis key")

    set_parser = subparsers.add_parser("set", help="Set a key-value pair")
    set_parser.add_argument("--key", required=True, help="Redis key")
    set_parser.add_argument("--value", required=True, help="Value to set")
    set_parser.add_argument("--ttl", type=int, help="Time to live in seconds")

    del_parser = subparsers.add_parser("del", help="Delete a key")
    del_parser.add_argument("--key", required=True, help="Redis key")

    keys_parser = subparsers.add_parser("keys", help="List keys matching pattern")
    keys_parser.add_argument(
        "--pattern", default="*", help="Key pattern (default: *)"
    )

    subparsers.add_parser("info", help="Get Redis server info")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = RedisClient()

    if args.command == "get":
        result = client.get(args.key)
    elif args.command == "set":
        result = client.set(args.key, args.value, args.ttl)
    elif args.command == "del":
        result = client.delete(args.key)
    elif args.command == "keys":
        result = client.keys(args.pattern)
    elif args.command == "info":
        result = client.info()

    print(json.dumps(result, indent=2, default=str))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

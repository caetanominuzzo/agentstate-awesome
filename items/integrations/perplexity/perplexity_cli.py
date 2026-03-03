#!/usr/bin/env python3
"""Perplexity CLI for searching and chatting with Perplexity AI models."""
import argparse
import json
import os
import sys
import requests


class PerplexityClient:
    """Client for Perplexity API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "PERPLEXITY_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.model = os.environ.get("PERPLEXITY_MODEL", "sonar")
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search(self, query):
        """Search using Perplexity AI."""
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": query}],
            }
            response = requests.post(
                f"{self.base_url}/chat/completions",
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

    def chat(self, message=None, messages_json=None):
        """Send a chat completion request."""
        try:
            if messages_json:
                messages = json.loads(messages_json)
            elif message:
                messages = [{"role": "user", "content": message}]
            else:
                return {"error": "Either --message or --messages-json is required"}

            payload = {
                "model": self.model,
                "messages": messages,
            }
            response = requests.post(
                f"{self.base_url}/chat/completions",
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
    parser = argparse.ArgumentParser(description="Perplexity CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    search_parser = subparsers.add_parser("search", help="Search using Perplexity AI")
    search_parser.add_argument("--query", required=True, help="Search query")

    chat_parser = subparsers.add_parser("chat", help="Send a chat completion request")
    chat_parser.add_argument("--message", help="Single message to send")
    chat_parser.add_argument(
        "--messages-json",
        help='JSON array of messages (e.g., \'[{"role":"user","content":"Hi"}]\')',
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = PerplexityClient()

    if args.command == "search":
        result = client.search(args.query)
    elif args.command == "chat":
        result = client.chat(
            message=getattr(args, "message", None),
            messages_json=getattr(args, "messages_json", None),
        )

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

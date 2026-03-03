#!/usr/bin/env python3
"""Anthropic CLI for chat completions and token counting via the official SDK."""
import argparse
import json
import os
import sys

try:
    import anthropic
except ImportError:
    print(
        '{"error": "anthropic package not installed. Run: pip install anthropic>=0.18.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class AnthropicClient:
    """Client for Anthropic API interactions via the official SDK."""

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "ANTHROPIC_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def chat(self, message=None, messages_json=None):
        """Send a message to Claude."""
        if messages_json:
            try:
                messages = json.loads(messages_json)
            except json.JSONDecodeError as e:
                return {"error": f"Invalid messages JSON: {e}"}
        elif message:
            messages = [{"role": "user", "content": message}]
        else:
            return {"error": "Either --message or --messages-json is required"}

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=messages,
            )
            return {
                "id": response.id,
                "model": response.model,
                "role": response.role,
                "content": [
                    {"type": block.type, "text": block.text}
                    for block in response.content
                    if block.type == "text"
                ],
                "stop_reason": response.stop_reason,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def count_tokens(self, text):
        """Count tokens for the given text using the Anthropic tokenizer."""
        try:
            response = self.client.messages.count_tokens(
                model=self.model,
                messages=[{"role": "user", "content": text}],
            )
            return {
                "input_tokens": response.input_tokens,
                "model": self.model,
            }
        except Exception as e:
            # Fallback: estimate using the messages API with a dry-run approach
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Anthropic CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    chat_parser = subparsers.add_parser("chat", help="Send a chat message")
    chat_parser.add_argument("--message", help="Single user message")
    chat_parser.add_argument(
        "--messages-json",
        help='JSON array of messages (e.g., \'[{"role":"user","content":"Hello"}]\')',
    )

    count_parser = subparsers.add_parser("count-tokens", help="Count tokens in text")
    count_parser.add_argument("--text", required=True, help="Text to count tokens for")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = AnthropicClient()

    if args.command == "chat":
        result = client.chat(
            message=getattr(args, "message", None),
            messages_json=getattr(args, "messages_json", None),
        )
    elif args.command == "count-tokens":
        result = client.count_tokens(args.text)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

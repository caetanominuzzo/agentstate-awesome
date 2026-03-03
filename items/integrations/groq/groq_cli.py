#!/usr/bin/env python3
"""Groq CLI for chatting with Groq-hosted LLMs and listing models."""
import argparse
import json
import os
import sys

from groq import Groq


class GroqClient:
    """Client for Groq API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "GROQ_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.model = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.client = Groq(api_key=self.api_key)

    def chat(self, message=None, messages_json=None):
        """Send a chat completion request."""
        try:
            if messages_json:
                messages = json.loads(messages_json)
            elif message:
                messages = [{"role": "user", "content": message}]
            else:
                return {"error": "Either --message or --messages-json is required"}

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return {
                "id": response.id,
                "model": response.model,
                "choices": [
                    {
                        "index": c.index,
                        "message": {
                            "role": c.message.role,
                            "content": c.message.content,
                        },
                        "finish_reason": c.finish_reason,
                    }
                    for c in response.choices
                ],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def list_models(self):
        """List available models."""
        try:
            response = self.client.models.list()
            return {
                "models": [
                    {
                        "id": m.id,
                        "owned_by": m.owned_by,
                        "created": m.created,
                    }
                    for m in response.data
                ]
            }
        except Exception as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Groq CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    chat_parser = subparsers.add_parser("chat", help="Send a chat completion request")
    chat_parser.add_argument("--message", help="Single message to send")
    chat_parser.add_argument(
        "--messages-json",
        help='JSON array of messages (e.g., \'[{"role":"user","content":"Hi"}]\')',
    )

    subparsers.add_parser("list-models", help="List available models")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = GroqClient()

    if args.command == "chat":
        result = client.chat(
            message=getattr(args, "message", None),
            messages_json=getattr(args, "messages_json", None),
        )
    elif args.command == "list-models":
        result = client.list_models()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

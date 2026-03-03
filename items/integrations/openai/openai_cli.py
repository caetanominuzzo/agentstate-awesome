#!/usr/bin/env python3
"""OpenAI CLI for chat completions, embeddings, and model listing."""
import argparse
import json
import os
import sys

try:
    from openai import OpenAI
except ImportError:
    print(
        '{"error": "openai package not installed. Run: pip install openai>=1.6.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class OpenAIClient:
    """Client for OpenAI API interactions via the official SDK."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "OPENAI_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o")
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, message=None, messages_json=None):
        """Send a chat completion request."""
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
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
            )
            return {
                "id": response.id,
                "model": response.model,
                "choices": [
                    {
                        "index": choice.index,
                        "message": {
                            "role": choice.message.role,
                            "content": choice.message.content,
                        },
                        "finish_reason": choice.finish_reason,
                    }
                    for choice in response.choices
                ],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def embed(self, text):
        """Generate embeddings for the given text."""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text,
            )
            return {
                "model": response.model,
                "data": [
                    {
                        "index": item.index,
                        "embedding_length": len(item.embedding),
                        "embedding_preview": item.embedding[:5],
                    }
                    for item in response.data
                ],
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            return {"error": str(e)}

    def list_models(self):
        """List available models."""
        try:
            response = self.client.models.list()
            models = [
                {
                    "id": model.id,
                    "owned_by": model.owned_by,
                    "created": model.created,
                }
                for model in response.data
            ]
            return {"models": sorted(models, key=lambda m: m["id"])}
        except Exception as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="OpenAI CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    chat_parser = subparsers.add_parser("chat", help="Send a chat completion")
    chat_parser.add_argument("--message", help="Single user message")
    chat_parser.add_argument(
        "--messages-json",
        help='JSON array of messages (e.g., \'[{"role":"user","content":"Hello"}]\')',
    )

    embed_parser = subparsers.add_parser("embed", help="Generate embeddings")
    embed_parser.add_argument("--text", required=True, help="Text to embed")

    subparsers.add_parser("list-models", help="List available models")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = OpenAIClient()

    if args.command == "chat":
        result = client.chat(
            message=getattr(args, "message", None),
            messages_json=getattr(args, "messages_json", None),
        )
    elif args.command == "embed":
        result = client.embed(args.text)
    elif args.command == "list-models":
        result = client.list_models()

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

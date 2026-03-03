#!/usr/bin/env python3
"""Spawn a new agent session via the Devin API."""
import argparse
import json
import os
import sys
import requests


def spawn_session(repo, task, context=None):
    """Spawn a new Devin session."""
    api_token = os.environ.get("DEVIN_API")
    if not api_token:
        print('{"error": "DEVIN_API environment variable not set"}', file=sys.stderr)
        sys.exit(1)

    base_url = "https://api.devin.ai/v1"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    payload = {"repo": repo, "task": task}
    if context:
        payload["context"] = context

    try:
        response = requests.post(
            f"{base_url}/sessions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


def main():
    parser = argparse.ArgumentParser(description="Spawn a new Devin session")
    parser.add_argument("--repo", required=True, help="Repository for the session")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--context", default=None, help="Additional context")

    args = parser.parse_args()
    result = spawn_session(args.repo, args.task, args.context)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

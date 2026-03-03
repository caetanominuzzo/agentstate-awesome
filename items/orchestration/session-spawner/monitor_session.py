#!/usr/bin/env python3
"""Monitor a Devin session status."""
import argparse
import json
import os
import sys
import requests


def get_session_status(session_id):
    """Get status of a Devin session."""
    api_token = os.environ.get("DEVIN_API")
    if not api_token:
        print('{"error": "DEVIN_API environment variable not set"}', file=sys.stderr)
        sys.exit(1)

    base_url = "https://api.devin.ai/v1"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{base_url}/sessions/{session_id}",
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "status_code": getattr(e.response, "status_code", None)}


def main():
    parser = argparse.ArgumentParser(description="Monitor a Devin session")
    parser.add_argument("session_id", help="Session ID to monitor")

    args = parser.parse_args()
    result = get_session_status(args.session_id)
    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

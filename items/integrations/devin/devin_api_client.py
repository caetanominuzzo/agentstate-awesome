#!/usr/bin/env python3
"""Shared Devin API HTTP client."""
import os
import sys
import requests


class DevinAPIClient:
    """Client for Devin API interactions."""

    def __init__(self):
        self.api_token = os.environ.get("DEVIN_API")
        if not self.api_token:
            print(
                '{"error": "DEVIN_API environment variable not set"}', file=sys.stderr
            )
            sys.exit(1)

        self.base_url = "https://api.devin.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    def spawn_session(self, repo, task, context=None):
        """Spawn a new Devin session."""
        payload = {"repo": repo, "task": task}
        if context:
            payload["context"] = context

        try:
            response = requests.post(
                f"{self.base_url}/sessions",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_session_status(self, session_id):
        """Get status of a Devin session."""
        try:
            response = requests.get(
                f"{self.base_url}/sessions/{session_id}",
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

#!/usr/bin/env python3
"""Figma CLI for retrieving files, comments, versions, and exporting images."""
import argparse
import json
import os
import sys
import requests


class FigmaClient:
    """Client for Figma API interactions."""

    def __init__(self):
        self.access_token = os.environ.get("FIGMA_ACCESS_TOKEN", "")
        if not self.access_token:
            print(
                '{"error": "FIGMA_ACCESS_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": self.access_token,
            "Content-Type": "application/json",
        }

    def get_file(self, file_key):
        """Get a Figma file by key."""
        try:
            response = requests.get(
                f"{self.base_url}/files/{file_key}",
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

    def list_comments(self, file_key):
        """List comments on a Figma file."""
        try:
            response = requests.get(
                f"{self.base_url}/files/{file_key}/comments",
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

    def export_images(self, file_key, node_ids, fmt="png"):
        """Export images from a Figma file."""
        try:
            response = requests.get(
                f"{self.base_url}/images/{file_key}",
                headers=self.headers,
                params={"ids": node_ids, "format": fmt},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_file_versions(self, file_key):
        """Get version history for a Figma file."""
        try:
            response = requests.get(
                f"{self.base_url}/files/{file_key}/versions",
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


def main():
    parser = argparse.ArgumentParser(description="Figma CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    get_file_parser = subparsers.add_parser("get-file", help="Get a Figma file")
    get_file_parser.add_argument("--file-key", required=True, help="Figma file key")

    comments_parser = subparsers.add_parser("list-comments", help="List file comments")
    comments_parser.add_argument("--file-key", required=True, help="Figma file key")

    export_parser = subparsers.add_parser("export-images", help="Export images")
    export_parser.add_argument("--file-key", required=True, help="Figma file key")
    export_parser.add_argument(
        "--node-ids", required=True, help="Comma-separated node IDs"
    )
    export_parser.add_argument(
        "--format", default="png", help="Export format (png, jpg, svg, pdf)"
    )

    versions_parser = subparsers.add_parser(
        "get-file-versions", help="Get file version history"
    )
    versions_parser.add_argument("--file-key", required=True, help="Figma file key")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = FigmaClient()

    if args.command == "get-file":
        result = client.get_file(args.file_key)
    elif args.command == "list-comments":
        result = client.list_comments(args.file_key)
    elif args.command == "export-images":
        result = client.export_images(args.file_key, args.node_ids, args.format)
    elif args.command == "get-file-versions":
        result = client.get_file_versions(args.file_key)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

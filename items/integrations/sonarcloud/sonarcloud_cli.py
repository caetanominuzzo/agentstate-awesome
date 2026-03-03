#!/usr/bin/env python3
"""SonarCloud CLI for listing projects, measures, and issues."""
import argparse
import json
import os
import sys
import requests


class SonarCloudClient:
    """Client for SonarCloud API interactions."""

    def __init__(self):
        self.token = os.environ.get("SONAR_TOKEN", "")
        if not self.token:
            print(
                '{"error": "SONAR_TOKEN environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.org = os.environ.get("SONAR_ORG", "")
        if not self.org:
            print(
                '{"error": "SONAR_ORG environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.base_url = "https://sonarcloud.io/api"
        self.auth = (self.token, "")

    def list_projects(self):
        """List all projects in the organization."""
        try:
            response = requests.get(
                f"{self.base_url}/projects/search",
                auth=self.auth,
                params={"organization": self.org},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def get_measures(self, project_key, metrics):
        """Get measures for a project."""
        try:
            response = requests.get(
                f"{self.base_url}/measures/component",
                auth=self.auth,
                params={"component": project_key, "metricKeys": metrics},
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_issues(self, project_key, severities=None):
        """List issues for a project."""
        try:
            params = {
                "componentKeys": project_key,
                "organization": self.org,
            }
            if severities:
                params["severities"] = severities
            response = requests.get(
                f"{self.base_url}/issues/search",
                auth=self.auth,
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def search_issues(self, project_key, query):
        """Search issues with a text query."""
        try:
            response = requests.get(
                f"{self.base_url}/issues/search",
                auth=self.auth,
                params={
                    "componentKeys": project_key,
                    "organization": self.org,
                    "q": query,
                },
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
    parser = argparse.ArgumentParser(description="SonarCloud CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-projects", help="List all projects")

    measures_parser = subparsers.add_parser("get-measures", help="Get project measures")
    measures_parser.add_argument("--project-key", required=True, help="Project key")
    measures_parser.add_argument(
        "--metrics",
        required=True,
        help="Comma-separated metric keys (e.g., coverage,bugs,vulnerabilities)",
    )

    issues_parser = subparsers.add_parser("list-issues", help="List project issues")
    issues_parser.add_argument("--project-key", required=True, help="Project key")
    issues_parser.add_argument(
        "--severities",
        help="Comma-separated severities (e.g., BLOCKER,CRITICAL,MAJOR)",
    )

    search_parser = subparsers.add_parser("search-issues", help="Search issues")
    search_parser.add_argument("--project-key", required=True, help="Project key")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SonarCloudClient()

    if args.command == "list-projects":
        result = client.list_projects()
    elif args.command == "get-measures":
        result = client.get_measures(args.project_key, args.metrics)
    elif args.command == "list-issues":
        result = client.list_issues(
            args.project_key,
            severities=getattr(args, "severities", None),
        )
    elif args.command == "search-issues":
        result = client.search_issues(args.project_key, args.query)

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

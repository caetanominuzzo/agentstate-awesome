#!/usr/bin/env python3
"""Linear CLI for managing issues via the Linear GraphQL API."""
import argparse
import json
import os
import sys
import requests


class LinearClient:
    """Client for Linear GraphQL API interactions."""

    def __init__(self):
        self.api_key = os.environ.get("LINEAR_API_KEY", "")
        if not self.api_key:
            print(
                '{"error": "LINEAR_API_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        self.api_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

    def _graphql(self, query, variables=None):
        """Execute a GraphQL query against the Linear API."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            if "errors" in data:
                return {"error": data["errors"][0]["message"], "errors": data["errors"]}
            return data.get("data", data)
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None),
            }

    def list_issues(self, team=None):
        """List issues, optionally filtered by team key."""
        filter_clause = ""
        variables = {}
        if team:
            filter_clause = '(filter: { team: { key: { eq: $team } } })'
            variables["team"] = team

        variable_defs = "($team: String)" if team else ""

        query = f"""
        query {variable_defs} {{
            issues{filter_clause} {{
                nodes {{
                    id
                    identifier
                    title
                    state {{ name }}
                    assignee {{ name }}
                    priority
                    createdAt
                    updatedAt
                }}
            }}
        }}
        """
        return self._graphql(query, variables if variables else None)

    def create_issue(self, team, title, description=None):
        """Create a new issue in a team."""
        # First resolve team key to team ID
        team_query = """
        query ($key: String!) {
            teams(filter: { key: { eq: $key } }) {
                nodes { id name key }
            }
        }
        """
        team_result = self._graphql(team_query, {"key": team})
        if "error" in team_result:
            return team_result

        teams = team_result.get("teams", {}).get("nodes", [])
        if not teams:
            return {"error": f"Team with key '{team}' not found"}

        team_id = teams[0]["id"]

        mutation = """
        mutation ($teamId: String!, $title: String!, $description: String) {
            issueCreate(input: { teamId: $teamId, title: $title, description: $description }) {
                success
                issue {
                    id
                    identifier
                    title
                    url
                }
            }
        }
        """
        variables = {"teamId": team_id, "title": title}
        if description:
            variables["description"] = description
        return self._graphql(mutation, variables)

    def update_issue(self, issue_id, state=None, title=None):
        """Update an existing issue."""
        input_fields = {}
        if title:
            input_fields["title"] = title
        if state:
            # Resolve state name to state ID
            state_query = """
            query ($name: String!) {
                workflowStates(filter: { name: { eq: $name } }) {
                    nodes { id name }
                }
            }
            """
            state_result = self._graphql(state_query, {"name": state})
            if "error" in state_result:
                return state_result
            states = state_result.get("workflowStates", {}).get("nodes", [])
            if not states:
                return {"error": f"Workflow state '{state}' not found"}
            input_fields["stateId"] = states[0]["id"]

        if not input_fields:
            return {"error": "At least --state or --title is required for update"}

        # Build dynamic input
        input_json = json.dumps(input_fields)
        mutation = f"""
        mutation {{
            issueUpdate(id: "{issue_id}", input: {input_json}) {{
                success
                issue {{
                    id
                    identifier
                    title
                    state {{ name }}
                }}
            }}
        }}
        """
        return self._graphql(mutation)

    def get_issue(self, issue_id):
        """Get details of a specific issue."""
        query = """
        query ($id: String!) {
            issue(id: $id) {
                id
                identifier
                title
                description
                state { name }
                assignee { name email }
                priority
                labels { nodes { name } }
                createdAt
                updatedAt
                url
            }
        }
        """
        return self._graphql(query, {"id": issue_id})


def main():
    parser = argparse.ArgumentParser(description="Linear CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    list_parser = subparsers.add_parser("list-issues", help="List issues")
    list_parser.add_argument("--team", help="Team key to filter by (e.g., ENG)")

    create_parser = subparsers.add_parser("create-issue", help="Create an issue")
    create_parser.add_argument(
        "--team", required=True, help="Team key (e.g., ENG)"
    )
    create_parser.add_argument("--title", required=True, help="Issue title")
    create_parser.add_argument("--description", help="Issue description (Markdown)")

    update_parser = subparsers.add_parser("update-issue", help="Update an issue")
    update_parser.add_argument("--issue-id", required=True, help="Linear issue ID")
    update_parser.add_argument("--state", help="New workflow state name")
    update_parser.add_argument("--title", help="New title")

    get_parser = subparsers.add_parser("get-issue", help="Get issue details")
    get_parser.add_argument("--issue-id", required=True, help="Linear issue ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = LinearClient()

    if args.command == "list-issues":
        result = client.list_issues(team=getattr(args, "team", None))
    elif args.command == "create-issue":
        result = client.create_issue(
            args.team, args.title,
            description=getattr(args, "description", None),
        )
    elif args.command == "update-issue":
        result = client.update_issue(
            args.issue_id,
            state=getattr(args, "state", None),
            title=getattr(args, "title", None),
        )
    elif args.command == "get-issue":
        result = client.get_issue(args.issue_id)

    print(json.dumps(result, indent=2))

    if isinstance(result, dict) and "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

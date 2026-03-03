#!/usr/bin/env python3
"""MySQL CLI for querying and managing MySQL databases."""
import argparse
import json
import os
import sys

try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
except ImportError:
    print(
        '{"error": "mysql-connector-python package required. Install with: pip install mysql-connector-python>=8.1.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class MySQLClient:
    """Client for MySQL interactions."""

    def __init__(self):
        self.host = os.environ.get("MYSQL_HOST", "")
        self.user = os.environ.get("MYSQL_USER", "")
        self.password = os.environ.get("MYSQL_PASSWORD", "")
        self.database = os.environ.get("MYSQL_DATABASE", "")
        self.port = int(os.environ.get("MYSQL_PORT", "3306"))
        if not self.host or not self.user or not self.password or not self.database:
            print(
                '{"error": "MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE environment variables required"}',
                file=sys.stderr,
            )
            sys.exit(1)

    def _connect(self):
        """Create a database connection."""
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            connection_timeout=30,
        )

    def query(self, sql):
        """Execute a SQL query and return results."""
        conn = None
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            if cursor.description:
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return {
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows),
                }
            else:
                conn.commit()
                return {"success": True, "rows_affected": cursor.rowcount}
        except MySQLError as e:
            return {"error": str(e)}
        finally:
            if conn and conn.is_connected():
                conn.close()

    def list_tables(self):
        """List all tables in the current database."""
        return self.query("SHOW TABLES")

    def describe_table(self, table):
        """Describe a table's columns."""
        try:
            conn = self._connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"DESCRIBE `{table}`")
            rows = cursor.fetchall()
            return {
                "table": table,
                "columns": rows,
                "column_count": len(rows),
            }
        except MySQLError as e:
            return {"error": str(e)}
        finally:
            if conn and conn.is_connected():
                conn.close()

    def list_databases(self):
        """List all databases."""
        return self.query("SHOW DATABASES")


def main():
    parser = argparse.ArgumentParser(description="MySQL CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    query_parser = subparsers.add_parser("query", help="Execute a SQL query")
    query_parser.add_argument("--sql", required=True, help="SQL query to execute")

    subparsers.add_parser("list-tables", help="List all tables")

    desc_parser = subparsers.add_parser("describe-table", help="Describe a table")
    desc_parser.add_argument("--table", required=True, help="Table name")

    subparsers.add_parser("list-databases", help="List all databases")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = MySQLClient()

    if args.command == "query":
        result = client.query(args.sql)
    elif args.command == "list-tables":
        result = client.list_tables()
    elif args.command == "describe-table":
        result = client.describe_table(args.table)
    elif args.command == "list-databases":
        result = client.list_databases()

    print(json.dumps(result, indent=2, default=str))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""PostgreSQL CLI for querying and managing PostgreSQL databases."""
import argparse
import json
import os
import sys

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print(
        '{"error": "psycopg2-binary package required. Install with: pip install psycopg2-binary>=2.9.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class PostgreSQLClient:
    """Client for PostgreSQL interactions."""

    def __init__(self):
        self.postgres_url = os.environ.get("POSTGRES_URL", "")
        if not self.postgres_url:
            print(
                '{"error": "POSTGRES_URL environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)

    def _connect(self):
        """Create a database connection."""
        try:
            return psycopg2.connect(self.postgres_url)
        except psycopg2.Error as e:
            return None, {"error": f"Connection failed: {str(e)}"}

    def query(self, sql):
        """Execute a SQL query and return results."""
        try:
            conn = psycopg2.connect(self.postgres_url)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql)
            if cursor.description:
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                return {
                    "columns": columns,
                    "rows": [dict(row) for row in rows],
                    "row_count": len(rows),
                }
            else:
                conn.commit()
                return {"success": True, "rows_affected": cursor.rowcount}
        except psycopg2.Error as e:
            return {"error": str(e)}
        finally:
            if "conn" in locals():
                conn.close()

    def list_tables(self):
        """List all tables in the current database."""
        sql = """
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
        """
        return self.query(sql)

    def describe_table(self, table):
        """Describe a table's columns."""
        sql = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """
        try:
            conn = psycopg2.connect(self.postgres_url)
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cursor.execute(sql, (table,))
            rows = cursor.fetchall()
            return {
                "table": table,
                "columns": [dict(row) for row in rows],
                "column_count": len(rows),
            }
        except psycopg2.Error as e:
            return {"error": str(e)}
        finally:
            if "conn" in locals():
                conn.close()

    def list_databases(self):
        """List all databases."""
        sql = "SELECT datname, pg_database_size(datname) as size_bytes FROM pg_database WHERE datistemplate = false ORDER BY datname"
        return self.query(sql)


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL CLI")
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

    client = PostgreSQLClient()

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

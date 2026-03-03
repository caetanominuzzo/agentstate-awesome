#!/usr/bin/env python3
"""Stripe CLI for managing customers, charges, subscriptions, and balance."""
import argparse
import json
import os
import sys

try:
    import stripe
except ImportError:
    print(
        '{"error": "stripe package required. Install with: pip install stripe>=7.0.0"}',
        file=sys.stderr,
    )
    sys.exit(1)


class StripeClient:
    """Client for Stripe API interactions."""

    def __init__(self):
        api_key = os.environ.get("STRIPE_SECRET_KEY", "")
        if not api_key:
            print(
                '{"error": "STRIPE_SECRET_KEY environment variable required"}',
                file=sys.stderr,
            )
            sys.exit(1)
        stripe.api_key = api_key

    def list_customers(self, limit=10):
        """List Stripe customers."""
        try:
            customers = stripe.Customer.list(limit=limit)
            return {"customers": [dict(c) for c in customers.data]}
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def get_customer(self, customer_id):
        """Get details of a Stripe customer."""
        try:
            customer = stripe.Customer.retrieve(customer_id)
            return dict(customer)
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def list_charges(self, limit=10):
        """List recent charges."""
        try:
            charges = stripe.Charge.list(limit=limit)
            return {"charges": [dict(c) for c in charges.data]}
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def list_subscriptions(self, customer_id):
        """List subscriptions for a customer."""
        try:
            subscriptions = stripe.Subscription.list(customer=customer_id)
            return {"subscriptions": [dict(s) for s in subscriptions.data]}
        except stripe.error.StripeError as e:
            return {"error": str(e)}

    def get_balance(self):
        """Get current Stripe balance."""
        try:
            balance = stripe.Balance.retrieve()
            return dict(balance)
        except stripe.error.StripeError as e:
            return {"error": str(e)}


def main():
    parser = argparse.ArgumentParser(description="Stripe CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    subparsers.add_parser("list-customers", help="List customers")

    get_cust_parser = subparsers.add_parser("get-customer", help="Get customer details")
    get_cust_parser.add_argument(
        "--customer-id", required=True, help="Stripe customer ID"
    )

    charges_parser = subparsers.add_parser("list-charges", help="List recent charges")
    charges_parser.add_argument(
        "--limit", type=int, default=10, help="Max results (default: 10)"
    )

    subs_parser = subparsers.add_parser(
        "list-subscriptions", help="List subscriptions for a customer"
    )
    subs_parser.add_argument(
        "--customer-id", required=True, help="Stripe customer ID"
    )

    subparsers.add_parser("get-balance", help="Get Stripe balance")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = StripeClient()

    if args.command == "list-customers":
        result = client.list_customers()
    elif args.command == "get-customer":
        result = client.get_customer(args.customer_id)
    elif args.command == "list-charges":
        result = client.list_charges(args.limit)
    elif args.command == "list-subscriptions":
        result = client.list_subscriptions(args.customer_id)
    elif args.command == "get-balance":
        result = client.get_balance()

    print(json.dumps(result, indent=2))

    if "error" in result:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

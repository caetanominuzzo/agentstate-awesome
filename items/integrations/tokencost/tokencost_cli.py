#!/usr/bin/env python3
"""Token cost CLI — fetch and query LLM pricing from OpenRouter."""
import argparse
import json
import sys
import urllib.request

OPENROUTER_URL = "https://openrouter.ai/api/v1/models"


def fetch_models():
    """Fetch all models from OpenRouter."""
    req = urllib.request.Request(OPENROUTER_URL)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["data"]


def normalize(model):
    """Normalize an OpenRouter model entry to a standard schema."""
    pricing = model.get("pricing", {})
    arch = model.get("architecture", {})

    def to_per_1m(val):
        if val is None:
            return None
        try:
            v = float(val)
            return round(v * 1_000_000, 4) if v > 0 else 0.0
        except (ValueError, TypeError):
            return None

    return {
        "id": model.get("id", ""),
        "name": model.get("name", ""),
        "vendor": model.get("id", "").split("/")[0],
        "context_window": model.get("context_length"),
        "modalities": {
            "input": arch.get("input_modalities", []),
            "output": arch.get("output_modalities", []),
        },
        "price_per_1m_tokens": {
            "input": to_per_1m(pricing.get("prompt")),
            "output": to_per_1m(pricing.get("completion")),
            "cached_input": to_per_1m(pricing.get("input_cache_read")),
            "image": to_per_1m(pricing.get("image")),
            "audio": to_per_1m(pricing.get("audio")),
            "web_search": to_per_1m(pricing.get("web_search")),
        },
    }


def cmd_list(args):
    """List all models with pricing."""
    models = fetch_models()
    normalized = [normalize(m) for m in models]

    if args.vendor:
        v = args.vendor.lower()
        normalized = [m for m in normalized if m["vendor"].lower() == v]

    if args.sort_by == "input":
        normalized.sort(key=lambda m: m["price_per_1m_tokens"]["input"] or float("inf"))
    elif args.sort_by == "output":
        normalized.sort(key=lambda m: m["price_per_1m_tokens"]["output"] or float("inf"))

    print(json.dumps(normalized, indent=2))


def cmd_get(args):
    """Get pricing for a specific model."""
    models = fetch_models()
    query = args.model.lower()
    for m in models:
        if m.get("id", "").lower() == query:
            print(json.dumps(normalize(m), indent=2))
            return
    # fuzzy match
    matches = [m for m in models if query in m.get("id", "").lower()]
    if matches:
        print(json.dumps([normalize(m) for m in matches], indent=2))
    else:
        print(json.dumps({"error": f"No model matching '{args.model}'"}))
        sys.exit(1)


def cmd_cost(args):
    """Calculate cost for a given token usage."""
    models = fetch_models()
    query = args.model.lower()
    target = None
    for m in models:
        if m.get("id", "").lower() == query:
            target = m
            break
    if not target:
        matches = [m for m in models if query in m.get("id", "").lower()]
        if matches:
            target = matches[0]
    if not target:
        print(json.dumps({"error": f"No model matching '{args.model}'"}))
        sys.exit(1)

    n = normalize(target)
    p = n["price_per_1m_tokens"]
    input_cost = (args.input_tokens / 1_000_000) * (p["input"] or 0)
    output_cost = (args.output_tokens / 1_000_000) * (p["output"] or 0)

    print(json.dumps({
        "model": n["id"],
        "input_tokens": args.input_tokens,
        "output_tokens": args.output_tokens,
        "input_cost_usd": round(input_cost, 6),
        "output_cost_usd": round(output_cost, 6),
        "total_cost_usd": round(input_cost + output_cost, 6),
        "prices_used": p,
    }, indent=2))


def cmd_compare(args):
    """Compare cost across models for a given workload."""
    models = fetch_models()
    normalized = [normalize(m) for m in models]

    # filter to models that have pricing
    normalized = [m for m in normalized if m["price_per_1m_tokens"]["input"] is not None]

    if args.vendor:
        vendors = [v.strip().lower() for v in args.vendor.split(",")]
        normalized = [m for m in normalized if m["vendor"].lower() in vendors]

    results = []
    for m in normalized:
        p = m["price_per_1m_tokens"]
        input_cost = (args.input_tokens / 1_000_000) * (p["input"] or 0)
        output_cost = (args.output_tokens / 1_000_000) * (p["output"] or 0)
        total = round(input_cost + output_cost, 6)
        results.append({
            "model": m["id"],
            "total_cost_usd": total,
            "context_window": m["context_window"],
        })

    results.sort(key=lambda r: r["total_cost_usd"])

    if args.top:
        results = results[:args.top]

    print(json.dumps({
        "workload": {
            "input_tokens": args.input_tokens,
            "output_tokens": args.output_tokens,
        },
        "results": results,
    }, indent=2))


def cmd_dump(args):
    """Dump full normalized pricing as a static JSON file."""
    models = fetch_models()
    normalized = [normalize(m) for m in models]
    output = {
        "schema_version": 1,
        "source": "openrouter.ai",
        "unit": "USD_per_1M_tokens",
        "model_count": len(normalized),
        "models": normalized,
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Token cost — LLM pricing CLI")
    sub = parser.add_subparsers(dest="command", help="Command to execute")

    # list
    list_p = sub.add_parser("list", help="List all models with pricing")
    list_p.add_argument("--vendor", help="Filter by vendor (e.g. openai, anthropic)")
    list_p.add_argument("--sort-by", choices=["input", "output"], default="input", help="Sort by price")

    # get
    get_p = sub.add_parser("get", help="Get pricing for a specific model")
    get_p.add_argument("model", help="Model ID (e.g. anthropic/claude-sonnet-4)")

    # cost
    cost_p = sub.add_parser("cost", help="Calculate cost for token usage")
    cost_p.add_argument("model", help="Model ID")
    cost_p.add_argument("--input-tokens", type=int, required=True, help="Number of input tokens")
    cost_p.add_argument("--output-tokens", type=int, required=True, help="Number of output tokens")

    # compare
    cmp_p = sub.add_parser("compare", help="Compare cost across models for a workload")
    cmp_p.add_argument("--input-tokens", type=int, required=True, help="Number of input tokens")
    cmp_p.add_argument("--output-tokens", type=int, required=True, help="Number of output tokens")
    cmp_p.add_argument("--vendor", help="Filter vendors (comma-separated)")
    cmp_p.add_argument("--top", type=int, help="Show only top N cheapest")

    # dump
    sub.add_parser("dump", help="Dump full normalized pricing JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    {"list": cmd_list, "get": cmd_get, "cost": cmd_cost, "compare": cmd_compare, "dump": cmd_dump}[args.command](args)


if __name__ == "__main__":
    main()

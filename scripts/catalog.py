#!/usr/bin/env python3
"""Query the local awesome-list catalogs built by build_catalogs.py.

    catalog.py list
    catalog.py categories mcp-servers
    catalog.py search postgres --catalog mcp-servers
    catalog.py search "object storage" --catalog free-for-dev --limit 5
    catalog.py search weather --catalog public-apis --no-auth
    catalog.py show public-apis --category Geocoding

Rows are ranked by where the terms hit: name matches outweigh category
matches, which outweigh description matches. All terms must appear
somewhere in a row for it to match.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# Let output pipe into head/less without a BrokenPipeError traceback.
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):  # non-POSIX
    pass

CATALOG_DIR = Path(__file__).resolve().parent.parent / "catalogs"

FIELD_WEIGHTS = {"name": 6, "category": 3, "install": 2}
DEFAULT_WEIGHT = 1


def load(slug: str) -> tuple[list[str], list[dict[str, str]]]:
    path = CATALOG_DIR / f"{slug}.tsv"
    if not path.exists():
        available = ", ".join(sorted(p.stem for p in CATALOG_DIR.glob("*.tsv"))) or "none"
        sys.exit(f"unknown catalog {slug!r}; available: {available}")
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def score(row: dict[str, str], terms: list[str]) -> int:
    """0 means "not a match" — every term has to land somewhere in the row."""
    total = 0
    for term in terms:
        best = 0
        for field, value in row.items():
            if term in value.lower():
                best = max(best, FIELD_WEIGHTS.get(field, DEFAULT_WEIGHT))
        if not best:
            return 0
        total += best
    return total


def render(rows: list[dict[str, str]], fields: list[str], as_json: bool) -> None:
    if as_json:
        json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return
    if not rows:
        print("no matches")
        return
    for row in rows:
        head = f"{row.get('name', '?')}  [{row.get('category', '')}]"
        print(head)
        if row.get("url"):
            print(f"  {row['url']}")
        for field in fields:
            if field in ("name", "category", "url"):
                continue
            value = row.get(field, "").strip()
            if value:
                print(f"  {field}: {value}")
        print()
    print(f"-- {len(rows)} result(s)")


def apply_filters(rows: list[dict[str, str]], args) -> list[dict[str, str]]:
    if args.category:
        want = args.category.lower()
        rows = [r for r in rows if want in r.get("category", "").lower()]
    if getattr(args, "no_auth", False):
        # public-apis writes "No" when an endpoint needs no credentials.
        rows = [r for r in rows if r.get("auth", "").strip().lower() in ("no", "")]
    if getattr(args, "https", False):
        rows = [r for r in rows if r.get("https", "").strip().lower() == "yes"]
    for flag in getattr(args, "flag", None) or []:
        rows = [r for r in rows if flag.lower() in r.get("flags", "").lower().split(",")]
    if getattr(args, "installable", False):
        rows = [r for r in rows if r.get("install", "").strip()]
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="show the available catalogs and when they were built")

    p_cat = sub.add_parser("categories", help="list a catalog's categories with counts")
    p_cat.add_argument("catalog")

    p_show = sub.add_parser("show", help="dump every entry in a category")
    p_show.add_argument("catalog")
    p_show.add_argument("--category", required=True)
    p_show.add_argument("--limit", type=int, default=0, help="0 = no limit")
    p_show.add_argument("--json", action="store_true")

    p_search = sub.add_parser("search", help="rank entries matching all terms")
    p_search.add_argument("terms", nargs="+")
    p_search.add_argument("--catalog", required=True)
    p_search.add_argument("--category", help="restrict to categories containing this text")
    p_search.add_argument("--limit", type=int, default=20)
    p_search.add_argument("--json", action="store_true")
    p_search.add_argument("--no-auth", action="store_true",
                          help="public-apis: only APIs needing no credentials")
    p_search.add_argument("--https", action="store_true",
                          help="public-apis: only APIs served over HTTPS")
    p_search.add_argument("--flag", action="append",
                          help="mcp-servers: require a flag (official, local, cloud, "
                               "python, typescript, macos, linux, windows, …)")
    p_search.add_argument("--installable", action="store_true",
                          help="mcp-servers: only entries with a known install command")

    args = ap.parse_args()

    if args.cmd == "list":
        for meta_path in sorted(CATALOG_DIR.glob("*.meta.json")):
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            print(f"{meta['catalog']:<14} {meta['entries']:>5} entries  "
                  f"{meta['categories']:>3} categories  built {meta['built_at']}")
            print(f"{'':<14} {meta['source']}")
        return

    fields, rows = load(args.catalog)

    if args.cmd == "categories":
        counts: dict[str, int] = {}
        for row in rows:
            counts[row["category"]] = counts.get(row["category"], 0) + 1
        for name in sorted(counts):
            print(f"{counts[name]:>5}  {name}")
        print(f"-- {len(counts)} categories, {len(rows)} entries")
        return

    if args.cmd == "show":
        picked = apply_filters(rows, args)
        render(picked[: args.limit] if args.limit else picked, fields, args.json)
        return

    terms = [t.lower() for t in args.terms]
    scored = [(score(r, terms), i, r) for i, r in enumerate(apply_filters(rows, args))]
    hits = [r for s, _, r in sorted((x for x in scored if x[0]),
                                    key=lambda x: (-x[0], x[1]))]
    render(hits[: args.limit], fields, args.json)


if __name__ == "__main__":
    main()

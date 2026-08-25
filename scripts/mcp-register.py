#!/usr/bin/env python3
"""Register MCP servers into this workspace's .mcp.json.

Nothing in mcp/servers.catalog.json is live until it is registered here, so
adding a server is always a deliberate step rather than a side effect of
cloning the repo.

    mcp-register.py available                 # vetted blocks you can add
    mcp-register.py status                    # what .mcp.json currently has
    mcp-register.py add filesystem git        # merge blocks into .mcp.json
    mcp-register.py add postgres --dry-run    # print the block, change nothing
    mcp-register.py remove memory
    mcp-register.py block <name> --command npx --arg -y --arg some-mcp-server

`block` generates a config block for any server in catalogs/mcp-servers.tsv
that is not pre-vetted here — look the entry up with scripts/catalog.py first
and copy its install command.
"""
from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

# Let output pipe into head/less without a BrokenPipeError traceback.
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):  # non-POSIX
    pass

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "mcp" / "servers.catalog.json"
MCP_JSON = ROOT / ".mcp.json"


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))["servers"]


def load_mcp() -> dict:
    if not MCP_JSON.exists():
        return {"mcpServers": {}}
    data = json.loads(MCP_JSON.read_text(encoding="utf-8"))
    data.setdefault("mcpServers", {})
    return data


def save_mcp(data: dict) -> None:
    MCP_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def cmd_available(_args) -> None:
    for name, spec in load_catalog().items():
        mark = "official" if spec.get("official") else "community"
        print(f"{name:<22} [{mark}] {spec['description']}")
        if spec.get("env"):
            print(f"{'':<22} requires env: {', '.join(spec['env'])}")
        print(f"{'':<22} {spec['upstream']}")


def cmd_status(_args) -> None:
    servers = load_mcp()["mcpServers"]
    if not servers:
        print(f"{MCP_JSON.name}: no servers registered")
        return
    for name, spec in servers.items():
        launch = spec.get("command", spec.get("url", "?"))
        args = " ".join(spec.get("args", []))
        print(f"{name:<22} {launch} {args}".rstrip())


def cmd_add(args) -> None:
    catalog = load_catalog()
    unknown = [n for n in args.names if n not in catalog]
    if unknown:
        sys.exit(f"not in the vetted catalog: {', '.join(unknown)}\n"
                 f"run `{Path(__file__).name} available` to see the list, or use "
                 f"`{Path(__file__).name} block` to build one by hand")

    data = load_mcp()
    for name in args.names:
        spec = catalog[name]
        block = spec["config"]
        if args.dry_run:
            print(f"// {name}: {spec['description']}")
            print(json.dumps({name: block}, indent=2))
            if spec.get("env"):
                print(f"// requires env: {', '.join(spec['env'])}")
            continue
        if name in data["mcpServers"] and not args.force:
            print(f"{name}: already registered (pass --force to overwrite)")
            continue
        data["mcpServers"][name] = block
        print(f"{name}: registered")
        if spec.get("notes"):
            print(f"  note: {spec['notes']}")
        if spec.get("env"):
            print(f"  set these first: {', '.join(spec['env'])}")

    if not args.dry_run:
        save_mcp(data)
        print(f"\nwrote {MCP_JSON}")
        print("Restart the session (or reload MCP servers) for changes to take effect.")


def cmd_remove(args) -> None:
    data = load_mcp()
    for name in args.names:
        if data["mcpServers"].pop(name, None) is None:
            print(f"{name}: not registered")
        else:
            print(f"{name}: removed")
    save_mcp(data)


def cmd_block(args) -> None:
    """Build a config block for a server that is not pre-vetted."""
    if args.install:
        parts = shlex.split(args.install)
        if not parts:
            sys.exit("--install was empty")
        command, argv = parts[0], parts[1:]
    else:
        command, argv = args.command, args.arg or []
    if not command:
        sys.exit("give either --install '<full command>' or --command with --arg")

    block: dict = {"command": command, "args": argv}
    if args.env:
        block["env"] = {}
        for pair in args.env:
            key, _, value = pair.partition("=")
            block["env"][key] = value or "${" + key + "}"

    print(json.dumps({args.name: block}, indent=2))
    print(f"\n// paste into the mcpServers object of {MCP_JSON}", file=sys.stderr)
    print("// review the upstream repo before running an unvetted server", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("available", help="list vetted server blocks").set_defaults(fn=cmd_available)
    sub.add_parser("status", help="show registered servers").set_defaults(fn=cmd_status)

    p_add = sub.add_parser("add", help="merge vetted blocks into .mcp.json")
    p_add.add_argument("names", nargs="+")
    p_add.add_argument("--dry-run", action="store_true", help="print, do not write")
    p_add.add_argument("--force", action="store_true", help="overwrite an existing entry")
    p_add.set_defaults(fn=cmd_add)

    p_rm = sub.add_parser("remove", help="drop servers from .mcp.json")
    p_rm.add_argument("names", nargs="+")
    p_rm.set_defaults(fn=cmd_remove)

    p_blk = sub.add_parser("block", help="generate a block for an unvetted server")
    p_blk.add_argument("name")
    p_blk.add_argument("--install", help="full launch command, e.g. 'npx -y some-mcp'")
    p_blk.add_argument("--command", help="launcher binary, e.g. npx or uvx")
    p_blk.add_argument("--arg", action="append", help="one argument (repeatable)")
    p_blk.add_argument("--env", action="append", metavar="KEY[=VALUE]",
                       help="env var to pass through (repeatable)")
    p_blk.set_defaults(fn=cmd_block)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()

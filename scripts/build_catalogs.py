#!/usr/bin/env python3
"""Turn upstream awesome-list READMEs into compact, grep-able TSV catalogs.

Reads raw README markdown from a cache directory and writes one TSV per
catalog into catalogs/, alongside a .meta.json describing the build.

Usage:  build_catalogs.py --cache <dir> --out <dir>
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
from pathlib import Path

# ---------------------------------------------------------------- helpers

IMG_BADGE = re.compile(r"\[!\[[^\]]*\]\([^)]*\)\]\([^)]*\)")   # [![alt](img)](link)
BARE_IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")                  # ![alt](img)
MD_LINK = re.compile(r"\[([^\]]+)\]\((\S+?)\)")
HTML_TAG = re.compile(r"<[^>]+>")


def clean(text: str) -> str:
    """Flatten a markdown fragment into a single safe TSV cell."""
    text = IMG_BADGE.sub("", text)
    text = BARE_IMG.sub("", text)
    text = HTML_TAG.sub("", text)
    text = MD_LINK.sub(r"\1 (\2)", text)
    text = text.replace("\t", " ").replace("\r", " ").replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -–—•*|")


def truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("\t".join(header) + "\n")
        for row in rows:
            fh.write("\t".join(clean(c) if "\t" in c else c for c in row) + "\n")


def write_meta(path: Path, **fields) -> None:
    fields["built_at"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    path.write_text(json.dumps(fields, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ------------------------------------------------------------ free-for-dev

def parse_free_for_dev(md: str) -> list[list[str]]:
    """free-for-dev nests offer details under each provider bullet.

    Top-level `  * [Name](url) - desc` opens an entry; deeper bullets are
    that provider's individual free-tier offers, so they are folded into the
    entry's notes rather than becoming rows of their own.
    """
    rows: list[list[str]] = []
    category = ""
    in_toc = False
    entry: dict | None = None

    def flush() -> None:
        nonlocal entry
        if entry and entry["name"]:
            notes = " | ".join(entry["notes"])
            desc = entry["desc"]
            if notes:
                desc = f"{desc} || {notes}" if desc else notes
            rows.append([category, entry["name"], entry["url"], truncate(clean(desc), 700)])
        entry = None

    for line in md.splitlines():
        if line.startswith("# ") or line.startswith("## "):
            flush()
            title = clean(line.lstrip("# ").strip())
            # The Table of Contents mirrors every section heading; skip it.
            in_toc = title.lower() == "table of contents"
            category = "" if in_toc or line.startswith("# ") else title
            continue
        if in_toc or not category:
            continue

        bullet = re.match(r"^(\s*)[*-]\s+(.*)$", line)
        if not bullet:
            if entry and line.strip():
                entry["desc"] += " " + line.strip()
            continue

        indent, body = len(bullet.group(1)), bullet.group(2)
        if indent <= 3:                     # new provider
            flush()
            link = MD_LINK.search(body)
            name = clean(link.group(1)) if link else clean(body.split(" - ")[0])
            url = link.group(2).rstrip(")") if link else ""
            desc = body[link.end():] if link else body
            entry = {"name": name, "url": url, "desc": clean(desc), "notes": []}
        elif entry is not None:             # an offer belonging to the provider
            entry["notes"].append(clean(body))

    flush()
    return rows


# ------------------------------------------------------------- public-apis

def parse_public_apis(md: str) -> list[list[str]]:
    """public-apis stores each category as a 5-column markdown table."""
    rows: list[list[str]] = []
    category = ""
    reached_index = False

    for line in md.splitlines():
        if line.startswith("## "):
            # Everything before the Index heading is sponsor content, not APIs.
            if clean(line.lstrip("# ")).lower() == "index":
                reached_index = True
            category = ""
            continue
        if line.startswith("### "):
            category = clean(line.lstrip("# "))
            continue
        if not reached_index or not category or not line.startswith("|"):
            continue

        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or set(cells[0]) <= set("-: "):
            continue
        link = MD_LINK.search(cells[0])
        if not link:                        # header row ("API | Description | …")
            continue
        rows.append([
            category,
            clean(link.group(1)),
            link.group(2).rstrip(")"),
            truncate(clean(cells[1]), 300),
            clean(cells[2]) or "No",        # auth: empty cell means none required
            clean(cells[3]),                # https
            clean(cells[4]),                # cors
        ])
    return rows


# ------------------------------------------------------ awesome-mcp-servers

# Legend from the upstream README; used to turn emoji flags into words.
MCP_FLAGS = {
    "🎖️": "official", "🐍": "python", "📇": "typescript", "🏎️": "go",
    "🦀": "rust", "#️⃣": "csharp", "☕": "java", "🌊": "c-cpp", "💎": "ruby",
    "☁️": "cloud", "🏠": "local", "📟": "embedded",
    "🍎": "macos", "🪟": "windows", "🐧": "linux",
}
# npx/uvx/pip/docker invocations quoted in an entry's description.
INSTALL_HINT = re.compile(
    r"`((?:npx|uvx|pipx|pip3?|uv|docker|go|cargo|bun|deno|brew)\s+[^`]+)`"
)


def parse_mcp_servers(md: str) -> list[list[str]]:
    rows: list[list[str]] = []
    category = ""
    in_servers = False

    for line in md.splitlines():
        if line.startswith("## "):
            title = clean(line.lstrip("# "))
            in_servers = title.lower() == "server implementations"
            category = ""
            continue
        if line.startswith("### "):
            # Headings are decorated ("### 🔗 <a name=...></a>Aggregators").
            category = clean(line.lstrip("# ")).lstrip("#*-– ")
            category = re.sub(r"^[^\w(]+", "", category).strip()
            continue
        if not in_servers or not category or not line.startswith("- ["):
            continue

        body = IMG_BADGE.sub("", line[2:])
        link = MD_LINK.search(body)
        if not link:
            continue
        name, url = clean(link.group(1)), link.group(2).rstrip(")")
        rest = body[link.end():]

        flags = [word for emoji, word in MCP_FLAGS.items() if emoji in rest]
        install = INSTALL_HINT.search(rest)
        # The flag emoji already live in their own column; drop them from prose.
        desc = rest
        for emoji in MCP_FLAGS:
            desc = desc.replace(emoji, "")
        rows.append([
            category,
            name,
            url,
            ",".join(sorted(flags)),
            install.group(1).strip() if install else "",
            truncate(clean(desc), 400),
        ])
    return rows


# -------------------------------------------------------------------- main

CATALOGS = {
    "free-for-dev": {
        "file": "ripienaar_free-for-dev.README.md",
        "source": "https://github.com/ripienaar/free-for-dev",
        "header": ["category", "name", "url", "notes"],
        "parser": parse_free_for_dev,
    },
    "public-apis": {
        "file": "public-apis_public-apis.README.md",
        "source": "https://github.com/public-apis/public-apis",
        "header": ["category", "name", "url", "description", "auth", "https", "cors"],
        "parser": parse_public_apis,
    },
    "mcp-servers": {
        "file": "punkpeye_awesome-mcp-servers.README.md",
        "source": "https://github.com/punkpeye/awesome-mcp-servers",
        "header": ["category", "name", "url", "flags", "install", "description"],
        "parser": parse_mcp_servers,
    },
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cache", required=True, type=Path, help="dir holding raw READMEs")
    ap.add_argument("--out", required=True, type=Path, help="dir to write TSVs into")
    args = ap.parse_args()

    for slug, spec in CATALOGS.items():
        src = args.cache / spec["file"]
        if not src.exists():
            print(f"skip {slug}: {src} not found")
            continue
        rows = spec["parser"](src.read_text(encoding="utf-8"))
        write_tsv(args.out / f"{slug}.tsv", spec["header"], rows)
        write_meta(
            args.out / f"{slug}.meta.json",
            catalog=slug,
            source=spec["source"],
            entries=len(rows),
            categories=len({r[0] for r in rows}),
            columns=spec["header"],
        )
        print(f"{slug}: {len(rows)} entries, {len({r[0] for r in rows})} categories")


if __name__ == "__main__":
    main()

---
name: mcp-servers
description: >
  Use when the user wants to find, evaluate, or install an MCP (Model Context
  Protocol) server — "is there an MCP server for X", "connect Claude to
  Notion/Slack/Postgres/Jira/Figma", "add an MCP server", "what MCP servers do
  I have", "register this MCP server locally", or when a task needs a
  capability this session lacks and an MCP server would supply it.

  Backed by a local 3350-entry index of punkpeye/awesome-mcp-servers across 56
  categories, filterable by language, official status, and local-vs-cloud.
  Also owns this workspace's .mcp.json: vetted blocks in
  mcp/servers.catalog.json register via scripts/mcp-register.py, and any other
  server from the index can have a config block generated for it.

  NOT for: using MCP tools that are already connected (just call them), or
  writing a new MCP server from scratch (use the mcp-builder skill).
metadata:
  homepage: https://github.com/punkpeye/awesome-mcp-servers
---

# mcp-servers — find and register MCP servers

Two jobs: searching a local index of 3350+ published servers, and wiring a
chosen one into this workspace's `.mcp.json`.

## 1. Find a server

```bash
python3 scripts/catalog.py categories mcp-servers

python3 scripts/catalog.py search notion --catalog mcp-servers
python3 scripts/catalog.py search postgres --catalog mcp-servers --flag official

# Runs on this machine rather than calling a hosted API
python3 scripts/catalog.py search browser --catalog mcp-servers --flag local

# Only entries whose README published an install command
python3 scripts/catalog.py search jira --catalog mcp-servers --installable

python3 scripts/catalog.py show mcp-servers --category "Version Control"
```

Columns: `category`, `name`, `url`, `flags`, `install`, `description`.

`flags` combines three upstream axes:
- language — `python`, `typescript`, `go`, `rust`, `csharp`, `java`, `c-cpp`, `ruby`
- scope — `local` (talks to software on this machine), `cloud` (talks to a remote API), `embedded`
- OS — `macos`, `windows`, `linux`
- `official` — published by the service's own vendor

Prefer `official` when one exists. An MCP server runs with your credentials and
your filesystem access, so treat an unvetted community server the way you'd
treat any dependency you're about to give a token to.

## 2. Register it

Nothing is live until it is registered. `.mcp.json` starts empty on purpose.

```bash
python3 scripts/mcp-register.py available            # 8 pre-vetted blocks
python3 scripts/mcp-register.py status               # what's registered now
python3 scripts/mcp-register.py add filesystem git   # merge into .mcp.json
python3 scripts/mcp-register.py add postgres --dry-run
python3 scripts/mcp-register.py remove memory
```

For a server not in the vetted set, take the `install` column from the search
result and generate a block:

```bash
python3 scripts/mcp-register.py block tavily \
    --install "npx -y tavily-mcp@latest" --env TAVILY_API_KEY
```

That prints the JSON; paste it into the `mcpServers` object of `.mcp.json`.

## Rules

- Ask before registering. A new MCP server changes what the session can do and
  costs startup time, so it is the user's call, not a silent side effect.
- Never hardcode a secret into `.mcp.json` — it is committed. Use
  `"KEY": "${KEY}"` and let the environment supply the value.
- Registering takes effect on the next session start or MCP reload; say so
  rather than letting the user wonder why the tools aren't there yet.
- `${PWD}` in the vetted filesystem and git blocks is a placeholder. Replace it
  with the directory you actually mean to expose.

## Keeping it current

```bash
./scripts/refresh-catalogs.sh
```

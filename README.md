# meridian-project

Workspace configuration for Claude Code: skills, catalogs, and MCP server
registration.

## Layout

```
.agents/skills/       skill definitions (source of truth)
.claude/skills/       symlinks into .agents/skills — where Claude Code looks
.mcp.json             registered MCP servers (starts empty, opt in per server)
catalogs/             generated TSV indexes of upstream awesome-lists
mcp/                  vetted, ready-to-register MCP server blocks
scripts/              catalog query + build tooling, installers
skills-lock.json      provenance for each skill
```

## Skills

| Skill | Use it for | Derived from |
|---|---|---|
| `agent-reach` | Fetching content from 15 web platforms | [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) |
| `free-infra` | Finding free-tier hosting, databases, CI, storage | [ripienaar/free-for-dev](https://github.com/ripienaar/free-for-dev) |
| `public-apis` | Finding a public API for a data need | [public-apis/public-apis](https://github.com/public-apis/public-apis) |
| `mcp-servers` | Finding and registering MCP servers | [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) |
| `easyspider` | No-code visual web scraping | [NaiboWang/EasySpider](https://github.com/NaiboWang/EasySpider) |
| `strix-pentest` | Autonomous AI penetration testing | [usestrix/strix](https://github.com/usestrix/strix) |

The three list-backed skills query local catalogs, so they work offline and
don't burn a web fetch on every lookup.

## Catalogs

Upstream READMEs are parsed into flat TSVs — one row per entry, grep-able and
diffable.

| Catalog | Entries | Categories | Columns |
|---|---|---|---|
| `free-for-dev` | ~1,230 | 57 | category, name, url, notes |
| `public-apis` | ~1,610 | 51 | category, name, url, description, auth, https, cors |
| `mcp-servers` | ~3,360 | 56 | category, name, url, flags, install, description |

```bash
python3 scripts/catalog.py list                                  # what's indexed, and when built
python3 scripts/catalog.py categories mcp-servers
python3 scripts/catalog.py search postgres --catalog free-for-dev
python3 scripts/catalog.py search weather --catalog public-apis --no-auth --https
python3 scripts/catalog.py search notion --catalog mcp-servers --flag official
python3 scripts/catalog.py show public-apis --category Geocoding --json
```

Upstream lists change constantly. Rebuild with:

```bash
./scripts/refresh-catalogs.sh
```

## MCP servers

`.mcp.json` ships empty. Registering a server is deliberate — it runs with your
credentials and filesystem access, and costs session startup time.

```bash
python3 scripts/mcp-register.py available          # 8 pre-vetted blocks
python3 scripts/mcp-register.py add filesystem git
python3 scripts/mcp-register.py status
python3 scripts/mcp-register.py remove memory
```

For anything outside the vetted set, find it in the catalog and generate a block:

```bash
python3 scripts/catalog.py search linear --catalog mcp-servers --installable
python3 scripts/mcp-register.py block linear --install "npx -y linear-mcp" --env LINEAR_API_KEY
```

Secrets belong in the environment, never in `.mcp.json` — it is committed. Use
`"KEY": "${KEY}"`.

## Standalone CLI tools

Neither ships as an MCP server; both are installed and driven from the shell.

```bash
./scripts/install-easyspider.sh   # clones source, venv, ExecuteStage deps
./scripts/install-strix.sh        # checks Docker, installs CLI, reports missing config
```

EasySpider's task *designer* is a desktop GUI download — the CLI only replays
tasks you designed there. Strix needs Docker running and an LLM API key, and
must only be pointed at systems you own or are authorized to test.

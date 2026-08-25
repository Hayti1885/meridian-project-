---
name: public-apis
description: >
  Use when the user needs a public API or data source to call — "is there an
  API for X", "where do I get weather / currency / geocoding / stock / sports /
  government / dictionary data", "free API for ...", "I need test data", or
  when building something that needs an external data feed and no specific
  provider has been chosen yet.

  Backed by a local 1600-entry index of public-apis/public-apis across 51
  categories, recording each API's auth requirement (none / apiKey / OAuth),
  HTTPS support, and CORS support — so you can filter to APIs that will
  actually work from the user's context.

  NOT for: finding free hosting or infrastructure (use the free-infra skill),
  or reading the docs of an API already chosen (fetch those directly).
metadata:
  homepage: https://github.com/public-apis/public-apis
---

# public-apis — find a public API endpoint

A local, offline index of [public-apis](https://github.com/public-apis/public-apis).

## Query it

All commands run from the repo root.

```bash
python3 scripts/catalog.py categories public-apis

# Search
python3 scripts/catalog.py search weather --catalog public-apis
python3 scripts/catalog.py search exchange rate --catalog public-apis

# Only APIs that need no credentials — usually what you want for a quick demo
python3 scripts/catalog.py search geocoding --catalog public-apis --no-auth

# No-auth AND HTTPS (required for browser-side calls)
python3 scripts/catalog.py search country --catalog public-apis --no-auth --https

python3 scripts/catalog.py show public-apis --category Cryptocurrency
python3 scripts/catalog.py search nasa --catalog public-apis --json
```

Columns: `category`, `name`, `url`, `description`, `auth`, `https`, `cors`.

- `auth` — `No` means no credentials needed; otherwise `apiKey`, `OAuth`, `X-Mashape-Key`.
- `cors` — `Yes` means callable straight from browser JavaScript. `Unknown` means untested, so
  assume a proxy is needed for front-end use.

## How to answer

1. Match the filters to the user's context before searching: browser front-end
   needs `--https` and CORS `Yes`; a throwaway script or demo is best served by
   `--no-auth`.
2. Offer a few candidates with their auth and CORS status stated, so the user
   sees the integration cost, not just the name.
3. The index carries no endpoint paths or schemas — link the API's own docs URL
   and fetch it when the user commits to one.
4. Entries are community-submitted and some are dead. If an API matters, check
   that it still responds before building on it.

## Keeping it current

```bash
./scripts/refresh-catalogs.sh
```

---
name: free-infra
description: >
  Use when the user needs a free tier, free hosting, or a no-cost service for
  something they are building — "where can I host this for free", "free
  Postgres", "free CI minutes", "cheapest way to run a cron job", "free object
  storage / CDN / email sending / error tracking / analytics / DNS", "what's
  the free tier on X", or when picking infrastructure and cost is a stated
  constraint.

  Backed by a local 1200-entry index of ripienaar/free-for-dev covering 57
  categories: cloud providers, PaaS, BaaS, databases, CI/CD, monitoring, log
  management, email, CDN, DNS, storage, auth, analytics, and more. Each entry
  records the actual free-tier limits.

  NOT for: paid-tier pricing comparisons, or picking a public data API (use
  the public-apis skill for that).
metadata:
  homepage: https://github.com/ripienaar/free-for-dev
---

# free-infra — find free-tier infrastructure

A local, offline index of [free-for-dev](https://github.com/ripienaar/free-for-dev).
Query it rather than guessing from memory: free tiers change constantly and the
index records the limits that were actually published.

## Query it

All commands run from the repo root.

```bash
# What categories exist?
python3 scripts/catalog.py categories free-for-dev

# Search (all terms must match; name hits rank above description hits)
python3 scripts/catalog.py search postgres --catalog free-for-dev
python3 scripts/catalog.py search object storage --catalog free-for-dev --limit 10

# Narrow to a category
python3 scripts/catalog.py search redis --catalog free-for-dev --category "Managed Data Services"

# Dump a whole category
python3 scripts/catalog.py show free-for-dev --category "PaaS"

# Machine-readable
python3 scripts/catalog.py search cron --catalog free-for-dev --json
```

Columns: `category`, `name`, `url`, `notes`. The `notes` field holds the
free-tier limits — quote them to the user, since that is the part they are
actually deciding on.

## How to answer

1. Search with two or three specific terms. If nothing lands, retry with a
   broader synonym (`postgres` → `database`, `serverless` → `functions`).
2. Give 3–5 options, not the whole list, each with its concrete limit
   ("Neon — 0.5 GB storage, 10 branches") so the user can compare.
3. Say when the index was built (`python3 scripts/catalog.py list`) and point
   at the provider's own pricing page for anything cost-critical. Limits in
   this index are a snapshot, not a guarantee.

## Keeping it current

```bash
./scripts/refresh-catalogs.sh     # re-fetches upstream and rebuilds all catalogs
```

Worth running if the index is more than a month or two old.

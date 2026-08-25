---
name: easyspider
description: >
  Use when the user asks to scrape or extract data from a website without
  writing scraper code — "scrape this site", "collect all the listings /
  products / prices from X", "no-code crawler", "automate clicking through
  these pages", or when they mention EasySpider / 易采集 by name, or have an
  existing EasySpider task JSON to run.

  EasySpider is a visual, code-free browser automation and scraping tool: you
  design a task by clicking elements in its desktop GUI, then replay it
  headlessly from the CLI, which is the half an agent can drive. Exports to
  CSV, Excel, JSON, or MySQL.

  NOT for: one-off fetches of a single page (just fetch it), API calls where a
  public API exists (check the public-apis skill first), or browser automation
  you would rather write directly (use Playwright).
metadata:
  homepage: https://github.com/NaiboWang/EasySpider
---

# easyspider — no-code visual web scraping

EasySpider splits into two halves, and the split matters:

| Half | What it is | Who drives it |
|---|---|---|
| **Designer** (ElectronJS GUI) | Click elements on a live page to define a task; saves a task JSON | The **user**, by hand — this is a desktop app |
| **ExecuteStage** (Python CLI) | Replays a saved task JSON headlessly | **You**, from the shell |

You cannot design a task for the user — element selection is a GUI action.
What you can do is run, schedule, parametrise, and post-process their tasks.

## Setup

```bash
./scripts/install-easyspider.sh
```

Clones the source to `vendor/EasySpider/`, creates a venv, installs the
ExecuteStage dependencies. The desktop designer is a separate download from
[Releases](https://github.com/NaiboWang/EasySpider/releases) — point the user
there if they have no task JSON yet.

The CLI also needs Chrome plus a matching chromedriver on `PATH`. The GUI
bundles its own; a standalone CLI install does not.

## Running a task

```bash
cd vendor/EasySpider/ExecuteStage
../.venv/bin/python easyspider_executestage.py \
    --ids [1] \
    --read_type local \
    --config_folder /path/to/task/configs \
    --headless 1
```

Key arguments (from `easyspider_executestage.py`):

| Argument | Default | Meaning |
|---|---|---|
| `--ids` | `[0]` | Task IDs to run, as a JSON list: `[1]`, `[1,2,3]` |
| `--read_type` | `remote` | `local` reads task JSON from disk; `remote` asks the running GUI |
| `--config_folder` | `""` | Where task JSON lives when `read_type=local` |
| `--config_file_name` | `config.json` | Task file name |
| `--saved_file_name` | `""` | Output file name |
| `--headless` | `False` | `1` runs without a visible browser — use this for automation |
| `--user_data` | `False` | `1` reuses a browser profile, keeping logins |
| `--server_address` | `http://localhost:8074` | GUI address when `read_type=remote` |
| `--keyboard` | `True` | `0` disables the keyboard listener; **set this for unattended runs** |
| `--docker_driver` | `""` | chromedriver path when running containerised |

`--read_type remote` requires the desktop GUI to be running. For unattended
work always use `--read_type local --keyboard 0 --headless 1`.

Full reference: [Argument Instruction wiki](https://github.com/NaiboWang/EasySpider/wiki/Argument-Instruction).

## How to help

1. Ask whether they already have a task JSON. If not, the first step is theirs:
   design it in the GUI. Offer to run it once they do.
2. Given a task JSON, read it — it is plain JSON describing the flow graph, so
   you can explain what it will collect, or edit URLs and loop counts directly.
3. After a run, the output CSV/Excel/JSON is ordinary data — parse, clean, and
   analyse it normally.
4. If the job is a single page or a documented API, say so. EasySpider is worth
   its setup cost for repeated multi-page extraction, not for one fetch.

## Before scraping

Check the target's `robots.txt` and terms of service, and keep request rates
modest. Flag it to the user if a target's terms appear to prohibit automated
collection — the decision is theirs, but they should make it knowingly.

Licence note: EasySpider is AGPL-3.0. Embedding it in a network service you
distribute carries source-provision obligations.

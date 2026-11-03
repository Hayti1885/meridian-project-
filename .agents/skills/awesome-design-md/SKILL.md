---
name: awesome-design-md
description: Library of 84 ready-made DESIGN.md design-system files (colors, typography, spacing, components) analyzed from real websites such as Stripe, Linear, Apple, Notion, Vercel, Spotify, Tesla, Airbnb. Use when building or styling a web page, landing page, app UI, or artifact and the user wants it to look like a named brand or wants a polished reference style, or asks for a DESIGN.md.
---

# Awesome DESIGN.md

Source: https://github.com/VoltAgent/awesome-design-md (MIT, see LICENSE), commit fcc7028.

Each folder in `designs/` holds one `DESIGN.md` file. The file opens with YAML front matter (colors, typography, rounded, spacing, components tokens) followed by prose rules for layout, components, and do/don't guidance.

## How to use

1. Pick the closest match from the list below. If the user names a brand, use that folder.
2. Read `designs/<name>/DESIGN.md` in full before writing UI code.
3. Apply its tokens and rules to the UI you build. Use the token values as CSS variables.
4. To give a project a persistent style, copy the chosen file to the project root as `DESIGN.md`.
5. These are inspired interpretations. Do not copy logos, trademarks, or proprietary font files. Use the fallback font stacks listed in each file.

## Available designs

1win, airbnb, airtable, aljazeera, apple, binance, bmw, bmw-m, bugatti, cal, claude, clay, clickhouse, cohere, coinbase, composio, cursor, dell-1996, dji, elevenlabs, expo, ferrari, figma, framer, hashicorp, hp, ibm, intercom, jobright, kraken, lamborghini, linear.app, lovable, mastercard, mercury, meta, minimax, mintlify, miro, mistral.ai, mongodb, mydealz, nerdwallet, nike, nintendo-2001, notion, nvidia, ollama, opencode.ai, oracle, oura, pinterest, playstation, posthog, raycast, renault, replicate, resend, revolut, runwayml, sanity, sap, sentry, shopify, slack, spacex, spotify, starbucks, stripe, supabase, superhuman, tesla, theverge, together.ai, uber, vercel, vodafone, voltagent, warp, webflow, wired, wise, x.ai, zapier

To see one file's summary: `grep -m1 '^description:' designs/<name>/DESIGN.md`

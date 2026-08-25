#!/usr/bin/env bash
# Re-fetch the upstream awesome-list READMEs and rebuild catalogs/*.tsv.
#
# The upstream lists change daily, so rerun this whenever the catalogs feel
# stale (`scripts/catalog.py list` prints each one's build time).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="${CATALOG_CACHE:-$(mktemp -d)}"

fetch() {
  local repo="$1" branch="$2" dest="$3"
  local url="https://raw.githubusercontent.com/${repo}/${branch}/README.md"
  echo "fetching ${repo}@${branch}"
  if ! curl -fsSL --retry 3 --retry-delay 2 "$url" -o "${CACHE}/${dest}"; then
    echo "  failed: $url" >&2
    return 1
  fi
}

mkdir -p "$CACHE"
fetch ripienaar/free-for-dev        master "ripienaar_free-for-dev.README.md"
fetch public-apis/public-apis       master "public-apis_public-apis.README.md"
fetch punkpeye/awesome-mcp-servers  master "punkpeye_awesome-mcp-servers.README.md"

python3 "${ROOT}/scripts/build_catalogs.py" --cache "$CACHE" --out "${ROOT}/catalogs"
echo "catalogs rebuilt in ${ROOT}/catalogs"

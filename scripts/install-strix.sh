#!/usr/bin/env bash
# Install the Strix AI pentesting CLI (https://github.com/usestrix/strix).
#
# Strix runs its agents inside a Docker sandbox and needs an LLM API key.
# This script installs the CLI and checks the prerequisites; it never starts
# a scan. Only ever point Strix at systems you own or are authorized to test.
set -euo pipefail

echo "==> Checking prerequisites"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: Docker is not installed. Strix runs its sandbox in Docker." >&2
  echo "       https://docs.docker.com/get-docker/" >&2
  exit 1
fi
if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker is installed but not running. Start it and re-run." >&2
  exit 1
fi
echo "    docker: ok"

if command -v strix >/dev/null 2>&1; then
  echo "==> Strix already installed: $(command -v strix)"
else
  echo "==> Installing Strix"
  if command -v pipx >/dev/null 2>&1; then
    # pipx keeps strix-agent isolated from the rest of your Python env.
    pipx install strix-agent
  elif command -v uv >/dev/null 2>&1; then
    uv tool install strix-agent
  else
    echo "    no pipx/uv found; using the upstream installer"
    curl -fsSL --retry 3 https://strix.ai/install | bash
  fi
fi

echo
echo "==> Configuration"
missing=0
if [ -z "${STRIX_LLM:-}" ]; then
  echo "    STRIX_LLM is unset. Pick a model, e.g.:"
  echo "      export STRIX_LLM=\"anthropic/claude-sonnet-4-6\""
  missing=1
fi
if [ -z "${LLM_API_KEY:-}" ]; then
  echo "    LLM_API_KEY is unset:  export LLM_API_KEY=\"...\""
  missing=1
fi
[ "$missing" -eq 0 ] && echo "    STRIX_LLM and LLM_API_KEY are set"

echo
echo "Optional:"
echo "  export PERPLEXITY_API_KEY=...     # enables the agent's search tooling"
echo "  export STRIX_REASONING_EFFORT=high"
echo "  ~/.strix/mcp-servers.json         # expose your MCP servers to Strix agents"
echo
echo "Strix caches config to ~/.strix/cli-config.json after the first run."
echo "First scan:   strix --target ./some-app-directory"
echo "Read results: strix view"
echo
echo "REMINDER: Strix actively attacks its target. Only run it against systems"
echo "you own or have explicit written permission to test."

#!/usr/bin/env bash
# Refresh the fallback release links on the landing page (the page resolves the latest
# release itself at load time via static/latest-release.js) and check every binary exists.
# Usage: scripts/bump-release.sh v0.12.3
set -euo pipefail
new="${1:?usage: $0 vX.Y.Z}"
cd "$(dirname "$0")/.."
old=$(grep -o -m1 'releases/download/v[0-9.]*' content/index.md | sed 's#.*/##')
sed -i "s/$old/$new/g" content/index.md
echo "index.md: $old -> $new"
grep -o "https://github.com/SciQLop/SciQLop/releases/download/[^\"]*" content/index.md | while read -r url; do
  printf '%s %s\n' "$(curl -sIL -o /dev/null -w '%{http_code}' "$url")" "${url##*/}"
done
echo "Now add a section to content/whats-new.md and move any 'coming in' items into it."

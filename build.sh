#!/bin/bash
# Build a write-up from drafts/<name>.md into writeups/<name>.html
#
#   ./build.sh <name>              public write-up (retired box, research, tutorial)
#   ./build.sh <name> '<password>' encrypted write-up (active box)
#
# Needs: pandoc, and staticrypt for encrypted builds (npm i -g staticrypt)
set -euo pipefail
cd "$(dirname "$0")"

NAME=${1:?usage: ./build.sh <name> [password]}
PASS=${2:-}
SRC="drafts/$NAME.md"
TMP="$NAME.tmp.html"
OUT="writeups/$NAME.html"
[ -f "$SRC" ] || { echo "Missing $SRC"; exit 1; }

TITLE=$(grep -m1 '^# ' "$SRC" | sed 's/^# //')
pandoc "$SRC" -o "$TMP" --standalone --template templates/writeup.html \
  --metadata title="$TITLE" --highlight-style=breezedark

if [ -n "$PASS" ]; then
  mkdir -p .enc
  staticrypt "$TMP" -p "$PASS" --short -d .enc \
    --template-title "$TITLE" \
    --template-color-primary "#a855f7" --template-color-secondary "#000000"
  mv ".enc/$TMP" "$OUT"
  rmdir .enc
else
  mv "$TMP" "$OUT"
fi
rm -f "$TMP"
echo "Built $OUT$( [ -n "$PASS" ] && echo ' (encrypted)')"

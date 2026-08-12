#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOK_DIR="$ROOT/books/local-only/81-How-Logic-Works-Hans-Halvorson"
ZIP="$BOOK_DIR/logic-works-main.zip"
SRC_DIR="$BOOK_DIR/logic-works-main"
OUT="$BOOK_DIR/81-How-Logic-Works-Hans-Halvorson.pdf"

if [[ ! -f "$ZIP" ]]; then
    echo "Source archive not found: $ZIP"
    echo "Run: python3 scripts/sync_books.py --scope local-only"
    exit 1
fi

for cmd in unzip latexmk; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Missing command: $cmd"
        echo "Install a sufficiently complete TeX Live distribution plus unzip, then retry."
        exit 1
    fi
done

rm -rf "$SRC_DIR"
unzip -q "$ZIP" -d "$BOOK_DIR"

cd "$SRC_DIR"

# The author's source uses tufte-book, glossaries, TikZ and svg-related packages.
# -shell-escape is enabled because some TeX installations require it for SVG handling.
latexmk -pdf -shell-escape -interaction=nonstopmode -halt-on-error main.tex

cp -f main.pdf "$OUT"
echo "Built: $OUT"
echo "This output is local-only. Do not commit it to the public repository."

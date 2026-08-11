#!/usr/bin/env python3
"""Download legally available ebook files into the local BookList checkout.

The repository is public, so files are split into two groups:

- books/public-domain/: files confirmed as public domain / redistributable.
- books/local-only/: files offered for official free download but not confirmed
  redistributable. This directory is ignored by Git and is intended only for
  the user's local checkout.

This script intentionally does not download borrow-only, preview-only, or
purchase-only books.
"""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BOOKS = [
    {
        "id": 40,
        "title": "Reminiscences of a Stock Operator",
        "author": "Edwin Lefevre",
        "scope": "public-domain",
        "url": "https://www.gutenberg.org/ebooks/60979.epub3.images",
        "dest": "books/public-domain/40-Reminiscences-of-a-Stock-Operator.epub",
        "source": "Project Gutenberg",
    },
    {
        "id": 54,
        "title": "The Crowd: A Study of the Popular Mind",
        "author": "Gustave Le Bon",
        "scope": "public-domain",
        "url": "https://www.gutenberg.org/ebooks/445.epub3.images",
        "dest": "books/public-domain/54-The-Crowd.epub",
        "source": "Project Gutenberg",
    },
    {
        "id": 80,
        "title": "Geography and World Power",
        "author": "James Fairgrieve",
        "scope": "public-domain",
        "url": "https://archive.org/download/geographyworldpo00fairrich/geographyworldpo00fairrich.pdf",
        "dest": "books/public-domain/80-Geography-and-World-Power.pdf",
        "source": "Internet Archive",
    },
    {
        "id": 62,
        "title": "America's Great Depression",
        "author": "Murray N. Rothbard",
        "scope": "local-only",
        "url": "https://cdn.mises.org/Americas%20Great%20Depression_3.epub",
        "dest": "books/local-only/62-Americas-Great-Depression.epub",
        "source": "Mises Institute",
    },
]


def download(book: dict[str, object], force: bool = False) -> bool:
    dest = ROOT / str(book["dest"])
    if dest.exists() and not force:
        print(f"[skip] {dest.relative_to(ROOT)} already exists")
        return True

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")

    request = urllib.request.Request(
        str(book["url"]),
        headers={"User-Agent": "BookList/1.0 (+personal ebook sync)"},
    )

    print(f"[download] {book['title']} <- {book['source']}")
    try:
        with urllib.request.urlopen(request, timeout=60) as response, tmp.open("wb") as out:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        tmp.replace(dest)
        print(f"[ok] {dest.relative_to(ROOT)} ({dest.stat().st_size / 1024 / 1024:.2f} MiB)")
        return True
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        if tmp.exists():
            tmp.unlink()
        print(f"[failed] {book['title']}: {exc}", file=sys.stderr)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync legally available ebooks into BookList")
    parser.add_argument(
        "--scope",
        choices=("all", "public-domain", "local-only"),
        default="all",
        help="which group to download (default: all)",
    )
    parser.add_argument("--force", action="store_true", help="overwrite files that already exist")
    args = parser.parse_args()

    selected = [b for b in BOOKS if args.scope == "all" or b["scope"] == args.scope]
    failures = 0
    for book in selected:
        if not download(book, force=args.force):
            failures += 1

    print(f"\nDone: {len(selected) - failures}/{len(selected)} downloads succeeded.")
    if args.scope in ("all", "local-only"):
        print("Note: books/local-only/ is intentionally excluded from Git commits.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

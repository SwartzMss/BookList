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
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "BookList/1.1 (+personal ebook sync)"

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
        "id": 47,
        "title": "General Economic History",
        "author": "Max Weber; translated by Frank H. Knight",
        "scope": "public-domain",
        "archive_item": "in.ernet.dli.2015.275058",
        "archive_ext": ".pdf",
        "archive_keywords": ["general", "economic", "history"],
        "dest": "books/public-domain/47-General-Economic-History-Max-Weber-1927-en.pdf",
        "source": "Internet Archive (1927 English edition; linked by Wikisource)",
    },
    {
        "id": 47,
        "title": "Wirtschaftsgeschichte",
        "author": "Max Weber",
        "scope": "public-domain",
        "url": "https://archive.org/download/wirtschaftsgesch00webe/wirtschaftsgesch00webe.pdf",
        "dest": "books/public-domain/47-Wirtschaftsgeschichte-Max-Weber-1923-de.pdf",
        "source": "Internet Archive / Open Library",
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
        "id": 18,
        "title": "The Federal Reserve and the Financial Crisis - Lecture 1",
        "author": "Ben S. Bernanke",
        "scope": "local-only",
        "url": "https://www.federalreserve.gov/newsevents/files/bernanke-lecture-one-20120320.pdf",
        "dest": "books/local-only/18-Federal-Reserve-and-Financial-Crisis/lecture-1-origins-and-mission.pdf",
        "source": "Federal Reserve Board",
    },
    {
        "id": 18,
        "title": "The Federal Reserve and the Financial Crisis - Lecture 2",
        "author": "Ben S. Bernanke",
        "scope": "local-only",
        "url": "https://www.federalreserve.gov/newsevents/files/bernanke-lecture-two-20120322.pdf",
        "dest": "books/local-only/18-Federal-Reserve-and-Financial-Crisis/lecture-2-after-world-war-II.pdf",
        "source": "Federal Reserve Board",
    },
    {
        "id": 18,
        "title": "The Federal Reserve and the Financial Crisis - Lecture 3",
        "author": "Ben S. Bernanke",
        "scope": "local-only",
        "url": "https://www.federalreserve.gov/newsevents/files/bernanke-lecture-three-20120327.pdf",
        "dest": "books/local-only/18-Federal-Reserve-and-Financial-Crisis/lecture-3-response-to-financial-crisis.pdf",
        "source": "Federal Reserve Board",
    },
    {
        "id": 18,
        "title": "The Federal Reserve and the Financial Crisis - Lecture 4",
        "author": "Ben S. Bernanke",
        "scope": "local-only",
        "url": "https://www.federalreserve.gov/newsevents/files/bernanke-lecture-four-20120329.pdf",
        "dest": "books/local-only/18-Federal-Reserve-and-Financial-Crisis/lecture-4-aftermath-of-crisis.pdf",
        "source": "Federal Reserve Board",
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
    {
        "id": 62,
        "title": "America's Great Depression",
        "author": "Murray N. Rothbard",
        "scope": "local-only",
        "url": "https://cdn.mises.org/Americas%20Great%20Depression_3.pdf",
        "dest": "books/local-only/62-Americas-Great-Depression.pdf",
        "source": "Mises Institute",
    },
]


def request_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def resolve_archive_url(book: dict[str, object]) -> str:
    item = str(book["archive_item"])
    metadata = request_json(f"https://archive.org/metadata/{urllib.parse.quote(item)}")
    files = metadata.get("files", [])
    if not isinstance(files, list):
        raise ValueError(f"Internet Archive item {item} has no file list")

    ext = str(book.get("archive_ext", "")).lower()
    keywords = [str(k).lower() for k in book.get("archive_keywords", [])]
    candidates: list[dict[str, object]] = []
    for entry in files:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name", ""))
        lower_name = name.lower()
        if ext and not lower_name.endswith(ext):
            continue
        candidates.append(entry)

    if not candidates:
        raise ValueError(f"Internet Archive item {item} has no matching {ext or 'file'}")

    def score(entry: dict[str, object]) -> tuple[int, int, int]:
        name = str(entry.get("name", "")).lower()
        keyword_score = sum(1 for keyword in keywords if keyword in name)
        original_score = 1 if str(entry.get("source", "")).lower() == "original" else 0
        try:
            size = int(str(entry.get("size", "0")))
        except ValueError:
            size = 0
        return keyword_score, original_score, size

    chosen = max(candidates, key=score)
    filename = str(chosen["name"])
    print(f"[resolve] archive.org item {item} -> {filename}")
    return f"https://archive.org/download/{urllib.parse.quote(item)}/{urllib.parse.quote(filename)}"


def resolve_url(book: dict[str, object]) -> str:
    if "url" in book:
        return str(book["url"])
    if "archive_item" in book:
        return resolve_archive_url(book)
    raise ValueError(f"No download source configured for {book['title']}")


def download(book: dict[str, object], force: bool = False) -> bool:
    dest = ROOT / str(book["dest"])
    if dest.exists() and not force:
        print(f"[skip] {dest.relative_to(ROOT)} already exists")
        return True

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")

    print(f"[download] {book['title']} <- {book['source']}")
    try:
        url = resolve_url(book)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=90) as response, tmp.open("wb") as out:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
        if tmp.stat().st_size == 0:
            raise OSError("downloaded file is empty")
        tmp.replace(dest)
        print(f"[ok] {dest.relative_to(ROOT)} ({dest.stat().st_size / 1024 / 1024:.2f} MiB)")
        return True
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
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

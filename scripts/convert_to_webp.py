#!/usr/bin/env python3
"""Convert raster images in a folder to WebP.

Usage:
  python3 scripts/convert_to_webp.py static/images
  python3 scripts/convert_to_webp.py media --replace
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.webp import CONVERT_SUFFIXES, convert_path_to_webp  # noqa: E402


def iter_images(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in CONVERT_SUFFIXES:
            files.append(path)
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert JPG/PNG/GIF to WebP")
    parser.add_argument("path", type=Path, help="File or directory")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Delete the original after a successful convert",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files without writing",
    )
    args = parser.parse_args()
    target = args.path.resolve()
    if not target.exists():
        print(f"Not found: {target}", file=sys.stderr)
        return 1

    paths = [target] if target.is_file() else iter_images(target)
    converted = 0
    skipped = 0
    for path in paths:
        if args.dry_run:
            print(f"would convert {path}")
            converted += 1
            continue
        result = convert_path_to_webp(path, replace=args.replace)
        if result is None:
            skipped += 1
            continue
        print(f"{path} -> {result}")
        converted += 1
    print(f"converted={converted} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

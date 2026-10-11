#!/usr/bin/env python3
"""Create a Compound GTM home, or a motion folder inside one, without overwriting anything.

Usage:
  python create_home.py <path> [--with-accounts] [--with-field]
  python create_home.py <home-path> --motion <slug>    # creates motions/<yyyy-mm>-<slug>/
"""
import argparse
import datetime
import re
import shutil
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "references" / "templates"


def copy_if_absent(src: Path, dst: Path, created: list, skipped: list) -> None:
    if dst.exists():
        skipped.append(dst)
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    created.append(dst)


def make_dir(path: Path, created: list, skipped: list) -> None:
    if path.exists():
        skipped.append(path)
    else:
        path.mkdir(parents=True)
        created.append(path)


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "motion"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="Folder for the GTM home (created if missing)")
    parser.add_argument("--with-accounts", action="store_true", help="Add an accounts/ folder for named-account plans")
    parser.add_argument("--with-field", action="store_true", help="Add a field/ folder for raw call notes and transcripts")
    parser.add_argument("--motion", metavar="SLUG", help="Create a dated motion folder inside an existing home")
    args = parser.parse_args()

    home = Path(args.path).expanduser().resolve()
    created, skipped = [], []

    if args.motion:
        if not home.exists():
            print(f"No GTM home at {home}. Create it first.", file=sys.stderr)
            return 1
        folder = home / "motions" / f"{datetime.date.today():%Y-%m}-{slugify(args.motion)}"
        for template in sorted((TEMPLATES / "motion").glob("*.md")):
            copy_if_absent(template, folder / template.name, created, skipped)
        make_dir(folder / "assets", created, skipped)
    else:
        home.mkdir(parents=True, exist_ok=True)
        for template in sorted((TEMPLATES / "home").glob("*.md")):
            copy_if_absent(template, home / template.name, created, skipped)
        make_dir(home / "motions", created, skipped)
        if args.with_accounts:
            make_dir(home / "accounts", created, skipped)
        if args.with_field:
            make_dir(home / "field", created, skipped)

    for path in created:
        print(f"created  {path}")
    for path in skipped:
        print(f"kept     {path} (already existed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

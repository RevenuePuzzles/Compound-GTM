#!/usr/bin/env python3
"""Build and check derived files from the canonical skill.

- commands/cg-<move>.md  : one Claude Code slash command per move, generated from each move's heading
- dist/compound-gtm.zip  : the skill folder, ready to upload to claude.ai (Customize → Skills → Upload a skill)

The skill in skills/compound-gtm/ is the only source of truth. Never edit commands/ or dist/ by hand.

Usage:
  python scripts/build.py           # validate, then regenerate commands/ and dist/
  python scripts/build.py --check   # validate and confirm commands/ and dist/ are up to date (CI)
"""
import argparse
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "compound-gtm"
MOVES = SKILL / "references" / "moves"
COMMANDS = ROOT / "commands"
DIST = ROOT / "dist"
ARCHIVE = DIST / "compound-gtm.zip"

HEADING = re.compile(r"^#\s+([a-z-]+)\s+—\s+(.+)$")
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ZIP_DATE = (1980, 1, 1, 0, 0, 0)  # fixed, so rebuilding an unchanged skill gives an identical archive

COMMAND_TEMPLATE = """---
description: {description}
argument-hint: {hint}
---

Use the compound-gtm skill. Read `references/context-contract.md`, `references/evidence.md` and `references/moves/{move}.md` from the skill, then run the **{move}** move on the input below. Load only the GTM home files the move needs.

$ARGUMENTS
"""

FRONT_DOOR = """---
description: Compound GTM front door — describe the GTM work and it routes to the smallest useful move.
argument-hint: what you're working on, or paste material
---

Use the compound-gtm skill. Read its SKILL.md and `references/context-contract.md`, find the starting point (material in hand, an existing GTM home, or nothing yet), and route by outcome to the smallest useful move. End substantial work by offering the compound step.

$ARGUMENTS
"""

HINTS = {
    "buyer": "paste the email, page or post (and the target role, if not in the GTM home)",
    "cfo": "paste the proposal, business case or ROI claim",
    "rival": "paste the material, and name the competitor or alternative",
    "inbox": "paste the email or message",
    "committee": "paste the proposal, deck or positioning",
    "sequence": "role, situation or motion name",
    "asset": "asset type and goal",
    "results": "attach or paste the results data",
    "winloss": "attach deal data or interview notes",
    "signals": "attach or paste calls, replies or reviews",
    "discovery": "company or prospect name, plus anything you know",
    "compound": "the lesson to save, or leave empty to collect from this session",
}


# ── generation ──────────────────────────────────────────────────────────────


def move_files() -> list:
    return sorted(MOVES.glob("*.md"))


def expected_commands() -> dict:
    """Map of command filename → content, generated from the move files."""
    commands = {}
    for move_file in move_files():
        match = HEADING.match(move_file.read_text(encoding="utf-8").splitlines()[0])
        if not match:
            continue  # reported by check_moves
        move, purpose = match.groups()
        description = purpose[0].upper() + purpose[1:]
        hint = HINTS.get(move, "what you're working on")
        commands[f"cg-{move}.md"] = COMMAND_TEMPLATE.format(description=description, hint=hint, move=move)
    commands["cg-desk.md"] = FRONT_DOOR
    return commands


def skill_files() -> list:
    return [
        path
        for path in sorted(SKILL.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store"
    ]


def archive_name(path: Path) -> str:
    return (Path("compound-gtm") / path.relative_to(SKILL)).as_posix()


def build_commands() -> int:
    COMMANDS.mkdir(exist_ok=True)
    for old in COMMANDS.glob("cg-*.md"):
        old.unlink()
    commands = expected_commands()
    for name, content in commands.items():
        (COMMANDS / name).write_text(content, encoding="utf-8")
    return len(commands)


def build_zip() -> Path:
    DIST.mkdir(exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in skill_files():
            info = zipfile.ZipInfo(archive_name(path), date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if path.suffix == ".py" else 0o644) << 16
            archive.writestr(info, path.read_bytes())
    return ARCHIVE


# ── validation ──────────────────────────────────────────────────────────────


def check_frontmatter(errors: list) -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if not text.startswith("---") or len(parts) < 3:
        errors.append("SKILL.md: missing YAML frontmatter")
        return
    fields = {}
    for line in parts[1].strip().splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    if set(fields) != {"name", "description"}:
        errors.append(f"SKILL.md: frontmatter should hold only name and description, found {sorted(fields)}")
    name, description = fields.get("name", ""), fields.get("description", "")
    if not NAME.match(name) or len(name) > 64:
        errors.append(f"SKILL.md: name '{name}' must be lowercase words joined by hyphens, max 64 characters")
    if name != SKILL.name:
        errors.append(f"SKILL.md: name '{name}' must match its folder '{SKILL.name}'")
    if not description or len(description) > 1024:
        errors.append(f"SKILL.md: description must be 1–1024 characters, is {len(description)}")
    if "<" in description or ">" in description:
        errors.append("SKILL.md: description must not contain angle brackets")


def check_moves(errors: list) -> None:
    moves = set()
    for move_file in move_files():
        first = move_file.read_text(encoding="utf-8").splitlines()[0]
        match = HEADING.match(first)
        if not match or match.group(1) != move_file.stem:
            errors.append(f"{move_file.relative_to(ROOT)}: first line must be '# {move_file.stem} — purpose'")
        moves.add(move_file.stem)

    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    table = skill.split("## Route by outcome", 1)[-1].split("Common compositions", 1)[0]
    routed = set(re.findall(r"`([a-z-]+)`", table))
    for move in sorted(moves - routed):
        errors.append(f"SKILL.md: move '{move}' has a file but no row in the routing table")
    for move in sorted(routed - moves):
        errors.append(f"SKILL.md: routing table names '{move}' but references/moves/{move}.md is missing")

    for doc in (SKILL / "SKILL.md", ROOT / "README.md", ROOT / "ARCHITECTURE.md"):
        for count in re.findall(r"\b(\d+) moves\b", doc.read_text(encoding="utf-8")):
            if int(count) != len(moves):
                errors.append(f"{doc.relative_to(ROOT)}: says '{count} moves', there are {len(moves)}")


def check_versions(errors: list) -> None:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    changelog = re.search(r"^## (\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.M)
    versions = {
        "plugin.json": plugin.get("version"),
        "marketplace.json metadata": market.get("metadata", {}).get("version"),
        "CHANGELOG.md": changelog.group(1) if changelog else None,
    }
    for entry in market.get("plugins", []):
        versions[f"marketplace.json plugin '{entry.get('name')}'"] = entry.get("version")
    if len(set(versions.values())) != 1:
        errors.append("versions disagree: " + ", ".join(f"{k}={v}" for k, v in versions.items()))


def check_links(errors: list) -> None:
    """Relative links and image paths in the repo's Markdown must point at real files."""
    pattern = re.compile(r"\]\(([^)\s]+)\)|(?:src|srcset)=\"([^\"]+)\"")
    for doc in sorted(ROOT.rglob("*.md")):
        if ".git" in doc.parts or doc.parent == COMMANDS:
            continue
        for match in pattern.finditer(doc.read_text(encoding="utf-8")):
            target = (match.group(1) or match.group(2)).split("#", 1)[0].split("?", 1)[0]
            if not target or re.match(r"^[a-z]+:", target):
                continue
            if not (doc.parent / target).exists():
                errors.append(f"{doc.relative_to(ROOT)}: broken link '{target}'")


def check_outputs(errors: list) -> None:
    """--check: generated files must match what the build would write."""
    expected = expected_commands()
    actual = {path.name: path.read_text(encoding="utf-8") for path in COMMANDS.glob("cg-*.md")}
    for name in sorted(set(expected) | set(actual)):
        if expected.get(name) != actual.get(name):
            errors.append(f"commands/{name} is out of date — run python scripts/build.py")
    if not ARCHIVE.exists():
        errors.append("dist/compound-gtm.zip is missing — run python scripts/build.py")
        return
    with zipfile.ZipFile(ARCHIVE) as archive:
        packed = {name: archive.read(name) for name in archive.namelist()}
    source = {archive_name(path): path.read_bytes() for path in skill_files()}
    if packed != source:
        errors.append("dist/compound-gtm.zip does not match skills/compound-gtm/ — run python scripts/build.py")


def validate(check_generated: bool) -> list:
    errors = []
    check_frontmatter(errors)
    check_moves(errors)
    check_versions(errors)
    check_links(errors)
    if check_generated:
        check_outputs(errors)
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate only; fail if generated files are stale")
    args = parser.parse_args()

    problems = validate(check_generated=args.check)
    if problems:
        print("\n".join(f"✗ {problem}" for problem in problems), file=sys.stderr)
        sys.exit(1)
    if args.check:
        print(f"✓ skill, {len(move_files())} moves, manifests, links and generated files all check out")
        sys.exit(0)

    count = build_commands()
    archive = build_zip()
    print(f"{count} commands written to {COMMANDS.relative_to(ROOT)}/")
    print(f"skill archive: {archive.relative_to(ROOT)}")

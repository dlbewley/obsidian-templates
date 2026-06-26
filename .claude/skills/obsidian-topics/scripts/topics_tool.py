#!/usr/bin/env python3
"""Maintain `Topics:` frontmatter across an Obsidian vault.

Subcommands:
  list-topics                       — print every topic page under Topics/
  scan [filters]                    — survey notes; report missing/empty/bare-word
  normalize [filters] [--dry-run]   — rewrite bare-word wikilinks to Topics/Foo
  add-topics --file PATH --topics "A,B"  — add or extend a Topics block

The script auto-detects the vault root by walking up from the current directory
until it finds a `Topics/` folder. Override with --vault.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

FM_RE = re.compile(r"^(---\n)(.*?)(\n---\n)", re.DOTALL)
TOPICS_LIST_RE = re.compile(
    r"(^Topics:\s*\n)((?:[ \t]+-\s+.*(?:\n|$))+)", re.MULTILINE | re.IGNORECASE
)
TOPICS_INLINE_RE = re.compile(r"^Topics:\s*(.*)$", re.MULTILINE | re.IGNORECASE)
CONTENTTYPE_RE = re.compile(r"^contenttype:\s*(\S+)\s*$", re.MULTILINE | re.IGNORECASE)
WIKILINK_LINE_RE = re.compile(r'^(\s*-\s*"?)\[\[([^\]]+)\]\]("?\s*)$')

EXCLUDE_DIRS = {".claude", ".obsidian", ".trash", ".git", "node_modules"}


def find_vault_root(start: Path) -> Path:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "Topics").is_dir():
            return candidate
    raise SystemExit(f"could not locate a Topics/ folder above {start}")


def iter_md_files(vault: Path):
    for path in vault.rglob("*.md"):
        rel = path.relative_to(vault)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        yield path


def load_topics(vault: Path) -> set[str]:
    return {p.stem for p in (vault / "Topics").glob("*.md")}


@dataclass
class NoteState:
    path: Path
    contenttype: str | None
    has_topics_field: bool
    topics_kind: str  # "missing" | "empty" | "list" | "inline"
    entries: list[str]  # raw wikilink targets, e.g. "Topics/AI" or "Networking"

    @property
    def bare_entries(self) -> list[str]:
        return [e for e in self.entries if "/" not in e]


def parse_note(path: Path) -> NoteState | None:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    m = FM_RE.match(text)
    if not m:
        return None
    fm = m.group(2)
    ct_match = CONTENTTYPE_RE.search(fm)
    ct = ct_match.group(1) if ct_match else None

    list_match = TOPICS_LIST_RE.search(fm)
    if list_match:
        entries = []
        for line in list_match.group(2).split("\n"):
            wm = WIKILINK_LINE_RE.match(line)
            if wm:
                entries.append(wm.group(2))
        return NoteState(path, ct, True, "list", entries)

    inline_match = TOPICS_INLINE_RE.search(fm)
    if inline_match:
        val = inline_match.group(1).strip()
        if val in ("", "[]", "~", "null"):
            return NoteState(path, ct, True, "empty", [])
        # inline non-empty (e.g. `Topics: [[Foo]]`) — extract any wikilinks
        entries = [m_.group(1) for m_ in re.finditer(r"\[\[([^\]]+)\]\]", val)]
        return NoteState(path, ct, True, "inline", entries)

    return NoteState(path, ct, False, "missing", [])


def matches_filter(state: NoteState, rel: Path, contenttype: str | None, path_glob: str | None) -> bool:
    if contenttype and (state.contenttype or "").lower() != contenttype.lower():
        return False
    if path_glob and not fnmatch(str(rel), path_glob):
        return False
    return True


def cmd_list_topics(vault: Path, args: argparse.Namespace) -> int:
    for name in sorted(load_topics(vault)):
        print(name)
    return 0


def cmd_scan(vault: Path, args: argparse.Namespace) -> int:
    available = load_topics(vault)
    rows = []
    for path in iter_md_files(vault):
        state = parse_note(path)
        if not state:
            continue
        rel = path.relative_to(vault)
        if not matches_filter(state, rel, args.contenttype, args.path):
            continue
        bare = state.bare_entries
        unknown_bare = [b for b in bare if b not in available]
        unknown_prefixed = [
            e for e in state.entries if "/" in e and e.split("/", 1)[1] not in available
        ]
        rows.append(
            {
                "path": str(rel),
                "contenttype": state.contenttype,
                "topics_kind": state.topics_kind,
                "entries": state.entries,
                "bare_entries": bare,
                "unknown_bare": unknown_bare,
                "unknown_prefixed": unknown_prefixed,
            }
        )

    if args.json:
        json.dump(rows, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0

    missing = [r for r in rows if r["topics_kind"] in ("missing", "empty")]
    bare = [r for r in rows if r["bare_entries"]]
    unknown = [r for r in rows if r["unknown_bare"] or r["unknown_prefixed"]]

    print(f"scanned: {len(rows)} notes")
    print(f"  missing/empty Topics: {len(missing)}")
    print(f"  with bare-word entries: {len(bare)}")
    print(f"  referencing unknown topics: {len(unknown)}")

    if missing and args.show_missing:
        print("\nmissing/empty Topics:")
        for r in missing:
            print(f"  [{r['contenttype']}] {r['path']}")

    if bare and args.show_bare:
        print("\nbare-word entries (would normalize):")
        for r in bare:
            print(f"  {r['path']}: {r['bare_entries']}")

    if unknown:
        print("\nlinks to topics with no Topics/<Name>.md (review manually):")
        for r in unknown:
            items = (r["unknown_bare"] or []) + (r["unknown_prefixed"] or [])
            print(f"  {r['path']}: {items}")

    return 0


def rewrite_topics_block(block: str, available: set[str]) -> tuple[str, int]:
    out = []
    changed = 0
    for line in block.split("\n"):
        wm = WIKILINK_LINE_RE.match(line)
        if wm:
            prefix, target, suffix = wm.group(1), wm.group(2), wm.group(3)
            if "/" not in target and target.strip() and target in available:
                out.append(f"{prefix}[[Topics/{target}]]{suffix}")
                changed += 1
                continue
        out.append(line)
    return "\n".join(out), changed


def cmd_normalize(vault: Path, args: argparse.Namespace) -> int:
    available = load_topics(vault)
    total_files = 0
    total_links = 0
    skipped_unknown: list[tuple[str, str]] = []

    for path in iter_md_files(vault):
        state = parse_note(path)
        if not state:
            continue
        rel = path.relative_to(vault)
        if not matches_filter(state, rel, args.contenttype, args.path):
            continue

        text = path.read_text(encoding="utf-8")
        fmm = FM_RE.match(text)
        if not fmm:
            continue
        fm = fmm.group(2)
        list_match = TOPICS_LIST_RE.search(fm)
        if not list_match:
            continue
        new_block, n = rewrite_topics_block(list_match.group(2), available)
        if n == 0:
            for b in state.bare_entries:
                if b not in available:
                    skipped_unknown.append((str(rel), b))
            continue
        if args.dry_run:
            print(f"would update {rel}: {n} link(s)")
            total_files += 1
            total_links += n
            continue

        new_fm = fm[: list_match.start(2)] + new_block + fm[list_match.end(2):]
        new_text = fmm.group(1) + new_fm + fmm.group(3) + text[fmm.end():]
        path.write_text(new_text, encoding="utf-8")
        print(f"updated {rel}: {n} link(s)")
        total_files += 1
        total_links += n

    verb = "would change" if args.dry_run else "changed"
    print(f"\n{verb} {total_links} link(s) across {total_files} file(s)")
    if skipped_unknown:
        print("\nbare-word entries with no matching Topics/<Name>.md (left alone):")
        for rel, target in skipped_unknown:
            print(f"  {rel}: [[{target}]]")
    return 0


def cmd_add_topics(vault: Path, args: argparse.Namespace) -> int:
    available = load_topics(vault)
    requested = [t.strip() for t in args.topics.split(",") if t.strip()]
    unknown = [t for t in requested if t not in available]
    if unknown:
        print(f"refusing: these topics have no Topics/<Name>.md: {unknown}", file=sys.stderr)
        return 2

    path = Path(args.file)
    if not path.is_absolute():
        path = (vault / path).resolve()
    text = path.read_text(encoding="utf-8")
    fmm = FM_RE.match(text)
    if not fmm:
        print(f"no frontmatter in {path}", file=sys.stderr)
        return 2
    fm = fmm.group(2)

    list_match = TOPICS_LIST_RE.search(fm)
    if list_match:
        existing_targets = set()
        for line in list_match.group(2).split("\n"):
            wm = WIKILINK_LINE_RE.match(line)
            if wm:
                t = wm.group(2)
                existing_targets.add(t.split("/", 1)[1] if "/" in t else t)
        additions = [t for t in requested if t not in existing_targets]
        if not additions:
            print(f"no changes: {path.name} already has {sorted(existing_targets)}")
            return 0
        block = list_match.group(2)
        if not block.endswith("\n"):
            block += "\n"
        block += "".join(f'  - "[[Topics/{t}]]"\n' for t in additions)
        new_fm = fm[: list_match.start(2)] + block + fm[list_match.end(2):]
    else:
        # No Topics block yet — insert one. Prefer placement before `contenttype:`,
        # else after `tags:` block, else at the end of the frontmatter.
        new_block_lines = ["Topics:"]
        new_block_lines.extend(f'  - "[[Topics/{t}]]"' for t in requested)
        new_block = "\n".join(new_block_lines) + "\n"

        ct_match = CONTENTTYPE_RE.search(fm)
        if ct_match:
            insert_at = ct_match.start()
        else:
            # try after tags: list
            tag_match = re.search(
                r"(^tags:\s*\n(?:[ \t]+-\s+.*\n)+)", fm, re.MULTILINE | re.IGNORECASE
            )
            if tag_match:
                insert_at = tag_match.end()
            else:
                insert_at = len(fm)
                if not fm.endswith("\n"):
                    new_block = "\n" + new_block
        new_fm = fm[:insert_at] + new_block + fm[insert_at:]

    new_text = fmm.group(1) + new_fm + fmm.group(3) + text[fmm.end():]
    path.write_text(new_text, encoding="utf-8")
    print(f"updated {path.relative_to(vault)}: {requested}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--vault", type=Path, help="vault root (default: auto-detect upward)")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-topics", help="print all topics under Topics/")

    s = sub.add_parser("scan", help="survey notes and report Topics state")
    s.add_argument("--contenttype", help="filter to this contenttype (e.g. Repo)")
    s.add_argument("--path", help="filter to vault-relative paths matching this glob")
    s.add_argument("--json", action="store_true", help="emit JSON instead of a summary")
    s.add_argument("--show-missing", action="store_true", help="list paths with missing/empty Topics")
    s.add_argument("--show-bare", action="store_true", help="list bare-word entries that would normalize")

    n = sub.add_parser("normalize", help="rewrite [[Foo]] -> [[Topics/Foo]] where Topics/Foo.md exists")
    n.add_argument("--contenttype")
    n.add_argument("--path")
    n.add_argument("--dry-run", action="store_true")

    a = sub.add_parser("add-topics", help="add a Topics block (or extend an existing one) for a single note")
    a.add_argument("--file", required=True, help="path to the note (absolute or vault-relative)")
    a.add_argument("--topics", required=True, help="comma-separated topic names (must exist under Topics/)")

    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    vault = (args.vault.resolve() if args.vault else find_vault_root(Path.cwd()))
    if not (vault / "Topics").is_dir():
        raise SystemExit(f"{vault} has no Topics/ folder")

    dispatch = {
        "list-topics": cmd_list_topics,
        "scan": cmd_scan,
        "normalize": cmd_normalize,
        "add-topics": cmd_add_topics,
    }
    return dispatch[args.cmd](vault, args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

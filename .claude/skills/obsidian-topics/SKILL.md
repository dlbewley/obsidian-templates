---
name: obsidian-topics
description: Populate empty Topics frontmatter and refine existing Topics in Obsidian notes. Use this skill whenever the user wants to add, fix, normalize, prefix, suggest, refine, or audit the `Topics:` property in Obsidian note frontmatter — including phrases like "add topics to these notes", "fix my topic links", "normalize Topics", "find notes missing Topics", "populate empty topics", "suggest topics for X", or any reference to bare-word topic wikilinks vs. `[[Topics/Foo]]` form. Also use when the user references filtering by `contentType` (Repo, Web, Mail, Meeting, Blog, Note, etc.) and asks for any Topics-related change. Only assigns Topics that already exist as files in the vault's `Topics/` directory.
---

# Obsidian Topics

Maintain the `Topics:` frontmatter property in an Obsidian vault. Two workflows:

1. **Normalize** — bare-word wikilinks like `[[Networking]]` become `[[Topics/Networking]]` so every Topic link resolves to the same canonical page. Deterministic; run the script.
2. **Populate / refine** — for notes whose `Topics:` is missing, empty, or sparse, read the note and assign Topics drawn from the existing `Topics/` directory. Requires judgment; do this per-note.

## Vault conventions

The skill assumes the standard layout in this vault:

- A `Topics/` folder at the vault root containing one `.md` file per topic (`Topics/AI.md`, `Topics/Networking.md`, ...). These files **define the universe of valid topics**. Never invent a Topic that has no file.
- Notes use YAML frontmatter delimited by `---`.
- `Topics:` is a YAML list of wikilinks in the form `  - "[[Topics/Foo]]"` (double-quoted, two-space indent). Match this exact format when writing new entries.
- Conventional ordering places `Topics:` after `tags:` and before `contenttype:`. Insert new blocks in that slot.
- The frontmatter key is literally `Topics` (capital T). The skill is case-insensitive when scanning, but writes `Topics:`.
- `contenttype:` (lowercase) is the usual filter dimension: `Repo`, `Web`, `Mail`, `Meeting`, `Blog`, `Note`, `Book`, etc.

Confirm these conventions hold by listing `Topics/` and reading 1-2 representative notes before making changes. If the vault diverges, adapt rather than forcing the script.

## The tool

`scripts/topics_tool.py` provides the deterministic operations. It auto-detects the vault root by walking up from the current directory until it finds a `Topics/` folder, or accepts `--vault <path>`. Run with `python3` — no dependencies beyond the standard library.

Subcommands:

- `list-topics` — print every topic name available in `Topics/`. Use this to ground assignments.
- `scan [--contenttype X] [--path GLOB]` — survey all matching notes and report, per note: whether Topics is missing/empty/list, the current entries, and which entries are bare-word (would be rewritten). Output is a JSON or table summary.
- `normalize [--contenttype X] [--path GLOB] [--dry-run]` — rewrite bare-word wikilinks in `Topics:` blocks to `[[Topics/Foo]]` form, but only when `Topics/Foo.md` exists. Skips entries that already have a `/` in the link target. Idempotent: re-running on already-normalized notes is a no-op.
- `add-topics --file PATH --topics "Foo,Bar"` — insert a `Topics:` block (or append to an existing one) on a single note, using the canonical format and placement. Refuses to add a topic that has no file in `Topics/`.

Always run `--dry-run` first on bulk normalization so the user can see what will change. Show the diff or summary before applying.

## Workflow: normalize bare-word links

When the user wants to "fix" or "normalize" Topics links:

1. `python3 scripts/topics_tool.py list-topics` to confirm the available set.
2. `python3 scripts/topics_tool.py scan --contenttype <X>` (or no filter for vault-wide) to see what would change.
3. If anything looks off — e.g., a bare word that has no matching `Topics/Foo.md` — surface it to the user before proceeding; they may want to create the topic page or fix a typo.
4. Run `normalize` with the same filter. Report the count of files changed.
5. Re-scan to confirm no bare-word entries remain.

## Workflow: populate empty Topics

When the user wants to add Topics to notes that lack them:

1. `list-topics` so you have the valid set in working memory.
2. `scan --contenttype <X>` (or other filter) and identify notes with `Topics:` missing, empty (`Topics:` with no items, `Topics: []`, etc.).
3. For each candidate, read the note — at minimum the title, frontmatter `description` if present, and the first ~40 lines of body. For ambiguous notes read more.
4. Pick 1-4 topics from the **existing** `Topics/` list that genuinely match the note's subject. Resist over-tagging; one strong match beats three weak ones. Never invent.
5. Present the proposed assignments as a table (note → topics) and apply them in a batch unless the user has already preapproved the work.
6. Use `add-topics --file PATH --topics "Foo,Bar"` per note, or write the changes in a single Python pass that mirrors `add-topics` logic.

For under-tagged notes (only one Topic when the content clearly spans more), apply the same analysis but propose *additions*, not replacements. Show the before → after.

## Picking topics well

When choosing topics from the available set:

- The note's title and `source`/`description` frontmatter usually decide it. Open the body when the title is generic.
- Prefer specificity. If the note is about OpenShift Virtualization networking, `OpenShift` + `Virtualization` + `Networking` is better than just `OpenShift`.
- Cross-cutting themes (AI, Security, Productivity) earn a Topic when they're load-bearing in the note, not just mentioned in passing.
- Personal-finance, lifestyle, and home topics (Finance, Energy, Cars, Homelab, Nutmeg Rental, Cotter) cluster naturally — don't sprinkle them onto unrelated tech notes.
- Look up the `Topics/Foo.md` page if you're unsure what a topic actually means in this vault — its frontmatter or summary often clarifies scope.

## Safety

- Never write a Topic value that doesn't exist as `Topics/<Name>.md`. The script enforces this for `add-topics`; preserve the same discipline when editing by hand.
- Preserve original frontmatter ordering and quoting style outside the Topics block.
- Skip `.claude/`, `.obsidian/`, and `.trash/` directories.
- Templates (`Templates/*.md`) use `<% %>` syntax; the frontmatter is still real YAML, so the script's normalize step is safe on them, but be cautious adding Topics to a template — it changes every future note created from it.
- For large refactors, dry-run first and confirm the count with the user before writing.

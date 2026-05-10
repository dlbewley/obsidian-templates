---
name: meeting-note-refresh
description: Refresh an existing Obsidian meeting note with newly available recordings, Gemini notes, chat transcripts, or other attachments that landed after the meeting ended. Works on a single note or a date range.
argument-hint: [filename, date, or "last N days" — e.g. "2026-04-20 Red Hat AI Agentic Office Hours", "last 7 days"]
allowed-tools: Bash, Read, Edit, Grep, Glob, mcp__Google_Workspace_MCP__get_events
---

Find calendar attachments that were not present when a meeting note was first created and patch them in. Most recordings, Gemini notes, and chat transcripts are generated hours to days after the meeting ends — this skill closes that gap.

`$ARGUMENTS` may be:
- A specific meeting note filename (with or without `.md`)
- A date (`YYYY-MM-DD`)
- A range ("last 7 days", "this week", "since 2026-04-01")
- Empty → default to **last 14 days**

## Step 1 — Resolve the target set

Build a list of meeting note paths to refresh:
- **Filename given** → just that file
- **Date given** → all `Meetings/<date> *.md`
- **Range given** → all `Meetings/<YYYY-MM-DD> *.md` where the date falls in range
- **Empty** → all meeting notes whose date (from filename) is within the last 14 days

Use `Glob` for `Meetings/*.md` and filter by the date prefix.

## Step 2 — For each note, read current state

Extract from the note:
- `date:` and inferred event date (from filename prefix)
- `recording:` (present or empty)
- Any existing `## 📚 Documents` section (collect URLs already linked)
- `summary:` (for matching)

## Step 3 — Query the calendar

For each note, call `mcp__Google_Workspace_MCP__get_events`:
- `time_min` = start of the meeting date
- `time_max` = end of the meeting date
- `query` = a distinctive keyword from the note title/summary
- `detailed: true`
- `include_attachments: true`

Match the calendar event to the note via:
1. Exact title substring match against the filename
2. Organizer email matches an owner in frontmatter
3. Date match (same day)

Do not guess if there are multiple same-day events with no clear winner — flag and skip.

## Step 4 — Collect new resources

From the matched event, gather:
- `attachments[*].fileUrl` + `title` — anything hosted in Drive
- URLs in the event description that look like recordings (`drive.google.com/file/.../view`), Gemini notes (`docs.google.com/document/...`), chat transcripts (`drive.google.com/file/.../view` with "chat" in name), or running notes docs
- Hangouts link (if the note lacks one)

Categorize each URL:
- **recording** → single `drive.google.com/file/` URL whose title/filename suggests video
- **chat transcript** → drive file titled "Chat" or ".txt"
- **gemini notes** → google doc titled "Notes by Gemini"
- **other docs** → any other linked doc/sheet/slide

## Step 5 — Diff against existing

Compare each collected URL to URLs already present in the note body and the `recording:` frontmatter value. Only enqueue additions that are new.

## Step 6 — Patch the file

Use `Edit`, not `Write`, to preserve the user's manual notes.

**Recording:**
- If `recording:` in frontmatter is empty and we found one, set it.
- If `recording:` is already set and we found a different one, do NOT overwrite — append to the `## 📚 Documents` list instead and flag.

**Documents section:**
- Find the `## 📚 Documents` heading (create one immediately after the `Date:` / header block if missing).
- Append new `- [Name](url)` lines for each new URL, using a clear label ("Chat Transcript", "Notes by Gemini", "Running Meeting Notes", or the attachment title).

Preserve existing bullets. Do not rearrange user-authored content.

## Step 7 — Update calendar_data.json (optional cache)

If `bin/calendar_data.json` exists, add an entry for the date so the batch script `bin/update_meeting_recordings.py` has the same data for future reruns. Structure:

```json
"YYYY-MM-DD": [
  {
    "event_name": "...",
    "match_keywords": ["..."],
    "recording": "...",
    "documents": [{"name": "...", "url": "..."}]
  }
]
```

Merge rather than replace if the date already exists.

## Step 8 — Report

Per-file summary:

```
Refreshed (N):
  ✓ 2026-04-20 Red Hat AI Agentic Office Hours.md
     + recording (frontmatter)
     + Chat Transcript, Notes by Gemini (Documents section)

Unchanged (M):
  - 2026-04-16 OpenShift Virt SME.md  (already complete)

Flagged (K):
  ⚠ 2026-04-15 West OpenShift SSA Tiger Role Meeting.md  (multiple events same day — could not match)
```

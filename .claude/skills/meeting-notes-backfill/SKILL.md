---
name: meeting-notes-backfill
description: Create Obsidian meeting notes for every calendar event in a date range that does not yet have a note. Useful for catching up on a past week or populating the week ahead.
argument-hint: <date range — e.g. "this week", "last week", "2026-04-13 to 2026-04-19", "next 7 days">
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__Google_Workspace_MCP__get_events
---

Create meeting notes for every calendar event in a date range that does not already have a corresponding file under `Meetings/`.

`$ARGUMENTS` describes the range. If empty, default to **last 7 days**.

## Step 1 — Resolve the range

Translate the natural-language range into `time_min` and `time_max` (RFC3339). Use the `currentDate` from system context as "today". Handle:
- "this week" → Mon 00:00 to Sun 23:59 of the current ISO week
- "last week" → previous ISO week
- "next week" → following ISO week
- "next N days" / "last N days" → today ±N
- `YYYY-MM-DD to YYYY-MM-DD` → explicit
- A single `YYYY-MM-DD` → that single day

State the resolved range back to the user before continuing.

## Step 2 — Fetch events

Call `mcp__Google_Workspace_MCP__get_events` with:
- `time_min`, `time_max` as resolved
- `detailed: true`
- `include_attachments: true`
- `max_results: 50`

If the response is very large, re-query a tighter window or split into day-sized chunks to avoid blowing context.

## Step 3 — Filter

Drop events that are:
- Declined, canceled, or marked "Free"
- Blocked time / focus time / OOO
- Events shorter than 15 minutes with no description and no other attendees (likely reminders)
- 1:1 with the user alone (self-events, lunches with no agenda)

Keep the user informed — list what's being skipped and why in the final report.

## Step 4 — Identify existing notes

For each remaining event, extract its date and search for an existing note:

```
Meetings/<YYYY-MM-DD> *.md
```

Read the frontmatter/summary of candidates. If an existing note matches this event (by series, by title keywords, or by overlap of organizer), mark it as "already exists — skip" unless the user explicitly asks to overwrite.

## Step 5 — Create notes

For each event without a note, apply the **`meeting-note-add`** procedure (Steps 4–7 of that skill):
- Look up series parent
- Build frontmatter
- Build body with agenda from description, attachments as Documents
- Write file

Do NOT ask the user to disambiguate each one — this is a bulk operation. Make reasonable defaults and report any cases that you flagged for manual review.

## Step 6 — Report

Print a table or list:

```
Created (N):
  ✓ 2026-04-22 <Event Title>.md  (series: <series or none>)
  ✓ 2026-04-23 <Event Title>.md  (series: none — consider creating a MeetingSeries parent)

Skipped (M):
  - 2026-04-22 <Event Title>  (note already exists)
  - 2026-04-21 Focus Time      (blocked time)

Flagged for review (K):
  ⚠ 2026-04-20 <Event>         (recurring but no MeetingSeries parent — create one?)
```

Summarise in 2–3 lines what the user should do next (usually: run `meeting-note-refresh` in a few days once recordings land).

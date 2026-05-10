---
name: meeting-notes-weekly-cleanup
description: Weekly housekeeping for Obsidian meeting notes — backfill any missing notes from the past week, refresh recordings and attachments on recent notes, and produce a consolidated report. Safe to run on a schedule.
argument-hint: [optional date reference — defaults to the most recent completed ISO week]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__Google_Workspace_MCP__get_events
---

Run the three individual meeting-note skills in sequence against the most recent completed week, then report. This is the skill you schedule.

`$ARGUMENTS` is optional — if the user provides a date or week reference, center the cleanup on that. Otherwise default to **last completed ISO week** (Monday through Sunday) plus the next 7 days.

## Step 1 — Determine the window

Based on `currentDate`:
- **Past window** (for backfill + refresh): the most recent completed Mon–Sun
- **Refresh window** (for stragglers): the past 14 days (covers two weeks of late-arriving recordings)
- **Future window** (for pre-creating upcoming notes): the next 7 days

State all three windows at the start of the run.

## Step 2 — Refresh existing notes (past 14 days)

Invoke the **`meeting-note-refresh`** procedure with `last 14 days`.

Goal: pick up recordings, Gemini notes, chat transcripts that have landed since the original note was created.

## Step 3 — Backfill past week

Invoke the **`meeting-notes-backfill`** procedure with the past-window dates.

Goal: create notes for any meetings from last week that never got one.

## Step 4 — Pre-create next week (optional, ask first)

If `$ARGUMENTS` mentions "ahead", "prep", "upcoming", or the user's weekly cleanup prefs include it, also backfill the next 7 days so templates are ready.

Otherwise skip this step — ask once, remember the answer via the report.

## Step 5 — Consolidated report

Combine the output of Steps 2–4 into a single report with three sections:

```
📼 Refreshed (attachments that landed since last run)
  ✓ ...
  ⚠ ...

📝 Backfilled (notes created for last week)
  ✓ ...
  - skipped: ...

📅 Upcoming (notes pre-created for next week) — if step 4 ran
  ✓ ...

🧹 Summary: X refreshed, Y created, Z flagged for review.
   Next run: <suggested date>
```

## Step 6 — Flag manual follow-up

At the end, enumerate the "flagged" items that need the user's judgment:
- Events that look recurring but have no `MeetingSeries` parent
- Notes where multiple calendar events matched ambiguously
- Events with unusual attachment types (PDFs, spreadsheets) that may need categorizing

---

## Scheduling this skill

There are three reasonable ways to run this on a weekly cadence. Pick whichever fits the user's workflow.

### Option A — Claude Code `CronCreate` (in-app, preferred)

From any Claude Code session:

```
Schedule the meeting-notes-weekly-cleanup skill to run every Monday at 9am local time.
```

Claude will invoke `CronCreate` with a cron expression like `0 9 * * 1` and the skill name. The job runs inside Claude Code, so it has the same MCP connectors (Google Workspace) available.

Verify with `/cron list` or by asking "what scheduled tasks do I have?"

### Option B — `mcp__scheduled-tasks__create_scheduled_task`

If the user prefers the scheduled-tasks MCP:

```json
{
  "name": "Weekly meeting notes cleanup",
  "cron": "0 9 * * 1",
  "prompt": "Run the meeting-notes-weekly-cleanup skill"
}
```

### Option C — macOS `launchd` / `cron` (out-of-app)

For a headless run outside Claude Code, wire a shell job that uses `claude -p` (non-interactive mode) with the skill slug:

```bash
# ~/Library/LaunchAgents/net.bewley.meeting-cleanup.plist
# schedule: Monday 09:00
claude -p "/meeting-notes-weekly-cleanup" --cwd "/Users/dale/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main"
```

This requires that Google Workspace MCP is available to the non-interactive session (auth cached). Prefer Option A unless you have a reason.

### Recommended cadence

- **Monday 09:00** — reviews last week, prepares for the day.
- If the user has a pre-week planning ritual on Sunday evening, **Sunday 18:00** is also reasonable.

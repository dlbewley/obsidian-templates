---
name: meeting-note-add
description: Create a single Obsidian meeting note from a Google Calendar event. Finds the event by date and/or keyword query, extracts metadata, agenda, attendees, attachments, and recording link.
argument-hint: [date or keyword query — e.g. "today PG Day", "2026-04-22 virtualization", or leave blank for next upcoming]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__Google_Workspace_MCP__get_events
---

Create a new Obsidian meeting note under `Meetings/` for a calendar event.

`$ARGUMENTS` may contain a date (`YYYY-MM-DD`, "today", "tomorrow"), a keyword to match against event titles, or both. If empty, create a note for the next upcoming event on the user's calendar.

## Step 1 — Parse arguments

From `$ARGUMENTS` extract:
- **date** — explicit date or relative word ("today" = currentDate from system). Default: today.
- **query** — any remaining keywords to pass to `get_events` as `query=`.

If no date and no query, use `time_min=now` with `max_results=5` and pick the next event the user has not already got a note for.

## Step 2 — Fetch the event

Call `mcp__Google_Workspace_MCP__get_events` with:
- `time_min` = start of the resolved date (or now)
- `time_max` = end of the resolved date (or +14 days if searching forward for "next")
- `query` = optional keyword string
- `detailed: true`
- `include_attachments: true`
- `max_results: 10`

If multiple events match, list the candidates back to the user and ask which one. Do NOT guess when ambiguous.

## Step 3 — Check for existing note

Before writing, glob for an existing note:

```
Meetings/<YYYY-MM-DD> *<slugified event summary>*.md
```

If a matching file already exists, stop and ask whether the user wants to refresh it (offer to invoke the `meeting-note-refresh` skill) instead of creating a duplicate.

## Step 4 — Determine the series link

Look in `Meetings/` for a `MeetingSeries` parent that matches the recurring event. Use `Grep` for `contentType: MeetingSeries` and match by title keywords. If found, set:

```yaml
series: "[[Meetings/<Series Name>]]"
```

If no series parent exists and this looks like a one-off, leave `series:` blank. If it looks recurring but has no parent, mention it in your summary so the user can create one.

## Step 5 — Build frontmatter

Use this schema (matches `Templates/Meeting.md`):

```yaml
---
contentType: Meeting
date: YYYY-MM-DD HH:MM   # local time, 24h
tags:
  - YYYY-MM
Topics:
  - "[[Topics/Meetings]]"
  - "[[Topics/<other relevant topic if obvious>]]"
attendees:
  - "[[People/<Name>]]"  # one per attendee, only those with @redhat.com or clearly identifiable
owners:
  - "[[People/<Organizer Name>]]"
series: "[[Meetings/<Series>]]"  # if applicable
summary: <one-line summary pulled from description or title>
recording:   # leave blank on initial creation unless already present
---
```

For `attendees`, only add entries where you can identify the person by name. Skip raw email addresses — the note can be updated later.

## Step 6 — Write the body

```markdown
# `=this.file.name`
Date: [[YYYY-MM-DD]]
Series: `=this.series`

## 📚 Documents
- Meeting Link: <meet url>
- [Attachment Name](url)  # for each calendar attachment
- [Description Doc](url)  # for each link found in the description

## 👥 Attendees
- `=this.attendees`

## 📝 Agenda
- <bulleted agenda from event description, preserving structure>

## 💬 Notes
-

## ✅ Action Items
- [ ]
```

## Step 7 — Write the file

Filename: `Meetings/YYYY-MM-DD <clean Title Case summary>.md`
- Strip characters that break filesystems: `/`, `:`, `"`, `<`, `>`, `|`, `?`, `*`
- Keep it short — drop things like "Q2 Week 3" if already implied by date

Write with the `Write` tool.

## Step 8 — Report

Tell the user:
- The created filename
- Which calendar event it matched
- Any series link applied (or that one was missing)
- Whether a recording was already available or is still pending (common for future/ongoing events — user can later invoke `meeting-note-refresh`)

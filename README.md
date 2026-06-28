# Obsidian Templates

![Built with AI](https://img.shields.io/badge/Built%20with-AI-blueviolet?style=for-the-badge)

I need a place to keep my collection of templates for Obsidian documents and the Obsidian Web Clipper extension.
These are some of them along with some notes on how I'm using Obsidian.


# My Obsidian Conventions

How I use Obsidian continues to evolve. But what follows is probably close to what I'm doing today.

## Agentic AI

I started by occasionally using [Cursor](https://cursor.com) to make sweeping edits or cleanups to my vault, by simply treating everything as simple Markdown. Which it is. I've recently been using [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) with the [Obsidian Skills](https://github.com/kepano/obsidian-skills) created by the Obsidian author. These skills take advantage of the [`obsidian` CLI](https://help.obsidian.md/cli) which allows the [Claude app](https://code.claude.com/docs/en/desktop-quickstart), not just Claude Code to make changes intelligently that allow Obsidian to maintain proper cross document linkages, etc.

This repo also ships Claude Code skills under [.claude/skills/](.claude/skills/) for Google Calendar–driven meeting notes (they expect the Google Workspace MCP and tools configured in each skill):

* [meeting-note-add](.claude/skills/meeting-note-add/SKILL.md) — Create one meeting note from a calendar event (by date and/or title query).
* [meeting-note-refresh](.claude/skills/meeting-note-refresh/SKILL.md) — Patch an existing note when recordings, Gemini notes, or transcripts arrive later.
* [meeting-notes-backfill](.claude/skills/meeting-notes-backfill/SKILL.md) — Create notes for every event in a range that does not yet have a file under `Meetings/`.
* [meeting-notes-weekly-cleanup](.claude/skills/meeting-notes-weekly-cleanup/SKILL.md) — Run backfill + refresh for the past week and emit a short report (intended for scheduling).

## Obsidian Community Plugins

Some plugins I am barely using but haven't removed, because I think they may be a good idea eventually. The Stickyness column indicates how much I use them.

A couple plugins are required by the for [Shimmering Obsidian](http://alfred.app/workflows/chrisgrieser/shimmering-obsidian/) workflow  for [Alfred](https://www.alfredapp.com/). You are using Alfred right?!

| Plugin | Description | Stickyness |
| --- | --- | --- |
| [Advanced URI](https://github.com/Vinzent03/obsidian-advanced-uri) | Extends Obsidian's URI scheme for automation and deep linking. For Alfred Workflow. | ⭐️⭐️⭐️⭐️⭐️ |
| [Calendar](https://github.com/liamcain/obsidian-calendar-plugin) | Calendar view for navigating and creating daily notes. | ⭐️⭐️️⭐️⭐️️️️️️️️  |
| [Dataview](https://github.com/blacksmithgu/obsidian-dataview) | Query and display vault data as tables, lists, and calendars using a SQL-like syntax. See [Templates/Person.md](Templates/Person.md). It's possible I could obviate this with the [Bases core plugin](https://obsidian.md/help/bases). 🤷‍♀️ | ⭐️⭐️⭐️⭐️⭐️ |
| [Git](https://github.com/Vinzent03/obsidian-git) | Automatically commit and push vault changes to a Git repository. | ⭐️⭐️ |
| [Marp Slides](https://github.com/samuele-cozzi/obsidian-marp-slides) | Markdown Presentation Engine frontmatter properties. See example in [Templates/Presentation.md](Templates/Presentation.md) and the [Themes](Templates/Marp/Themes/) | ⭐️⭐️⭐️⭐️ |
| [Meta Bind](https://github.com/mProjectsCode/obsidian-meta-bind-plugin) | Inline input fields and buttons bound to note frontmatter properties. See example in [Templates/Meeting.md](Templates/Meeting.md) | ⭐️⭐️⭐️⭐️ |
| [Metadata Extractor](https://github.com/kometenstaub/metadata-extractor) | Exports vault metadata to JSON for use by external tools. For Alfred Workflow. | ⭐️⭐⭐⭐⭐️ |
| [Omnisearch](https://github.com/scambier/obsidian-omnisearch) | Full-text search with fuzzy matching and PDF/image content indexing. | ⭐️⭐⭐️⭐️⭐️️ |
| [Style Settings](https://github.com/mgmeyers/obsidian-style-settings) | UI for customizing theme CSS variables without editing code. | ⭐️️ |
| [Tasks](https://publish.obsidian.md/tasks/Introduction) | Task management with due dates, recurrence, and queries across the vault. | ⭐️️⭐️⭐️ |
| [Task Board](https://github.com/tu2-atmanand/Task-Board) | Task management with Kanban board. I'm not really using it much yet. | ⭐️️⭐️️ |
| [Templater](https://github.com/SilentVoid13/Templater) | Powerful template engine with JavaScript scripting and auto-file placement. | ⭐️⭐️⭐️⭐️⭐️ |
| [Text Extractor](https://github.com/scambier/obsidian-text-extractor) | Extracts text from PDFs and images to make them searchable by Omnisearch. | ⭐⭐⭐⭐️⭐️ |

## Content Types

Documents in my vault have content types (`contenttype` property) which are particularly helpful for reference by bases. For example see the [Topic Template](Templates/Topic%20Template.md) (it embeds [Topic Links.base](Bases/Topic%20Links.base)).

The value is intially set by the Template or the Web Clipper Template and may be adjusted as the contents are refined.

| Emoji | Content Type | Description |
| --- | --- | --- |
| 📖 | Book | Notes and highlights from books being read. |
| 🔖 | Bookmark | Curated collections of external URLs organized by topic. |
| 💬 | Chat | Saved conversation logs or chat transcripts. |
| 👤 | Contact | People notes for colleagues and professional contacts. |
| 🗂️ | Index | Topic index pages that aggregate and link related notes. |
| 📓 | Journal | Daily and weekly journal entries. |
| 👩🏻‍🏫 | Lesson | Learning notes from courses, enablement sessions, and training. |
| ✉️ | Mail | Clipped emails of interest saved for reference. |
| 📅 | Meeting | Individual dated notes for a specific meeting instance. |
| 🔁 | MeetingSeries | Parent doc for a recurring meeting, accumulating themes and linking instances. |
| 📝 | Note | General-purpose reference and knowledge notes. |
| 📊️ | Presentation | Marp slide decks and exported talks. |
| 📦 | Repo | Clipped GitHub repository pages saved for reference. |
| 🌐 | Web | Web pages clipped from the browser for future reference. |

## Obsidian Vault Folder Structure

Do not get too obsessed about where to place notes. I find it helpful for certain content types to live in their own location, like People. When typing a link to a note that doesn't exist, you can influence where it goes if you include the folder in the name. I generally have a top level folder for each contenttype. Eg. Meetings, People, Presentations. Clippings use a subfolder.

For example, if I'm actively taking notes in a meeting (yes I do that) and a name comes up, I may type `[[People/Dale Bewley]]` so that later if I decide to click on that and flesh out the note it will already be in the right place.

This is one reason I often use the Templater style of templates. My [Person](Templates/Person.md) template would automatically move the note for me when I applied it to the 'Fred Jones' note even if I hadn't already prefixed it with `People`.

Remember, it is really easy to move notes, and it is really easy to find them regardless of where they are. Don't let figuring out a folder structure block you from getting started with Obsidian.

* Obsidian Bases are easily constructed by Agents, let them do it for you. Store them in `Bases/` to make them easy to differentitate from normal notes. It is helpful to included bases in templates.

```
Bases/
  ├── Clippings.base
  └── Topic Links.base
```

* Web Clipper Clippings By Source
```
Clippings/
  ├── GitHub/
  ├── Mail/
  ├── YouTube/
  └── Web/
```

* Daily notes over time

Notes are moved to Archive after they have been processed into weekly or monthly notes.

```
Journal/
  ├── Archive/
  ├── Daily/
  ├── Weekly/
  └── Monthly/
```

* Meetings
All meeting notes are in a folder. Individual meeting notes have a date prefix.

If those meetings are part of a series they include a `series` property pointing to a parent doc tracking the meetings from above. This can be helpful for tracking weekly office hours calls with product managers for example. The series note can contain current links to roadmap documents etc while the dated meeting notes retain a historical log.

It may make sense to move the dated meeting notes to a subdirectory at some point.

```
Meetings/
  ├── 2026-04-05 Fidget Spinner.md
  └── Fidget Spinner.md
```

* Career Stuff

```
ProDev/
  └─── Quarterly Connections/
    ├── 2025-Q3.md
    └── 2025-Q4.md
```

* Topics make a great overview page for a collection of notes on a topic. This is highly augmented by using the local Graph view to see connections. Here is a random sample of topics.

```
Topics/
  ├── Career.md
  ├── Meetings.md
  ├── Networking.md
  ├── OpenShift.md
  ├── People.md
  └── Virtualization.md
```

# Other Template Sources I Benefited From

- https://github.com/obsidian-community/web-clipper-templates/tree/main
- https://github.com/Fred-Vatin/Web-Clipper-Templates
- https://dannb.org/blog/2022/obsidian-people-note-template/
- https://www.moritzjung.dev/obsidian-meta-bind-plugin-docs/

# Repo Contents
## Web Clipper Templates

These are based on the works of others. I have modified them to better suit my needs or just copied them here for convenience. See the [list of sources below](#other-template-sources-i-benefited-from).

* [default-clipper.json](web-clipper-templates/default-clipper.json)
  - Clipper for general web pages

* [github-repository-clipper.json](web-clipper-templates/github-repository-clipper.json)
  - Clipper for GitHub repositories

* [google-mail-clipper.json](web-clipper-templates/google-mail-clipper.json)
  - Clipper for Google Mail

## Obsidian Document Templates

These are basic templates that may use dataviewjs to perform some inline queries.

* [daily.md](Templates/daily.md)
  - Create a daily note

* [Person.md](Templates/Person.md)
  - Collect details about a person and generate dynamic links to find emails, git repos, and company profiles

* [Meeting.md](Templates/Meeting.md)
  - Create a meeting note. Tracks attendees, agenda, notes, and action items. Moves the file into the appropriate Meetings folder and links to series.

* [MeetingSeries.md](Templates/MeetingSeries.md)
  - Create a meeting series note. Used to collect recurring or related meetings. Tracks owners, cadence, and automatically gathers all meeting instances in the series.
  - Agenda ideas for the next meeting; knowledge gleaned from individual meetings may be summarized on the meeting series page.

* [monthly.md](Templates/monthly.md)
  - Create a monthly note with links to all days and weeks that month

* [Note.md](Templates/Note.md)
  - General-purpose note with summary, key concepts, references, and connections (`contenttype: Note`).

* [Presentation.md](Templates/Presentation.md)
  - Marp slide deck starter (`marp: true` frontmatter). Custom CSS lives under [Templates/Marp/Themes/](Templates/Marp/Themes/) (for example `mylogo.css`, `palette-3.css`, `redhat.css`); [logo.png](Templates/logo.png) is referenced by some themes.

* [Topic Template.md](Templates/Topic%20Template.md)
  - Form an overview or "Index" of a topic. Notes that reference `Topics: "[[Topics/Foo]]"` making them easy to discover via the topic page.
  - Used as the basis for new topic files and for indexing connections between notes and topics. Embeds the [Topic Links.base](Bases/Topic%20Links.base) to surface all notes on a topic.

* [Quarterly Connection.md](Templates/Quarterly%20Connection.md)
  - Create a quarterly connections note used for employee reviews.

* [weekly.md](Templates/weekly.md)
  - Create a weekly note with links to all days that week

## Obsidian Bases

* [Clippings.base](Bases/Clippings.base)
  - Table and card views over notes in `Clippings/`, ordered by content type and metadata (for example `Topics`, `url`, `reviewed`).

* [Meetings by Series.base](Bases/Meetings%20by%20Series.base)
  - Meeting notes grouped by `series`, with formula columns for recording and series links; includes filtered views such as meetings in the current month.

* [Topic Links.base](Bases/Topic%20Links.base)
  - Lists notes that link to a given topic, grouped by content type with custom icons (typically embedded from a topic or [Topic Template](Templates/Topic%20Template.md)).

---
name: ai-frontier-news
description: Gather new announcements and blog posts from leading AI frontier labs (Anthropic, OpenAI, Google, Microsoft, and others) and add them to a daily journal note. Use when the user wants to collect, round up, or catch up on the latest AI lab news, model releases, or frontier-lab blog posts into their Obsidian daily note. Trigger phrases: "AI frontier news", "AI lab announcements", "what did the AI labs announce", "round up AI news into today's journal".
argument-hint: [date — e.g. "today", "yesterday", "2026-07-01"]
allowed-tools: Bash, Read, Edit, WebSearch, WebFetch
---

Gather recent announcements and blog posts from leading AI frontier labs and append them to the target daily journal note under a `## 🤖 AI Frontier Labs` section.

`$ARGUMENTS` is a date reference for the daily note to update. Default to today (`currentDate` in system context) if empty. Accepted forms:
- empty / `today` → current date
- `yesterday` → previous day
- `YYYY-MM-DD` → that specific day

## Step 1 — Resolve the target note

Compute **noteDate** = `YYYY-MM-DD` from `$ARGUMENTS`. The file is `Journal/Daily/{noteDate}.md`.

Verify the file exists with Bash. If it does not, tell the user and stop (do not create it — that is the daily-note template's job).

The **news window** is the ~7 days ending on `noteDate` (inclusive). Only include posts published within this window. This keeps the round-up focused on what is genuinely new as of that journal day.

## Step 1.5 — Collect already-reported URLs (deduplication)

The news window overlaps between consecutive runs, so a post published a few days ago is legitimately "in window" on multiple journal days. Without this step the same story gets logged repeatedly (e.g. the same Anthropic post appearing on both 2026-07-09 and 2026-07-13). To prevent that, build an **exclusion set** of URLs already reported in recent daily notes *before* gathering.

Scan the `## 🤖 AI Frontier Labs` sections of the daily notes for roughly the **14 days preceding `noteDate`** (a window wider than the news window, so nothing slips through the overlap). Extract every external post URL already listed. One Bash command does this — grep the markdown-link URLs out of the recent daily notes:

```bash
# from the vault root; adjust the date list to the 14 days before noteDate
grep -rhoE '\]\((https?://[^)]+)\)' Journal/Daily/{list-of-recent-dates}.md \
  | sed -E 's/^\]\((.*)\)$/\1/' | sort -u
```

Alternatively, `Read` the handful of recent daily notes directly and note the URLs under their AI Frontier Labs sections. Either way, capture the set of **canonical post URLs already reported**.

Normalize URLs before comparing (strip trailing slashes, `utm_*`/tracking query params, and `#fragments`) so the same story isn't re-added under a slightly different URL.

## Step 2 — Gather posts from each lab

Cover **at least** these four labs. Add others when relevant (e.g. Meta AI / Llama, Mistral, xAI, DeepSeek, NVIDIA).

| Lab | Primary sources |
|-----|-----------------|
| **Anthropic** | https://www.anthropic.com/news |
| **OpenAI** | https://openai.com/news/ |
| **Google** | https://deepmind.google/discover/blog/ · https://blog.google/technology/ai/ |
| **Microsoft** | https://blogs.microsoft.com/ai/ · https://news.microsoft.com/source/topics/ai/ · Microsoft Research blog |

For each lab, run **WebSearch** with a date-scoped query, then **WebFetch** the specific post URLs you find to confirm the publish date, the real title, and a one-line summary. Prefer official first-party URLs over third-party coverage.

Suggested WebSearch queries (substitute the note's month/year):
- `Anthropic announcement OR blog post {Month} {Year}`
- `OpenAI news release {Month} {Year}`
- `Google DeepMind OR Google AI announcement {Month} {Year}`
- `Microsoft AI announcement {Month} {Year}`

Filtering rules:
- **Keep**: model releases, research papers, product/feature launches, safety and policy posts, major partnerships — anything published within the news window **whose URL is not in the exclusion set from Step 1.5**.
- **Drop**: anything outside the window; **any post already reported in a recent daily note (its URL is in the exclusion set)**; duplicates within this run; pure marketing recaps; and low-signal social posts.
- Because already-reported stories are excluded, most runs will surface only a handful of genuinely new posts — that is expected and correct. Do **not** pad the list by re-including older stories to make a lab look active.
- If a lab has nothing new in the window (after exclusion), note it as `_No new posts this week._` under that lab (or omit the lab — your call, but be consistent).

For each kept post capture: **lab**, **title**, **canonical URL**, **publish date**, and a **1–2 sentence headline** in your own words describing what it is and why it matters.

## Step 3 — Build the section

Group by lab, most recent first within each group. Use this exact structure:

```markdown
## 🤖 AI Frontier Labs

_Gathered [[{noteDate}]]. Window: [[{windowStart}]] → [[{noteDate}]]._

### Anthropic
- [{Title}]({URL}) — [[{YYYY-MM-DD}]]. {1–2 sentence headline.}

### OpenAI
- [{Title}]({URL}) — [[{YYYY-MM-DD}]]. {1–2 sentence headline.}

### Google
- [{Title}]({URL}) — [[{YYYY-MM-DD}]]. {1–2 sentence headline.}

### Microsoft
- [{Title}]({URL}) — [[{YYYY-MM-DD}]]. {1–2 sentence headline.}
```

Link conventions:
- **Dates** are always Obsidian wikilinks in `[[YYYY-MM-DD]]` form (they resolve to daily notes) — including the publish date on each post and the gathered/window dates in the italic line.
- **External sources** (post titles) use plain Markdown links (`[text](url)`), not wikilinks.

Keep headlines factual and concise — one or two sentences.

## Step 4 — Insert into the daily note

Read the note. If a `## 🤖 AI Frontier Labs` section already exists, **replace** its body with the freshly gathered list (do not duplicate the section). Otherwise, insert the new section **before the `## 🔗 Linked Here` section** (or at the end of the note if that section is absent), using Edit.

Do not disturb existing frontmatter, dataview blocks, or other sections.

## Step 5 — Report

Summarize to the user: how many posts were added per lab, the news window used, and the note path. Flag any lab that had no new posts. Also report **how many candidate posts were skipped as already-reported** (from Step 1.5), so the dedup is visible and verifiable.

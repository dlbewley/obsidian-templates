# Marp Presentations — Theme & Authoring Guide

This folder holds the [Marp](https://marp.app/) themes for slide decks in this
vault. Decks live in `Presentations/`; this guide explains how to build one,
how the `mylogo` theme works, and — importantly — the conventions that keep
decks looking right **both** in the Obsidian preview **and** in exported PDFs.

> **Plugin:** decks are previewed/exported with the **Marp Slides** community
> plugin. It loads themes from the folder set in its settings
> (`ThemePath: Templates/Marp/Themes`), so any `.css` here is available to every
> deck by name.

---

## Quick start

Create a deck in `Presentations/` (or run the `weekly-review` skill, which
scaffolds one). Every deck begins with this frontmatter:

```yaml
---
marp: true
theme: mylogo        # references Themes/mylogo.css by its @theme name
paginate: true       # page numbers, bottom-right
size: hd             # 1920×1080
---
```

Slides are separated by `---`. Set per-slide options with a Marp **class
directive** — an HTML comment placed right under the slide separator:

```markdown
---
<!-- _class: icon ai kick -->
## AI & Enablement Landscape
Staying abreast

### Artificial Intelligence
- …
```

The leading underscore (`_class`) scopes it to **that one slide**. Without the
underscore (`class`) it applies to that slide and all following slides.

---

## The golden rule: keep decks HTML-free

**Do not put a `<style>` block or body HTML (`<span>`, `<div>`) in a deck.** Put
all styling in the theme, and drive per-slide looks off `_class` directives.

Why this matters: the Marp Slides plugin passes `--html` to marp-cli only for
**HTML** and **preview** exports — **not** for **PDF / PPTX / PNG**. On those,
marp-cli strips raw HTML from the slide body. So anything that depends on a
`<span>`/`<div>` in the markdown silently breaks on PDF export, even though it
looks fine in the live preview. Two real bugs this caused:

- A `<span class="logo-emoji">🚀</span>` watermark got stripped on PDF export,
  leaving a bare emoji that an image-fit rule then **ballooned to fill the
  slide**.
- `<div class="cta">` call-to-action boxes lost their styling on PDF export.

The fix for both was to stop hanging styling off body HTML and instead drive it
from `_class` directives (which are comments, not HTML, so they always survive)
plus theme CSS. That's the convention below.

`_class` directives, Markdown images (`![bg …]`, `![logo …]`), and emoji typed
**inline in text/headings** are all export-safe. Only hand-written `<span>` /
`<div>` / `<style>` are the problem.

---

## `_class` vocabulary (the `mylogo` theme)

Mix and match: one layout, optionally one watermark glyph, plus any helpers —
e.g. `<!-- _class: icon tech kick -->`.

### Layout (pick one)

| Class | Use |
|-------|-----|
| `title` | Cover slide. Shows the image logo (`![logo](img/…)`) bottom-right. |
| `icon` | Standard content slide. Corner emoji watermark, tilted −45°. |
| `lead` | Centered closing / section slide. |

### Watermark glyph (pick one, pair with a layout)

The watermark is referenced by a **name**, not by typing the emoji. The theme
maps the name to an emoji. See [mylogo.css](Themes/mylogo.css) for current glyph map.

| Name | Emoji | Name | Emoji |
|------|:-----:|------|:-----:|
| `note` | 🗒 | `watch` | 🔭 |
| `star` | ⭐ | `idea` | 💡 |
| `tech` | ☸️ | `chart` | 📊 |
| `cal` | 📅 | `target` | 🎯 |
| `ai` | 🤖 | `rocket` | 🚀 |
| `win` | 🏆 | | |

Omit the glyph (`<!-- _class: icon -->`) for no watermark.

### Helpers (optional, stackable)

| Class | Effect |
|-------|--------|
| `kick` | Styles the first paragraph after the heading as a small grey "kicker" tagline. Write the tagline as a normal line right under the `##`. |
| `cta` | Styles a plain Markdown list on the slide as red-accented call-to-action cards. |

---

## Referencing & adjusting the watermark emoji

Three operations, in increasing scope:

**1. Change which mark a slide shows** — edit the slide's `_class` only:

```markdown
<!-- _class: icon win -->     <!-- swap "win" for any name in the table -->
```

**2. Remap a name to a different emoji** — edit one line in
`Themes/mylogo.css` (changes it everywhere that name is used):

```css
section.ai::before { content: "🤖"; }   /* change the emoji in the quotes */
```

**3. Add a brand-new name** — clone a line in `Themes/mylogo.css`, then use it:

```css
section.lock::before { content: "🔒"; }
```
```markdown
<!-- _class: icon lock -->
```

On macOS, <kbd>Ctrl</kbd>+<kbd>Cmd</kbd>+<kbd>Space</kbd> opens the emoji picker;
paste the emoji between the quotes.

### Notes

- The name is **arbitrary and semantic** — pick something memorable (`lock`,
  `db`, `cloud`); it just has to match between the slide's `_class` and the
  `section.<name>::before` rule in the theme.
- **One glyph per slide.** Stacking two (`icon ai win`) is ambiguous.
- **Why some marks tilt:** `icon` slides rotate the watermark −45°
  (`section.icon::before { transform: rotate(-45deg); }`); `title`/`lead` don't.

### Why the watermark is on `::before` (not `::after`)

`paginate: true` renders the page number on `section::after`
(`content: attr(data-marpit-pagination)`). A pseudo-element exists only once per
element, so a watermark on `::after` collides with pagination — the page number
wins the content and the watermark's sizing leaks onto it. The watermark
therefore lives on `section::before`, which Marp leaves free. **If you add new
watermark rules, keep them on `::before`.**

---

## Exporting

Because decks are HTML-free, **all** export targets render identically to the
preview — no `--html` workaround needed.

- **From Obsidian:** Command Palette → *Marp: Export Slide* → choose PDF / PPTX /
  PNG / HTML.
- **From the CLI** (if you have `marp` installed):

  ```bash
  marp "Presentations/My Deck.md" --pdf --allow-local-files \
    --theme-set "Templates/Marp/Themes/mylogo.css"
  ```

- **Sanity-check a render** the way PDF export sees it (HTML disabled) and eyeball
  the PNGs:

  ```bash
  marp "Presentations/My Deck.md" --images png --html=false \
    --theme-set "Templates/Marp/Themes/mylogo.css" -o /tmp/check.png
  ```

> Color emoji need a color-emoji font on the rendering machine (macOS has Apple
> Color Emoji). A headless renderer without one will show watermarks in
> monochrome — cosmetic to that render only.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `Themes/mylogo.css` | **Primary theme.** Red Hat styling, the `_class` watermark/kicker/cta system, image-logo handling. Has a quick-reference comment at the top. |
| `Themes/redhat.css` | Alternate, heavier Red Hat theme. |
| `Themes/palette-3.css` | Alternate color palette. |
| `README.md` | This guide. |

Related: the `weekly-review` skill (`.claude/skills/weekly-review/`) scaffolds
HTML-free decks using this theme; its `assets/deck-template.md` is a ready-made
starting point.

<%* let author = await tp.system.prompt("Author name", "Dale Bewley") -%>
<%* let theme = await tp.system.prompt("Marp Theme", "mylogo") -%>
<%* await tp.file.move(`Presentations/${tp.file.title}`) -%>
---
contenttype: Presentation
author: <% author %>
created: "[[<% tp.file.creation_date("YYYY-MM") %>]]"
tags:
  - presentation
  -  <% tp.file.creation_date("YYYY-MM") %>
topics: []
marp: true
theme: <% theme %>
paginate: true
html: true
size: hd
---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 1 — Title
  Class options:  title · invert · lead · icon
  Use _class (underscore) to apply to this slide only.
  Use class (no underscore) to set a global default for all subsequent slides.
  ───────────────────────────────────────────────────────────────────────── -->
<!-- _paginate: skip -->
<!-- _class: title invert -->
<!-- _footer: '[github.com/dlbewley](https://github.com/dlbewley/)' -->
![bg grayscale opacity:20%](img/openshift.png)

# Presentation Title

### <% author %>

> ### Principal Specialist SA
> OpenShift NA West
> Red Hat

![logo Logo](img/logo.png)

---

<!-- ─────────────────────────────────────────────────────────────────────────
  Set a running footer for the rest of the deck (markdown + links supported).
  ───────────────────────────────────────────────────────────────────────── -->
<!-- footer: '**[<% author %>](https://www.linkedin.com/in/example)**  **|**  **[github.com/dlbewley/example](https://github.com/dlbewley/)**' -->

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 2 — Overview / At a Glance
  Table + notepad emoji watermark.
  ───────────────────────────────────────────────────────────────────────── -->
<!-- _class: icon note -->
## Overview

| Section     | Description                          |
| ----------- | ------------------------------------ |
| **Topic A** | Brief description of the first area  |
| **Topic B** | Brief description of the second area |
| **Topic C** | Brief description of the third area  |
| **Topic D** | Brief description of the fourth area |


---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 3 — Section divider (invert)
  Use for chapter / topic transitions. No emoji needed — the heading fills it.
  ───────────────────────────────────────────────────────────────────────── -->
<!-- _class: invert icon idea -->
<!-- header: Topic A -->

# Topic A

## Subtitle or key question being answered


---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 4 — Bullet list with emoji watermark
  ───────────────────────────────────────────────────────────────────────── -->
<!-- class: icon note -->

## Key Concept

Brief introductory sentence that frames the slide.

- First important point with a **bold keyword** highlighted
- Second point — use em-dashes for asides
- Third point with _italics_ for emphasis
- Fourth point

> 💡 A blockquote works well for tips, warnings, or key takeaways.


---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 5 — Two-column layout (scoped CSS)
  Headings and paragraphs span both columns; lists split naturally.
  ───────────────────────────────────────────────────────────────────────── -->
<style scoped>
  section { columns: 2; column-rule: 1px solid #ccc; }
  p, h1, h2 { column-span: all; }
</style>

## Comparing Two Things

Brief framing sentence that spans both columns.

### 🅰 Option / Approach A
- First characteristic
- Second characteristic
- Third characteristic

### 🅱 Option / Approach B
- First characteristic
- Second characteristic
- Third characteristic


---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 6 — Code block(s)
  Two fenced code blocks split across columns automatically.
  Use `![logo Name](img/file.png)` to render a logo as the watermark image
  instead of a text emoji (position is identical — lower-right, rotated).
  ───────────────────────────────────────────────────────────────────────── -->
<!-- header: Topic A › Code -->
<style scoped>
  section { columns: 2; column-rule: 1px solid #ccc; }
  p, h1, h2 { column-span: all; }
</style>

## Configuration Example

Short description of what this config does.

```yaml
# resource-type.yaml
apiVersion: example.io/v1
kind: ExampleResource
metadata:
  name: my-resource
spec:
  setting: value
  nested:
    key: value
```

```bash
# Verify the resource
$ example-cli get ExampleResource my-resource
NAME          STATUS   AGE
my-resource   Ready    2m
```

![logo Example](img/logo.png)

---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 7 — Output / command walkthrough
  Inline code, shell output, and an emoji watermark.
  Speaker notes go in an HTML comment after the slide content.
  ───────────────────────────────────────────────────────────────────────── -->
<!-- class: icon magnify -->

## Examining the Result

Key observations about the output below:

- `field-one` — explains what this field means
- `field-two` — explains what this field means  
- `field-three` — explains what this field means

```bash
$ example-cli describe resource my-resource
Name:    my-resource
Status:  Ready
Field:   value
Output:  expected-result
```


<!--
  Speaker notes go here — not visible in the slide, only in presenter view.
  - Key talking point 1
  - Key talking point 2
-->

---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 8 — Summary / recap
  Collect the key takeaways after a topic section.
  ───────────────────────────────────────────────────────────────────────── -->
<!-- header: Topic A › Summary -->
<!-- class: icon books -->

## Topic A — Summary

### Component / Perspective 1
- First takeaway
- Second takeaway
- Third takeaway

### Component / Perspective 2
- First takeaway
- Second takeaway


---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 9 — Full-bleed background image slide
  Good for diagrams or architecture drawings. `contain` fits the image inside
  the slide without cropping; `cover` fills the whole background.
  ───────────────────────────────────────────────────────────────────────── -->
<!-- _class: icon crane -->
<!-- header: Topic B -->

## Architecture Diagram

![contain](img/openshift.png)

---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 10 — References / further reading
  ───────────────────────────────────────────────────────────────────────── -->
<!-- header: References -->
<!-- class: icon books -->

## References & Further Reading

### Official Documentation
- [Product Docs — Topic A](https://docs.example.com/topic-a)
- [Product Docs — Topic B](https://docs.example.com/topic-b)

### GitHub Repositories
- **Repo Name** — [github.com/org/repo](https://github.com/org/repo)

### Blog Posts & Talks
- [Title of Post](https://example.com/post) — _Author, YYYY-MM_


---

<!-- ─────────────────────────────────────────────────────────────────────────
  SLIDE 11 — Closing / lead
  ───────────────────────────────────────────────────────────────────────── -->
<!-- _class: lead icon target -->
<!-- _paginate: skip -->

# Thank You

_Questions?_

**<% author %>** · [linkedin.com/in/example](https://linkedin.com/in/example)


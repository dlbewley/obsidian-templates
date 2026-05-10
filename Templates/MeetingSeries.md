---
contentType: MeetingSeries
tags: []
Topics:
  - "[[Topics/Meetings]]"
attendees: []
owners:
  - "[[People/First Last]]"
cadence:
summary:
---

<% await tp.file.move("/Meetings/" + tp.file.title) %>

# `=this.file.name`

## Overview

**`=this.file.name`** is  _`=this.cadence`_

### 👥 Host
- `=this.owners`

## 📝 Agenda
-

## 💬 Notes
- Upstream [Meeting Notes](replace-with-google-notes-or-other-link)

## ✅ Action Items
- \[ \] Task one

## 📅 Instances
```dataview
LIST date + " — " + summary
FROM "Meetings"
WHERE series = this.file.link
SORT date DESC
```

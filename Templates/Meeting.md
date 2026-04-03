---
contentType: Meeting
date: <% tp.file.creation_date() %>
tags:
  - <% tp.date.now("YYYY-MM") %>
Topics:
  - "[[Topics/Meetings]]"
attendees:
  - "[[People/First Last]]"
owners: []
series:
summary:
---

<% await tp.file.move("/Meetings/" + tp.date.now("YYYY-MM-DD") + " " + tp.file.title) %>

# `=this.file.name`
Date: [[<% tp.date.now("YYYY-MM-DD") %>]]
Series: `=this.series`

## 👥 Attendees
- `=this.attendees`

## 📝 Agenda
-

## 💬 Notes
-

## ✅ Action Items
- \[ \] Task one
---
tags:
  - topic
Topics: []
contenttype: Index
---

`BUTTON[new-meeting, new-meeting-series]`

```meta-bind-button
label: New Meeting Note
icon: lucide-calendar-plus
style: default
class: ""
cssStyle: ""
backgroundImage: ""
tooltip: ""
id: "new-meeting"
hidden: true
actions:
  - type: templaterCreateNote
    templateFile: "Templates/Meeting.md"
    folderPath: Meetings
    fileName: StubMeeting
    openNote: true
    openIfAlreadyExists: false

```

```meta-bind-button
label: New Meeting Series
icon: lucide-calendar-sync
style: default
class: ""
cssStyle: ""
backgroundImage: ""
tooltip: ""
id: "new-meeting-series"
hidden: true
actions:
  - type: templaterCreateNote
    templateFile: "Templates/MeetingSeries.md"
    folderPath: Meetings
    fileName: StubMeetingSeries
    openNote: true
    openIfAlreadyExists: false

```


## Meeting Notes

```dataview
TABLE file.cday as Date, summary
FROM "Meetings"
SORT file.cday DESC
```

## Meetings
```dataview
TABLE file.cday as Created, summary AS "Summary"
FROM "Meetings" where contains(file.outlinks, [[]])
SORT file.cday DESC
```

## Meetings

```dataview
TABLE file.name as "Meeting", file.cday as "Date", summary as "Summary"
FROM "Meetings" where contains(file.outlinks, [[]])
SORT file.cday DESC
```

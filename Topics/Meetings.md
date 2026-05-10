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


## Recurring Meetings
```dataview
LIST "**" + summary + "** _(" + cadence + ")_ " + owners
FROM "Meetings" 
WHERE contentType = "MeetingSeries"
SORT file.name
```


## Meetings Grouped by Series

![[Meetings by Series.base]]

[[Topic Links.base |Items]] in the `=this.file.name` topic
![[Topic Links.base]]

# Dataview Query Examples
## Individual Meetings
```xxxdataview
TABLE file.cday as Date, summary 
FROM "Meetings"
WHERE contentType = "Meeting"
SORT file.cday DESC
```

## Meetings
```xxxdataview
TABLE file.cday as Created, summary AS "Summary"
FROM "Meetings" where contains(file.outlinks, [[]])
SORT file.cday DESC
```

## Meetings

```xxxdataview
TABLE file.name as "Meeting", file.cday as "Date", summary as "Summary"
FROM "Meetings" where contains(file.outlinks, [[]])
SORT file.cday DESC
```

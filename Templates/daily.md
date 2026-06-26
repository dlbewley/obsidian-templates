<%*
const input = await tp.system.prompt("Date for daily note (YYYY-MM-DD)", tp.date.now("YYYY-MM-DD"));
const noteDateStr = input.trim();
const [yStr, mStr, dStr] = noteDateStr.split("-");
const noteDate = new Date(parseInt(yStr), parseInt(mStr) - 1, parseInt(dStr));
const year = noteDate.getFullYear();
const month = String(noteDate.getMonth() + 1).padStart(2, '0');
const day = String(noteDate.getDate()).padStart(2, '0');
const weekNumber = getWeekNumber(noteDate);
const weekPadded = String(weekNumber).padStart(2, '0');

// Function to get week number of the year
function getWeekNumber(date) {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    return Math.ceil((((d - yearStart) / 86400000) + 1)/7);
}

// Generate the filename
const filePath = `Journal/Daily`;
const fileName = `${year}-${month}-${day}`;
const monthlyFilePath = `Journal/Monthly`;
const weekFilePath = `Journal/Weekly`;
const weekFileName = `${year}-${month}-W${weekPadded}`;

// Offset from the prompted date (fileName), not today
const yesterdayFileName = tp.date.now("YYYY-MM-DD", -1, fileName, "YYYY-MM-DD");
const tomorrowFileName = tp.date.now("YYYY-MM-DD", 1, fileName, "YYYY-MM-DD");

// Generate the content
tR += `---
tags:
  - daily
  - ${year}-W${weekPadded}
  - ${year}-${month}
contenttype: Journal
---

_[[${yesterdayFileName}|<< Yesterday]] - **${fileName}** - [[${tomorrowFileName}|Tomorrow >>]]_
_Month: [[${monthlyFilePath}/${year}-${month}]]_
_Week: [[${weekFilePath}/${weekFileName}]]_
`;

console.log(`Attempting to rename to: ${filePath}/${fileName}`);
await tp.file.move(`${filePath}/${fileName}`);
console.log("Rename completed");
%>

## 📌 Tasks
- \#todo \[\]

## 📅 Meetings
-
```dataview
TABLE summary
FROM [[]]
WHERE (contentType = "Meeting" OR contentType = "MeetingSeries")
sort file.ctime DESC
```


## 📘 Notes
-

## ✅ Done
- \#prodev
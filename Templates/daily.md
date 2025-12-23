<%*
const now = new Date();
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
const day = String(now.getDate()).padStart(2, '0');
const weekNumber = getWeekNumber(now);
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
const weekFilePath = `Journal/Weekly`;
const weekFileName = `${year}-${month}-W${weekPadded}`;

// Generate the content
tR += `---
tags:
  - daily
  - ${year}-W${weekPadded}
  - ${year}-${month}
---

# ${fileName}

_Week: [[${weekFilePath}/${weekFileName}]]_
`;

console.log(`Attempting to rename to: ${filePath}/${fileName}`);
await tp.file.move(`${filePath}/${fileName}`);
console.log("Rename completed");
%>

## 📌 Tasks
- [ ]

## 📅 Meetings
-

## 📘 Notes
-

## 💡 Ideas (fleeting note)
- #idea:

## ✅ Done
-
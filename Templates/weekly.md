<%*
const now = new Date();
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');
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
const filePath = `Journal/Weekly`;
const fileName = `${year}-${month}-W${weekPadded}`;
const monthFilePath = `Journal/Monthly`;
const monthFileName = `${year}-${month}`;

// Get the start and end dates of the week
const startOfWeek = new Date(now);
const day = startOfWeek.getDay();
const diff = startOfWeek.getDate() - day + (day === 0 ? -6 : 1); // Adjust when day is Sunday
startOfWeek.setDate(diff);

const endOfWeek = new Date(startOfWeek);
endOfWeek.setDate(startOfWeek.getDate() + 6);

// Format dates for daily note links
const formatDate = (date) => {
    return date.getFullYear() + '-' +
           String(date.getMonth() + 1).padStart(2, '0') + '-' +
           String(date.getDate()).padStart(2, '0');
};

// Generate daily note links for the week
const dailyLinks = [];
for (let i = 0; i < 7; i++) {
    const currentDate = new Date(startOfWeek);
    currentDate.setDate(startOfWeek.getDate() + i);
    const dateStr = formatDate(currentDate);
    const dayName = currentDate.toLocaleDateString('en-US', { weekday: 'long' });
    dailyLinks.push(`- [[${dateStr}|${dayName}, ${dateStr}]]`);
}

// Generate the content
tR += `---
tags:
  - weekly
  - ${year}-W${weekPadded}
---

# Week of ${formatDate(startOfWeek)} - ${formatDate(endOfWeek)}

_[[${monthFilePath}/${monthFileName}]]_

## 📅 Daily Notes

${dailyLinks.join('\n')}

`;

console.log(`Attempting to rename to: ${filePath}/${fileName}`);
await tp.file.move(`${filePath}/${fileName}`);
console.log("Rename completed");
%>
## 🎯 Weekly Goals
- [ ]
- [ ]
- [ ]

## 📊 Week Summary

### Key Accomplishments
-

### Challenges Faced
-

### Lessons Learned
-

### Next Week Priorities
- [ ]
- [ ]
- [ ]

## 📈 Metrics & Progress
-

## 💭 Reflections
-

## 🔗 Important Links
-

## 📝 Notes
-

---


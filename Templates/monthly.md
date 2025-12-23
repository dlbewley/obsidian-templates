<%*
const now = new Date();
const year = now.getFullYear();
const month = String(now.getMonth() + 1).padStart(2, '0');


// Get the first and last day of the month
const firstDay = new Date(year, now.getMonth(), 1);
const lastDay = new Date(year, now.getMonth() + 1, 0);

// Format dates for daily note links
const formatDate = (date) => {
    return date.getFullYear() + '-' +
           String(date.getMonth() + 1).padStart(2, '0') + '-' +
           String(date.getDate()).padStart(2, '0');
};

// Generate calendar grid for the month
const calendarGrid = [];
const currentDate = new Date(firstDay);

// Get the first day of the month and find what day of the week it falls on
const firstDayOfMonth = new Date(year, now.getMonth(), 1);
const firstDayOfWeek = firstDayOfMonth.getDay(); // 0 = Sunday, 1 = Monday, etc.

// Create calendar header
const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
calendarGrid.push('| ' + weekDays.join(' | ') + ' |');
calendarGrid.push('|' + ' --- |'.repeat(7));

// Add empty cells for days before the first day of the month
const emptyCells = firstDayOfWeek;
const firstRow = [];
for (let i = 0; i < emptyCells; i++) {
    firstRow.push(' |');
}

// Add days of the month
let currentRow = [...firstRow];
const lastDayOfMonth = lastDay.getDate();

for (let day = 1; day <= lastDayOfMonth; day++) {
    const dateStr = formatDate(new Date(year, now.getMonth(), day));
    const dayOfWeek = new Date(year, now.getMonth(), day).getDay();

    // If it's Sunday (0), start a new row
    if (dayOfWeek === 0 && day > 1) {
        // Fill remaining cells in current row with empty cells
        while (currentRow.length < 7) {
            currentRow.push(' |');
        }
        calendarGrid.push('|' + currentRow.join(''));
        currentRow = [];
    }

    currentRow.push(` [[${dateStr}\\|${day}]] |`);
}

// Fill remaining cells in the last row
while (currentRow.length < 7) {
    currentRow.push(' |');
}
calendarGrid.push('|' + currentRow.join(''));

// Function to get week number of the year
function getWeekNumber(date) {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    return Math.ceil((((d - yearStart) / 86400000) + 1)/7);
}

// Generate weekly note links for the month
const weeklyLinks = [];
const weekStart = new Date(firstDay);
// Adjust to start of week (Monday)
const dayOfWeek = weekStart.getDay();
const diff = weekStart.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
weekStart.setDate(diff);

const weekEnd = new Date(lastDay);
// Adjust to end of week (Sunday)
const endDayOfWeek = weekEnd.getDay();
const endDiff = weekEnd.getDate() - endDayOfWeek + (endDayOfWeek === 0 ? 0 : 7 - endDayOfWeek);
weekEnd.setDate(endDiff);

const currentWeek = new Date(weekStart);
while (currentWeek <= weekEnd) {
    const weekNumber = getWeekNumber(currentWeek);
    const weekPadded = String(weekNumber).padStart(2, '0');
    const weekFileName = `${year}-${month}-W${weekPadded}`;

    // Get the start and end of this week for display
    const weekStartDate = new Date(currentWeek);
    const weekEndDate = new Date(currentWeek);
    weekEndDate.setDate(weekStartDate.getDate() + 6);

    const weekStartStr = formatDate(weekStartDate);
    const weekEndStr = formatDate(weekEndDate);

    weeklyLinks.push(`- [[${weekFileName}|Week ${weekNumber} (${weekStartStr} - ${weekEndStr})]]`);
    currentWeek.setDate(currentWeek.getDate() + 7);
}

// Get month name
const monthName = firstDay.toLocaleDateString('en-US', { month: 'long' });

// Generate the filename
const filePath = `Journal/Monthly`;
const fileName = `${year}-${month}`;

// Generate the content
tR += `---
tags:
  - monthly
  - ${year}-${month}
---

# ${monthName} ${year}

## 📅 Weekly Notes
${weeklyLinks.join('\n')}

## 📅 Calendar
${calendarGrid.join('\n')}
`;

console.log(`Attempting to rename to: ${filePath}/${fileName}`);
await tp.file.move(`${filePath}/${fileName}`);
console.log("Rename completed");
%>

## 🎯 Monthly Goals
- [ ]
- [ ]
- [ ]

## 📊 Month Summary
### Key Accomplishments
-

### Major Milestones
-

### Kudos Recieved

- #prodev #kudos
### Challenges Overcome
-

### Lessons Learned
-

## 📈 Progress Tracking
### Projects Completed
-

### Projects In Progress
-

### New Projects Started
-

## 🔄 Monthly Review
### What Went Well
-

### What Could Be Improved
-

### Action Items for Next Month
- [ ]
- [ ]
- [ ]

## 📊 Metrics & KPIs
-

## 💭 Reflections
### Personal Growth
-

### Professional Development
-

### Work-Life Balance
-

## 🔗 Important Resources
-

## 📝 Notes & Observations
-

## 🎯 Next Month Focus
-



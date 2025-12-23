<%*
const d = tp.date.now("YYYY-MM-DD");
const year = tp.date.now("YYYY");
const month = Number(tp.date.now("MM"));

// Figure out quarter
let q;
if (month >= 1 && month <= 3) { q = "Q1"; }
else if (month >= 4 && month <= 6) { q = "Q2"; }
else if (month >= 7 && month <= 9) { q = "Q3"; }
else { q = "Q4"; }

// Generate the frontmatter and content
tR += `---
employer: Red Hat
title: Quarterly Connection ${year}-${q}
url: https://source.redhat.com/career/talent_management#tab-quarterly-connections
date: ${d}
quarter: ${year}-${q}
tags:
  - prodev
  - ${year}-${q}
Topics:
  - Topics/Career
---

# Quarterly Connection ${year}-${q}

`;

console.log(`Attempting to rename to: ProDev/Quarterly-Connections/${year}-${q}-qc`);
await tp.file.move(`ProDev/Quarterly-Connections/${year}-${q}`);
console.log("Rename completed");
%>


## Goals
- [ ] Goal 1 – _description / progress update_
- [ ] Goal 2 – _description / progress update_

---

## Accomplishments (Last Quarter)
### **WHAT:**
  - *List tangible results delivered.*
### **HOW:**
  - *Describe behaviors, collaboration, or methods you used.*

---

## Priorities (This Quarter)
1. Priority 1
2. Priority 2
3. Priority 3

---

<%* if (q === "Q1") { %>
## Role Enjoyment
- Most enjoyable parts of my job:
- Least enjoyable parts of my job:
- What gives me energy / takes my energy away:

---

## Manager Support
- Support I need to be successful:
- Specific ways my manager can help:
<%* } else if (q === "Q3") { %>
## Feedback & Development
- Feedback received over past 2 quarters (emails, 1:1s, Reward Zone, etc.):
- Actions/adjustments I am making:

---

## Impact & Career Growth
### **Impact at Red Hat:**
### **Career aspirations:**
  - Short term (1–2 years):
  - Long term (3–5 years):

---

## Manager Support
- Support I need to be successful:
- Specific ways my manager can help:
<%* } %>

## Notes
- Freeform space for anything that doesn’t fit neatly into the prompts.

## Reference
- Workday Goals https://wd5.myworkday.com/redhat/d/task/2998$46108.htmld
- Example Responses https://docs.google.com/presentation/d/1QOiHC65CNh8aPa_qpIWggS4yLHWdU6hyIobaHdMvIks/edit?slide=id.g32cdd77b92d_0_169#slide=id.g32cdd77b92d_0_169
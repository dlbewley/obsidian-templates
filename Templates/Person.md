---
tags:
  - person
Topics:
  - "[[Topics/People]]"
email: []
blog:
github-login:
work-login:
---

## Contact
- Email `= "[" + this.email + "](mailto://" + this.email[0] + ")"`
- Rover `= "[" + this.work-login + "](https://rover.redhat.com/people/profile/" + this.work-login + ")"`
- Blog  `= elink(this.blog, this.blog)`

## Correspondance
- Gmail `= "[search](https://mail.google.com/mail/u/0/#search/" + firstvalue(this.email) + ")"`
- Calendar `= "[events](https://calendar.google.com/calendar/u/0/r/search?q=" + firstvalue(this.email) + ")"`

## Repositories
- Github `= "[" + this.github-login + "](https://github.com/" + this.github-login + ")"`
- Github `= "[search](https://github.com/search?type=users&q=" + this.github-login + ")"`

### Saved Repositories
```dataview
LIST
WHERE contenttype = "Repo" AND owner = this.github-login
```
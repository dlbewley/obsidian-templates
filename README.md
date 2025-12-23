# Obsidian Templates

![Built with AI](https://img.shields.io/badge/Built%20with-AI-blueviolet?style=for-the-badge)

I need a place to keep my collection of templates for Obsidian documents and the Obsidian Web Clipper extension.
These are some of them.

## Web Clipper Templates

These are based on the works of others. I have modified them to better suit my needs or just copied them here for convenience. See the [list of sources below](#other-template-sources-i-benefited-from).

* [default-clipper.json](web-clipper-templates/default-clipper.json)
  - Clipper for general web pages

* [github-repository-clipper.json](web-clipper-templates/github-repository-clipper.json)
  - Clipper for GitHub repositories

* [google-mail-clipper.json](web-clipper-templates/google-mail-clipper.json)
  - Clipper for Google Mail

## Obsidian Document Templates

These are basic templates that may use dataviewjs to perform some inline queries.

* [Person.md](Templates/Person.md)
  - Collect details about a person

* [Topic.md](Templates/Topic.md)
  - Form an overview of a topic. Notes frontmatter will referrence `Topics: "[[Topics/Foo]]"` making them easy to discover via the topic page.

> [!NOTE]
> These following document templates rely on the [Templater plugin](https://github.com/SilentVoid13/Templater).

* [daily.md](Templates/daily.md)
  - Create a daily note

* [weekly.md](Templates/weekly.md)
  - Create a weekly note with links to all days that week

* [monthly.md](Templates/monthly.md)
  - Create a monthly note with links to all days and weeks that month

* [Quarterly Connections.md]("Templates/Quarterly Connections.md")
  - Create a quarterly connections note used for employee reviews

# Obsidian Vault Folder Structure

This is all still a WIP after months of dabbling in Obsidian, but here you go...

* Web Clipper Clippings By Source
```
Clippings/
  ├── GitHub/
  ├── Google/
  └── Web/
```

* Daily notes over time

Notes are moved to Archive after they have been processed into weekly or monthly notes.

```
Journal/
  ├── Archive/
  ├── Daily/
  ├── Weekly/
  └── Monthly/
```

* Career Stuff

```
ProDev/
  └─── Quarterly Connections/
    ├── 2025-Q3.md
    └── 2025-Q4.md
```

* Topics make a great overview page for a collection of notes on a topic. This is highly augmented by using the local Graph view to see connections. Here is a random sample of topics.

```
Topics/
  ├── Career.md
  ├── Networking.md
  ├── OpenShift.md
  ├── People.md
  ├── Sales.md
  └── Virtualization.md
```

# Other Template Sources I Benefited From

- https://github.com/obsidian-community/web-clipper-templates/tree/main
- https://github.com/Fred-Vatin/Web-Clipper-Templates
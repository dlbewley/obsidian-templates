# Obsidian Web Clipper Templates

## Official Documentation

*   **Official Help**: [Obsidian Web Clipper Help](https://help.obsidian.md/web-clipper)
*   **GitHub Repository**: [obsidianmd/obsidian-clipper](https://github.com/obsidianmd/obsidian-clipper)
*   **Template Reference**: [Templates.md](https://github.com/obsidianmd/obsidian-clipper/blob/main/docs/Templates.md) (Formal schema definition)
*   **Variable Reference**: [Variables.md](https://github.com/obsidianmd/obsidian-clipper/blob/main/docs/Variables.md)


## Schema Reference

The top-level structure of a clipper template is a JSON object with the following fields:

| Field | Type | Description |
| :--- | :--- | :--- |
| `schemaVersion` | String | The version of the schema verification (e.g., `"0.1.0"`). |
| `name` | String | The display name of the template in the extension. |
| `behavior` | String | The action to take. Common value: `"create"`. |
| `noteContentFormat` | String | The template string for the content of the new note. |
| `noteNameFormat` | String | The template string for the filename of the new note. |
| `path` | String | The default folder path where the note will be created. |
| `triggers` | Array\<String\> | A list of URL patterns that automatically trigger this template. |
| `properties` | Array\<Object\> | A list of frontmatter properties to add to the note. |

### Property Object

Each item in the `properties` array defines a frontmatter field:

| Field | Type | Description |
| :--- | :--- | :--- |
| `name` | String | The key name of the property in the frontmatter. |
| `value` | String | The value for the property. Can contain variables. |
| `type` | String | The data type (e.g., `"text"`, `"multitext"`, `"date"`, `"datetime"`, `"number"`). |

## Variables

Variables are placeholders enclosed in double curly braces `{{...}}` that are replaced with extracted data when the clipper runs.

### Standard Variables

| Variable | Description |
| :--- | :--- |
| `{{title}}` | The title of the web page. |
| `{{content}}` | The main content of the article (often simplified). |
| `{{url}}` | The URL of the web page. |
| `{{date}}` | The current date. |
| `{{time}}` | The current time. |
| `{{published}}` | The publication date (if detectable). |
| `{{author}}` | The author's name (if detectable). |
| `{{description}}` | The meta description of the page. |

### Selector Variables

Extract content from specific HTML elements using CSS selectors.

*   **Text content**: `{{selector:css_selector}}`
    *   Example: `{{selector:#repo-stars-counter-star}}` gets the text inside the element with ID `repo-stars-counter-star`.
*   **HTML content**: `{{selectorHtml:css_selector}}`
    *   Example: `{{selectorHtml:article}}` gets the raw HTML of the `<article>` element.

### Meta Variables

Extract content from `<meta>` tags.

*   Syntax: `{{meta:name:attribute_value}}`
*   Example: `{{meta:name:octolytics-dimension-user_login}}` looks for `<meta name="octolytics-dimension-user_login" content="...">`.

### JSON-LD / Schema.org Variables

Extract data from Schema.org structured data (JSON-LD).

*   Syntax: `{{schema:property}}`
*   Example: `{{schema:datePublished}}`

## Filters

Filters transform the value of a variable. They are applied using the pipe `|` character.

*   **`date:"format"`**: Format a date string (e.g., `date:"YYYY-MM-DD"`).
*   **`split:"separator"`**: Split a string into a list.
*   **`join:"separator"`**: Join a list into a string.
*   **`first`**: Get the first item from a list or the first match of a selector.
*   **`markdown`**: Convert HTML to Markdown.
*   **`remove_tags:"tags"`**: Remove specific HTML tags (e.g., `remove_tags:"table,tr"`).
*   **`wikilink`**: valid only for generic text, transforms text into `[[text]]`.
*   **`safe_name`**: Sanitize a string for use in valid filenames.

## Examples

### Basic Template

```json
{
  "schemaVersion": "0.1.0",
  "name": "Simple Clip",
  "behavior": "create",
  "noteContentFormat": "{{content}}",
  "properties": [
    {
      "name": "url",
      "value": "{{url}}",
      "type": "text"
    }
  ],
  "triggers": [],
  "noteNameFormat": "{{title}}",
  "path": "Clippings"
}
```

### Advanced Selectors (GitHub Example)

```json
{
  "name": "GitHub Repo",
  "noteContentFormat": "## README\n\n{{selectorHtml:article|markdown}}",
  "properties": [
    {
      "name": "stars",
      "value": "{{selector:#repo-stars-counter-star}}",
      "type": "number"
    },
    {
      "name": "tags",
      "value": "github, {{selector:.topic-tag|join:\", \"}}",
      "type": "multitext"
    }
  ]
}
```

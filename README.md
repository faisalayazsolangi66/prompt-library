# Prompt Library

Save, list and search reusable prompt templates.

Templates are stored as JSON in a local file — by default
`~/.prompt-library.json` (override with `--store FILE`). Each template
has a name, the prompt text, and optional tags.

## Requirements

- Python 3 (standard library only — no extra packages)

## Usage

```bash
python3 main.py add code-review --text "Review this code: {code}" --tag code
python3 main.py list
python3 main.py search review
python3 main.py get code-review
python3 main.py delete code-review
```

Commands:

- `add NAME --text TEXT [--text-file FILE] [--tag TAG ...] [--force]`
  — save a template (refuses to overwrite unless `--force` is given)
- `list` — list all saved templates with a preview
- `get NAME` — print one template's full text
- `search QUERY` — search names, text, and tags
- `delete NAME` — delete a template

## Example

```bash
$ python3 main.py add code-review --text "Review this code: {code}" --tag code
Saved template 'code-review' (24 chars).

$ python3 main.py search review
code-review: Review this code: {code}

1 match(es).

$ python3 main.py get code-review
Review this code: {code}
```

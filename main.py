#!/usr/bin/env python3
"""Save, list and search reusable prompt templates.

Templates are stored as JSON in a local file (default:
~/.prompt-library.json). Each template has a name, the prompt text,
and optional tags.

Usage:
    python3 main.py add code-review --text "Review this code: {code}" --tag code
    python3 main.py list
    python3 main.py search review
    python3 main.py get code-review
    python3 main.py delete code-review
"""
import argparse
import json
import os
import sys

DEFAULT_STORE = os.path.expanduser("~/.prompt-library.json")


def load_store(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"ERROR: cannot read store {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if not isinstance(data, dict):
        print(f"ERROR: store {path} is not a JSON object.", file=sys.stderr)
        raise SystemExit(1)
    return data


def save_store(path, data):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def cmd_add(args):
    store = load_store(args.store)
    if args.name in store and not args.force:
        print(f"ERROR: template {args.name!r} already exists; "
              f"use --force to overwrite.", file=sys.stderr)
        return 1
    text = args.text
    if args.text_file:
        with open(args.text_file, encoding="utf-8") as handle:
            text = handle.read().strip()
    store[args.name] = {"text": text, "tags": args.tag or []}
    save_store(args.store, store)
    print(f"Saved template {args.name!r} ({len(text)} chars).")
    return 0


def cmd_list(args):
    store = load_store(args.store)
    if not store:
        print("No templates saved yet. Add one with: "
              "python3 main.py add <name> --text \"...\"")
        return 0
    for name in sorted(store):
        entry = store[name]
        tags = ", ".join(entry.get("tags", []))
        preview = entry["text"].splitlines()[0][:70]
        print(f"{name}" + (f"  [{tags}]" if tags else ""))
        print(f"    {preview}")
    print(f"\n{len(store)} template(s).")
    return 0


def cmd_get(args):
    store = load_store(args.store)
    entry = store.get(args.name)
    if entry is None:
        print(f"ERROR: no template named {args.name!r}.", file=sys.stderr)
        return 1
    print(entry["text"])
    return 0


def cmd_search(args):
    store = load_store(args.store)
    query = args.query.lower()
    hits = {n: e for n, e in store.items()
            if query in n.lower() or query in e["text"].lower()
            or any(query in t.lower() for t in e.get("tags", []))}
    if not hits:
        print(f"No templates matching {args.query!r}.")
        return 0
    for name in sorted(hits):
        print(f"{name}: {hits[name]['text'].splitlines()[0][:80]}")
    print(f"\n{len(hits)} match(es).")
    return 0


def cmd_delete(args):
    store = load_store(args.store)
    if args.name not in store:
        print(f"ERROR: no template named {args.name!r}.", file=sys.stderr)
        return 1
    del store[args.name]
    save_store(args.store, store)
    print(f"Deleted template {args.name!r}.")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Save, list and search reusable prompt templates.")
    parser.add_argument("--store", default=DEFAULT_STORE,
                        help="JSON store file (default: %(default)s)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="save a new template")
    p.add_argument("name", help="template name")
    p.add_argument("--text", help="prompt text")
    p.add_argument("--text-file", help="read prompt text from a file")
    p.add_argument("--tag", action="append", default=[],
                   help="tag for the template (repeatable)")
    p.add_argument("--force", action="store_true",
                   help="overwrite an existing template of the same name")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="list all templates")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("get", help="print one template's text")
    p.add_argument("name", help="template name")
    p.set_defaults(func=cmd_get)

    p = sub.add_parser("search", help="search names, text and tags")
    p.add_argument("query", help="search term")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("delete", help="delete a template")
    p.add_argument("name", help="template name")
    p.set_defaults(func=cmd_delete)

    args = parser.parse_args(argv)
    if args.command == "add" and not args.text and not args.text_file:
        parser.error("add needs --text or --text-file")
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

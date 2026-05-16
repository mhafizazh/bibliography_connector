# Bibliography Connector — Integration Plan

Rewrite the existing Interlisp.org `update_bibliography.sh` pipeline (bash + jq + Perl) into this Python library.

## Current Architecture (to be replaced)

```
update_bibliography.sh
├── curl (Zotero API, paginated, recursive collections)
├── jq + bib-fns.jq (~20 inline transforms)
├── bibSplit.pl (Perl → Hugo .md generation)
├── bash flags (--rawitems, --tagsfile, --typefiles, --collectionsfiles, --infolevel)
```

## Draft Assessment: What's Good

The hexagonal architecture (`providers/`, `transforms/`, `exporters/`, `pipeline.py`, `cli.py`) and dependency choices (httpx, typer, rich, pyyaml) are solid. The PLAN.md shows good understanding of the full scope.

## Draft Assessment: What's Missing

The implementation is roughly **10% complete** relative to the bash script.

### 1. Provider (`providers/zotero.py`)

| Missing Feature | As implemented in bash |
|---|---|
| **Pagination** | Fetches only 1 page (max 100 items). Bash paginates with `start=0; limit=100` loop |
| **Subcollection recursion** | Fetches only one collection. Bash recursively calls `add_items_from_collection()` on subcollections |
| **Child/parent fetching** | Bash calls `getNeededUrls` to fetch parent items not yet in the set |
| **`include=data,csljson`** | URL is bare — no `?include=...` params |

**Fix needed:** Rewrite `fetch()` to:
- Accept optional `input_file` for offline mode
- Recursively walk collection tree
- Paginate at 100 items per request
- Fetch missing parent items after initial collection fetch

### 2. Transforms (`transforms/` — only 2 of ~20 exist)

Only `clean.py` (extracts 4 fields) and `remdup.py` (simple dedup) exist. **18+ transforms missing:**

- `semiflatten` — elevate `.csljson` and `.data` sub-keys to top level
- `clean_notes` — unwrap HTML `<div>` from note fields
- `strip_metadata` — remove `library`, `links`, `meta`, `accessed`, `dateAdded`
- `consolidate_urls` — `URL` → `url` casing
- `doi_to_url` — construct URL from DOI when missing
- `resolve_targets` — add `target` field (parentItem or self)
- `group_and_embed_children` — group by parent, nest children
- `remove_deleted` — filter `.deleted == true`
- `apply_child_amendments` — update parent URL from child
- `clean_abstracts` — reconcile abstract vs abstractNote
- `format_dates` — add `isoDateString`, `readableDateString`
- `format_authors` — add `authorsFormatted`, `editorsFormatted`
- `generate_tags` (conditional, for `--tagsfile`)
- `generate_type_info` (conditional, for `--typefiles`)

### 3. Exporter (`exporters/hugo.py`)

Current output (4 fields) vs **required output** (20+ fields):

```yaml
# Current draft:
title: "TENEX and TOPS-20"
date: "2015-01-01"
URL: https://...

# Required (matches bibSplit.pl output):
---
title: |
  TENEX and TOPS-20
date: 2015-01-01
readabledate: 2015-01-01
type: bibliography
item_type: article-journal
authors:
  - "Murphy, Dan"
editors:
abstract: |
  In the late 1960s...
publication_title: "Annals of History of Computing, IEEE"
volume: "37"
issue: ""
pages: "75-82"
tags:
url_source: https://...
zotero_url: "https://www.zotero.org/groups/2914042/items/23ZCTJ9Z"
lastmod: 2024-06-12T09:27:22Z
---
```

Also missing:
- **Type-specific extra fields** (bibSplit.pl has 10+ branches: `paper-conference` → conference_name/place/proceedings_title; `article-journal` → publication_title/volume/issue/pages; `book` → publisher/place; etc.)
- **Unicode sanitization** (NFC normalization, control char removal, NBSP→space, `\n•` → `\n*` for bulleted abstracts)
- **`bibliography-items-by-line.json`** output (one JSON object per line, not pretty-printed array)
- **JSON files** for `collections.json`, `grouped_collections.json`, `tags.json`, type info files

### 4. CLI & Config

| Aspect | Current draft | Needs |
|---|---|---|
| **Flags** | None | `-h`, `-r/--rawitems`, `-g/--tagsfile`, `-y/--typefiles`, `-c/--collectionsfiles`, `-i/--infolevel`, `--input-items path` |
| **Config paths** | Only `markdown_dir` + `json_file` | Needs `bibitems_dir`, Zotero API base URL, `v=3` param, collection metadata |
| **Logging** | None (uses `rich.print`) | Infolevel 0–10 system matching bash |
| **Offline mode** | Not implemented | Accept cached JSON file instead of API call |

### 5. Integration Script (`update_bibliography.sh`)

The bash script currently isn't mentioned in the draft — it needs to become a thin wrapper:

```bash
#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python "$SCRIPT_DIR/bibliography_connector/cli.py" sync "$@"
```

## Required Changes Summary

| Module | Effort | Key Changes |
|---|---|---|
| `providers/zotero.py` | Medium | Rewrite with pagination, recursion, child fetching, offline mode |
| `transforms/` | Large | Create 8-12+ new transform modules (currently 2 of ~20 exist) |
| `exporters/hugo.py` | Large | Rewrite to match full bibSplit.pl output (YAML front matter, type branches, sanitization) |
| `pipeline.py` | Medium | Wire all transforms in correct order |
| `cli.py` | Medium | Add all flags, infolevel, offline mode, configurable paths |
| `config.yaml` | Small | Add all paths, API params |
| `update_bibliography.sh` | Small | Rewrite as thin Python wrapper |

**Biggest gap:** The transforms and exporter are where the complexity lives. The bash script has ~400 lines of jq logic and ~200 lines of Perl generation — only about 30 lines of Python exist so far.

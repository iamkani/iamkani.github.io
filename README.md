# iamkani.github.io

A portfolio of data projects that say how sure they are. Served by GitHub Pages from `docs/`.

## Build

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python build.py    # content/*.md -> docs/
.venv/bin/python check.py    # leak and link check; must pass before every push
```

- **Pages** are markdown files in `content/`, with YAML front matter. The front matter holds the page's evidence ledger: what was verified by running, what is built but only dry-run, and what isn't proven yet.
- **Figures and tables** are generated from the project repos at build time (`AC_SAR_REPO`, default `~/Documents/GitHub/ac-sar`). Only the built HTML is committed.
- **`check.py`** fails the build on email addresses, on internal working terms, on any term in a local `.blocklist` (gitignored), and on broken internal links.

## Design

The evidence desk: a charcoal rail, a paper-grey desk, a white evidence panel, and one accent, a yellow tag used only for citations. Typeset in IBM Plex.

## Sources

See [Sources and licences](https://iamkani.github.io/sources/). The project pages are derived from Government of Canada publications, used for non-commercial purposes. This site is not affiliated with or endorsed by the Government of Canada.

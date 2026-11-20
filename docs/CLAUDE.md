# docs/CLAUDE.md

Documentation guidance. The root `CLAUDE.md` holds the project-wide rules, gates
and commands.

## Stack

Sphinx with MyST: pages are Markdown (`.md`), and each section's `index.rst` is
a toctree only. The theme is Furo, and diagrams use `sphinxcontrib-mermaid`.
`make docs.write` serves a live-reloading build on `DOCS_PORT`. `make
docs.render` builds with `-nW`, so any warning, such as a page missing from
every toctree, fails it.

## Structure

`docs/source/` holds the `domain/` and `process/` sections, each an `index.rst`
with its pages under `source/`, plus loose pages at the top. A new page appears
only once a toctree lists it.

## Markup

- Admonitions use colon fences: `:::{note}` ... `:::`.
- Glossary terms live in `domain/source/terminology.md`, the only `{.glossary}`.
  Link a term with `` {term}`Bounded Context` `` and never define one inline.
- Every code block names its language.

## What the docs are not

A page says how things work and cites the ADR or ticket for why. It does not
restate a decision, which lives in its ADR, or the domain model, which lives in
`CONTEXT.md`.

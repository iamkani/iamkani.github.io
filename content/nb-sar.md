---
slug: nb-sar
nav: NB-SAR
status: live
order: 2
kicker: Project · document intelligence · built July 2026
title: "NB-SAR: 30 species-at-risk documents, one cited knowledge graph"
lede: A per-page extraction pipeline that reads federal species-at-risk recovery documents for New Brunswick, links the species, threats, measures and places they mention, and ties every item to a quote on the page it came from.
ev_kicker: NB-SAR
ev_title: Evidence ledger
ev_note: Measured over the 30-document corpus. The model layer stands in as a deterministic extractor until the live pass is run.
ledger:
  - kind: ok
    head: Verified by running
    rows:
      - [Corpus, "30 documents, 1,600 pages, 3 document types, English and bilingual"]
      - [Graph, "562 nodes, 76 edges, 693 node → document links"]
      - [Grounding, "100 %: 149 of 149 items in the hand-built gold, and every graph edge"]
      - [Scale, "1 → 30 documents with no structural rewrites; a 183-page document runs in under a minute"]
      - [Routing, "Figure pages picked for the gold document match the hand-labelled set exactly"]
  - kind: caution
    head: Built, dry-run only
    rows:
      - [Text pass, "LLM executor wired, cached and checkpointed; not run live yet"]
      - [Vision pass, "Renders figure pages with a document digest as context; not run yet"]
      - [Page cards, "Image page → retrievable text: one worked example"]
  - kind: unverified
    head: Not yet proven
    issues:
      - q: Relationships are sparse
        note: 17 non-trivial edges beyond the gold; 10 multi-species action plans produced none
      - q: 94 image-only pages unextracted
        note: Critical-habitat maps and figures in 22 of the 30 documents
      - q: Cross-document identity is exact-name only
        note: 521 of 562 nodes appear in a single document
      - q: One merge bug, found while building this page
        note: 29 different publication dates collapsed into one node named "publication", so the honest count of shared entities is 40, not 41
---

## What problem does it solve?

Recovery strategies, action plans and management plans are long PDFs, 20 to 183 pages each, full of species rosters, threat tables and maps. The useful questions cut across documents. Which threats recur for bats? Which measures are planned on the Saint John River? Which species share a park's action plan with the one you're working on?

NB-SAR turns 30 of these documents into one graph. Every node and edge points back to the page, and the words, it came from.

## How is it built?

Four rules shape the design:

- **The page is the unit and the citation key.** Every result maps back to a document and page, and merges into the graph by that key.
- **Flag, don't invent.** Every entity and relationship carries a verbatim quote from its page. Anything that can't be found on the page is flagged, never loaded silently.
- **The model proposes; a deterministic layer disposes.** A grounding gate, a predicate registry and entity resolution decide what enters the graph.
- **Provenance everywhere.** Nodes know their source documents, and edges carry their evidence page and quote.

The flow:
1. Route each page: text only, text and image, or image only.
2. Reconstruct its tables.
3. Run a text pass, and build a digest of the document.
4. Run a vision pass on figure pages, with the digest as context.
5. Validate, normalise, and merge into one corpus graph. [[PIPELINE_EVALUATION §1]]

## What held up across 30 documents?

The corpus grew in rounds (1 → 3 → 5 → 10 → 30 documents), and each round was picked to break something: action plans with 5 to 42 species, a 183-page strategy, a 115-page map atlas, bilingual tables, and a roster with a Mi'kmaq-name column. Every break was diagnosed by running, and logged: [[DECISIONS_LEDGER]]

- The PDF library invented tables from ruled prose → a gate that recognises real tables.
- A species roster spread over three pages stopped at the first → parsing continues across pages.
- A Mi'kmaq column moved the Latin names → parsing no longer depends on column order.
- A title pattern that assumed "for **the** species" missed two documents → the parser anchors on the scientific name instead.

Every fix landed in the stand-in extractor; none needed a change to the pipeline's structure. [[PIPELINE_EVALUATION §2]]

{{figure:top_species}}

## What is the bar the model has to beat?

The LLM layer hasn't been run yet, so a deterministic extractor stands in for it. It is scored against a hand-built gold for one document: the 25-page recovery strategy for the Cobblestone Tiger Beetle. [[CORPUS_EVALUATION]]

| | Precision | Recall |
|---|---:|---:|
| Entities | 0.74 | 0.19 |
| Relationships | 0.67 | 0.15 |

That's the floor. The live model pass has to raise recall without giving up grounding.

## What isn't proven yet?

No live LLM or vision call has been made. 94 image-only pages are unextracted, relationships are sparse, cross-document identity is exact-name only, and there's no query layer yet. The ledger on the right gives the numbers.

## What did extending it reveal?

Scoping the Atlantic extension showed that the federal registry tags documents by **species range**, not by place. Five of NB-SAR's 30 documents are plans for parks in British Columbia, Ontario and Quebec, included because they cover wide-ranging bats. They stay in the graph and will be flagged. The rest of that story is on [AC-SAR](/ac-sar/).

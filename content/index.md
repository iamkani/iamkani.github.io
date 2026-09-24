---
slug: ""
nav: Home
order: 1
plain: true
kicker: Portfolio
title: Data projects that say how sure they are
lede: Each project here separates what was verified by running from what is only built, planned, or waiting on someone else. Claims carry their evidence the way an answer carries its citations.
cards:
  - href: /nb-sar/
    kind: Live · document intelligence
    title: NB-SAR
    text: 30 species-at-risk recovery documents (1,600 pages) turned into one knowledge graph where every item cites the page it came from.
    foot: 562 nodes · 76 edges · 100 % of edges grounded
  - href: /ac-sar/
    kind: Scoping · extension of NB-SAR
    title: AC-SAR
    text: Taking NB-SAR to Atlantic Canada. Counting what the registry really holds turned up a filter that overshoots, and 74 new documents in scope.
    foot: 117 tagged → 99 in scope → 74 new
ev_kicker: Reading this site
ev_title: The evidence ledger
ev_note: Every project page ends its claims in a ledger like this one, on the right.
ledger:
  - kind: ok
    head: Verified by running
    rows:
      - [Means, "A number produced by running the code on the real documents, and reproducible"]
  - kind: caution
    head: Built, dry-run only
    rows:
      - [Means, "The code exists and runs end to end, but the step that matters hasn't been run for real yet"]
  - kind: unverified
    head: Not yet proven
    issues:
      - q: A gap, stated plainly
        note: With the number that shows it, rather than left out
---

## What ties these together

Both projects come from the same habit: before believing a result, look for the test that could break it, then say which claims survived.

NB-SAR grew from 1 to 30 documents by picking documents that would break it, and logging every fix. AC-SAR started by counting what the federal registry actually holds before running anything, and found that the registry's own province filter follows species ranges, not places.

Yellow tags such as [[DECISIONS_LEDGER]] cite the document a claim rests on.

---
slug: ac-sar
nav: AC-SAR
status: scoping
order: 3
kicker: Project · extension of NB-SAR · scoped September 2026
title: "AC-SAR: taking NB-SAR to Atlantic Canada"
lede: Before running anything, count what exists. Scoping against the federal registry's own index found 74 new documents in scope, a province filter that quietly overshoots, and provincial sources that need permission first.
ev_kicker: AC-SAR
ev_title: Evidence ledger
ev_note: Counts measured on 2026-09-24 against the registry's document index. One script reproduces them.
ledger:
  - kind: ok
    head: Measured
    rows:
      - [Tagged, "117 final recovery documents carry at least one Atlantic province"]
      - [Scope, "18 are site plans for parks elsewhere; 99 remain in scope"]
      - [New, "25 of the 99 are already in NB-SAR; 74 are new"]
  - kind: caution
    head: Planned
    rows:
      - [AC1, "Run the 74 new documents through the existing pipeline and log every break"]
      - [AC2, "Scope and jurisdiction fields; de-duplicate across jurisdictions; score against CAN-SAR"]
      - [AC4, "Live LLM and vision passes over the Atlantic corpus (needs an API budget)"]
  - kind: unverified
    head: Waiting on others
    issues:
      - q: Nova Scotia provincial plans
        note: About 67 documents under Crown copyright, with no reuse licence stated. Permission needed; request drafted
      - q: New Brunswick provincial registry
        note: NB supplements and protection assessments. Permission needed; request drafted
      - q: Newfoundland and Labrador plans
        note: Listed species have plans, but none are linked online. Documents and permission needed; request drafted
---

## What counts as "Atlantic"?

The federal Species at Risk registry lists these final recovery documents (recovery strategies, action plans and management plans) for each province:

| New Brunswick | Nova Scotia | Prince Edward Island | Newfoundland and Labrador | Any of the four |
|---:|---:|---:|---:|---:|
| 84 | 85 | 47 | 66 | **117** |

But the registry tags a document with every province in its **species'** range. A multi-species plan for Banff or Kootenay counts as "New Brunswick" because it covers a wide-ranging bat. **18 of the 117 are site plans for places outside Atlantic Canada**, and 5 of those were already in NB-SAR.

The scope rule that follows: a species document is in scope if any Atlantic province is in its range; a site-based plan is in scope only if the site is in Atlantic Canada.

## What's left after the rule?

**99 documents are in scope. 25 are already in NB-SAR, so 74 are new.**

- **By type:** 34 recovery strategies, 21 management plans, 14 action plans, and 5 combined documents.
- **By range:** 18 cover Newfoundland and Labrador only, 13 Nova Scotia only and 8 New Brunswick only; 35 span two or more provinces.
- **By department:** most are led by Environment and Climate Change Canada, 14 by Fisheries and Oceans Canada (marine and freshwater species), and a few by Parks Canada.
- **By size:** about 3,400 pages. This is an estimate, using NB-SAR's median of about 46 pages per document.

All five Atlantic Parks Canada site plans in the index (Kouchibouguac, Kejimkujik, Prince Edward Island, Gros Morne and Terra Nova) are already in NB-SAR.

## Where else do the documents live?

| Tier | Source | Adds | Access |
|---|---|---|---|
| 1 | Federal registry: recovery strategies, action plans, management plans | The 74 new documents | Open; non-commercial reuse with attribution |
| 1 | Critical-habitat national dataset | Polygons to check map-page extraction against | Open |
| 1 | CAN-SAR (1,146 documents, 594 species) | Threats and actions transcribed by people from the same documents | Open, CC BY 4.0 |
| 2 | Nova Scotia *Endangered Species Act* plans | About 67 provincial documents; the same species under a second authority | Online; permission needed |
| 2 | New Brunswick provincial registry | NB supplements, protection assessments | Online; permission needed |
| 2 | Newfoundland and Labrador *Endangered Species Act* | Provincial recovery and management plans | Not online; request needed |
| 3 | Fisheries and Oceans science advice (recovery potential assessments) | A second, marine-science genre | Open |
| 3 | Atlantic Canada Conservation Data Centre | Real occurrence records to check extracted locations | Paid request; only if needed |

Prince Edward Island has no species designated under provincial law, so it relies on federal documents only.

## What will it stress?

- **The same species under several authorities:** a federal strategy, a Nova Scotia plan, an NB supplement and a park action plan. Entity resolution has to merge the species while keeping four documents with different authority.
- **Marine documents,** with new taxa, new threats (bycatch, entanglement, vessel strikes) and new table layouts.
- **Provincial formats** that don't follow the federal template.
- **Scale:** 3–4 times NB-SAR once provincial documents join.

## How will it be judged?

Against something the pipeline didn't produce. CAN-SAR records threat categories and action types that people transcribed from the same recovery documents, so it is an independent benchmark for what AC-SAR extracts. Each new genre (a Nova Scotia provincial plan, a marine strategy) also gets a hand-built gold for one document, as NB-SAR did with the Cobblestone Tiger Beetle.

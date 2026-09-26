---
doc_id: RDK-DDR-002
title: ReadyKit recommendations accepted
project: ReadyKit
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CC-BY-SA-4.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted. Every item below that carried a recommendation is "Decided by Amish, 2026-09-25: go with recommendation". Items with no recommendation stay "Proposed, awaiting Amish".

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." RDK-DDR-001 had adopted seven items (D1 to D7) for TRL 3 work, open for his review, and the TRL 3 review note (`docs/REVIEW.md`) proposed a route for two unmet requirements (R6 and R15). This record turns each of those recommendations into a decision, says what changed in the repository because of it, and lists what is still open.

TRL 4 remains on hold by Amish's instruction. A decision whose implementation is building, packaging, publishing or testing the tool is recorded as decided but on hold. Changes to the shared kit (`.kit/`) are not made inside a project repository; they are listed as cross-repo actions in `docs/REVIEW.md`.

## Options considered

The options for D1 to D7 are in RDK-DDR-001 and in `docs/REVIEW.md` (session 2026-09-25, /populate). The routes for R6 and R15 are in RDK-REQ-001 v0.3, Table 3. Where a recommendation offered several options, the recommended option is the decision.

## Decision

*Table 1. Items decided on 2026-09-25.*

| # | Item | Decision | Status | What changed in this repository |
| --- | --- | --- | --- | --- |
| D1 | Distribution | Pip package `readykit` with a pinned `.kit/` stub, plus a GitHub template repository | Decided by Amish, 2026-09-25: go with recommendation. Build on hold (TRL 4) | Wording in RDK-PRC-001, RDK-REQ-001 (R10, R12), `bom/bom.csv` item 7 and RDK-DWG-001 notes. Nothing built |
| D2 | Identity and branding | Organization name, website, repository owner, author and colors in `readykit.yaml`, with Design Molecule defaults | Decided by Amish, 2026-09-25: go with recommendation. Build on hold (TRL 4); kit change listed as a cross-repo action | R11 wording. RDK-CAL-001 v0.2 recounts the hard-coded identity after the site change: 13 occurrences of 5 values (was 13 of 4) |
| D3 | Sheet sizes | Add ISO A3 (420 x 297 mm) beside ANSI B; ISO A2 later if asked for | Decided by Amish, 2026-09-25: go with recommendation. Kit change on hold (TRL 4) | `cad/src/model.py` already switches the sheet parameter between ANSI B and ISO A3; comment and RDK-DWG-001 notes now say "decided" |
| D4 | Command-line interface | One `readykit` command (`init`, `check`, `render`, `media`, `upgrade`); present scripts kept as wrappers | Decided by Amish, 2026-09-25: go with recommendation. Build on hold (TRL 4) | R18 wording |
| D5 | Licensing | Code under MIT; non-code content (documents, drawings, CAD, BOM, media) under CC BY-SA 4.0 | Decided by Amish, 2026-09-25: go with recommendation. **Applied** | `LICENSE` now holds the CC BY-SA 4.0 legal code (was CERN-OHL-S v2); `project.yaml` `licenses.hardware` CERN-OHL-S-2.0 to CC-BY-SA-4.0 (key name kept so the website card still reads it) and tag `cern-ohl-s` to `cc-by-sa`; README badge and Licenses section; `CONTRIBUTING.md`; the `license` field of every controlled document; the title block of RDK-DWG-001 (Rev P2) and of the concept blueprint RDK-DWG-010 |
| D6 | Standards interoperability | Open Know-How 1.0 manifest export (R16) | Decided by Amish, 2026-09-25: go with recommendation. Exporter on hold (TRL 4) | R16 wording |
| D7 | TRL 3 evidence for a software project | Massing STEP and STL, pipeline GA sheet, measurement note, budget $0 | Decided by Amish, 2026-09-25: go with recommendation | Already in place; no further change. `budget_usd` stays $0 |
| D8 | Route for R6, check coverage | Add at least six of the eight missing checks in RDK-REQ-001, Table 4 | Decided by Amish, 2026-09-25: go with recommendation. Build on hold (TRL 4); kit change listed as a cross-repo action | R6 route in RDK-REQ-001 Table 3 |
| D9 | Route for R15, documentation | Write the getting-started guide together with the package | Decided by Amish, 2026-09-25: go with recommendation. On hold with D1 (TRL 4) | R15 route in RDK-REQ-001 Table 3 |

*Table 2. Items still open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Name "ReadyKit" for PyPI and GitHub. No recommendation was made. | Proposed, awaiting Amish |
| O2 | Pilot users: a university lab, an open science hardware group or a startup. No preference was stated. | Proposed, awaiting Amish |
| O3 | Windows: native support required, or WSL2 enough? No recommendation was made. | Proposed, awaiting Amish |
| O4 | Decision-wording check (R13): generic, or tied to the portfolio phrase? No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: `licenses.hardware` and one tag change (D5); DDR-002 added to the TRL evidence list. `budget_usd` stays $0, and the pitch and problem are unchanged, because no recommendation touched them. `trl` and `trl_target` stay at 3.
- Controlled documents revised: RDK-PRB-001 v0.3, RDK-PRC-001 v0.4, RDK-REQ-001 v0.4, RDK-CAL-001 v0.2 and RDK-DDR-001 v0.2. RDK-DWG-001 moves to Rev P2 because its title block license and notes changed; the geometry is unchanged.
- Requirement status is unchanged at 8 met, 8 not met, 0 at risk and 2 not verifiable. The eight unmet requirements are features that the decisions above define but that TRL 4 would build.
- TRL 4 remains on hold. Nothing in this record authorizes building, packaging, publishing or testing the tool.

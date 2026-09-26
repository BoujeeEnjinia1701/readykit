---
doc_id: RDK-DDR-001
title: ReadyKit TRL 2 review decisions
project: ReadyKit
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CC-BY-SA-4.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted for D1 to D7. Amish accepted every recommendation on 2026-09-25, so each of D1 to D7 is "Decided by Amish, 2026-09-25: go with recommendation" (RDK-DDR-002). Items O1 to O4 carry no recommendation and remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", and the design precis RDK-PRC-001 v0.2 listed six key design choices, each with options and a recommendation. On 2026-09-25 Amish asked for this batch of repositories to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the ReadyKit items one by one. Under that instruction, every item that carries a recommendation is adopted as recommended so that the TRL 3 work can proceed, and each stayed open for his review. Later on 2026-09-25 he accepted all of them (RDK-DDR-002). Items without a recommendation are not decided here.

The session brief also set how the TRL 3 evidence rules apply to ReadyKit as a software project (item D7). That item answers the question the TRL 2 note raised as its recommended next step.

## Options considered

The options for items D1 to D6 are listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in RDK-PRC-001 v0.2, Key design choices. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3 work, now decided (RDK-DDR-002).*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Distribution | A pip package `readykit` with a small `.kit/` stub pinned to a version, plus a GitHub template repository for a one-click start. The vendored `.kit/` folder stays in use until the package exists. | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |
| D2 | Identity and branding | Organization name, website, repository owner, default author and colors move into a `readykit.yaml` file, with the Design Molecule values as defaults. | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |
| D3 | Sheet sizes | Add ISO A3 (420 x 297 mm) first, beside ANSI B. ISO A2 later if asked for. | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |
| D4 | Command-line interface | One `readykit` command with `init`, `check`, `render`, `media` and `upgrade`, keeping the present scripts as thin wrappers so existing repositories keep working. | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |
| D5 | Licensing of the tool | Code under MIT and non-code content (documents, media, BOM) under CC BY-SA 4.0, matching the standard itself. Applied to the repository on 2026-09-25 (RDK-DDR-002). | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |
| D6 | Standards interoperability | Add an Open Know-How (OKH) manifest export as a TRL 3 requirement. | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |
| D7 | TRL 3 evidence for a software project | `cad/src/model.py` exports the illustrative massing of the kit's outputs as STEP and STL; the general arrangement sheet RDK-DWG-001 shows the pipeline layout; RDK-CAL-001 covers measured check and render times and check coverage; `budget_usd` stays at $0. | Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002) |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Name. Confirm "ReadyKit" before publishing to PyPI. No recommendation was made. On 2026-09-25, `pypi.org/project/readykit/` returned "not found", so the name appeared free on PyPI; GitHub was not checked, and nothing was reserved. | Proposed, awaiting Amish |
| O2 | Pilot users: a university lab, an open science hardware group (GOSH, AfricaOSH or reGOSH) or a startup. No preference was stated. | Proposed, awaiting Amish |
| O3 | Windows: is native support required, or is WSL2 enough? No recommendation was made. R2 accepts either. | Proposed, awaiting Amish |
| O4 | Decision-wording check (R13): generic, or tied to the portfolio's "Proposed, awaiting" phrase? No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields changed when this record was first issued (the D5 license change followed under RDK-DDR-002). No budget, pitch or problem change was recommended, so `budget_usd` stays at $0 and the pitch and problem lines are unchanged.
- RDK-PRC-001 and RDK-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed". In the requirements, R10 (footprint) and R12 (upgrade path) are redefined for pip distribution (D1), R11 names `readykit.yaml` (D2), and three requirements are added: R16, OKH manifest export (D6); R17, ANSI B and ISO A3 sheets (D3); R18, one `readykit` command (D4). RDK-PRB-001 is unchanged at v0.2.
- D5 was not applied to the files when this record was first issued. After Amish accepted it on 2026-09-25, `LICENSE` was replaced by the CC BY-SA 4.0 legal code, and `project.yaml`, the README, `CONTRIBUTING.md`, the controlled documents and the drawing title blocks were changed to match (RDK-DDR-002). Code stays under MIT.
- RDK-CAL-001 measures the tool against every requirement. It finds eight requirements not met (R6, R11, R12, R13, R15, R16, R17, R18), all features still to be written, and none of them a speed, cost or reproducibility target.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building, packaging, publishing or testing the tool.

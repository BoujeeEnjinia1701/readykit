---
doc_id: RDK-DDR-001
title: ReadyKit TRL 2 review decisions
project: ReadyKit
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 work under Amish's 2026-09-25 instruction, and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items D1 to D7 are adopted for TRL 3 work, pending Amish's review. Items O1 to O4 remain "Proposed, awaiting Amish".

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed eight items as "Proposed, awaiting Amish", and the design precis RDK-PRC-001 v0.2 listed six key design choices, each with options and a recommendation. On 2026-09-25 Amish asked for this batch of repositories to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the ReadyKit items one by one. Under that instruction, every item that carries a recommendation is adopted as recommended so that the TRL 3 work can proceed, and each stays open for his review. Items without a recommendation are not decided here.

The session brief also set how the TRL 3 evidence rules apply to ReadyKit as a software project (item D7). That item answers the question the TRL 2 note raised as its recommended next step.

## Options considered

The options for items D1 to D6 are listed in `docs/REVIEW.md` (session 2026-09-25, /populate) and in RDK-PRC-001 v0.2, Key design choices. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Adopted recommendation | Status |
| --- | --- | --- | --- |
| D1 | Distribution | A pip package `readykit` with a small `.kit/` stub pinned to a version, plus a GitHub template repository for a one-click start. The vendored `.kit/` folder stays in use until the package exists. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D2 | Identity and branding | Organization name, website, repository owner, default author and colors move into a `readykit.yaml` file, with the Design Molecule values as defaults. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D3 | Sheet sizes | Add ISO A3 (420 x 297 mm) first, beside ANSI B. ISO A2 later if asked for. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D4 | Command-line interface | One `readykit` command with `init`, `check`, `render`, `media` and `upgrade`, keeping the present scripts as thin wrappers so existing repositories keep working. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D5 | Licensing of the tool | Code under MIT and non-code content (documents, media, BOM) under CC BY-SA 4.0, matching the standard itself. The license files and `project.yaml` are not changed in this session (see Consequences). | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D6 | Standards interoperability | Add an Open Know-How (OKH) manifest export as a TRL 3 requirement. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |
| D7 | TRL 3 evidence for a software project | `cad/src/model.py` exports the illustrative massing of the kit's outputs as STEP and STL; the general arrangement sheet RDK-DWG-001 shows the pipeline layout; RDK-CAL-001 covers measured check and render times and check coverage; `budget_usd` stays at $0. | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review |

*Table 2. Items that remain open.*

| # | Item | Status |
| --- | --- | --- |
| O1 | Name. Confirm "ReadyKit" before publishing to PyPI. No recommendation was made. On 2026-09-25, `pypi.org/project/readykit/` returned "not found", so the name appeared free on PyPI; GitHub was not checked, and nothing was reserved. | Proposed, awaiting Amish |
| O2 | Pilot users: a university lab, an open science hardware group (GOSH, AfricaOSH or reGOSH) or a startup. No preference was stated. | Proposed, awaiting Amish |
| O3 | Windows: is native support required, or is WSL2 enough? No recommendation was made. R2 accepts either. | Proposed, awaiting Amish |
| O4 | Decision-wording check (R13): generic, or tied to the portfolio's "Proposed, awaiting" phrase? No recommendation was made. | Proposed, awaiting Amish |

## Consequences

- `project.yaml`: only the TRL fields change. No budget, pitch or problem change was recommended, so `budget_usd` stays at $0 and the pitch and problem lines are unchanged.
- RDK-PRC-001 and RDK-REQ-001 are revised to v0.3. The key design choices in the precis are no longer "proposed". In the requirements, R10 (footprint) and R12 (upgrade path) are redefined for pip distribution (D1), R11 names `readykit.yaml` (D2), and three requirements are added: R16, OKH manifest export (D6); R17, ANSI B and ISO A3 sheets (D3); R18, one `readykit` command (D4). RDK-PRB-001 is unchanged at v0.2.
- D5 is adopted as the licensing for the standalone release, but it is not applied to the files in this session. Applying it needs the full CC BY-SA 4.0 legal text in the repository and a change to the `licenses` keys that the website card reads; both are left for Amish's review. The repository stays under CERN-OHL-S-2.0 and MIT until then.
- RDK-CAL-001 measures the tool against every requirement. It finds eight requirements not met (R6, R11, R12, R13, R15, R16, R17, R18), all features still to be written, and none of them a speed, cost or reproducibility target.
- TRL 4 is on hold by Amish's instruction. Nothing in this record authorizes building, packaging, publishing or testing the tool.

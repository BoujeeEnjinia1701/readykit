---
doc_id: RDK-REQ-001
title: ReadyKit requirements
project: ReadyKit
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Fifteen measurable requirements for the tool with targets, current status and verification
---

# ReadyKit requirements

ReadyKit meets its speed, cost and licensing targets today, measured on one sample repository. It does not yet meet the targets for check coverage, Windows support, configurable branding, one-command upgrades or a published getting-started guide (Table 2). Those gaps define the TRL 3 work.

Measured values come from running kit 1.3.1 on a copy of the TremorTrace repository (three controlled documents, six-part massing model) in a 2-core Linux container with Python 3.11 on 2026-09-25. Everything else is an estimate and is marked as one.

Table 1. Requirements.

| ID | Requirement | Target | Status at TRL 2 | Verification |
| --- | --- | --- | --- | --- |
| R1 | Setup time from an empty folder to a first passing check | 15 min or less on Linux or macOS with Python installed | Not verified; estimated 10 to 20 min, dominated by installing WeasyPrint system libraries | Timed trial by a new user |
| R2 | Platforms | Linux, macOS and Windows (native or WSL2) | Linux met (CI on Ubuntu); macOS expected; Windows native **not met** (WeasyPrint needs Pango, not tested) | CI matrix on three operating systems |
| R3 | Check time per repository | 2 s or less | Met: about 0.1 s (measured) | Timed run in CI |
| R4 | PDF render time | 10 s or less for three documents | Met: about 1.6 s (measured) | Timed run |
| R5 | Concept media render time | 60 s or less for a model of up to 20 parts, no GPU | Met for 6 to 7 parts: about 5 to 7 s (measured); 20 parts not tested | Timed run on a 20-part model |
| R6 | Check coverage | 90% or more of the machine-checkable rules in the standard are checked automatically | **Not met**: 12 of 20 rules, 60% (Table 3) | Rule-by-rule audit against STANDARDS.md |
| R7 | False failures | No check fails a document that follows the standard | Not verified; no false failure seen in the portfolio so far | Test corpus of conforming documents |
| R8 | Reproducible output | Same inputs give the same PDF text and images, apart from date and commit | Not verified | Render twice and compare |
| R9 | Offline use | Check and render run with no network | Met, except `viewer.html`, which loads its viewer script from a CDN | Run with network disabled |
| R10 | Footprint | Vendored kit folder 2 MB or less | Met: about 1.1 MB, mostly fonts (measured) | `du` in CI |
| R11 | Configurable identity | Organization name, website, repository owner, author and colors set in one config file, none hard-coded | **Not met**: footer site, repository owner and author default are hard-coded | Render a repo with a second identity |
| R12 | Upgrade path | One command updates the kit in a repo to a new version and shows the diff | **Not met**: kit is copied by hand into each repo | Upgrade trial across 5 repos |
| R13 | Agent guardrails | Check flags TRL above the cap, work beyond the cap, and decisions recorded as made without an owner | Partly met: cap and beyond-cap work checked; decision wording **not** checked (manual grep today) | Seeded test documents |
| R14 | Cost to user | $0; runs on free CI for public repositories | Met: all dependencies free and open source | Dependency license audit |
| R15 | Documentation | Getting-started guide of 5 pages or fewer, plus a reference for every check | **Not met**: only STANDARDS.md and the kit README exist | Guide review by a new user |

Table 2. Requirements not met at TRL 2.

| ID | Gap | Proposed route (awaiting Amish) |
| --- | --- | --- |
| R2 | Windows native untested | Add a Windows CI job; document WSL2 as the fallback |
| R6 | 60% check coverage | Add the eight missing checks in Table 3 |
| R11 | Hard-coded identity | Move identity into a `readykit.yaml` file with the portfolio values as defaults |
| R12 | Manual kit sync | Package the kit for pip with a `readykit upgrade` command |
| R13 | Decision wording unchecked | Promote the portfolio's decision-wording grep into the checker |
| R15 | No getting-started guide | Write it at TRL 3 |

Table 3. Machine-checkable rules in STANDARDS.md and whether the checker covers them today.

| Rule | Checked |
| --- | --- |
| Required front matter fields present | Yes |
| Document ID matches PRJ-TYP-NNN | Yes |
| Document ID unique within the repository | No |
| Version format (quoted, n.n) | Yes |
| Version equals newest revision row | Yes |
| Every revision row complete | Yes |
| Status in the allowed set | Yes |
| Released documents at 1.0 or later | Yes |
| No em dash anywhere in the repository | Partly (controlled documents only), counted as No |
| TRL evidence present for the claimed level | Yes |
| TRL and target within the phase cap | Yes |
| Required concept media present | Yes (warning at TRL 2) |
| Concept media carry the "not for fabrication" label | No |
| BOM columns and numbering match the exploded view | No |
| BOM fully priced at TRL 3 | Yes |
| Evidence files listed in project.yaml exist | Yes |
| Figures and tables numbered and captioned | No |
| Safety note present where hazard keywords appear | No |
| README sections in the required order | No |
| SI unit formatting (space between value and unit) | No |

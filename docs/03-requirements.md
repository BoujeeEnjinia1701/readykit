---
doc_id: RDK-REQ-001
title: ReadyKit requirements
project: ReadyKit
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-26'
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
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from RDK-CAL-001; R10 and R12 redefined for pip distribution and R11 names readykit.yaml (RDK-DDR-001, D1 and D2); R16 to R18 added (D3, D4, D6); R2 reclassified as not verifiable here; coverage audit checked by seeded faults
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: D5 reversed by Amish (RDK-DDR-002); license back to CERN-OHL-S-2.0
---

# ReadyKit requirements

ReadyKit meets every speed, footprint, cost, offline and reproducibility target, measured in RDK-CAL-001 on this repository, on synthetic repositories of up to 400 documents and on a corpus of 38 finished portfolio repositories. It does not meet eight requirements, all of them features still to be written: check coverage (R6), configurable identity (R11), one-command upgrades (R12), the decision-wording guardrail (R13), a getting-started guide (R15), Open Know-How export (R16), ISO A3 sheets (R17) and a single command (R18). Setup time (R1) and macOS and Windows support (R2) cannot be verified at TRL 3 on the machine used.

Requirements R10, R11 and R12 are reworded and R16 to R18 added to reflect the TRL 2 review items, each now decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-001, RDK-DDR-002). Building the features they call for is TRL 4 work and is on hold by Amish's instruction, so their status is unchanged. Measured values are from `docs/04-calcs/sizing.py` on a 2-core Linux container with Python 3.11 and kit 1.3.1. Times vary from run to run by up to a factor of two because other jobs share the machine; RDK-CAL-001 gives the ranges.

Table 1. Requirements and status at TRL 3.

| ID | Requirement | Target | Status at TRL 3 (RDK-CAL-001) | Verification |
| --- | --- | --- | --- | --- |
| R1 | Setup time from an empty folder to a first passing check | 15 min or less on Linux or macOS with Python installed | Not verifiable at TRL 3. The pip install of the kit's dependencies into a fresh environment took 32 to 47 s (1.09 GB), with WeasyPrint's system libraries already present; a new user on a clean machine is still needed | Timed trial by a new user |
| R2 | Platforms | Linux, macOS and Windows (native or WSL2) | Not verifiable at TRL 3: Linux met (this container and CI on Ubuntu); no macOS or Windows machine was available. The TRL 2 note listed Windows native as not met; it is untested rather than shown to fail | CI matrix on three operating systems |
| R3 | Check time per repository | 2 s or less | Met: 0.09 to 0.12 s for this repository, 0.10 to 0.11 s median and 0.12 to 0.27 s maximum across the corpus; 0.6 to 1.0 ms per added document, so the 2 s limit is reached at about 2,000 to 3,100 documents | Timed run in CI |
| R4 | PDF render time | 10 s or less for three documents | Met: 1.8 to 3.1 s for three documents (0.6 to 1.0 s per document) | Timed run |
| R5 | Concept media render time | 60 s or less for a model of up to 20 parts, no GPU | Met: 12 to 23 s for a 20-part model with cutaway, exploded view and scale figure; 5 to 6 s for this repository | Timed run on a 20-part model |
| R6 | Check coverage | 90% or more of the machine-checkable rules in the standard are checked automatically | **Not met**: 12 of 20 rules (60%) caught by seeded faults; 18 needed | Seeded faults, one per rule (RDK-CAL-001, section E) |
| R7 | False failures | No check fails a document that follows the standard | Met on the evidence available: 0 failures across 38 conforming TRL 3 repositories and this one | Corpus of conforming repositories |
| R8 | Reproducible output | Same inputs give the same PDF text and images, apart from date and commit | Met: PDF text identical in 5 of 5 documents and PNG renders byte-identical in 4 of 4 across two runs | Render twice and compare |
| R9 | Offline use | Check and render run with no network | Met for check and render with no network interface; `viewer.html` still loads its viewer script from a CDN | Run with network disabled |
| R10 | Footprint | Kit files in each repository (vendored folder today, pinned stub after D1) 2 MB or less; Python dependencies excluded | Met: 1.05 MB, of which fonts are 94% | `du` in CI |
| R11 | Configurable identity | Organization name, website, repository owner, author and colors set in `readykit.yaml`, with Design Molecule defaults; none hard-coded | **Not met**: 13 hard-coded occurrences of 5 identity values in kit code, style and templates (the site switch to designmolecule.com changed the values, not the count) | Render a repository with a second identity |
| R12 | Upgrade path | `pip install -U readykit` followed by `readykit upgrade` updates a repository to a new kit version and shows the diff | **Not met**: the kit is copied by hand. All 38 corpus repositories carry kit 1.3.1, yet none has this repository's `STANDARDS.md` or kit code, which shows the drift a versioned package would prevent | Upgrade trial across 5 repositories |
| R13 | Agent guardrails | Check flags TRL above the cap, work beyond the cap, and decisions recorded as made without an owner | **Not met** (partly): 2 of 3 seeded faults caught; a decision written as made ("Approved") passes | Seeded test documents |
| R14 | Cost to user | $0; runs on free CI for public repositories | Met: BOM total $0.00; all 8 direct dependencies free and open source, one of them (CairoSVG) under LGPL-3.0 | Dependency license audit |
| R15 | Documentation | Getting-started guide of 5 pages or fewer, plus a reference for every check | **Not met**: only STANDARDS.md and the kit README exist | Guide review by a new user |
| R16 | Open Know-How export | Writes an `okh.yml` manifest (OKH 1.0) with every required field from `project.yaml` and `readykit.yaml` | **Not met**: no exporter; 3 of the 5 required fields are available from `project.yaml` today, and the author and project link need R11 | Validate the manifest against OKH 1.0 |
| R17 | Sheet sizes | ANSI B and ISO A3 drawing sheets, chosen per repository | **Not met**: ANSI B only, fixed in the sheet generator | Render one sheet at each size |
| R18 | Command-line interface | One `readykit` command with `init`, `check`, `render`, `media` and `upgrade`; the present scripts keep working as wrappers | **Not met**: three separate scripts | Run each subcommand on a repository |

Table 2. Summary of status at TRL 3.

| Status | Count | Requirements |
| --- | --- | --- |
| Met | 8 | R3, R4, R5, R7, R8, R9, R10, R14 |
| Not met | 8 | R6, R11, R12, R13, R15, R16, R17, R18 |
| At risk | 0 | |
| Not verifiable at TRL 3 | 2 | R1, R2 |

Table 3. Requirements not met, and the route decided by Amish on 2026-09-25 (RDK-DDR-002). Every route is a build step, on hold while TRL 4 is on hold.

| ID | Gap | Route |
| --- | --- | --- |
| R6 | 12 of 20 rules checked | Add at least six of the eight missing checks in Table 4 (D8) |
| R11 | Hard-coded identity | `readykit.yaml` with Design Molecule defaults (D2) |
| R12 | Manual kit sync, and drift already present | pip package plus `readykit upgrade` (D1, D4) |
| R13 | Decision wording unchecked | Promote the portfolio's decision-wording grep into the checker; generic or portfolio-specific wording is open (O4) |
| R15 | No getting-started guide | Write it with the package (D9) |
| R16 | No OKH export | Exporter reading `project.yaml` and `readykit.yaml` (D6) |
| R17 | ANSI B only | Sheet size as a parameter of the sheet generator, ISO A3 first (D3) |
| R18 | Three scripts | One command with the scripts as wrappers (D4) |

Table 4. Machine-checkable rules in STANDARDS.md. "Checked" is the TRL 2 audit; "Seeded fault" is the result of planting one fault per rule in a passing fixture repository (RDK-CAL-001, section E). The two agree on every rule.

| Rule | Checked | Seeded fault |
| --- | --- | --- |
| Required front matter fields present | Yes | Caught |
| Document ID matches PRJ-TYP-NNN | Yes | Caught |
| Document ID unique within the repository | No | Missed |
| Version format (quoted, n.n) | Yes | Caught |
| Version equals newest revision row | Yes | Caught |
| Every revision row complete | Yes | Caught |
| Status in the allowed set | Yes | Caught |
| Released documents at 1.0 or later | Yes | Caught |
| No em dash anywhere in the repository | Partly (controlled documents only), counted as No | Missed in README.md |
| TRL evidence present for the claimed level | Yes | Caught |
| TRL and target within the phase cap | Yes | Caught |
| Required concept media present | Yes (warning at TRL 2) | Caught |
| Concept media carry the "not for fabrication" label | No | Missed |
| BOM columns and numbering match the exploded view | No | Missed |
| BOM fully priced at TRL 3 | Yes | Caught |
| Evidence files listed in project.yaml exist | Yes | Caught |
| Figures and tables numbered and captioned | No | Missed |
| Safety note present where hazard keywords appear | No | Missed |
| README sections in the required order | No | Missed |
| SI unit formatting (space between value and unit) | No | Missed |

> **Safety:** Adding the safety-note check (Table 4) must raise a flag for a person to review. It must never remove the human review of hazards, and a passing check never means a design is safe.

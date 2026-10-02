---
doc_id: RDK-DDR-003
title: ReadyKit design for construction
project: ReadyKit
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the design constructable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "A1 decided as (a) and A2 as (b) by Amish; P1 to P6 still open for his review"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** Draft. Every change below was made under Amish's 2026-09-30 instruction to make the design physically buildable; the changes P1 to P6 in Table 1 remain open for his review. The items in Table 3 were decided by Amish on 2026-10-02: "i approve your recommendations for all 555 open decisions." A1 is decided as (a); A2 is decided as (b), Python 3.11 or later, the later recommendation, since Python 3.10 reaches end of life in October 2026. Both are recorded in the design decisions register (RDK-DEC-001).

## Context

On 2026-09-30 Amish asked for a build plan for every repository that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." (STANDARDS section 18.)

ReadyKit is software. Its components are the modules of the kit, and its massing model (`cad/src/model.py`) is an illustration in which each object stands for one module (RDK-DDR-001, D7). For ReadyKit, "constructable" therefore means two things:

1. **The software design.** Every module can be written with the stated tools, and every module has a defined interface to the modules next to it: what it reads, what it hands on, and in what form. The constructability review traced each module of RDK-PRC-001 Table 1 against the present kit code (`.kit/`, kit 1.7.0) and the decisions D1 to D9. It found five places where the design could not be assembled as described: parts with no defined joint, a part that cannot live where the design puts it, and a part that is missing.
2. **The illustration.** Every object in the massing model rests on what holds it, no two objects overlap, and separate objects stand clear of each other, so the pictures in the build plan read correctly. The model now runs these checks itself (`python cad/src/model.py --check`): 82 checks, all pass.

The changes keep what ReadyKit does: the same seven modules, the same commands, outputs, requirements and decisions D1 to D9. Nothing here changes the pitch or the safety case.

## Decision

*Table 1. Changes made to the design, the model and the BOM.*

| # | Problem found | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | No shared way to read the repository. The project file is read in eight places in seven kit scripts, in three different ways (a YAML load, a regular expression on the repository line, and the project slug joined to an owner name written into the code), so the PDF footer and the drawing title block can name different repositories. D2 needs the identity file read by four modules, and D6 needs the same fields for the Open Know-How export, but no module was given that job. | A new made module, the **repository reader** (BOM line 12, making sketch RDK-DWG-102): one loader each for the project file, identity file, phase file, document front matter and bill of materials, with defaults for missing identity values. It hands every other module one record; no other module opens these files. | One joint instead of eight. Identity values (R11) then have exactly one place to be read and defaulted, and the exporter of R16 gets the same record. |
| P2 | The per-repository stub of D1 was undefined, and the agent guardrails (module 6) could not live where the design put them. Agents read their rules from the repository they work in, so rules held only inside a pip package would never be read. | The stub is defined: version pin and identity file, agent rules and session commands, and a copy of the standard. Code and the bundled fonts stay in the package. Setup writes the stub; upgrade rewrites it and shows the difference first. Measured from the files it would hold: about 47 kB, against 1.20 MB of kit in each repository today (83% fonts). | Keeps the guardrails readable by agents, meets R10 by a wide margin and gives R12 a defined thing to upgrade. |
| P3 | One dependency list for everything: the CI check job installs about 1.1 GB (build123d, WeasyPrint and the rest) to run a check that needs three small libraries. | Dependencies split into a **core** (PyYAML, Python-Markdown, Jinja2; about 5 MB installed, measured) and optional extras: PDF, drawings, media and release. The template's check job installs the core only; the release job installs every extra. | Shortens the first install a new user waits for (R1) and every CI check run. The check already loads the PDF library late, so no module changes behaviour. |
| P4 | The viewer page loads its 3D viewer script from a content delivery network, the one gap left in R9 (offline use). | A pinned copy of the viewer script (model-viewer, Apache-2.0; new bought BOM line 13) ships in the package and is copied beside the 3D model; the page loads it by a relative link. | Closes R9 without changing the page. The license notice travels with the script. |
| P5 | The TRL badge had no joint to the README: the gate writes the TRL on PDF covers, but the README badge is typed by hand and can disagree with the project file. | The gate also writes the badge line under the README title from the claimed TRL, and only when the gate passes. It replaces that one line and touches nothing else. | One TRL value written in two places by the same module (build plan joint 3). |
| P6 | Illustration: the fanned document stack hung 12 mm over the folder's edge, and the model had no object for the reader or for the bought parts. | The stack now fans about its middle page and lies inside the folder. Two objects added: the reader as a card index box (one card per source it reads) and the bought open-source parts as a tray. Illustration checks added to the model. | The overview, steps and joints need an object for every component, and the pictures should show nothing that could not sit as drawn. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| BOM | Lines 12 (repository reader, make) and 13 (3D viewer script, buy) added; lines 2, 5, 7, 8 and 10 reworded. Every line USD 0.00. Value-engineering target USD 0 (`budget_usd`); estimated cost of the constructable design USD 0 (USD 0 over the target). | P1 to P5 |
| Drawings | RDK-DWG-001 Rev P4 (reader, stub, core install, badge). Blueprint RDK-DWG-010 Rev P4. Making sketches RDK-DWG-101 to 108 added. STEP and STL re-exported. | Follows the model |
| Media | Hero, exploded, blueprint, model and viewer page regenerated with the two added objects. | P6 |
| Calculations | RDK-CAL-001 unchanged: nothing has been built, so no measured figure moves. The stub size (47 kB) and core install size (5 MB) are measured here from the files and installed libraries they would contain; they are estimates for the package until TRL 4. | |
| Requirements | No status changes. P2, P3 and P4 are expected to help R10, R1 and R9; each is verified at TRL 4. | |

*Table 3. Items proposed for Amish, decided by Amish on 2026-10-02.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | Scope of the first package. Kit 1.7.0 holds tools that the concept's seven modules do not name: the release gate, the archive helper (REUSE and Zenodo), storefront cards, photoreal renders (need Blender) and the build plan picture helper. Adding them changes what the product offers. | (a) Add the release gate and archive helper to the release extra; keep photoreal renders and storefront cards for the portfolio only; build plan pictures go with the media extra. (b) Everything in the kit. (c) The seven modules only. | (a): these support document control and releases, which the pitch names; photoreal rendering needs Blender, which breaks the no-paid, offline, laptop-only promise for most users. Decided by Amish, 2026-10-02: (a). |
| A2 | Oldest Python version supported. The portfolio CI uses 3.12 and the measurements used 3.11. | (a) 3.10 or later; (b) 3.11 or later; (c) 3.12 only. | At first (a), tested in CI on the oldest and newest supported versions; it covers most university and lab machines. Decided by Amish, 2026-10-02, on the later recommendation: (b), Python 3.11 or later, tested in CI on 3.11 and the newest release, because 3.10 reaches end of life in October 2026 and the measurements were made on 3.11. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan RDK-BLD-001 shows every module and step in pictures generated from the model (`cad/src/build_plan_media.py`), and the design decisions register RDK-DEC-001 carries A1, A2 and the items O1 to O4, all decided on 2026-10-02. With A2 decided as (b), the package metadata and CI matrix of build plan step 1 are for Python 3.11 and the newest release.
- The photoreal render (`media/render-hero.png`), `media/card.png` and `media/social-preview.png` show the concept scene without the reader and the tray, so they are stale; they are made on Amish's Mac.
- Building any of this is TRL 4 work and stays on hold.

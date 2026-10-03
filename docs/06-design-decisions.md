---
doc_id: RDK-DEC-001
title: ReadyKit design decisions register
project: ReadyKit
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 6 (RDK-DDR-003 A1 and A2 decided); moved to decisions made; To confirm item 2 updated"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Design for construction (RDK-DDR-003, P1 to P6) accepted by Amish on 2026-10-02; the 2026-09-30 row no longer says open for review"
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Value-engineering wording restated; follow-ups of the 2026-10-02 decisions carried into the model, BOM, calculations and pictures"
---

# ReadyKit design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

*Table 2. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The pinned 3D viewer script's size (about 1 MB assumed) and its Apache-2.0 notice | It is copied into every repository's media folder beside the 3D model, and its notice must travel with it | RDK-DDR-003, P4 |
| 2 | Pango and fontconfig install cleanly on macOS (Homebrew) and on Windows through WSL2, the route decided on 2026-10-02 | PDF output needs them; R2 cannot be checked without them | RDK-REQ-001, R2 |
| 3 | The license audit still holds for every library in every extra, including CairoSVG under LGPL-3.0 used as an installed dependency | R14 and the MIT license of the package | RDK-CAL-001, section F |
| 4 | The free CI runner images still provide the Pango packages the workflow installs | The release job renders PDFs on the runner | Build plan section 3.1 |
| 5 | The core install really is about 5 MB in a clean environment (measured here from installed libraries, not from a fresh install) | Sets the setup time (R1) and the CI check time | RDK-DDR-003, P3 |

## Value engineering

Value-engineering target: USD 0. Estimated cost of the constructable design: USD 0 (USD 0 over the target). The target is a hypothetical control target, not a limit. Main cost drivers and savings worth trying:

- No line costs money: every module is written in-house under MIT and every bought part is free and open source. The two added lines (the repository reader and the 3D viewer script) are also USD 0.
- The real costs to a user are install size and CI time. Splitting the dependencies (RDK-DDR-003, P3) cuts the install for a check from about 1.1 GB to about 5 MB, and the per-repository stub (P2) cuts the kit carried by each repository from 1.20 MB to about 47 kB.
- Savings worth trying: cache the extras between CI runs on release tags; publish the template so setup needs no clone of a finished repository.
- The only paid option is private-repository CI time beyond GitHub's included minutes, which the tool does not need.

## Decisions made

*Table 3. Decisions made.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | D1 distribution as a pip package plus a template repository; D2 identity in `readykit.yaml`; D3 add ISO A3 sheets; D4 one `readykit` command; D6 Open Know-How export; D7 TRL 3 evidence for a software project; D8 add at least six missing checks (R6); D9 write the getting-started guide with the package (R15) | Amish: "i accept all your recommendations, go with them across all repos." | RDK-DDR-001, RDK-DDR-002 |
| 2026-09-25 | Hold TRL 4 work across the portfolio | Amish: "you know the drill, nothing gets past TRL 3" | RDK-DDR-001 |
| 2026-09-26 | D5 reversed: keep the portfolio license pair, CERN-OHL-S v2 for hardware and content, MIT for software | Amish: "apply the same MIT license pairing across the board for all repos." | RDK-DDR-002 |
| 2026-09-30 | Make every design constructable while drawing the build plan, and keep outstanding decisions out of the plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." and "don't log outstanding decisions in this build plan - that is not the place for it." | RDK-DDR-003 (changes P1 to P6 made under this instruction; accepted on 2026-10-02, below) |
| 2026-10-01 | Budgets are value-engineering targets, not limits | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register, Value engineering |
| 2026-10-02 | Name: keep "ReadyKit"; recheck the package index just before the first release and publish the first real release under that name as soon as the package installs (the GitHub repository already exists under Amish's account) | Amish: "i approve your recommendations for all 555 open decisions." | RDK-DDR-001, O1 |
| 2026-10-02 | Pilot users: an open science hardware group, with GOSH (Gathering for Open Science Hardware) as the first candidate, recruiting two or three member projects through its community forum; a university lab as the second pilot | Amish: "i approve your recommendations for all 555 open decisions." | RDK-DDR-001, O2 |
| 2026-10-02 | Windows: supported through WSL2 for the first release; native Windows added later if pilot users ask for it | Amish: "i approve your recommendations for all 555 open decisions." | RDK-DDR-001, O3 |
| 2026-10-02 | Decision-wording rule (R13): generic, so any decision written as made must name an owner and a date; each repository sets its 'still open' phrase in its identity file, defaulting to "Proposed, awaiting" | Amish: "i approve your recommendations for all 555 open decisions." | RDK-DDR-001, O4 |
| 2026-10-02 | Scope of the first package (option a): release gate and archive helper in the release extra, build plan pictures in the media extra; photoreal renders and storefront cards kept for the portfolio only | Amish: "i approve your recommendations for all 555 open decisions." | RDK-DDR-003, A1 |
| 2026-10-02 | Oldest Python supported: 3.11 or later (option b), tested in CI on 3.11 and the newest release; 3.10 reaches end of life in October 2026. This differs from the register's earlier recommendation (a) | Amish: "i approve your recommendations for all 555 open decisions." | RDK-DDR-003, A2 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P6, as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [RDK-DDR-003](decisions/0003-design-for-construction.md), Table 1 |

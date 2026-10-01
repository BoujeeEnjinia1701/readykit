---
doc_id: RDK-DEC-001
title: ReadyKit design decisions register
project: ReadyKit
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# ReadyKit design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions, all Proposed, awaiting Amish.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Name "ReadyKit" on the package index and GitHub | Keep "ReadyKit"; choose another name | None made. The package index showed the name free on 2026-09-25; GitHub not checked; nothing reserved | Package name, template name and the single command's name (build plan step 1) | RDK-DDR-001, O1 |
| 2 | Pilot users | A university lab; an open science hardware group (GOSH, AfricaOSH or reGOSH); a startup | None stated | Who runs the setup-time and false-failure checks (R1, R7) at TRL 4 | RDK-DDR-001, O2 |
| 3 | Windows support | Native Windows required; the Linux subsystem (WSL2) enough | None made; R2 accepts either | CI platforms and the PDF system libraries on Windows | RDK-DDR-001, O3 |
| 4 | Wording of the decision-wording rule (R13) | Generic (any decision written as made with no owner and date); tied to the portfolio's "Proposed, awaiting" phrase | None made | The rule added to the readiness gate (build plan section 3.5, step 3) | RDK-DDR-001, O4 |
| 5 | Scope of the first package beyond the seven modules: release gate, archive helper, storefront cards, photoreal renders, build plan pictures | (a) release gate and archive helper in the release extra, build plan pictures in the media extra, photoreal renders and cards kept for the portfolio; (b) everything in the kit; (c) the seven modules only | (a): photoreal rendering needs Blender, which breaks the free, offline, laptop-only promise for most users | The extras defined in build plan section 3.1 and step 2 | RDK-DDR-003, A1 |
| 6 | Oldest Python version supported | (a) 3.10 or later; (b) 3.11 or later; (c) 3.12 only | (a), tested in CI on the oldest and newest versions | Package metadata and the CI matrix (build plan step 1) | RDK-DDR-003, A2 |

## To confirm when parts are bought

*Table 2. Items to confirm.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The pinned 3D viewer script's size (about 1 MB assumed) and its Apache-2.0 notice | It is copied into every repository's media folder beside the 3D model, and its notice must travel with it | RDK-DDR-003, P4 |
| 2 | Pango and fontconfig install cleanly on macOS (Homebrew) and on the chosen Windows route | PDF output needs them; R2 cannot be checked without them | RDK-REQ-001, R2 |
| 3 | The license audit still holds for every library in every extra, including CairoSVG under LGPL-3.0 used as an installed dependency | R14 and the MIT license of the package | RDK-CAL-001, section F |
| 4 | The free CI runner images still provide the Pango packages the workflow installs | The release job renders PDFs on the runner | Build plan section 3.1 |
| 5 | The core install really is about 5 MB in a clean environment (measured here from installed libraries, not from a fresh install) | Sets the setup time (R1) and the CI check time | RDK-DDR-003, P3 |

## Value engineering

Value-engineering target: USD 0 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 0 (USD 0 over the target). Main cost drivers and savings worth trying:

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
| 2026-09-30 | Make every design constructable while drawing the build plan, and keep outstanding decisions out of the plan, in this register | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." and "don't log outstanding decisions in this build plan - that is not the place for it." | RDK-DDR-003 (changes P1 to P6 made under this instruction; open for his review) |
| 2026-10-01 | Budgets are value-engineering targets, not limits | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens." | This register, Value engineering |

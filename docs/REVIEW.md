# Review note: ReadyKit

## Session 2026-09-25: /populate to a strong TRL 2 (batch run, no questions asked)

### What was done

- `docs/01-problem.md` (RDK-PRB-001 v0.2): problem in numbers with sources, users and context, prior work (GitBuilding, DIN SPEC 3105, Open Know-How, OSHWA certification, build123d), constraints, out of scope.
- `docs/03-requirements.md` (RDK-REQ-001 v0.2): 15 measurable requirements about the tool (setup time, platforms, check and render time, check coverage, reproducibility, offline use, footprint, branding, upgrades, guardrails, cost, documentation), with status, a gap table and a rule-by-rule coverage audit.
- `docs/02-concept.md` (RDK-PRC-001 v0.2): how it works, seven modules, measured first-order numbers, six proposed design choices, safety, open questions.
- `cad/src/concept_media.py`: illustrative massing of the kit's outputs (document set, PDF style bands, drawing sheet on a board, printed massing part, TRL badge, guardrail tent card, template folder), numbered 1 to 7 to match the BOM, with a laptop as the scale context instead of the 1.75 m figure. Hero and exploded renders are stamped "ILLUSTRATIVE, SOFTWARE PROJECT". A custom pipeline diagram replaces the kit's linear flow chart because the pipeline has two inputs and four outputs.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png`, `flow.png`, `model.glb`, `viewer.html`. No cutaway: nothing is inside.
- `bom/bom.csv` and `bom/bom-notes.md`: nine lines (seven modules plus fonts and CI hosting), all $0.00.
- `README.md`: hero image and links line, expanded concept rationale, burning platform (four cited figures), use tables by industry and region, origin, updated concept and components.
- `docs/pdf/`: PDFs of the three controlled documents.

### Key results

Measured with kit 1.3.1 on a copy of the TremorTrace repository (3 documents, 6-part model), 2-core Linux container, Python 3.11.

| Quantity | Value | Requirement |
| --- | --- | --- |
| Check time | about 0.1 s | R3 met |
| PDF render, 3 documents | about 1.6 s | R4 met |
| Concept media | about 5 to 7 s for 6 to 7 parts | R5 met at this size; 20 parts untested |
| Kit folder | about 1.1 MB | R10 met |
| Check coverage | 12 of 20 machine-checkable rules (60%) | R6 **not met** (target 90%) |
| Parts cost | $0 | R14 met; budget_usd 0 not exceeded |

Requirements **not met**: R2 (Windows native untested), R6 (check coverage), R11 (identity hard-coded: footer site, repository owner, default author), R12 (no one-command upgrade), R13 (decision wording not checked automatically), R15 (no getting-started guide). R1, R7 and R8 are not verified.

### Proposed, awaiting Amish

1. **Distribution:** vendored `.kit/` (today), pip package, or template repository plus sync action. Recommendation: pip package plus template. **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002).**
2. **Identity:** keep portfolio branding hard-coded, or move it to a `readykit.yaml` with Design Molecule defaults. Recommendation: config file. **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002).**
3. **Sheet sizes:** ANSI B only, or add ISO A3 and A2. Recommendation: add A3. **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002).**
4. **Command-line interface:** separate scripts, or one `readykit` command (`init`, `check`, `render`, `media`, `upgrade`). Recommendation: one command with the scripts as wrappers. **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002).**
5. **Licenses:** `project.yaml` lists CERN-OHL-S for hardware and MIT for software. For a software-only project, option to switch non-code content to CC BY-SA 4.0 (as the standard uses). Recommendation: switch; not changed in this session. **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002).** Applied in the session of 2026-09-25 (recommendations accepted).
6. **Standards interop:** add Open Know-How manifest export at TRL 3. Recommendation: yes. **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002).**
7. **Name:** confirm "ReadyKit" before publishing to PyPI; availability not checked. No recommendation; still Proposed, awaiting Amish.
8. **Pilot users:** a university lab, an open science hardware group (GOSH, AfricaOSH or reGOSH) or a startup. No preference stated; still Proposed, awaiting Amish.

`project.yaml` pitch and problem were left unchanged; the numbers found support them.

### Safety concerns

- No physical hazards. The main risk is false confidence: a passing check is not an engineering review. Documents and README say so.
- Automating the safety-section check must add a flag, never remove human review.

### Gaps against the brief

- The README badge for TRL is still hand-written; the kit only prints TRL on PDF covers. Recorded as a gap, not changed (kit files are not edited inside a project repo).
- The India row in the README use table has no cited figure; the web search budget ran out before one could be verified.

### Suggestions (not in the repo)

- Run the checker across all portfolio repos and publish the pass rate as ReadyKit's first case study.

### Recommended next step

Review this note and the media. If approved, run `/advance-trl3`: a calculation note on check coverage and timing across the whole portfolio, a proposal for how the TRL 3 evidence rules (working `model.py`, STEP export, drawing sheet) apply to a software project, and a decision record on distribution.

## Session 2026-09-25: TRL 3

Batch run under Amish's 2026-09-25 instruction ("you know the drill, nothing gets past TRL 3"). He has not reviewed the ReadyKit items one by one, so every recommendation below is adopted for TRL 3 work and stays open for his review.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (RDK-DDR-001 v0.1): seven items adopted as recommended, four left open.
- `docs/04-calcs/01-sizing.md` (RDK-CAL-001 v0.1) and `docs/04-calcs/sizing.py`, which writes `docs/04-calcs/results.csv`. The script measures this repository, synthetic repositories of 10 to 400 documents, a 20-part media model, a corpus of 38 finished TRL 3 portfolio repositories (read-only copies in a temporary folder, each given this repository's kit) and a fixture repository with one seeded fault per rule. `--setup` also times a fresh install. A Git shim keeps Git out of every measurement.
- `docs/03-requirements.md` (RDK-REQ-001 v0.3): status at TRL 3 for every requirement; R10 to R12 reworded for the adopted decisions; R16 (Open Know-How export), R17 (ISO A3 sheets) and R18 (one `readykit` command) added; the coverage audit now shows the seeded-fault result per rule.
- `docs/02-concept.md` (RDK-PRC-001 v0.3): design choices no longer "proposed", measured first-order numbers, TRL 3 evidence for a software project, open questions trimmed. `docs/01-problem.md` is unchanged at v0.2.
- `cad/src/model.py`: parametric build123d massing of the kit's outputs (page, sheet size, stack, board, badge, tent card and laptop as parameters; sheet size switchable between ANSI B and ISO A3), exporting `cad/step/readykit-massing.step` and `cad/stl/readykit-massing.stl`. `cad/src/concept_media.py` now takes its geometry from the model.
- `cad/src/sheets.py` and `cad/drawings/RDK-DWG-001.svg`, `.pdf` and `.png`: general arrangement at Rev P1, laid out as the documentation pipeline (inputs, modules 1 to 7, outputs, CI gate and fail path) with the massing as the isometric view; scale NTS; "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION" on the sheet. The concept blueprint remains RDK-DWG-010, so DWG-001 was the next free number.
- `bom/bom.csv` and `bom/bom-notes.md`: 11 lines (dependencies and system libraries added), every line priced at $0.00 with a supplier or supplier type; total $0.00 against `budget_usd` of $0.
- `media/`: hero, exploded, blueprint, flow, GLB and viewer regenerated from the model with the new numbers. Each image was inspected. No `_views` folders remain. The kit's cutaway is not used here (`cut=False`), so the cutaway's origin limit does not arise.
- `README.md`: TRL 3 badge and line, links to the drawing and calculation note, measured numbers, the eight unmet requirements, and a cited figure for the India row (Atal Innovation Mission, 10,000 Atal Tinkering Labs and 72 Atal Incubation Centres, checked with WebFetch on 2026-09-25). Section order unchanged.
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence list extended. Pitch, problem and budget unchanged.
- `docs/pdf/`: PDFs of the five controlled documents.

### Requirements at TRL 3 (RDK-CAL-001)

8 met, 8 not met, 0 at risk, 2 not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R6 | **Not met** | Check coverage 12 of 20 rules (60%); 18 needed |
| R11 | **Not met** | 13 hard-coded occurrences of 4 identity values |
| R12 | **Not met** | Manual kit copy; STANDARDS.md differs in all 38 corpus repositories at the same KIT_VERSION 1.3.1 |
| R13 | **Not met** | 2 of 3 guardrail faults caught; a decision written as "Approved" passes |
| R15 | **Not met** | No getting-started guide |
| R16 | **Not met** | No OKH exporter; 3 of 5 required fields available |
| R17 | **Not met** | ANSI B only |
| R18 | **Not met** | Three separate scripts |
| R1 | Not verifiable | Dependency install 32 to 43 s, 1.09 GB; no new-user trial |
| R2 | Not verifiable | Linux only; the TRL 2 "not met" for Windows was untested, not a failure |
| R3 | Met | Check 0.10 s; 0.6 to 0.7 ms per added document |
| R4 | Met | 1.8 to 3.1 s for three PDFs |
| R5 | Met | 12 to 23 s for a 20-part model |
| R7 | Met | 0 false failures across 38 conforming repositories |
| R8 | Met | PDF text 5 of 5 and PNGs 4 of 4 identical on repeat |
| R9 | Met | Check and render pass with no network (viewer page excepted) |
| R10 | Met | Kit folder 1.05 MB |
| R14 | Met | $0.00; all dependencies free (CairoSVG is LGPL-3.0) |

Times vary by up to a factor of two between runs because other jobs share the 2-core machine; the note quotes ranges over four runs and judges each target on the worst value.

### Decisions recorded (RDK-DDR-001)

Each of D1 to D7 was "Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review" and is now **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002)**:

1. D1 Distribution: pip package plus template repository.
2. D2 Identity: `readykit.yaml` with Design Molecule defaults.
3. D3 Sheet sizes: add ISO A3 first.
4. D4 Command-line interface: one `readykit` command, scripts kept as wrappers.
5. D5 Licenses: code MIT, documentation CC BY-SA 4.0 for the standalone release. **Not applied to the files in this session**: it needs the full CC BY-SA 4.0 legal text in the repository and a change to the `licenses` keys the website card reads. The repository stays CERN-OHL-S-2.0 and MIT until Amish reviews it.
6. D6 Open Know-How manifest export as a TRL 3 requirement (R16).
7. D7 TRL 3 evidence for a software project: massing STEP and STL, pipeline GA sheet, measurement note, budget $0 (from the session brief).

### Still awaiting Amish

- O1 Name "ReadyKit" for PyPI and GitHub. `pypi.org/project/readykit/` returned "not found" on 2026-09-25; GitHub not checked; nothing reserved.
- O2 Pilot users (a university lab, an open science hardware group or a startup).
- O3 Windows: native support required, or WSL2 enough?
- O4 Decision-wording check (R13): generic, or tied to the portfolio phrase?
- Proposed route for R6: add at least six of the eight missing checks (RDK-REQ-001 Table 4). Proposed route for R15: write the guide with the package. Both now **Decided by Amish, 2026-09-25: go with recommendation (RDK-DDR-002, D8 and D9)**, build on hold (TRL 4).
- Carried from the TRL 2 note: the README TRL badge is still hand-written; kit files were not edited inside this repository.

### Findings for the kit owner

- **Kit drift.** All 38 finished repositories report KIT_VERSION 1.3.1, but none has this repository's `STANDARDS.md`: this batch added 38 project codes without a version bump. The kit code (`render.py`, `drawing.py`, `concept.py`) is identical everywhere.
- **ThermaBrick** (in the finished corpus) still carries `bom/purchasing-checklist.md` and `build-log/TEMPLATE.md`, which the check correctly warns about as beyond-cap material. It was only read, not changed. No TRL 4 material exists in ReadyKit.
- The em dash rule is only enforced inside controlled documents; an em dash in `README.md` passes the check.
- The calculation script's first duplicate-ID probe gave a false "caught" (it removed TRL evidence instead of creating a duplicate). It was corrected before the final run; the note records this.

### Citations

The India row's missing figure is now cited (Atal Innovation Mission home page). The Open Know-How 1.0 required fields quoted in RDK-CAL-001 were checked against the published standard with WebFetch. WebSearch was not used (quota exhausted). No other unchecked citations were listed.

### Safety concerns

- No physical hazards. The main risk remains false confidence: a passing check is not an engineering review. RDK-CAL-001 shows the checker does not yet look for a safety note where hazard keywords appear; adding that check must raise a flag for a person, never replace the review.
- The guardrail gap (R13) matters for agent-written repositories: a decision written as "Approved" passes the check today, so the decision-rights rule still relies on reviewers.

### Recommended next step

TRL 4 is on hold by Amish's instruction; nothing here should start it. The next step is Amish's review of D1 to D7 (especially D5, licensing, and D1, distribution) and a choice on O1 to O4. For reference only, TRL 4 would need: the pip package, `readykit.yaml`, the `readykit` command, ISO A3 sheets, the OKH exporter and the six or more missing checks built; a lab test report (TST, `environment: lab`) covering setup time with new users on Linux, macOS and Windows, coverage by seeded faults, false failures on repositories written by outside teams, and upgrade trials across five repositories; and build log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every ReadyKit item with a recommendation is now "Decided by Amish, 2026-09-25: go with recommendation"; items without one stay "Proposed, awaiting Amish". The record is RDK-DDR-002.

### Decisions applied and what changed

| # | Decision | Applied at TRL 3 | Before | After |
| --- | --- | --- | --- | --- |
| D5 | Code MIT; documents, drawings, CAD, BOM and media CC BY-SA 4.0 | Yes | `LICENSE` CERN-OHL-S v2; `licenses.hardware` CERN-OHL-S-2.0; tag `cern-ohl-s`; front matter and title blocks CERN-OHL-S-2.0 | `LICENSE` CC BY-SA 4.0 legal code (SPDX text); `licenses.hardware` CC-BY-SA-4.0 (key kept for the website card); tag `cc-by-sa`; every controlled document, RDK-DWG-001 and RDK-DWG-010 CC-BY-SA-4.0; README badge and Licenses section; `CONTRIBUTING.md` |
| D1 | Pip package plus template repository | Wording only; build on hold (TRL 4) | "Adopted for TRL 3 work" | "Decided"; BOM item 7 and RDK-DWG-001 note updated |
| D2 | `readykit.yaml` for identity | Wording only; kit change on hold (TRL 4) | 13 hard-coded occurrences of 4 values | 13 occurrences of 5 values after the kit's site switch (designmolecule.com x3, Design Molecule Lab x2, GitHub owner x1, author x4, portfolio name x3) |
| D3 | Add ISO A3 sheets | Wording only; kit change on hold (TRL 4) | "ISO A3 adopted" on RDK-DWG-001 and BOM item 3 | "ISO A3 decided"; `model.py` already switches the sheet parameter |
| D4 | One `readykit` command | Wording only; build on hold (TRL 4) | | R18 route unchanged |
| D6 | Open Know-How export | Wording only; build on hold (TRL 4) | | R16 route unchanged |
| D7 | TRL 3 evidence for software | Already in place | | No change |
| D8 | R6 route: add at least six missing checks | Build on hold (TRL 4); kit change | Proposed, awaiting Amish | Decided |
| D9 | R15 route: write the guide with the package | On hold with D1 (TRL 4) | Proposed, awaiting Amish | Decided |

Budget: `budget_usd` stays $0 (no recommendation changed it; BOM total $0.00). Pitch and problem are unchanged.

Documents: RDK-PRB-001 v0.2 to v0.3, RDK-PRC-001 v0.3 to v0.4, RDK-REQ-001 v0.3 to v0.4, RDK-CAL-001 v0.1 to v0.2, RDK-DDR-001 v0.1 to v0.2, RDK-DDR-002 v0.1 new. RDK-DWG-001 Rev P1 to P2 (title block license, D1 and D3 notes, measured times); geometry unchanged, STEP and STL re-exported. The concept blueprint RDK-DWG-010 is Rev P2 for the license change.

`sizing.py` now also counts "Design Molecule Lab" as an identity value and reports a new line [B8], the changed kit-code lines against the corpus. The rerun changed these numbers: kit code identical to the corpus in 38 of 38 before, 0 of 38 after (3 changed lines, all site and organization strings); setup 32 to 43 s before, 32 to 47 s after; check slope 0.6 to 0.7 ms per document before, 0.6 to 1.0 ms after (the last run shared the machine with other jobs), so the 2 s limit moves from 2,700 to 3,100 documents to 2,000 to 3,100. No requirement changed status.

README: "What sparked the idea" rewritten around the GAO report of 1999 (GAO/NSIAD-99-162), which recommended that the Department of Defense assess technology maturity with TRLs and commit to a baseline only at a level analogous to TRL 7; the reference to how the portfolio was assembled is removed, and the first line of the concept rationale no longer refers to it. The other three write-up sections are kept. `docs/01-problem.md` did not attribute the idea to a review; only its license line changed.

### Requirements status (RDK-REQ-001 v0.4)

8 met, 8 not met, 0 at risk, 2 not verifiable at TRL 3, unchanged.

| ID | Status | Value |
| --- | --- | --- |
| R6 | **Not met** | 12 of 20 rules (60%); 18 needed. Route D8 decided, on hold |
| R11 | **Not met** | 13 hard-coded occurrences of 5 identity values. Route D2 decided, on hold |
| R12 | **Not met** | Manual kit copy; STANDARDS.md and kit code differ in 38 of 38 corpus repositories at KIT_VERSION 1.3.1. Route D1 and D4 decided, on hold |
| R13 | **Not met** | 2 of 3 guardrail faults caught. Wording choice O4 open |
| R15 | **Not met** | No getting-started guide. Route D9 decided, on hold |
| R16 | **Not met** | No OKH exporter; 3 of 5 fields. Route D6 decided, on hold |
| R17 | **Not met** | ANSI B only. Route D3 decided, on hold |
| R18 | **Not met** | Three scripts. Route D4 decided, on hold |
| R1, R2 | Not verifiable | No new-user trial; Linux only |
| R3, R4, R5, R7, R8, R9, R10, R14 | Met | Check 0.09 to 0.12 s; three PDFs 1.8 to 3.1 s; 20-part media 12 to 23 s; 0 false failures in 38; outputs reproducible; offline; 1.05 MB; $0.00 |

### Still awaiting Amish

- O1 Name "ReadyKit" for PyPI and GitHub (no recommendation).
- O2 Pilot users (no preference stated).
- O3 Windows native, or WSL2 enough (no recommendation).
- O4 Decision-wording check: generic, or tied to the portfolio phrase (no recommendation).

### Cross-repo actions

Not done here; listed for the owners of the other repositories.

1. **Kit source (shared `.kit/`):** bump KIT_VERSION. The site switch changed 3 lines of kit code and the project-code table changed `STANDARDS.md`, both at version 1.3.1 (RDK-CAL-001, B7 and B8).
2. **Kit source:** D2 (`readykit.yaml`), D3 (ISO A3 in `drawing.py`), D4 (`readykit` command), D8 (six or more new checks) and the R13 wording check belong in the kit, not in this repository. Decided, but on hold with TRL 4.
3. **Kit source:** `concept.render_all` has no license argument, so `cad/src/concept_media.py` sets the blueprint license through a subclass of `drawing.Sheet`. A `license` argument in the kit would remove the workaround. *Update 2026-09-26: the workaround was removed when D5 was reversed; the kit default license applies.*
4. **Website (designmolecule.com card):** ReadyKit's `licenses.hardware` now reads CC-BY-SA-4.0. The key name was kept so the card still parses; the site may want to label it "content" for software projects. *Update 2026-09-26: back to CERN-OHL-S-2.0 after D5 was reversed; no website change needed.*

### Safety concerns

No change. A passing check is not an engineering review, and the future safety-note check (part of D8) must raise a flag for a person, never replace the review.

### TRL 4

TRL 4 remains on hold by Amish's instruction. No package, command, exporter, check, test, trial or purchase was started. `trl: 3`, `trl_target: 3`.

## Session 2026-09-26: D5 license change reversed

Amish wrote on 2026-09-26: "apply the same MIT license pairing across the board for all repos." D5 reversed: decided by Amish, 2026-09-26. Keep the portfolio license pair (CERN-OHL-S v2 and MIT) on every repo for consistency. ReadyKit now matches every other repo: hardware and non-code content under CERN-OHL-S v2 (`LICENSE`), software under MIT (`LICENSE-SOFTWARE`).

- `LICENSE`: CC BY-SA 4.0 legal code replaced by the CERN-OHL-S v2 text, copied verbatim from `fieldnode/LICENSE`.
- `project.yaml`: `licenses.hardware` back to CERN-OHL-S-2.0; tag `cern-ohl-s` restored in place of `cc-by-sa`. `budget_usd`, `trl: 3` and `trl_target: 3` unchanged.
- `README.md` badge and Licenses section, `CONTRIBUTING.md` and `bom/bom.csv` line 7 restored to the portfolio wording.
- Controlled documents, `license` field back to CERN-OHL-S-2.0 and version bumped: RDK-PRB-001 v0.4, RDK-PRC-001 v0.5 (design choice 5 rewritten), RDK-REQ-001 v0.5, RDK-CAL-001 v0.3, RDK-DDR-001 v0.3 (D5 row marked superseded), RDK-DDR-002 v0.2 (reversal recorded).
- Drawings and media: RDK-DWG-001 Rev P3 and blueprint RDK-DWG-010 Rev P3 with CERN-OHL-S-2.0 in the title block. The `drawing.Sheet` subclass workaround in `cad/src/concept_media.py` was removed, which also closes kit finding 3 above. Drawings, media and PDFs regenerated; temporary `_views` folders deleted.
- Check: the only remaining mentions of the content license are the historical text in RDK-DDR-001, RDK-DDR-002 and this note, plus the kit's own `.kit/STANDARDS.md` front matter, which is shared, unchanged kit content identical in every repo.

## Session 2026-09-26: photoreal renders

Amish asked on 2026-09-26 for photoreal renders across the portfolio, starting with the software and playbook repos (Group C). This repo has no new product model: the existing concept scene from `cad/src/concept_media.py` was rendered with Blender Cycles (`.kit/scene_export.py`, `.kit/photoreal.py`) on Amish's Mac and captioned with the project, repository and viewing direction.

- New: `media/render-hero.png`. The README now leads with `media/render-hero.png`.
- Geometry, BOM, calculations and drawings are unchanged. `trl` stays 3; TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

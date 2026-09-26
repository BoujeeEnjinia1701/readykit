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

1. **Distribution:** vendored `.kit/` (today), pip package, or template repository plus sync action. Recommendation: pip package plus template.
2. **Identity:** keep portfolio branding hard-coded, or move it to a `readykit.yaml` with Design Molecule defaults. Recommendation: config file.
3. **Sheet sizes:** ANSI B only, or add ISO A3 and A2. Recommendation: add A3.
4. **Command-line interface:** separate scripts, or one `readykit` command (`init`, `check`, `render`, `media`, `upgrade`). Recommendation: one command with the scripts as wrappers.
5. **Licenses:** `project.yaml` lists CERN-OHL-S for hardware and MIT for software. For a software-only project, option to switch non-code content to CC BY-SA 4.0 (as the standard uses). Recommendation: switch; not changed in this session.
6. **Standards interop:** add Open Know-How manifest export at TRL 3. Recommendation: yes.
7. **Name:** confirm "ReadyKit" before publishing to PyPI; availability not checked.
8. **Pilot users:** a university lab, an open science hardware group (GOSH, AfricaOSH or reGOSH) or a startup.

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

Each of D1 to D7 is "Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review":

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
- Proposed route for R6: add at least six of the eight missing checks (RDK-REQ-001 Table 4). Proposed route for R15: write the guide with the package.
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

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

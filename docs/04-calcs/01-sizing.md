---
doc_id: RDK-CAL-001
title: ReadyKit sizing and measurement note
project: ReadyKit
doc_type: Calculation
version: "0.5"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (kit footprint and identity, check time and scaling, corpus false failures, PDF and media render time, reproducibility, offline use, check coverage by seeded faults, guardrails, cost, licenses, OKH fields, sheet sizes, setup)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: D5 reversed by Amish (RDK-DDR-002); license back to CERN-OHL-S-2.0
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Requirement table: R2 and R13 targets as restated on 2026-10-02 (RDK-DEC-001); no figure changed"
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "New section G from sizing.py: identity values, package extras, CI platforms, Python floor and model checks after the 2026-10-02 follow-ups; no measured figure and no requirement status changed"
---

# ReadyKit sizing and measurement note

ReadyKit meets all eight of its speed, footprint, cost, offline, reproducibility and false-failure targets, most by a wide margin: the check runs in about 0.1 s against a 2 s target, and a 20-part media render takes 12 to 23 s against 60 s. It misses eight requirements, and every one is a feature not yet written rather than a performance shortfall. The largest is check coverage (R6): planting one fault per rule in a passing repository shows that the checker catches 12 of the standard's 20 machine-checkable rules (60%), exactly as the TRL 2 audit claimed, against a 90% target that needs 18. Setup time (R1) and macOS and Windows support (R2) cannot be verified on the one Linux machine available. The measurements also found a problem the TRL 2 note did not: all 38 finished portfolio repositories carry kit version 1.3.1, but none has the current `STANDARDS.md`, and since the switch of the site string to designmolecule.com none has this repository's kit code either, so the kit has drifted twice without a version change. That is evidence for the pip distribution that Amish decided on 2026-09-25 (D1, RDK-DDR-002). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B3], is the line of that script's output that carries it.

> **Safety:** ReadyKit has no physical hazards. These measurements show that the tool is fast and consistent; they do not show that any design it documents is safe. A passing check means the documents are complete and consistent with the standard, not that the engineering has been reviewed.

## Scope and method

The note checks every requirement in RDK-REQ-001 v0.4 against kit 1.3.1 as vendored in this repository. The script runs the kit as a user would, as a separate process, and times wall-clock medians. It works in a temporary folder and only reads the repository. It measures four things:

- **This repository**, as it stands.
- **Synthetic repositories** with 10, 100 and 400 controlled documents, and a 20-part build123d model, built by the script.
- **A corpus** of 38 portfolio repositories already at TRL 3 (`/home/claude/trl3`, or any folder passed with `--corpus`). Each is copied without its Git history and given this repository's kit, so the kit under test is ReadyKit's.
- **A fixture repository**: a minimal repository that passes the check at TRL 3, into which the script plants one fault per rule (section E).

Run it from the repo root with `python docs/04-calcs/sizing.py`; add `--setup` to time a fresh install (F6). It writes `docs/04-calcs/results.csv`.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Machine | A 2-core Linux container with Python 3.11 is representative of a modest laptop and of a free CI runner | Free GitHub-hosted Linux runners also have two or more cores; to be confirmed on real laptops |
| Noise | Other jobs share the machine, so times vary by up to a factor of two between runs; the note quotes the range over repeat runs and judges each target on the worst value | Observed across six runs of the script |
| Git | The kit's call to Git is replaced by a shim that fails, so the PDF commit field reads "uncommitted" in every run | Makes runs comparable and keeps Git out of the measurement |
| Corpus | The 38 finished repositories follow the standard, so any check failure on them would be a false failure | Each passed the check and a human-written review at TRL 3 |
| Coverage | One planted fault per rule is enough to show whether a rule is checked; a rule counts as checked only if the check fails or warns | Standard mutation-testing logic; a rule could be checked for some faults and not others |
| Rules | The 20 machine-checkable rules are those listed in RDK-REQ-001, Table 4 | TRL 2 audit of STANDARDS.md |
| Setup | WeasyPrint's system libraries (Pango) are already installed; pip reaches PyPI through a proxy | True of this machine only |

## A. Kit footprint, size and identity (R10, R11)

- **Machine.** Linux x86_64, 2 CPUs, Python 3.11.15, kit 1.3.1 [A0].
- **Footprint.** The vendored `.kit/` folder is 1.05 MB in 18 files, and the fonts make up 0.99 MB (94%) of it [A1]. R10 (2 MB) is met. After D1 the per-repository stub would drop to the fonts and a version pin, if the fonts stay vendored.
- **Source size.** The kit is 808 lines of Python: `concept.py` 282, `drawing.py` 300 and `render.py` 226 [A2].
- **Reach.** The standard lists 85 project codes, plus OHP for the portfolio as a whole [A3].
- **Identity.** Kit code, style and templates hold 13 hard-coded occurrences of five identity values: the website designmolecule.com (3), the organization name Design Molecule Lab (2), the GitHub owner (1), the default author (4) and the portfolio name (3), spread over `drawing.py`, `render.py`, `concept.py`, the PDF template and stylesheet and the document template [A4]. Version 0.1 counted 13 occurrences of four values; the site switch replaced the old domain and two portfolio-name strings with the new domain and the organization name, so the count is unchanged and the values are still hard-coded. R11 is not met; D2 moves them into `readykit.yaml`.

## B. Check time, scaling and false failures (R3, R7, R12)

- **This repository.** The check takes 0.09 to 0.12 s [B1], of which Python start-up and imports take 0.08 to 0.10 s [B2]. The checking itself takes about 10 to 25 ms.
- **Scaling.** On synthetic repositories the check takes 0.10 to 0.12 s for 10 documents, 0.15 to 0.19 s for 100 and 0.35 to 0.49 s for 400 over six runs. The slope is 0.6 to 1.0 ms per document, so the 2 s target is reached at about 2,000 to 3,100 documents [B3]. The slowest run was the last, made while other jobs loaded the machine. R3 is met with a margin of more than 15 times for any real repository. The TRL 2 assumption that check time grows linearly with document count holds.
- **Corpus.** Across 38 finished repositories with 5 to 8 controlled documents each, the check takes 0.10 to 0.11 s median and 0.12 to 0.27 s at most [B4].
- **False failures.** None of the 38 conforming repositories fails [B5]. One warns, correctly: ThermaBrick holds a purchasing checklist and a build log template, which are TRL 4 material kept under the cap rule [B6]. R7 is met on the evidence available; a corpus written by other teams would be a stronger test.
- **Drift.** `STANDARDS.md` differs in all 38 corpus repositories, although every one reports KIT_VERSION 1.3.1 [B7]. The difference is the project-code table, which gained 38 project codes for this batch without a version change. Since the site switch, the kit code differs too: none of the 38 matches this repository's, and the difference is 3 changed lines, all of them the site and organization strings [B8]. Version 0.1 found the code identical in 38 of 38. A kit version that does not identify its content is the failure R12 exists to prevent.

## C. PDF render, reproducibility and offline use (R4, R8, R9)

- **Render time.** A copy of the WaterWatch repository, 5 controlled documents and 31 pages, renders in 3.0 to 5.2 s including the check, which is 0.6 to 1.0 s per document or 1.8 to 3.1 s for three documents [C1]. Per page it is 0.10 to 0.17 s [C2]. R4 (10 s for three documents) is met in the worst run with a margin of about three times.
- **Reproducibility.** Rendering the same repository twice gives identical extracted text in 5 of 5 PDFs [C3]. With the commit field fixed and the dates taken from front matter, nothing in the text depends on when the render ran. R8 is met for text; section D covers images.
- **Offline.** In a network namespace with no interfaces, both the check and the full render pass [C4]. R9 is met; `viewer.html` still loads its viewer script from a CDN, which is a website concern rather than a render step.

## D. Concept media (R5, R8)

- **This repository.** `cad/src/concept_media.py` renders the 7-module massing with the laptop for scale, the exploded view, the blueprint sheet, the GLB model and the pipeline diagram in 5 to 6 s [D1].
- **Twenty parts.** A synthetic 20-part model, each part a box with a bore and a boss, with cutaway, exploded view, the 1.75 m scale figure and the blueprint sheet, renders in 12 to 23 s [D2]. R5 (60 s) is met with a margin of at least 2.6 times, with no GPU.
- **Reproducibility.** Rendering the 20-part model twice gives byte-identical PNG images, 4 of 4 [D3]. R8 is met for images.

## E. Check coverage and guardrails (R6, R13)

- **Method.** The fixture repository passes the unmodified check [E0]. For each of the 20 rules in RDK-REQ-001 Table 4 the script copies the fixture, plants one fault, for example a missing `author` field, a duplicated document ID, an unpriced BOM line or a hazard keyword with no safety note, and runs the check.
- **Result.** The check catches 12 of the 20 faults (60%) and misses 8 [E1]. The result agrees with the TRL 2 audit on every rule. The em dash rule is only half covered: an em dash in a controlled document fails the check, but one in `README.md` passes. R6 is not met; 18 rules are needed for 90%, a gap of 6 [E2].
- **First probe corrected.** The first version of the duplicate-ID probe changed the requirements document's ID to the problem statement's. The check failed, but only because the requirements document then disappeared from the TRL evidence, not because it saw a duplicate. The probe now adds a second file that reuses an ID while all evidence stays present, and the rule is correctly recorded as missed.
- **Guardrails.** A TRL above the cap and a TST folder are both caught. A decision written as made ("Decision: the budget is raised to $900. Approved.") passes [E3]. R13 is not met.

## F. Cost, licenses, interoperability, sheets and setup (R1, R14, R16, R17)

- **Cost.** The BOM has 11 lines, none unpriced, and totals $0.00 against `budget_usd` of $0.00 [F1]. R14 is met.
- **Licenses.** The eight direct dependencies are PyYAML (MIT), Python-Markdown (BSD-3-Clause), Jinja2 (BSD), WeasyPrint (BSD), CairoSVG (LGPL-3.0-or-later), build123d (Apache-2.0), NumPy (BSD-3-Clause and others) and Matplotlib (PSF-based) [F2]. One is copyleft: CairoSVG, which the kit imports without modifying, so it does not constrain the MIT license of the kit's own code [F3]. Transitive dependencies, such as the OpenCascade bindings under build123d, were not audited.
- **Open Know-How.** OKH 1.0 requires a title, a description, a manifest author's name, a license and either a project link or a documentation home ([OKH 1.0](https://standards.internetofproduction.org/pub/okh/release/1)). `project.yaml` supplies 3 of the 5 (title, description, license); the manifest author and the project link are missing [F4], and both belong in `readykit.yaml` (D2). R16 is not met.
- **Sheets.** The drawing generator supports 1 sheet size, ANSI B, fixed as module constants [F5]. R17 is not met.
- **Setup.** A fresh virtual environment plus `pip install` of the kit requirements took 32 to 47 s over six runs and installed 1.09 GB; the check then passed [F6]. That is under 5% of R1's 15 minutes, but it excludes WeasyPrint's system libraries, Python itself and a new user reading instructions. R1 is not verifiable at TRL 3.

## Design record counts after the 2026-10-02 decisions

*Table 1a. Counts read from the massing model by `sizing.py` section G (run with `--design-only`).*

| Tag | Quantity | Value |
| --- | --- | --- |
| G1 | Identity values handed on by the reader | 6, the sixth being the still-open phrase (default "Proposed, awaiting") |
| G2 | Extras beside the core install | 4: PDF, drawings, media, release (release gate and archive helper in the release extra; build plan pictures in the media extra) |
| G3 | CI platforms for the first release | 3: Linux, macOS, Windows through WSL2 |
| G4 | Oldest Python supported | 3.11; CI on 3.11 and the newest release; this run used 3.11.15 |
| G5 | Massing model checks failing | 0 |

No timing or size changed, so sections A to F were not re-run.

## Results

*Table 2. Every requirement in RDK-REQ-001 v0.4 against the measurements. Worst value of the repeat runs.*

| ID | Quantity | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Setup time, empty folder to first passing check | Dependency install 32 to 47 s [F6]; full new-user trial not run | 15 min or less | Not verifiable at TRL 3 |
| R2 | Platforms | Linux works [B1, F6]; macOS and Windows not available; CI matrix of 3 platforms and Python 3.11 and newest planned [G3, G4] | Linux, macOS, Windows through WSL2 for the first release (RDK-DEC-001) | Not verifiable at TRL 3 |
| R3 | Check time per repository | 0.12 s here; 0.27 s worst in corpus; 0.49 s at 400 documents [B1, B3, B4] | 2 s or less | Met |
| R4 | PDF render, three documents | 3.1 s [C1] | 10 s or less | Met |
| R5 | Media render, 20 parts, no GPU | 23 s [D2] | 60 s or less | Met |
| R6 | Check coverage | 12 of 20 rules, 60% [E1] | 90% or more (18 rules) | **Not met** |
| R7 | False failures | 0 of 38 conforming repositories [B5] | None | Met |
| R8 | Reproducible output | Text 5 of 5 PDFs [C3]; images 4 of 4 [D3] | Identical apart from date and commit | Met |
| R9 | Offline use | Check and render pass with no network [C4] | No network needed | Met (viewer page excepted) |
| R10 | Kit footprint per repository | 1.05 MB [A1] | 2 MB or less | Met |
| R11 | Configurable identity | 13 hard-coded occurrences of 5 values [A4]; the sixth value, the still-open phrase, is hard-coded nowhere [G1] | None hard-coded | **Not met** |
| R12 | Upgrade path | Manual copy; STANDARDS.md and kit code differ in 38 of 38 repositories at the same version [B7, B8] | One command with a diff | **Not met** |
| R13 | Agent guardrails | 2 of 3 seeded faults caught [E3] | 3 of 3; the decision fault judged by the generic owner-and-date rule (RDK-DEC-001) | **Not met** |
| R14 | Cost to user | $0.00 [F1]; all dependencies free [F2] | $0 | Met |
| R15 | Documentation | No getting-started guide | Guide of 5 pages or fewer, plus check reference | **Not met** |
| R16 | Open Know-How export | No exporter; 3 of 5 required fields available [F4] | Complete `okh.yml` | **Not met** |
| R17 | Sheet sizes | 1 (ANSI B) [F5] | ANSI B and ISO A3 | **Not met** |
| R18 | Command-line interface | Three separate scripts | One `readykit` command | **Not met** |

Summary: 8 met, 8 not met, 0 at risk, 2 not verifiable at TRL 3.

## Checks against the other documents

- The TRL 2 figures in RDK-PRC-001 v0.2 (check about 0.1 s, render about 1.6 s for three documents, media about 5 to 7 s, kit about 1.1 MB, about 810 lines, about 85 codes) are confirmed or narrowed. The three-document render is now 1.8 to 3.1 s rather than 1.6 s, still far inside R4. RDK-PRC-001 v0.4, RDK-REQ-001 v0.4, the README, the concept media and RDK-DWG-001 Rev P2 use the numbers above.
- The TRL 2 note listed R2 as not met for Windows native. It is untested rather than shown to fail, so RDK-REQ-001 v0.3 lists it as not verifiable at TRL 3.
- The TRL 2 coverage audit (12 of 20) is confirmed rule by rule.
- Version 0.2 reruns the script after Amish accepted the recommendations (RDK-DDR-002) and after the kit's site string was switched to designmolecule.com. The decisions change no measured quantity: the D5 license change touches front matter and title blocks only, and the other decisions are features not yet built. The rerun changes the identity breakdown (A4), the kit-code drift (B7, B8) and the upper end of the setup range (F6); every other value stays inside the ranges of version 0.1.

## Limits of this note

- One machine, one operating system and one Python version. Times on a laptop without other load should be lower; times on Windows are unknown.
- The corpus was written by the same authors and tools as the kit, so it cannot reveal false failures that only other teams' habits would trigger.
- The coverage probes plant one fault per rule. A rule marked "caught" may still miss other forms of the same fault.

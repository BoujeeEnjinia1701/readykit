# ReadyKit

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827) [![DOI](https://zenodo.org/badge/1388477875.svg)](https://zenodo.org/badge/latestdoi/1388477875) [![REUSE compliant](https://github.com/BoujeeEnjinia1701/readykit/actions/workflows/reuse.yml/badge.svg)](https://github.com/BoujeeEnjinia1701/readykit/actions/workflows/reuse.yml) [![Archived in Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/BoujeeEnjinia1701/readykit/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/BoujeeEnjinia1701/readykit)

**Area:** Open Engineering · **TRL:** 3 of 9 (proof of concept) · **Prototype budget:** software only · **Difficulty:** 2 of 5

The lab's documentation and readiness kit released as an open tool: document control, technology readiness level gating, concept renders, drawings and branded PDFs from plain Markdown and Python, usable by any hardware team.

![ReadyKit: documentation and readiness kit for open hardware, photoreal render](media/render-hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement (PDF)](cad/drawings/RDK-DWG-001.pdf) · [Calculation note](docs/04-calcs/01-sizing.md) · [Prototype build plan](docs/05-build-plan.md) · [Design decisions](docs/06-design-decisions.md) · [Review note](docs/REVIEW.md)

## Concept rationale

The lab's documentation method is itself reusable. Every repository keeps its documents as Markdown with version-controlled front matter and its geometry as build123d Python, and one checker refuses a TRL claim unless the evidence files exist. Publishing that kit as a standalone tool lets other teams adopt the same discipline without inventing their own templates, and it keeps the portfolio's method open to review.

It stays open and garage-friendly because it needs nothing but Python and Git: no CAD license, no GPU, no paid service, and it runs offline on an ordinary laptop. Plain text means every change to a requirement or a drawing shows up in a diff that anyone can review.

## Burning platform

Open hardware often cannot be rebuilt from what is published. In a study of 132 open source hardware products, only 11 (8%) shared all eight documentation elements the authors assessed, and the average was 4.2 of 8 ([Bonvoisin et al. 2017](https://doi.org/10.5334/joh.7)). In a *Nature* survey of about 1,500 researchers, more than 70% had tried and failed to reproduce another scientist's experiment ([Baker 2016](https://www.nature.com/articles/533452a)).

At the same time, public funders expect openness and a stated readiness level. The UNESCO Recommendation on Open Science, adopted by 193 countries in November 2021, covers sharing of hardware as well as publications and data ([UNESCO](https://www.unesco.org/en/articles/unesco-sets-ambitious-international-standards-open-science)), and Horizon Europe calls are framed in Technology Readiness Levels ([Horizon Europe NCP portal](https://horizoneuropencpportal.eu/sites/default/files/2022-12/trl-assessment-tool-guide-final.pdf)). Small teams need a cheap way to meet both expectations.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| University research labs | Controlled documents and TRL evidence for lab-built instruments, theses and grant reports |
| Open science hardware | Rebuildable documentation for shared instruments, with a readiness level other labs can trust |
| Hardware startups | TRL claims tied to evidence for grant and accelerator applications |
| Engineering education | Student design teams learn document control, revisions and drawings on real projects |
| Makerspaces and fab labs | A standard repo layout for community projects so others can build and maintain them |
| Nonprofit and humanitarian engineering | Designs handed to local partners with clear status, safety notes and "not for fabrication" marking |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| European Union | Horizon Europe frames calls in TRLs, so applicants need evidence for the level they claim ([NCP portal](https://horizoneuropencpportal.eu/sites/default/files/2022-12/trl-assessment-tool-guide-final.pdf)) |
| Germany | DIN published DIN SPEC 3105 on open hardware documentation in 2020 ([Journal of Open Hardware](https://journalopenhw.medium.com/din-spec-3105-explained-2cce6134c207)), and the Prototype Fund supports individuals and small teams building open hardware ([Prototype Fund Hardware](https://hardware.prototypefund.de/en/about-2/)) |
| United States | The TRL scale comes from NASA ([NASA](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/)), and a 2022 White House memo requires public access to the results of federally funded research ([OSTP](https://bidenwhitehouse.archives.gov/wp-content/uploads/2022/08/08-2022-OSTP-Public-Access-Memo.pdf)) |
| Ghana and West Africa | The first Africa Open Science Hardware summit met in Kumasi in April 2018 ([Open AIR](https://openair.africa/historic-gathering-of-africas-open-science-hardware-osh-innovators-the-africaosh-summit-kumasi-ghana/)); a free, offline tool suits labs with limited budgets and bandwidth |
| Argentina and Latin America | The reGOSH network runs open hardware residencies, such as Mendoza in 2022 ([reGOSH](https://regosh.libres.cc/en/residencies/residency-mendoza-2022/)), where shared documentation lets projects move between labs |
| India | The Atal Innovation Mission reports 10,000 Atal Tinkering Labs and 72 Atal Incubation Centres ([AIM](https://aim.gov.in/)); student teams and incubated startups could use a free template to document projects to a common standard |

## What sparked the idea

The starting point was a 1999 report by the U.S. General Accounting Office, *Best Practices: Better Management of Technology Development Can Improve Weapon System Outcomes* ([GAO/NSIAD-99-162](https://www.gao.gov/products/nsiad-99-162)). It recommended that the Department of Defense assess technology maturity DoD-wide with a disciplined, knowledge-based method such as Technology Readiness Levels, and commit to a program's cost, schedule and performance baseline only once key technologies reached a level analogous to TRL 7. The point that carries over is that a readiness level is only as good as the evidence behind it. ReadyKit brings that rule down to the scale of a garage team: the checker refuses a TRL claim in `project.yaml` unless the evidence files for that level exist in the repository, so the claim and its proof travel together.

## Problem

Small hardware teams and open projects rarely document requirements, decisions and readiness consistently, so work is hard to review, reproduce or fund.

## Concept

The lab's documentation and readiness kit released as an open tool: document control, technology readiness level gating, concept renders, drawings and branded PDFs from plain Markdown and Python, usable by any hardware team.

Authors write documents in Markdown with YAML front matter and geometry in build123d Python. One command checks every document and the claimed TRL against the evidence in the repository, and CI blocks a merge when the check fails. A second command renders branded PDFs, drawing sheets and concept media. Measured on a 2-core machine ([RDK-CAL-001](docs/04-calcs/01-sizing.md)), the check takes about 0.1 s per repository, PDFs take 0.6 to 1.0 s per document, and concept media for a 20-part model take 12 to 23 s. Across 38 finished portfolio repositories the check raised no false failures.

![Documentation pipeline](media/flow.png)

Full design precis: [docs/02-concept.md](docs/02-concept.md). Requirements, including the eight not yet met (check coverage, configurable branding, one-command upgrades, the decision-wording guardrail, a getting-started guide, Open Know-How export, ISO A3 sheets and a single command): [docs/03-requirements.md](docs/03-requirements.md). The checker catches 12 of the standard's 20 machine-checkable rules; the target is 18. The general arrangement sheet [RDK-DWG-001](cad/drawings/RDK-DWG-001.pdf) lays out the pipeline, and decisions are in [RDK-DDR-001](docs/decisions/0001-trl2-review-decisions.md) and [RDK-DDR-002](docs/decisions/0002-recommendations-accepted.md). Amish accepted the recommended distribution, identity, sheet-size, command-line, licensing and Open Know-How choices on 2026-09-25; building them is TRL 4 work and is on hold.

A passing check means the documents are complete and consistent. It does not mean a design is safe or fit for use.

## Key components

Numbered as in the exploded view and the bill of materials.

1. Document control checker
2. PDF renderer and house style
3. Drawing sheet generator
4. Concept media renderer
5. TRL gate and badge
6. Agent guardrails
7. Template repository and CI workflow

The working bill of materials is in [bom/bom.csv](bom/bom.csv). Value-engineering target: USD 0. Estimated cost of the constructable design: USD 0 (USD 0 over the target): the modules are MIT and the dependencies are free and open source. Line 12, the repository reader, and line 13, the bundled 3D viewer script, were added to make the design constructable.

## Building the prototype

The prototype build plan ([RDK-BLD-001](docs/05-build-plan.md)) sets out how to build the first standalone ReadyKit, module by module, with a making sketch for each module, a close-up of every interface and a picture for every step. Drawing it showed five joints that could not work as the concept described them, so the design was made constructable (decision record [RDK-DDR-003](docs/decisions/0003-design-for-construction.md), accepted by Amish on 2026-10-02): a shared repository reader, a defined 47 kB stub in each repository with the agent rules in it, a small core install for the check, a bundled viewer script so everything works offline, and a README badge written by the readiness gate. Decisions still open are in the [design decisions register](docs/06-design-decisions.md). Building to the plan is TRL 4 work and is on hold.

![ReadyKit prototype: every component pulled apart and numbered in build order](docs/05-build-plan/overview.png)

## Safety

ReadyKit is software and has no physical hazards of its own. A passing check means the documents are complete and consistent with the standard; it does not mean a design is safe, correct or fit for use. Rendered documents and drawings keep their "Draft" or "not for fabrication" marking until a qualified person has reviewed the engineering, and the planned safety-note check raises a flag for a person, never replacing that review.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (RDK-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `RDK-PRC-001/v1.0`.

## Credits

Designed by Amish Chadha. See [CONTRIBUTORS.md](CONTRIBUTORS.md) for roles. To cite this design, use [CITATION.cff](CITATION.cff) (GitHub shows it as "Cite this repository").

AI assistance (Claude) was used to accelerate concept renders, prototype documentation and first-pass sizing calculations. Design direction and all decisions are Amish Chadha's, recorded in this repository's decision records (`docs/decisions/`).

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab.

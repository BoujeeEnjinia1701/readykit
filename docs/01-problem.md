---
doc_id: RDK-PRB-001
title: ReadyKit problem statement
project: ReadyKit
doc_type: Problem statement
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CC-BY-SA-4.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Users, context, prior work with sources, constraints and out of scope for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# ReadyKit problem statement

Small hardware teams and open projects rarely document requirements, decisions and readiness consistently, so work is hard to review, reproduce or fund. The tools that exist cover pieces of the job (assembly instructions, metadata, certification) but no free tool ties document control, readiness levels, drawings and concept renders together in one repository with a check that runs on every push.

## The problem in numbers

- In a study of 132 open source hardware products, only 11 (8%) published all eight documentation elements the authors assessed, such as editable CAD, a bill of materials and assembly instructions; the mean score was 4.2 of 8 ([Bonvoisin et al. 2017, *Journal of Open Hardware*](https://doi.org/10.5334/joh.7)).
- In a *Nature* survey of about 1,500 researchers, more than 70% said they had tried and failed to reproduce another scientist's experiment ([Baker 2016, *Nature* 533](https://www.nature.com/articles/533452a)).
- Funders ask for readiness in a common language. NASA defines Technology Readiness Levels 1 to 9 ([NASA](https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/)), and Horizon Europe uses the same scale in its calls ([Horizon Europe NCP portal, TRL self-assessment guide](https://horizoneuropencpportal.eu/sites/default/files/2022-12/trl-assessment-tool-guide-final.pdf)). Small teams seldom keep the evidence that would support a claimed level.

## Users and context

| User | Situation | What they need from ReadyKit |
| --- | --- | --- |
| Solo maker or two-person team | Builds in a garage or makerspace; documents in a README, if at all | A repo that starts documented, and a check that says what is missing |
| University lab or student team | Needs reviewable designs for supervisors, theses and competitions | Controlled documents with versions and revision history that print cleanly |
| Open science hardware group | Shares instruments with other labs (GOSH, AfricaOSH, reGOSH networks) | Documentation others can rebuild from, with a stated readiness level |
| Early-stage hardware startup | Prepares grant or accelerator applications that ask for a TRL | TRL claims tied to evidence files, checked in CI |
| Team using AI coding agents | Lets an agent draft documents and CAD | Written guardrails the agent reads, plus automatic checks that catch drift |

The kit was built for the Design Molecule open hardware portfolio of about 85 project codes and is in daily use there. ReadyKit is the proposal to release it as a standalone, reusable tool.

## Prior work

| Tool or standard | What it covers | Gap ReadyKit addresses |
| --- | --- | --- |
| [GitBuilding](https://gitbuilding.io/) | Markdown-based assembly instructions for open hardware | No document control, TRL gating or CAD-driven media |
| [DIN SPEC 3105-1](https://journalopenhw.medium.com/din-spec-3105-explained-2cce6134c207) | Requirements for open hardware technical documentation | A specification, not a tool; no automatic check |
| [Open Know-How (OKH)](https://standards.internetofproduction.org/pub/okh/release/1) | Metadata manifest so designs can be found and indexed | Describes a project; does not produce its documents |
| [OSHWA certification](https://certification.oshwa.org/) | Self-certified openness of a hardware project | Licensing and openness, not document quality or readiness |
| [build123d](https://github.com/gumyr/build123d) | Python CAD library | Geometry only; ReadyKit builds sheets and renders on top of it |

## Constraints

- Hardware budget $0: ReadyKit is software, free to use and free of paid services.
- Runs on a normal laptop with Python 3.11 or later; no GPU and no CAD license needed.
- Plain text in Git as the source of truth (Markdown, YAML, Python), so every change is reviewable in a diff.
- Works offline, except for installing packages and the 3D viewer page, which loads its viewer script from a public CDN.
- Open licenses throughout: code MIT; documents, drawings, CAD, BOM and media CC BY-SA 4.0, as the standard itself uses (RDK-DDR-002); fonts SIL OFL.

## Out of scope at this stage

- A hosted web service or account system.
- Formal quality management certification (for example ISO 9001) or regulatory submissions.
- Electronics design checks (KiCad) and firmware documentation beyond linking to the files.
- Any claim that the kit makes a design safe or fit for use; it checks documentation, not engineering.

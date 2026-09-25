# ReadyKit

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Open Engineering · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** software only · **Difficulty:** 2 of 5

The lab's documentation and readiness kit released as an open tool: document control, technology readiness level gating, concept renders, drawings and branded PDFs from plain Markdown and Python, usable by any hardware team.

## Concept rationale

The method that moved the lab's portfolio to TRL 3 is itself reusable; publishing it lets others adopt the same discipline.

## Burning platform

Open hardware projects are often abandoned or unusable because the documentation needed to build, review or certify them is missing.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. The kit was built for this portfolio and is the lab's open engineering practice in concrete form.

## Problem

Small hardware teams and open projects rarely document requirements, decisions and readiness consistently, so work is hard to review, reproduce or fund.

## Concept

The lab's documentation and readiness kit released as an open tool: document control, technology readiness level gating, concept renders, drawings and branded PDFs from plain Markdown and Python, usable by any hardware team.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Document control front matter and checker
- TRL gating rules and badge
- Concept render and drawing scripts
- PDF rendering with house style
- Agent guardrail files
- Template repository

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

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

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Gap-filling areas set.

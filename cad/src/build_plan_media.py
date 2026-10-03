"""ReadyKit prototype build plan pictures (RDK-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...]
With no argument it draws everything. Every 3D picture is drawn from cad/src/model.py
(modules), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/RDK-DWG-101 to 108        making sketches for the eight made modules
    docs/05-build-plan/joint-NN.png        close-ups of the interfaces that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step

ReadyKit is software. Each massing object stands for one module (cad/src/model.py), so a making
sketch shows what the module reads, what it hands on and the parts inside it (an interface view)
in place of three orthographic views, with the module's object highlighted in the kit as the
"where it goes" inset. Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import modules, laptop  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
DATE2 = "2026-10-02"          # date of the revision that carried out the decisions of 2026-10-02
REV2 = {"template", "reader", "gate"}   # making sketches revised to P2 on 2026-10-02
INK, MUTED, ACCENT, FAIL = "#111827", "#4B5563", "#0F766E", "#C2410C"

M = {no: (name, shape, color) for no, name, shape, color, _ in modules()}


def part(no, name, explode=(0, 0, 0), color=None):
    return Part(name, M[no][1], color or M[no][2], no, tuple(explode), 1.0)


# ----------------------------------------------------------------- components, in build order
# key: (bom number, plain name, overview offset, fitting direction for its step)
ORDER = [
    ("template", 7, "Template repository and CI workflow", (0, 0, -60), (0, 0, 160)),
    ("bought", 10, "Bought open-source parts", (-60, -120, 0), (-120, -160, 120)),
    ("reader", 12, "Repository reader", (60, 20, 110), (40, 80, 150)),
    ("checker", 1, "Document control checker", (0, 0, 120), (0, 0, 150)),
    ("gate", 5, "TRL gate and badge", (-40, -150, 0), (-60, -160, 110)),
    ("pdf", 2, "PDF renderer and house style", (0, 0, 230), (0, 0, 140)),
    ("drawing", 3, "Drawing sheet generator", (60, 40, 0), (160, 80, 120)),
    ("media", 4, "Concept media renderer", (90, -160, 60), (60, -140, 140)),
    ("guard", 6, "Agent guardrails", (-120, -40, 0), (-140, -80, 120)),
]
P = {k: part(no, name) for k, no, name, _, _ in ORDER}


def overview():
    parts = [part(no, f"{name}", off) for _, no, name, off, _ in ORDER]
    return bv.overview(parts, OUT / "overview.png", "ReadyKit prototype: every component, pulled apart",
                       subtitle="Numbered in build order; each object stands for one software module. Seen from the front right and above",
                       size=(10, 6.2), elev=34, key=True)


# ----------------------------------------------------------------- making sketches (interface view)
MODS = {
    "template": dict(
        dwg="RDK-DWG-101", title="Template repository and CI workflow: making sketch",
        material="Software: Python package skeleton, GitHub template repository, CI workflow; MIT",
        reads=["Folder layout of a portfolio repository", "Controlled-document template", "License texts (MIT; CERN-OHL-S v2)"],
        inside=["Package skeleton with a version number", "Per-repository stub, about 47 kB", "CI workflow: Linux, macOS, Windows (WSL2)", "Release job: PDFs on a document tag"],
        writes=["A new repository, ready to check", "A pass or fail on every push", "PDFs attached to a release"],
        sizes=["Stub in each repository: about 47 kB (today 1.20 MB of kit)", "Check job installs the core only: about 5 MB",
               "Release job installs every extra: about 1.1 GB",
               "Python 3.11 or later; CI on 3.11 and the newest release"],
        notes=["Make it first, so every later module is checked by CI from day one.",
               "1. Start an empty package with a version number, a license file and",
               "   Python 3.11 or later; list the four extras (PDF, drawings,",
               "   media, release), each with its libraries.",
               "2. Copy the folder layout of a finished repository into the template:",
               "   docs, cad, bom, media, the license files and the citation file.",
               "3. Write the stub: the version pin, the identity file, the agent rules",
               "   and commands, and a copy of the standard. No code, no fonts.",
               "4. Write the CI workflow: check on every push and pull request with",
               "   the core install, on Linux, macOS and Windows through WSL2, on",
               "   Python 3.11 and the newest release; render and publish PDFs on",
               "   a release tag only.",
               "Fits: the stub is the only kit content inside a repository (joint 6);",
               "the check job reads the checker's exit code (joint 2).",
               "Check: the template repository passes the check before any other",
               "module exists (an empty TRL 1 project with its problem statement)."]),
    "reader": dict(
        dwg="RDK-DWG-102", title="Repository reader: making sketch",
        material="Software: Python, PyYAML; MIT",
        reads=["Project file (name, TRL, evidence list)", "Identity file (six values, with the still-open phrase)", "Phase file (TRL cap)",
               "Front matter of every controlled document", "Bill of materials (numbered lines)"],
        inside=["One loader per source", "Defaults for any missing identity value", "Clear error naming the file and the line"],
        writes=["One record of the repository, used by every other module"],
        sizes=["Five sources, read once per run", "Replaces eight separate reads of the project file in seven scripts",
               "Identity defaults: the Design Molecule values;", "still-open phrase: Proposed, awaiting"],
        notes=["New for construction (RDK-DDR-003, change P1).",
               "1. Write one loader for each of the five sources in the interface view.",
               "2. Give every identity value a default, so a repository with no",
               "   identity file still renders with the Design Molecule values.",
               "   The sixth value is the still-open phrase, default Proposed,",
               "   awaiting.",
               "3. When a file cannot be read, stop with the file name and line;",
               "   never fall back silently to an empty value.",
               "4. Hand back one record. No other module opens these files itself.",
               "Fits: the checker and the gate read the record (joint 1); the",
               "renderer, sheet generator and media renderer read its identity",
               "part (joint 4).",
               "Check: run it on the 38 finished portfolio repositories; every",
               "record matches what the present scripts read, field for field."]),
    "checker": dict(
        dwg="RDK-DWG-103", title="Document control checker: making sketch",
        material="Software: Python, PyYAML; MIT",
        reads=["The reader's record of every controlled document", "The whole text of each document (dash scan)"],
        inside=["20 machine-checkable rules of the standard", "One message per fault: file, then reason", "Exit code 0 for pass, 1 for fail"],
        writes=["Pass or fail to CI (exit code)", "A list of faults for the author"],
        sizes=["Rules: 12 of 20 today; at least 18 (R6)", "Time: 2 s or less per repository (R3); about 0.1 s today",
               "False failures on conforming repositories: none (R7)"],
        notes=["1. Carry over the twelve rules that work today, unchanged.",
               "2. Add at least six of the eight missing rules (decision D8):",
               "   unique document numbers, dashes in every file, the \"not for",
               "   fabrication\" label on media, BOM numbering against the exploded",
               "   view, figure and table captions, and a safety note where hazard",
               "   words appear. The safety-note rule raises a flag for a person;",
               "   it never replaces the human review.",
               "3. For each rule, keep one seeded-fault test repository that must",
               "   fail, and the passing fixture that must pass.",
               "Fits: reads only the reader's record (joint 1); hands CI an exit",
               "code and a fault list (joint 2).",
               "Check: every seeded fault is caught; the 38 finished repositories",
               "still pass; a full run stays under 2 s."]),
    "gate": dict(
        dwg="RDK-DWG-104", title="TRL gate and badge: making sketch",
        material="Software: Python; MIT",
        reads=["Claimed TRL and target (project file)", "Evidence files for each level", "TRL cap (phase file)",
               "Still-open phrase (identity file)"],
        inside=["Evidence rules for TRL 1 to 6", "Phase cap rule", "Badge writer (README line and PDF cover)"],
        writes=["Pass or fail for the claimed TRL", "README badge line", "TRL on every PDF cover"],
        sizes=["Evidence rules: TRL 1 to 6 today", "Badge: one line, rewritten only when the TRL changes",
               "Cap: TRL 3 in this portfolio phase"],
        notes=["1. Carry over the evidence rules for TRL 1 to 6 and the phase cap.",
               "2. Add the badge writer (RDK-DDR-003, change P5): it writes the TRL",
               "   badge line at the top of the README from the claimed TRL, so",
               "   the badge can no longer disagree with the project file.",
               "3. Add the decision-wording rule of R13: a decision written as",
               "   made with no owner and date fails; the still-open phrase comes",
               "   from the identity file, default Proposed, awaiting.",
               "Fits: reads the reader's record (joint 1); the badge line and the",
               "PDF cover take the same TRL value (joint 3).",
               "Check: a TRL claimed one level above its evidence fails; the",
               "badge changes when, and only when, the TRL changes."]),
    "pdf": dict(
        dwg="RDK-DWG-105", title="PDF renderer and house style: making sketch",
        material="Software: Python-Markdown, Jinja2, WeasyPrint, IBM Plex fonts; MIT and OFL",
        reads=["Controlled documents (after a passing check)", "Identity values from the reader", "Page template and style sheet"],
        inside=["Markdown to web page", "Page template: cover, control table, revisions", "Web page to PDF", "Bundled fonts"],
        writes=["One PDF per document and version", "Older versions removed (kept in history)"],
        sizes=["Page: US Letter, 216 x 279 mm, 20 mm margins", "Time: 10 s or less for three documents (R4); 1.8 to 3.1 s today",
               "Same text on every run, apart from date and commit (R8)"],
        notes=["1. Move every identity string out of the template and style sheet;",
               "   take them from the reader's identity record (decision D2).",
               "   Today 13 such strings are written in by hand (R11).",
               "2. Ship the fonts inside the package (RDK-DDR-003, change P2), not",
               "   in each repository.",
               "3. Render only after a passing check; a failing check renders",
               "   nothing.",
               "Fits: identity values arrive through joint 4; the TRL on the cover",
               "comes from the gate (joint 3). Needs the PDF extra and the Pango",
               "and fontconfig system libraries.",
               "Check: render one repository with the default identity and once",
               "with a second identity; no Design Molecule text in the second."]),
    "drawing": dict(
        dwg="RDK-DWG-106", title="Drawing sheet generator: making sketch",
        material="Software: Python, build123d, CairoSVG; MIT",
        reads=["Parts from the project's own model", "Identity values from the reader", "Sheet size chosen per repository"],
        inside=["Sheet frame, title block, revision table", "Three views with overall sizes", "Text-overlap check", "Third-angle symbol"],
        writes=["Drawing sheets: SVG, PDF and PNG", "Making sketches for build plans"],
        sizes=["ANSI B 431.8 x 279.4 mm today", "ISO A3 420 x 297 mm to add (decision D3, R17)",
               "Title block 190 x 56 mm in either size"],
        notes=["1. Make the sheet size a setting read from the project file:",
               "   ANSI B (the default) or ISO A3 (decision D3).",
               "2. Lay out frame, zone ticks, title block and revision table from",
               "   the sheet size, so both sizes use the same code.",
               "3. Take the footer organisation and website from the identity",
               "   record (joint 4).",
               "4. Keep the text-overlap check and run it on every sheet saved.",
               "Fits: the project's model hands over named parts (joint 5). The",
               "model and its STEP and STL exports belong to the project, not",
               "to the kit.",
               "Check: render one sheet at each size; the overlap check reports",
               "nothing; the title block reads the second identity."]),
    "media": dict(
        dwg="RDK-DWG-107", title="Concept media renderer: making sketch",
        material="Software: Python, build123d, NumPy, Matplotlib; viewer script Apache-2.0; MIT",
        reads=["Numbered parts from the project's model", "Key figures from the calculation note", "Identity values from the reader"],
        inside=["Shaded renderer with no graphics card", "Hero, exploded, blueprint, cutaway", "3D model file and viewer page", "Bundled viewer script"],
        writes=["Concept images and blueprint sheet", "3D model and a viewer page that works with no network"],
        sizes=["Time: 60 s or less for 20 parts (R5); 12 to 23 s today", "Same images on every run (R8)",
               "Viewer script: about 1 MB, copied beside the model"],
        notes=["1. Carry over the renderer unchanged; it already gives the same",
               "   images on every run.",
               "2. Bundle a pinned copy of the 3D viewer script in the package and",
               "   copy it beside the 3D model file; the viewer page loads it from",
               "   there, not from the internet (RDK-DDR-003, change P4, for R9).",
               "3. Add the viewer script's license notice to the licensing file",
               "   the template writes.",
               "4. Stamp every image \"concept, not for fabrication\".",
               "Fits: parts arrive from the project's model (joint 5); the viewer",
               "page and its script sit side by side (joint 7).",
               "Check: open the viewer page with the network switched off; the",
               "model turns and zooms."]),
    "guard": dict(
        dwg="RDK-DWG-108", title="Agent guardrails: making sketch",
        material="Software: Markdown rule files and commands; MIT",
        reads=["Phase file (TRL cap)", "The standard", "The repository's review note"],
        inside=["Agent rules: cap, decision rights, one step per session", "Session commands: populate, advance, rein in, media, build plan, release",
                "Review-note template"],
        writes=["Rule files inside each repository, written by setup and refreshed by upgrade"],
        sizes=["Rules and commands: part of the 47 kB stub", "Commands today: eight",
               "Decision-wording rule: in the checker (R13)"],
        notes=["1. Keep the agent rules and the session commands as plain text",
               "   files: an agent reads them from the repository it works in,",
               "   so they must live in the repository, not only in the package",
               "   (RDK-DDR-003, change P2).",
               "2. Setup writes them into a new repository; upgrade rewrites them",
               "   and shows the difference before anything is kept.",
               "3. Take the organisation and owner names in them from the",
               "   identity record, so another team's agents get their own names.",
               "Fits: part of the stub (joint 6); the cap they quote is the cap",
               "the gate enforces.",
               "Check: after an upgrade the rule files match the new version and",
               "the difference was shown first."]),
}


def interface_layout(key):
    d = MODS[key]
    n = len(d["reads"])
    reads_bottom = 14 + n * 14 - 2
    mod_bottom = 14 + 18 + 15 * len(d["inside"])
    writes_bottom = 14 + len(d["writes"]) * 16
    sy = max(reads_bottom, mod_bottom, writes_bottom) + 10
    return sy, sy + 14 + 9 * len(d["sizes"])


def interface_png(key, path):
    """Interface view: what the module reads, the parts inside it and what it hands on."""
    d = MODS[key]
    sy, height = interface_layout(key)
    fig = plt.figure(figsize=(240 / 25.4, height / 25.4), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 240); ax.set_ylim(height, 0); ax.set_axis_off()

    def box(x, y, w, h, text, fc="#FFFFFF", ec=INK, size=8.0, weight="normal", color=INK):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.5", fc=fc, ec=ec, lw=0.8))
        import textwrap
        text = "\n".join(textwrap.wrap(text, int((w - 4) / (size * 0.19))))
        ax.text(x + 2.5, y + h / 2, text, fontsize=size, va="center", ha="left", color=color, fontweight=weight,
                linespacing=1.15)

    def head(x, text):
        ax.text(x, 7, text, fontsize=8.5, color=ACCENT, fontweight="bold")
    head(2, "READS"); head(80, "THE MODULE AND THE PARTS INSIDE IT"); head(178, "HANDS ON")
    name = [n for k, _, n, _, _ in ORDER if k == key][0]
    for i, t in enumerate(d["reads"]):
        y = 14 + i * 14
        box(2, y, 68, 12, t, size=6.9)
        ax.annotate("", xy=(80, y + 6), xytext=(70, y + 6),
                    arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=0.9, mutation_scale=8))
    mh = 18 + 15 * len(d["inside"])
    ax.add_patch(FancyBboxPatch((80, 14), 88, mh, boxstyle="round,pad=0,rounding_size=2", fc="#F0FDFA", ec=ACCENT, lw=1.3))
    ax.text(84, 22, name, fontsize=9, fontweight="bold", color=INK, va="center")
    for i, t in enumerate(d["inside"]):
        box(84, 30 + 15 * i, 80, 12, t, fc="#FFFFFF", ec=MUTED, size=6.9)
    ax.annotate("", xy=(178, 20), xytext=(168, 20),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=0.9, mutation_scale=8))
    for i, t in enumerate(d["writes"]):
        box(178, 14 + i * 16, 60, 13, t, size=6.9)
    ax.add_patch(FancyBboxPatch((2, sy), 236, height - sy - 2, boxstyle="round,pad=0,rounding_size=1.5", fc="#F9FAFB", ec=MUTED, lw=0.6))
    ax.text(6, sy + 6, "SIZES THAT MATTER", fontsize=8, color=ACCENT, fontweight="bold", va="center")
    for i, t in enumerate(d["sizes"]):
        ax.text(6, sy + 14 + 9 * i, t, fontsize=8, color=INK, va="center")
    fig.savefig(path, facecolor="white"); plt.close(fig)
    return path, height


def sheets(only=None):
    from drawing import Sheet
    outs = []
    for i, (key, no, name, _, _) in enumerate(ORDER):
        if key not in MODS or (only and key not in only):
            continue
        d = MODS[key]
        work = DWG / f"_{d['dwg']}_views"; work.mkdir(parents=True, exist_ok=True)
        png, ih = interface_png(key, work / "interface.png")
        others = [P[k] for k, *_ in ORDER if k != key]
        inset = bv.where_it_goes(P[key], others, work / "where.png")
        rev2 = key in REV2
        revs = [("P1", "Making sketch for the prototype build plan", DATE, "AC")]
        if rev2:
            revs.append(("P2", "Decisions of 2026-10-02 carried in (CI platforms, Python range, identity phrase)", DATE2, "AC"))
        s = Sheet(project="ReadyKit", title=d["title"], dwg_no=d["dwg"], rev="P2" if rev2 else "P1", author="Amish Chadha",
                  date=DATE2 if rev2 else DATE,
                  concept="BUILD PLAN SKETCH, PLAN NOT YET BUILT", scale=None, units="n/a (software)",
                  material=d["material"], revisions=revs)
        s.add_image(str(png), 16, 26, 240, ih, label="Interface view",
                    sublabel="What the module reads, the parts inside it and what it hands on; not to scale")
        s.add_image(str(inset), 276, 30, 140, 70, label="Where it goes",
                    sublabel="This module's object in colour, the rest of the kit in grey")
        s.add_notes("How to make it and how it fits", d["notes"], x=276, y=112, width=140)
        svg = s.save(DWG / d["dwg"])
        svg_text = svg.read_text().replace('text-anchor="start">1:1</text>', 'text-anchor="start">NTS</text>')
        svg.write_text(svg_text)
        import cairosvg
        cairosvg.svg2pdf(bytestring=svg_text.encode(), write_to=str(svg.with_suffix(".pdf")))
        cairosvg.svg2png(bytestring=svg_text.encode(), write_to=str(svg.with_suffix(".png")),
                         output_width=int(431.8 / 25.4 * 300), output_height=int(279.4 / 25.4 * 300))
        shutil.rmtree(work, ignore_errors=True)
        outs.append(svg)
    return outs


# ----------------------------------------------------------------- joints (interfaces)
JOINTS = [
    ("joint-01.png", "Joint 1: repository reader to the checker and the TRL gate", ["reader", "checker", "gate"],
     "The reader hands over one record; neither module opens a file itself",
     ["For each controlled document: number, title, type,", "version, status, date, author, license,",
      "revision rows, and the file it came from.", "For the project: claimed TRL, target TRL,",
      "evidence list, design state, sheet size.", "From the phase file: the TRL cap.",
      "A file that cannot be read stops the run", "with its name and line number."]),
    ("joint-02.png", "Joint 2: checker to the CI workflow", ["template", "checker"],
     "The workflow trusts only the exit code; the fault list is for the author",
     ["Exit code 0: every rule passed; the merge may go on.", "Exit code 1: at least one fault; CI blocks the merge.",
      "Each fault is one line: the file, then the reason.", "Warnings never change the exit code.",
      "The check job installs the core only (about 5 MB:", "PyYAML, Python-Markdown and Jinja2).",
      "Runs on every push and every pull request.", "Time budget: 2 s per repository (R3).",
      "CI platforms: Linux, macOS, Windows through WSL2;", "Python 3.11 and the newest release."]),
    ("joint-03.png", "Joint 3: TRL gate to the README badge and the PDF cover", ["gate", "checker", "pdf"],
     "One TRL value, written in two places by the same module",
     ["The gate passes the claimed TRL only when its", "evidence is present and it is within the cap.",
      "Badge line: the first line under the README title,", "replaced as a whole, never edited by hand.",
      "PDF cover: TRL number and name, beside the", "document control table.",
      "If the gate fails, neither is written."]),
    ("joint-04.png", "Joint 4: identity values to the three renderers", ["reader", "pdf", "drawing"],
     "Organisation, website, repository owner, author, colours and the still-open phrase come from one file",
     ["The reader fills every missing value with the", "Design Molecule default; the still-open phrase", "of the decision-wording rule defaults to", "Proposed, awaiting.",
      "The PDF renderer uses all five values;", "the sheet generator uses organisation, website,",
      "owner and colours; the media renderer uses", "organisation, owner and colours.",
      "No renderer holds an identity string of its own:", "13 written-in strings today, none after (R11)."]),
    ("joint-05.png", "Joint 5: project model to the drawing and media renderers", ["drawing", "media"],
     "The model belongs to the project; the kit only reads its parts",
     ["The project's model hands over a list of parts.", "Each part: number (as in the BOM), name, solid,",
      "colour, and the direction it comes out in.", "The sheet generator draws three views and sizes",
      "from a part's solid; the media renderer shades", "the whole list.",
      "STEP and STL files are written by the project's", "model, not by the kit."]),
    ("joint-06.png", "Joint 6: package to the stub in each repository", ["template", "guard"],
     "Code and fonts stay in the package; the repository keeps only what people and agents read",
     ["Stub, about 47 kB: version pin and identity file,", "agent rules and commands, a copy of the standard.",
      "Setup writes the stub into a new repository.", "Upgrade installs the new package, rewrites the",
      "stub and shows the difference before it is kept.", "Today each repository carries 1.20 MB of kit,",
      "83% of it fonts (R10 limit 2 MB)."]),
    ("joint-07.png", "Joint 7: viewer page to the bundled viewer script", ["media", "bought"],
     "The page loads its script from beside the 3D model, so it works offline",
     ["The media renderer writes the 3D model, the viewer", "page and a copy of the viewer script side by side.",
      "The page loads the script by a relative link,", "not from a content delivery network.",
      "The script version is pinned in the package and", "its license notice goes with it.",
      "Closes the last offline gap in R9."]),
]


def joint_picture(fname, title, keys, subtitle, lines, size=(9, 5.2), dpi=160):
    rename = {"bought": "Bought viewer script (in the tray)"} if "media" in keys else {}
    parts = [Part(rename.get(k, P[k].name), P[k].shape, P[k].color, P[k].bom, (0, 0, 0), 1.0) for k in keys]
    W, H = int(size[0] * dpi * 0.56), int(size[1] * dpi * bv.PIC_HEIGHT)
    img, proj, verts = bv._raster([(p, p.color, 1.0, (0, 0, 0)) for p in parts], 30, -58, W, H)
    fig, ax0 = bv._frame(size, dpi, title, subtitle)
    ax0.remove()
    ax = fig.add_axes([0, bv.PIC_BOTTOM, 0.56, bv.PIC_HEIGHT]); ax.set_axis_off()
    ax.imshow(img, interpolation="bilinear")
    for p, v in zip(parts, verts):
        x, y = proj(bv._anchor(v))
        ax.annotate(p.name, xy=(x, y), xytext=(min(max(x, 0.16 * W), 0.84 * W), max(y - 0.10 * H, 0.05 * H)), fontsize=7.5, color=INK, ha="center",
                    arrowprops=dict(arrowstyle="-", color=bv.EDGE, lw=0.6),
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=bv.EDGE, lw=0.5))
    bx = fig.add_axes([0.58, 0.12, 0.40, 0.72]); bx.set_axis_off(); bx.set_xlim(0, 1); bx.set_ylim(1, 0)
    bx.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.02", fc="#F0FDFA", ec=ACCENT, lw=1.0,
                                transform=bx.transAxes))
    bx.text(0.04, 0.07, "WHAT CROSSES THE JOINT", fontsize=7.5, color=ACCENT, fontweight="bold", va="center")
    for i, t in enumerate(lines):
        bx.text(0.04, 0.17 + i * 0.095, t, fontsize=7.4, color=INK, va="center")
    out = OUT / fname; out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


def joints():
    return [joint_picture(*j) for j in JOINTS]


# ----------------------------------------------------------------- assembly steps
STEPS = [
    ("template", "Step 1: template repository and CI workflow", "The folder every other module goes into; CI checks it from the first commit"),
    ("bought", "Step 2: bought open-source parts", "Core libraries first; the PDF, drawings, media and release extras each go in at the step that needs them"),
    ("reader", "Step 3: repository reader", "Hold point: its records match the present scripts on 38 repositories"),
    ("checker", "Step 4: document control checker", "Hold point: every seeded fault caught; no false failures"),
    ("gate", "Step 5: TRL gate and badge", "The badge line and the PDF cover take the gate's TRL"),
    ("pdf", "Step 6: PDF renderer and house style", "Renders only after a passing check; identity from the reader"),
    ("drawing", "Step 7: drawing sheet generator", "ANSI B and ISO A3 from the same code"),
    ("media", "Step 8: concept media renderer", "Viewer page and its script side by side; works offline"),
    ("guard", "Step 9: agent guardrails", "Written into the repository by setup; refreshed by upgrade"),
]


def steps():
    outs, done = [], []
    fit = {k: f for k, _, _, _, f in ORDER}
    for i, (key, title, sub) in enumerate(STEPS, 1):
        p = P[key]
        new = Part(p.name, p.shape, p.color, p.bom, fit[key], 1.0)
        outs.append(bv.step(done, [new], OUT / f"step-{i:02d}.png", title, sub, label_done=False))
        done = done + [P[key]]
    lap = Part("Fresh laptop or CI runner", laptop(), "#0F766E", None, (0, 0, 0), 1.0)
    outs.append(bv.step(done, [lap], OUT / "step-10.png", "Step 10: first run on a fresh machine",
                        "Install the core, set up a new repository from the template, run the check; then add the extras",
                        label_done=False))
    return outs


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "joints", "steps"]
    OUT.mkdir(parents=True, exist_ok=True)
    if "overview" in what:
        print(overview())
    if "sheets" in what:
        for s in sheets(REV2):
            print(s)
    if "joints" in what:
        for j in joints():
            print(j)
    if "steps" in what:
        for s in steps():
            print(s)

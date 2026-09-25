"""ReadyKit concept media (TRL 2).

ReadyKit is a software project. This is an ILLUSTRATIVE massing of the kit's outputs,
not a product to fabricate: each numbered object stands for one kit module and the
artifact it produces. Numbers match bom/bom.csv.

Run from the repo root:  python cad/src/concept_media.py

Coordinates in mm, desk surface at Z = 0, X to the right, Y away from the viewer.
Paper thickness is exaggerated so the sheets read in the renders.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Polyline, make_face, extrude, Plane
from concept import Part, render_all

LETTER = (216.0, 279.0)      # US Letter page, the kit's document format
ANSI_B = (431.8, 279.4)      # ANSI B landscape, the kit's drawing sheet
SHEET_T = 2.5                # exaggerated paper thickness for visibility

# 7  Template repository: a folder the document set sits in
folder = Pos(125, 160, 3) * Box(240, 310, 6)

# 1  Controlled document set (PRB, PRC, REQ): three pages, slightly fanned
stack = None
for i, (dx, dy, rz) in enumerate([(0, 0, 0), (6, -4, -2.5), (12, -8, -5)]):
    page = Pos(125 + dx, 160 + dy, 6 + SHEET_T / 2 + i * SHEET_T) * Rot(0, 0, rz) * Box(*LETTER, SHEET_T)
    stack = page if stack is None else stack + page
top_z = 6 + 3 * SHEET_T      # top face of the stack

# 2  PDF house style: teal header band and status band on the top page
band = (Pos(137, 160 - 8, top_z + 0.5) * Rot(0, 0, -5)
        * (Pos(0, LETTER[1] / 2 - 22, 0) * Box(LETTER[0] - 20, 26, 1.0)
           + Pos(0, -LETTER[1] / 2 + 14, 0) * Box(LETTER[0] - 20, 8, 1.0)))

# 3  Drawing sheet on a board (drawing sheet generator)
board = Pos(560, 170, 6) * Box(ANSI_B[0] + 30, ANSI_B[1] + 30, 12)
sheet = Pos(560, 170, 12 + SHEET_T / 2) * Box(*ANSI_B, SHEET_T)
title_block = Pos(560 + ANSI_B[0] / 2 - 70, 170 - ANSI_B[1] / 2 + 25, 12 + SHEET_T + 0.5) * Box(120, 36, 1.0)
drawing = board + sheet + title_block

# 4  Small printed part: the massing model that concept renders come from
bracket = Pos(470, -90, 4) * Box(70, 45, 8) + Pos(438, -90, 30) * Box(6, 45, 52)
bracket = bracket - Pos(485, -90, 0) * Cylinder(6, 30)

# 5  TRL badge: a round token printed with the readiness level
badge = Pos(330, -95, 3) * Cylinder(32, 6)
badge_mark = Pos(330, -95, 6.5) * Box(34, 10, 1.0)

# 6  Agent guardrails: a tent card standing on the desk (CLAUDE.md, PHASE.yaml)
tri = Polyline((-50, 0), (50, 0), (0, 85), (-50, 0))
tent = Plane.XZ * extrude(make_face(tri), 120)      # profile in XZ, depth along -Y
tent = tent - Plane.XZ * extrude(make_face(Polyline((-44, 0), (44, 0), (0, 75), (-44, 0))), 120)
tent = Pos(20, -150, 0) * tent

parts = [
    Part("Controlled document set (PRB, PRC, REQ)", stack, "#F3F4F6", 1, (0, 0, 120)),
    Part("PDF house style: header and status bands", band, "#0F766E", 2, (0, 0, 230)),
    Part("Drawing sheet on board (ANSI B)", drawing, "#1D4F8A", 3, (120, 60, 60)),
    Part("Printed massing part (concept renders)", bracket, "#C2410C", 4, (60, -80, 110)),
    Part("TRL gate badge", badge + badge_mark, "#D4A017", 5, (-40, -260, 40)),
    Part("Agent guardrail card (CLAUDE.md, phase cap)", tent, "#6B7280", 6, (-120, -80, 40)),
    Part("Template repository folder", folder, "#9CA3AF", 7, (0, 0, 0)),
]

# Context for scale: a 14 in class laptop (about 320 x 225 mm) to the left of the desk items
lap_base = Pos(-260, 120, 9) * Box(320, 225, 18)
lap_screen = Pos(-260, 232, 18) * Rot(-15, 0, 0) * Pos(0, 0, 105) * Box(320, 8, 210)
context = [Part("Laptop, 14 in class", lap_base + lap_screen, "#C8CDD3")]

outs = render_all(
    parts, project="ReadyKit", title="Illustrative massing, software project", dwg_no="RDK-DWG-010",
    key_figures=["ILLUSTRATIVE, SOFTWARE PROJECT",
                 "Inputs: Markdown with YAML front matter, build123d Python",
                 "Check: about 0.1 s per repo (measured, 3 docs)",
                 "PDF render: about 1.6 s for 3 docs (measured)",
                 "Concept media: about 7 s, 6-part model (measured)",
                 "Kit folder about 1.1 MB; hardware budget $0"],
    cut=False, scale_figure=False, context=context,
)


def pipeline_flow(out):
    """Two inputs merge into the check and TRL gate, then branch into four outputs."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
    INK, ACCENT, FAIL = "#111827", "#0F766E", "#C2410C"
    fig, ax = plt.subplots(figsize=(13, 5.2), dpi=160)
    ax.set_xlim(0, 13); ax.set_ylim(-0.4, 5.4); ax.set_axis_off()

    def box(x, y, w, h, name, sub, fc="#F0FDFA", ec=ACCENT):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.4))
        ax.text(x + w / 2, y + h * 0.64, name, ha="center", va="center", fontsize=9, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=8, color=ec)

    def arrow(a, b, color=ACCENT):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=2, color=color, alpha=0.7))

    box(0.2, 3.1, 2.6, 1.0, "Markdown + YAML", "docs/*.md, README, BOM")
    box(0.2, 1.1, 2.6, 1.0, "build123d Python", "cad/src/*.py")
    box(3.6, 2.1, 2.6, 1.0, "Check and TRL gate", "about 0.1 s (measured)")
    box(7.0, 2.1, 2.2, 1.0, "Render", "about 7 s (measured)")
    outs_ = [("Checked PDFs", "docs/pdf/, house style"), ("Drawing sheets", "blueprint, ANSI B"),
             ("Renders and 3D", "hero, exploded, GLB"), ("TRL badge", "README, PDF cover")]
    for k, (n, t) in enumerate(outs_):
        y = 3.9 - k * 1.25
        box(10.0, y, 2.8, 0.95, n, t)
        arrow((9.2, 2.6), (10.0, y + 0.47))
    arrow((2.8, 3.6), (3.6, 2.8)); arrow((2.8, 1.6), (3.6, 2.4)); arrow((6.2, 2.6), (7.0, 2.6))
    box(3.6, 0.0, 2.6, 0.9, "Fail: stop", "CI blocks merge", fc="#FFF7ED", ec=FAIL)
    arrow((4.9, 2.1), (4.9, 0.9), FAIL)
    fig.text(0.01, 0.97, "ReadyKit: documentation pipeline", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.92, "CONCEPT, NOT FOR FABRICATION. ILLUSTRATIVE, SOFTWARE PROJECT. "
             "Times measured on one sample repo, 2-core Linux container; other machines will differ.",
             fontsize=7, color="#B45309", va="top")
    fig.savefig(out, facecolor="white", bbox_inches="tight"); plt.close(fig)
    return out


pipeline_flow(Path("media") / "flow.png")


def stamp(png, text="ILLUSTRATIVE, SOFTWARE PROJECT"):
    """Add the software-project label under the concept label on a kit render."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.open(png).convert("RGB")
    font = ImageFont.truetype(str(Path(__file__).resolve().parents[2] / ".kit/fonts/IBMPlexSans-SemiBold.ttf"),
                              max(11, im.width // 95))
    ImageDraw.Draw(im).text((int(im.width * 0.235), int(im.height * 0.066)), text, fill="#B45309", font=font)
    im.save(png)


for name in ("hero.png", "exploded.png"):
    stamp(Path("media") / name)

import shutil
for tmp in Path("media").glob("_views*"):
    shutil.rmtree(tmp, ignore_errors=True)

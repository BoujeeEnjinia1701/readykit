"""ReadyKit concept media (TRL 3).

ReadyKit is a software project. This is an ILLUSTRATIVE massing of the kit's outputs,
not a product to fabricate: each numbered object stands for one kit module and the
artifact it produces. Numbers match bom/bom.csv.

Run from the repo root:  python cad/src/concept_media.py

The massing geometry and its parameters live in cad/src/model.py.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from dataclasses import dataclass
import drawing
from concept import Part, render_all
from model import modules, laptop


@dataclass
class _Sheet(drawing.Sheet):
    """Kit sheet with this repository's content license (RDK-DDR-002, D5) in the title block."""
    license: str = "CC-BY-SA-4.0"


drawing.Sheet = _Sheet  # render_all imports Sheet from drawing at call time

# Geometry comes from the parametric model (cad/src/model.py), so the media follow its parameters.
parts = [Part(name, shape, color, no, explode) for no, name, shape, color, explode in modules()]
context = [Part("Laptop, 14 in class", laptop(), "#C8CDD3")]

outs = render_all(
    parts, project="ReadyKit", title="Illustrative massing, software project", dwg_no="RDK-DWG-010", rev="P2",
    key_figures=["ILLUSTRATIVE, SOFTWARE PROJECT",
                 "Inputs: Markdown with YAML front matter, build123d Python",
                 "Check: about 0.1 s per repo (measured, RDK-CAL-001)",
                 "PDF render: 2 to 3 s for 3 docs (measured)",
                 "Concept media: 5 to 6 s here, 12 to 23 s for 20 parts",
                 "Coverage 12 of 20 rules (target 18); budget $0"],
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
    box(3.6, 2.1, 2.6, 1.0, "Check and TRL gate", "about 0.1 s; 12 of 20 rules")
    box(7.0, 2.1, 2.2, 1.0, "Render", "PDFs 2 to 3 s; media 5 s")
    outs_ = [("Checked PDFs", "docs/pdf/, house style"), ("Drawing sheets", "blueprint, ANSI B"),
             ("Renders and 3D", "hero, exploded, GLB"), ("TRL badge", "PDF cover; README by hand")]
    for k, (n, t) in enumerate(outs_):
        y = 3.9 - k * 1.25
        box(10.0, y, 2.8, 0.95, n, t)
        arrow((9.2, 2.6), (10.0, y + 0.47))
    arrow((2.8, 3.6), (3.6, 2.8)); arrow((2.8, 1.6), (3.6, 2.4)); arrow((6.2, 2.6), (7.0, 2.6))
    box(3.6, 0.0, 2.6, 0.9, "Fail: stop", "CI blocks merge", fc="#FFF7ED", ec=FAIL)
    arrow((4.9, 2.1), (4.9, 0.9), FAIL)
    fig.text(0.01, 0.97, "ReadyKit: documentation pipeline", fontsize=10, fontweight="bold", color=INK, va="top")
    fig.text(0.01, 0.92, "CONCEPT, NOT FOR FABRICATION. ILLUSTRATIVE, SOFTWARE PROJECT. "
             "Times measured in RDK-CAL-001 on a 2-core Linux container; other machines will differ.",
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

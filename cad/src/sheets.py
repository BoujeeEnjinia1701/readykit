"""ReadyKit general arrangement sheet RDK-DWG-001, Rev P2 (TRL 3).

ReadyKit is software, so its general arrangement is the layout of the documentation pipeline:
inputs, the seven numbered modules (as in bom/bom.csv), outputs and the CI gate, with the
illustrative massing from cad/src/model.py as the isometric view. Measured times are read from
docs/04-calcs/results.csv (written by docs/04-calcs/sizing.py), so the sheet follows RDK-CAL-001.

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/RDK-DWG-001.svg, .pdf and .png with .kit/drawing.py.
The concept blueprint in media/ is RDK-DWG-010.
"""
import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _t, INK, MUTED, ACCENT  # noqa: E402
from model import PARAMS, assembly, derived  # noqa: E402

DATE = "2026-09-25"
FAIL = "#C2410C"


class DiagramSheet(Sheet):
    """A pipeline diagram is not drawn to scale; print NTS in the title block scale cell."""
    def svg(self):
        return super().svg().replace('font-weight="500" fill="#111827" text-anchor="start">1:1</text>',
                                     'font-weight="500" fill="#111827" text-anchor="start">NTS</text>')


def results():
    f = ROOT / "docs/04-calcs/results.csv"
    return {r["tag"]: r["value"] for r in csv.DictReader(f.open())} if f.exists() else {}


def safe_iso(part, workdir):
    """Isometric view of the massing, edge by edge so a degenerate projected edge is skipped."""
    from build123d import ExportSVG, Unit
    workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    visible, _ = part.project_to_viewport((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1), (c.X, c.Y, c.Z))
    ex = ExportSVG(unit=Unit.MM, line_weight=0.35)
    ex.add_layer("Visible", line_color=0x111827)
    for e in visible:
        try:
            ex.add_shape(e, layer="Visible")
        except (AssertionError, ValueError, ZeroDivisionError):
            pass
    p = workdir / "iso.svg"
    ex.write(str(p))
    return p


def box(x, y, w, h, title, sub=(), no=None, fill="#F0FDFA", stroke=ACCENT, dash=False):
    g = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1.5" fill="{fill}" stroke="{stroke}" '
         f'stroke-width="0.45"{" stroke-dasharray=" + chr(34) + "2 1" + chr(34) if dash else ""}/>']
    tx = x + 3
    if no is not None:
        g += [f'<circle cx="{x + 4.2:.1f}" cy="{y + 4.4:.1f}" r="2.5" fill="{ACCENT}"/>',
              _t(x + 4.2, y + 5.3, str(no), 2.5, 700, "#FFFFFF", "middle")]
        tx = x + 8.5
    g.append(_t(tx, y + 5.4, title, 2.6, 600, INK))
    for i, s in enumerate(sub):
        g.append(_t(x + 3, y + 9.6 + 3.6 * i, s, 2.05, 400, MUTED, mono=s.startswith(("docs/", "cad/", "media/", ".kit", "bom/", "project", ".claude", ".github", "CLAUDE"))))
    return g


def arrow(pts, color=ACCENT, w=0.4):
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    L, H = 2.2, 0.9
    hx = [x2 - L * math.cos(a) + H * math.sin(a), x2 - L * math.cos(a) - H * math.sin(a)]
    hy = [y2 - L * math.sin(a) - H * math.cos(a), y2 - L * math.sin(a) + H * math.cos(a)]
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts[:-1]) + f" L{x2 - L * 0.8 * math.cos(a):.2f} {y2 - L * 0.8 * math.sin(a):.2f}"
    return [f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{w}"/>',
            f'<path d="M{x2:.2f} {y2:.2f} L{hx[0]:.2f} {hy[0]:.2f} L{hx[1]:.2f} {hy[1]:.2f} Z" fill="{color}"/>']


def main():
    R = results()
    t_check = R.get("B1", "0.10"); t_pdf = R.get("C1", "3.1"); t_media = R.get("D1", "5.3"); t_20 = R.get("D2", "23")
    L = []
    # column headers
    for x, label in ((18, "INPUTS (AUTHORED)"), (84, "CHECK AND GATE"), (152, "RENDER"), (220, "OUTPUTS")):
        L.append(_t(x, 30, label, 2.3, 600, ACCENT))
    # inputs
    ins = [("Controlled documents", ["docs/*.md", "Markdown + YAML front matter"]),
           ("Project card and TRL claim", ["project.yaml", "trl, trl_target, trl_evidence"]),
           ("Portfolio phase", [".kit/PHASE.yaml", "TRL cap 3 (set by the owner)"]),
           ("Geometry source", ["cad/src/*.py", "build123d Python"]),
           ("Bill of materials", ["bom/bom.csv", "numbered as the exploded view"])]
    iy = [34, 56, 78, 104, 126]
    for (t, s), y in zip(ins, iy):
        L += box(18, y, 56, 18, t, s, fill="#FFFFFF", stroke=INK)
    # check and gate
    L += box(84, 34, 58, 28, "Document control checker", ["render.py --check", f"{R.get('E1', 12)} of 20 rules caught (CAL E1)",
                                                             f"about {float(t_check):.1f} s per repository"], no=1)
    L += box(84, 70, 58, 26, "TRL gate and badge", ["render.py trl_check, phase_check", "evidence for TRL 1 to 6",
                                                      "cap from PHASE.yaml"], no=5)
    L += box(84, 150, 58, 16, "Fail: exit code 1", ["CI blocks the merge; author fixes"], fill="#FFF7ED", stroke=FAIL)
    # render
    L += box(152, 34, 58, 24, "PDF renderer, house style", ["render.py (Markdown, Jinja2,", "WeasyPrint)",
                                                            f"about {float(t_pdf):.1f} s for 3 documents"], no=2)
    L += box(152, 66, 58, 24, "Drawing sheet generator", ["drawing.py, called by", "cad/src/sheets.py", "ANSI B; ISO A3 decided (D3)"], no=3)
    L += box(152, 98, 58, 28, "Concept media renderer", ["concept.py render_all, called by", "cad/src/concept_media.py",
                                                         f"{float(t_media):.1f} s for 7 parts;", f"{float(t_20):.0f} s for 20 parts"], no=4)
    # outputs
    outs = [(34, "Controlled PDFs", ["docs/pdf/<ID>_v<ver>.pdf"]), (66, "Drawing sheets", ["cad/drawings/*-DWG-*", ".svg, .pdf, .png"]),
            (98, "Concept media", ["media/hero.png, exploded,", "blueprint, model.glb"]), (130, "Model exports", ["cad/step, cad/stl", "(project model.py)"]),
            (150, "TRL on PDF cover", ["README badge by hand (gap)"])]
    for y, t, s in outs:
        L += box(220, y, 46, 14 if len(s) == 1 else 17, t, s, fill="#FFFFFF", stroke=INK)
    # arrows: inputs to checker and gate (the gate reads project.yaml, PHASE.yaml, model.py, STEP and the BOM)
    L += arrow([(74, 43), (84, 43)])
    L += arrow([(74, 65), (76, 65), (76, 76), (84, 76)])
    L += arrow([(74, 87), (78, 87), (78, 82), (84, 82)])
    L += arrow([(74, 110), (80, 110), (80, 88), (84, 88)], color=MUTED)
    L += arrow([(74, 135), (82, 135), (82, 94), (84, 94)], color=MUTED)
    L += arrow([(113, 62), (113, 70)])
    # gate to render, fail path
    L += arrow([(142, 83), (147, 83), (147, 46), (152, 46)])
    L += arrow([(147, 78), (152, 78)])
    L += arrow([(147, 83), (147, 112), (152, 112)])
    L += arrow([(113, 96), (113, 150)], color=FAIL)
    L.append(_t(115, 140, "any error", 2.0, 400, FAIL))
    L += arrow([(74, 118), (152, 118)], color=MUTED)
    # render to outputs
    L += arrow([(210, 46), (215, 46), (215, 41), (220, 41)])
    L += arrow([(210, 78), (215, 78), (215, 74), (220, 74)])
    L += arrow([(210, 112), (215, 112), (215, 106), (220, 106)])
    L += arrow([(142, 92), (144, 92), (144, 146), (216, 146), (216, 157), (220, 157)])
    L += arrow([(74, 121), (77, 121), (77, 172), (212, 172), (212, 138), (220, 138)], color=MUTED)
    L.append(_t(130, 170.5, "project model.py exports STEP and STL (not a kit module)", 2.0, 400, MUTED, "middle"))
    # guardrails and template/CI band
    L += box(18, 178, 110, 24, "Agent guardrails", ["CLAUDE.md: TRL cap, decision rights, one step per session,",
                                                   "review note; .claude/commands/: populate, advance-trl3,",
                                                   "rein-in, refresh-media. Decision wording not yet checked (R13)."], no=6)
    L += box(136, 178, 130, 24, "Template repository and CI workflow", [
        ".github/workflows/docs.yml: check on every push and pull request;",
        "render and publish PDFs on release tags <ID>/v<ver> and <DWG>/rev<X>.",
        "Distribution decided: pip package plus template (D1); build on hold."], no=7)
    L.append(f'<rect x="14" y="24" width="256" height="182" fill="none" stroke="{MUTED}" stroke-width="0.3" stroke-dasharray="3 1.5"/>')
    L.append(_t(16, 209.5, "Dashed boundary: one project repository (item 7). Modules 1 to 5 live in its .kit/ folder today (vendored, kit 1.3.1).",
                2.1, 400, MUTED))

    s = DiagramSheet(project="ReadyKit", title="General arrangement: documentation pipeline", dwg_no="RDK-DWG-001", rev="P3", license="CERN-OHL-S-2.0",
                     author="Amish Chadha", date="2026-09-26", scale=None, units="mm (iso view)", theme="technical",
                     material="Software; nothing to fabricate. Massing is illustrative. PRELIMINARY, NOT FOR FABRICATION",
                     revisions=[("P1", "Preliminary GA for TRL 3 (pipeline layout, cad/src/model.py)", DATE, "AC"),
                               ("P2", "Recommendations accepted (DDR-002): D5 content license; D1, D3 decided", DATE, "AC"),
                               ("P3", "D5 reversed (DDR-002): back to CERN-OHL-S-2.0", "2026-09-26", "AC")])
    s._layers += L
    work = ROOT / "cad" / "drawings" / "_views"
    iso = safe_iso(assembly(), work)
    D = derived()
    s.add_svg(iso, 276, 30, 140, 72, label="Isometric view, illustrative massing",
              sublabel="Not to scale; numbers match bom/bom.csv (see media/exploded.png)")
    s.add_notes("Interfaces and key figures (RDK-CAL-001)", [
        "Inputs: Markdown with YAML front matter; build123d Python; project.yaml",
        f"Check: {float(t_check):.2f} s per repository; about {R.get('B3', '0.7')} ms per extra document",
        f"PDF: about {float(t_pdf):.1f} s for 3 documents; text reproducible",
        f"Media: {float(t_media):.1f} s (7 parts), {float(t_20):.0f} s (20 parts); no GPU",
        f"Kit folder {float(R.get('A1', 1.05)):.2f} MB; dependencies 1.1 GB, install under 1 min",
        f"Coverage {R.get('E1', 12)} of 20 rules; target 18 (R6 not met)",
        "Exit code 0 pass, 1 fail; CI blocks the merge on 1",
        "Times: last sizing.py run; ranges over runs in RDK-CAL-001",
        f"Sheet {PARAMS['sheet']} {D['sheet_w']} x {D['sheet_h']} mm; ISO A3 420 x 297 decided (D3)",
        "Page US Letter 216 x 279 mm, 20 mm margins",
        "Cost $0; budget_usd $0",
    ], x=276, y=118, width=140)
    out = s.save(ROOT / "cad" / "drawings" / "RDK-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    for f in (ROOT / "cad" / "drawings").glob("_views*"):
        shutil.rmtree(f, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png")


if __name__ == "__main__":
    main()

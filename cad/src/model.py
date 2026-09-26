"""ReadyKit parametric massing model (build123d), TRL 3.

ReadyKit is a software project. This model is an ILLUSTRATIVE massing of the kit's outputs,
not a product to fabricate: each numbered object stands for one kit module and the artifact
it produces. Numbers match bom/bom.csv and media/exploded.png. The geometry is the source for
the concept media (cad/src/concept_media.py) and for the STEP and STL exports that the TRL 3
evidence rule asks for (RDK-DDR-001, D7).

Run from the repo root:  python cad/src/model.py
Exports cad/step/readykit-massing.step and cad/stl/readykit-massing.stl.

Coordinates in mm, desk surface at Z = 0, X to the right, Y away from the viewer.
Paper thickness is exaggerated so the sheets read in the renders.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
SHEET_SIZES = {                       # sheet sizes the drawing generator supports or will support
    "ANSI B": (431.8, 279.4),         # current kit sheet (drawing.py)
    "ISO A3": (420.0, 297.0),         # decided (RDK-DDR-002, D3); not yet in the kit
}
PARAMS = {
    "page": (216.0, 279.0),           # US Letter, the kit's document page (216 x 279 mm, 8.5 x 11 in)
    "sheet": "ANSI B",                # drawing sheet shown on the board; "ISO A3" shows the proposed size
    "sheet_t": 2.5,                   # exaggerated paper thickness for visibility
    "pages": 3,                       # controlled documents in the stack (PRB, PRC, REQ)
    "fan": (6.0, -4.0, -2.5),         # per-page offset dx, dy (mm) and rotation (deg) in the stack
    "folder": (240.0, 310.0, 6.0),    # template repository folder
    "stack_at": (125.0, 160.0),       # center of the document stack and folder
    "board_margin": 15.0,             # drawing board border around the sheet
    "board_t": 12.0,
    "board_at": (560.0, 170.0),
    "title_block": (120.0, 36.0),     # drawing title block patch, bottom right of the sheet
    "bracket_at": (470.0, -90.0),     # printed massing part (source of the concept renders)
    "badge_r": 32.0,                  # TRL badge radius
    "badge_at": (330.0, -95.0),
    "tent": (100.0, 85.0, 120.0),     # guardrail tent card: base width, height, depth
    "tent_at": (20.0, -150.0),
    "laptop": (320.0, 225.0, 18.0),   # 14 in class laptop for scale (context only, not exported)
}


def derived(p=PARAMS):
    """Dimensions that follow from the parameters (used by the drawing and the calc note)."""
    sw, sh = SHEET_SIZES[p["sheet"]]
    fx, fy, ft = p["folder"]
    bx, by = p["board_at"]
    return {
        "sheet_w": sw, "sheet_h": sh,
        "board_w": sw + 2 * p["board_margin"], "board_h": sh + 2 * p["board_margin"],
        "stack_top": ft + p["pages"] * p["sheet_t"],
        "extent_x": (p["tent_at"][0] - p["tent"][0] / 2, bx + sw / 2 + p["board_margin"]),
        "extent_y": (p["tent_at"][1] - p["tent"][2], max(p["stack_at"][1] + fy / 2, by + sh / 2 + p["board_margin"])),
    }


def modules(p=PARAMS):
    """The seven numbered massing objects: [(bom_no, name, shape, color, explode_offset)]."""
    from build123d import Box, Cylinder, Pos, Rot, Polyline, make_face, extrude, Plane
    d = derived(p)
    page_w, page_h = p["page"]
    t = p["sheet_t"]
    sx, sy = p["stack_at"]
    fx, fy, ft = p["folder"]
    dx, dy, rz = p["fan"]

    # 7  Template repository: a folder the document set sits in
    folder = Pos(sx, sy, ft / 2) * Box(fx, fy, ft)

    # 1  Controlled document set: pages slightly fanned
    stack = None
    for i in range(p["pages"]):
        page = Pos(sx + i * dx, sy + i * dy, ft + t / 2 + i * t) * Rot(0, 0, i * rz) * Box(page_w, page_h, t)
        stack = page if stack is None else stack + page
    top_z = d["stack_top"]
    k = p["pages"] - 1

    # 2  PDF house style: teal header band and status band on the top page
    band = (Pos(sx + k * dx, sy + k * dy, top_z + 0.5) * Rot(0, 0, k * rz)
            * (Pos(0, page_h / 2 - 22, 0) * Box(page_w - 20, 26, 1.0)
               + Pos(0, -page_h / 2 + 14, 0) * Box(page_w - 20, 8, 1.0)))

    # 3  Drawing sheet on a board (drawing sheet generator)
    bx, by = p["board_at"]
    bt = p["board_t"]
    sw, sh = d["sheet_w"], d["sheet_h"]
    tw, th = p["title_block"]
    drawing = (Pos(bx, by, bt / 2) * Box(d["board_w"], d["board_h"], bt)
               + Pos(bx, by, bt + t / 2) * Box(sw, sh, t)
               + Pos(bx + sw / 2 - tw / 2 - 10, by - sh / 2 + th / 2 + 7, bt + t + 0.5) * Box(tw, th, 1.0))

    # 4  Small printed part: the massing model that concept renders come from
    qx, qy = p["bracket_at"]
    bracket = Pos(qx, qy, 4) * Box(70, 45, 8) + Pos(qx - 32, qy, 30) * Box(6, 45, 52)
    bracket = bracket - Pos(qx + 15, qy, 0) * Cylinder(6, 30)

    # 5  TRL badge: a round token printed with the readiness level
    gx, gy = p["badge_at"]
    badge = Pos(gx, gy, 3) * Cylinder(p["badge_r"], 6) + Pos(gx, gy, 6.5) * Box(34, 10, 1.0)

    # 6  Agent guardrails: a tent card standing on the desk (CLAUDE.md, PHASE.yaml)
    w, h, dep = p["tent"]
    outer = Plane.XZ * extrude(make_face(Polyline((-w / 2, 0), (w / 2, 0), (0, h), (-w / 2, 0))), dep)
    inner = Plane.XZ * extrude(make_face(Polyline((-w / 2 + 6, 0), (w / 2 - 6, 0), (0, h - 10), (-w / 2 + 6, 0))), dep)
    tent = Pos(*p["tent_at"], 0) * (outer - inner)

    return [
        (1, "Controlled document set (PRB, PRC, REQ)", stack, "#F3F4F6", (0, 0, 120)),
        (2, "PDF house style: header and status bands", band, "#0F766E", (0, 0, 230)),
        (3, f"Drawing sheet on board ({p['sheet']})", drawing, "#1D4F8A", (120, 60, 60)),
        (4, "Printed massing part (concept renders)", bracket, "#C2410C", (60, -80, 110)),
        (5, "TRL gate badge", badge, "#D4A017", (-40, -260, 40)),
        (6, "Agent guardrail card (CLAUDE.md, phase cap)", tent, "#6B7280", (-120, -80, 40)),
        (7, "Template repository folder", folder, "#9CA3AF", (0, 0, 0)),
    ]


def laptop(p=PARAMS):
    """Scale context for the hero render: a 14 in class laptop to the left of the desk items."""
    from build123d import Box, Pos, Rot
    lw, ld, lt = p["laptop"]
    base = Pos(-260, 120, lt / 2) * Box(lw, ld, lt)
    screen = Pos(-260, 120 + ld / 2, lt) * Rot(-15, 0, 0) * Pos(0, 0, 105) * Box(lw, 8, 210)
    return base + screen


def assembly(p=PARAMS):
    from build123d import Compound
    kids = []
    for no, name, shape, _, _ in modules(p):
        shape.label = f"{no} {name}"
        kids.append(shape)
    return Compound(children=kids, label="ReadyKit illustrative massing")


if __name__ == "__main__":
    from build123d import export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    asm = assembly()
    export_step(asm, str(out / "step" / "readykit-massing.step"))
    export_stl(asm, str(out / "stl" / "readykit-massing.stl"))
    bb = asm.bounding_box()
    d = derived()
    print(f"sheet {PARAMS['sheet']} {d['sheet_w']} x {d['sheet_h']} mm; board {d['board_w']:.1f} x {d['board_h']:.1f} mm")
    print(f"massing extent {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; {len(modules())} modules")
    print("wrote cad/step/readykit-massing.step and cad/stl/readykit-massing.stl")

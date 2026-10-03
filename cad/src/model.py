"""ReadyKit parametric massing model (build123d), TRL 3, constructable design (RDK-DDR-003).

ReadyKit is a software project. This model is an ILLUSTRATIVE massing of the kit's outputs,
not a product to fabricate: each numbered object stands for one kit module and the artifact
it produces. Numbers match bom/bom.csv and media/exploded.png. The geometry is the source for
the concept media (cad/src/concept_media.py) and for the STEP and STL exports that the TRL 3
evidence rule asks for (RDK-DDR-001, D7).

Run from the repo root:  python cad/src/model.py          (exports STEP and STL)
                         python cad/src/model.py --check  (illustration consistency checks)
Exports cad/step/readykit-massing.step and cad/stl/readykit-massing.stl.

RDK-DDR-003 (design for construction, 2026-10-01) added two objects: the repository reader
(BOM 12, a card index box, because every module now reads the repository through it) and the
tray of bought open-source parts (BOM 8, 10, 11 and 13). The fanned document stack is now
centred on the folder so no page hangs over its edge.

RDK-DDR-003 follow-ups carried out on 2026-10-02 (decisions of the same day): the identity card in the
reader carries six field tabs, the sixth being the "still open" phrase of the decision-wording rule
(decision 4); the tray has five bays, one for the core libraries and one for each extra: PDF, drawings,
media and release (decisions 5 and 6).

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
    "fan": (6.0, -4.0, -2.5),         # per-page offset dx, dy (mm) and rotation (deg) in the stack, centred on the folder
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
    "reader": (60.0, 90.0, 40.0),     # repository reader: card index box, outside width, depth, height
    "reader_wall": 3.0,
    "reader_cards": 5,                # one card per thing it reads: project file, identity, phase, front matter, BOM
    "reader_at": (287.0, 80.0),
    "identity_fields": ["organisation", "website", "repository owner", "author", "colours", "still-open phrase"],
    "tab": (7.0, 1.0, 5.0),           # one tab per identity field, standing on the identity card: width, thickness, height
    "tab_pitch": 8.5,
    "tray": (110.0, 80.0, 20.0),      # tray of bought open-source parts: width, depth, height
    "tray_at": (185.0, -100.0),
    "tray_bays": ["core", "pdf", "drawings", "media", "release"],   # core libraries, then one bay per extra
    "bay": (18.0, 60.0),              # bay width and depth (heights vary with the contents)
    "bay_pitch": 20.5,
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
    """The numbered massing objects: [(bom_no, name, shape, color, explode_offset)]."""
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
    c0 = (p["pages"] - 1) / 2                      # fan about the middle page so the stack sits on the folder
    for i in range(p["pages"]):
        page = Pos(sx + (i - c0) * dx, sy + (i - c0) * dy, ft + t / 2 + i * t) * Rot(0, 0, (i - c0) * rz) * Box(page_w, page_h, t)
        stack = page if stack is None else stack + page
    top_z = d["stack_top"]
    k = p["pages"] - 1

    # 2  PDF house style: teal header band and status band on the top page
    band = (Pos(sx + (k - c0) * dx, sy + (k - c0) * dy, top_z + 0.5) * Rot(0, 0, (k - c0) * rz)
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

    # 12  Repository reader (RDK-DDR-003, P1): an open card index box with one card per source it reads
    rw, rd, rh = p["reader"]
    wt = p["reader_wall"]
    rx, ry = p["reader_at"]
    reader = Pos(rx, ry, rh / 2) * Box(rw, rd, rh) - Pos(rx, ry, rh / 2 + wt) * Box(rw - 2 * wt, rd - 2 * wt, rh)
    n = p["reader_cards"]
    pitch = (rd - 2 * wt - 10) / max(n - 1, 1)
    for i in range(n):
        ch = rh - 2 + (6 if i % 2 else 12)          # cards stand proud of the box, alternate heights
        reader = reader + Pos(rx, ry - (rd - 2 * wt) / 2 + 5 + i * pitch, wt + ch / 2) * Box(rw - 2 * wt - 2, 1.0, ch)
    # identity card (second card): one tab per identity field, the last for the "still open" phrase (decision 4)
    tbw, tbt, tbh = p["tab"]
    nf = len(p["identity_fields"])
    ich = rh - 2 + 6
    for j in range(nf):
        reader = reader + Pos(rx + (j - (nf - 1) / 2) * p["tab_pitch"], ry - (rd - 2 * wt) / 2 + 5 + pitch,
                              wt + ich + tbh / 2 - 0.5) * Box(tbw, tbt, tbh + 1.0)

    # 10  Bought open-source parts (fonts, libraries, system libraries, viewer script): an open tray
    tw_, td, th_ = p["tray"]
    ux, uy = p["tray_at"]
    tray = Pos(ux, uy, th_ / 2) * Box(tw_, td, th_) - Pos(ux, uy, th_ / 2 + 2) * Box(tw_ - 4, td - 4, th_)
    nb = len(p["tray_bays"])
    bw, bd = p["bay"]
    heights = [24, 30, 18, 26, 20][:nb] + [22] * max(nb - 5, 0)
    for k2, bh in enumerate(heights):
        tray = tray + Pos(ux + (k2 - (nb - 1) / 2) * p["bay_pitch"], uy, 2 + bh / 2) * Box(bw, bd, bh)

    return [
        (1, "Controlled document set (PRB, PRC, REQ)", stack, "#F3F4F6", (0, 0, 120)),
        (2, "PDF house style: header and status bands", band, "#0F766E", (0, 0, 230)),
        (3, f"Drawing sheet on board ({p['sheet']})", drawing, "#1D4F8A", (120, 60, 60)),
        (4, "Printed massing part (concept renders)", bracket, "#C2410C", (60, -80, 110)),
        (5, "TRL gate badge", badge, "#D4A017", (-40, -260, 40)),
        (6, "Agent guardrail card (CLAUDE.md, phase cap)", tent, "#6B7280", (-120, -80, 40)),
        (7, "Template repository folder", folder, "#9CA3AF", (0, 0, 0)),
        (12, "Repository reader (shared metadata)", reader, "#7C3AED", (40, 80, 90)),
        (10, "Bought open-source parts (8, 10, 11, 13)", tray, "#16A34A", (-40, 40, 110)),
    ]


def laptop(p=PARAMS):
    """Scale context for the hero render: a 14 in class laptop to the left of the desk items."""
    from build123d import Box, Pos, Rot
    lw, ld, lt = p["laptop"]
    base = Pos(-260, 120, lt / 2) * Box(lw, ld, lt)
    screen = Pos(-260, 120 + ld / 2, lt) * Rot(-15, 0, 0) * Pos(0, 0, 105) * Box(lw, 8, 210)
    return base + screen


SUPPORTS = {   # object: what it rests on (must touch); everything else stands on the desk at Z = 0
    1: 7, 2: 1,
}
CLEAR = 10.0   # minimum gap between separate objects on the desk (mm)


def check(p=PARAMS, verbose=True):
    """Illustration consistency checks (RDK-DDR-003): no two objects overlap, each object rests on
    its support or on the desk, separate objects stand at least CLEAR apart, and the document stack
    lies within the folder. Returns the list of failures."""
    mods = {no: (name, shape) for no, name, shape, _, _ in modules(p)}
    fails, n = [], 0
    nos = sorted(mods)
    for i, a in enumerate(nos):
        for b in nos[i + 1:]:
            sa, sb = mods[a][1], mods[b][1]
            n += 1
            try:
                ov = (sa & sb).volume
            except Exception:
                ov = 0.0
            if ov > 1e-3:
                fails.append(f"{a} and {b} overlap by {ov:.1f} mm3")
            d = sa.distance_to(sb)
            touching = SUPPORTS.get(a) == b or SUPPORTS.get(b) == a
            n += 1
            if touching and d > 1e-3:
                fails.append(f"{a} should rest on {b} but is {d:.2f} mm away")
            if not touching and not ({a, b} <= {1, 2, 7}) and d < CLEAR:
                fails.append(f"{a} and {b} are {d:.1f} mm apart (need {CLEAR})")
    for no, (name, shape) in mods.items():
        n += 1
        z0 = shape.bounding_box().min.Z
        if no not in SUPPORTS and abs(z0) > 1e-3:
            fails.append(f"{no} {name} does not stand on the desk (lowest point Z = {z0:.2f})")
    fb, sb = mods[7][1].bounding_box(), mods[1][1].bounding_box()
    n += 1
    if sb.min.X < fb.min.X or sb.max.X > fb.max.X or sb.min.Y < fb.min.Y or sb.max.Y > fb.max.Y:
        fails.append("document stack hangs over the folder edge")
    # identity tabs: one per field, all on the identity card inside the reader box
    rw, rd, rh = p["reader"]
    nf = len(p["identity_fields"])
    n += 1
    if nf * p["tab_pitch"] > rw - 2 * p["reader_wall"]:
        fails.append("identity tabs do not fit across the identity card")
    n += 1
    if p["identity_fields"][-1] != "still-open phrase":
        fails.append("the still-open phrase is not an identity field (decision 4)")
    n += 1
    if p["tab"][0] >= p["tab_pitch"]:
        fails.append("identity tabs touch each other")
    n += 1
    if p["reader_cards"] != 5:
        fails.append("the reader has one card for each of its five sources")
    # tray bays: one for the core and one for each extra, inside the tray and clear of each other (decisions 5 and 6)
    tw_, td, th_ = p["tray"]
    nb = len(p["tray_bays"])
    n += 1
    if p["tray_bays"][0] != "core" or set(p["tray_bays"][1:]) != {"pdf", "drawings", "media", "release"}:
        fails.append("tray bays must be core, pdf, drawings, media and release")
    n += 1
    if nb * p["bay_pitch"] - (p["bay_pitch"] - p["bay"][0]) > tw_ - 4 or p["bay"][1] > td - 4:
        fails.append("tray bays do not fit inside the tray")
    n += 1
    if p["bay"][0] > p["bay_pitch"] - 1.5:
        fails.append("tray bays are closer than 1.5 mm")
    if verbose:
        print(f"{n} checks, {len(fails)} failures")
        for f in fails:
            print("FAIL", f)
    return fails


def assembly(p=PARAMS):
    from build123d import Compound
    kids = []
    for no, name, shape, _, _ in modules(p):
        shape.label = f"{no} {name}"
        kids.append(shape)
    return Compound(children=kids, label="ReadyKit illustrative massing")


if __name__ == "__main__":
    import sys
    if "--check" in sys.argv:
        sys.exit(1 if check() else 0)
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
    print(f"massing extent {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm; {len(modules())} objects")
    print("wrote cad/step/readykit-massing.step and cad/stl/readykit-massing.stl")

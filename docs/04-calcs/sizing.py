"""ReadyKit TRL 3 calculation and measurement script (RDK-CAL-001).

Run from the repo root:
    python docs/04-calcs/sizing.py                 # measurements on this repo, fixtures and the corpus
    python docs/04-calcs/sizing.py --setup         # also time a fresh virtual environment install (R1)
    python docs/04-calcs/sizing.py --corpus DIR    # folder of finished repositories (default /home/claude/trl3)

Prints every number that RDK-CAL-001 quotes, tagged [A1], [B2] and so on, and writes
docs/04-calcs/results.csv. All work happens in a temporary folder (set TMPDIR to move it);
the repository itself is only read. A `git` shim that always fails is put first on PATH for
every kit run, so measurements never call Git and the PDF commit field is always "uncommitted".
Times are wall-clock medians and depend on the machine; the machine is printed in [A0].
"""
from __future__ import annotations
import argparse, csv, hashlib, importlib.metadata as im, os, platform, re, shutil, statistics
import subprocess, sys, tempfile, time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
KIT = ROOT / ".kit"
HERE = Path(__file__).resolve().parent
EM = chr(0x2014)  # em dash, built from its code point so this file contains none
RESULTS: list[tuple[str, str, str]] = []


def out(tag, text, value=None):
    print(f"[{tag}] {text}")
    if value is not None:
        RESULTS.append((tag, text, str(value)))


# ---------------------------------------------------------------- helpers
def shim_env(tmp: Path) -> dict:
    b = tmp / "bin"
    b.mkdir(exist_ok=True)
    g = b / "git"
    g.write_text("#!/bin/sh\nexit 1\n")
    g.chmod(0o755)
    env = dict(os.environ)
    env["PATH"] = f"{b}{os.pathsep}{env['PATH']}"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run(cmd, cwd, env, netns=False):
    if netns:
        cmd = ["unshare", "-rn"] + cmd
    t = time.perf_counter()
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    return time.perf_counter() - t, p


def timed(cmd, cwd, env, n=5):
    ts, last = [], None
    for _ in range(n):
        dt, last = run(cmd, cwd, env)
        ts.append(dt)
    return statistics.median(ts), last


def copy_repo(src: Path, dst: Path, with_pdf=False):
    """Copy a repository without .git and with this repo's kit, so the kit under test is ReadyKit's."""
    ign = shutil.ignore_patterns(".git", "__pycache__", ".kit", *([] if with_pdf else ["pdf"]))
    shutil.copytree(src, dst, ignore=ign, symlinks=True)
    shutil.copytree(KIT, dst / ".kit", ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def check_cmd():
    return [sys.executable, "-B", ".kit/render.py", "--check"]


def fm(meta: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n" + body


def doc_meta(doc_id, title, typ, version="0.1", status="Draft"):
    return {"doc_id": doc_id, "title": title, "project": "Fixture", "doc_type": typ, "version": version,
            "status": status, "date": "2026-09-25", "author": "Fixture Author", "license": "MIT",
            "revisions": [{"version": version, "date": "2026-09-25", "author": "Fixture Author", "change": "First issue"}]}


def make_fixture(dst: Path) -> Path:
    """A minimal repository that passes the check at TRL 3. Used for the coverage probes (section E)."""
    shutil.copytree(KIT, dst / ".kit", ignore=shutil.ignore_patterns("__pycache__"))
    for d in ("docs/04-calcs", "docs/decisions", "cad/src", "cad/step", "cad/drawings", "bom", "media", "build-log"):
        (dst / d).mkdir(parents=True, exist_ok=True)
    docs = {"docs/01-problem.md": ("FIX-PRB-001", "Problem", "Problem statement"),
            "docs/02-concept.md": ("FIX-PRC-001", "Precis", "Design precis"),
            "docs/03-requirements.md": ("FIX-REQ-001", "Requirements", "Requirements"),
            "docs/04-calcs/01-sizing.md": ("FIX-CAL-001", "Sizing", "Calculation")}
    for path, (i, t, ty) in docs.items():
        (dst / path).write_text(fm(doc_meta(i, t, ty), f"\n# {t}\n\nFixture text.\n"))
    (dst / "project.yaml").write_text(yaml.safe_dump({
        "name": "Fixture", "slug": "fixture", "trl": 3, "trl_target": 3,
        "trl_evidence": list(docs) + ["bom/bom.csv"], "budget_usd": 0}, sort_keys=False))
    (dst / "cad/src/model.py").write_text("print('model')\n")
    (dst / "cad/step/part.step").write_text("ISO-10303-21;\n")
    (dst / "cad/drawings/FIX-DWG-001.svg").write_text("<svg xmlns='http://www.w3.org/2000/svg'/>\n")
    (dst / "bom/bom.csv").write_text("item,qty,unit_cost_usd\n1 Part,1,0.00\n")
    for m in ("hero.png", "concept-blueprint.png", "model.glb", "exploded.png"):
        (dst / "media" / m).write_bytes(b"x")
    (dst / "README.md").write_text("# Fixture\n\n## Concept rationale\n\n## Problem\n")
    return dst


# ---------------------------------------------------------------- section A: machine and kit
def sec_a():
    out("A0", f"Machine: {platform.system()} {platform.machine()}, {os.cpu_count()} CPU, "
              f"Python {platform.python_version()}, kit {(KIT / 'KIT_VERSION').read_text().strip()}")
    files = [f for f in KIT.rglob("*") if f.is_file() and "__pycache__" not in f.parts]
    size = sum(f.stat().st_size for f in files)
    fonts = sum(f.stat().st_size for f in (KIT / "fonts").glob("*"))
    out("A1", f"Vendored kit folder: {size / 1e6:.2f} MB in {len(files)} files; fonts {fonts / 1e6:.2f} MB "
              f"({100 * fonts / size:.0f}%)", f"{size / 1e6:.2f}")
    lines = {f.name: sum(1 for _ in f.open()) for f in sorted(KIT.glob("*.py"))}
    out("A2", "Kit source: " + ", ".join(f"{k} {v}" for k, v in lines.items())
              + f"; total {sum(lines.values())} lines of Python", sum(lines.values()))
    codes = re.findall(r"\|\s([A-Z]{3})\s\|\s[A-Z]", (KIT / "STANDARDS.md").read_text())
    codes = [c for c in codes if c != "OHP"]
    out("A3", f"Project codes in STANDARDS.md section 7: {len(codes)} (plus OHP, portfolio-wide)", len(codes))
    ident = {"amishchadha.com": 0, "BoujeeEnjinia1701": 0, "Amish Chadha": 0, "Open Hardware Portfolio": 0}
    where = {}
    for f in [*KIT.glob("*.py"), *(KIT / "style").glob("*"), *(KIT / "templates").glob("*")]:
        t = f.read_text(errors="ignore")
        for k in ident:
            c = t.count(k)
            ident[k] += c
            if c:
                where.setdefault(k, []).append(f.name)
    n_id = sum(1 for v in ident.values() if v)
    out("A4", f"Hard-coded identity strings in kit code, style and templates: {sum(ident.values())} occurrences "
              f"of {n_id} identity values: " + "; ".join(f"{k} x{v} ({', '.join(where.get(k, []))})"
                                                        for k, v in ident.items() if v), sum(ident.values()))
    return {"kit_mb": size / 1e6, "identity": sum(ident.values()), "codes": len(codes)}


# ---------------------------------------------------------------- section B: check time and scaling
def sec_b(tmp, env, corpus):
    t_self, p = timed(check_cmd(), ROOT, env, 7)
    ndocs = sum(1 for l in p.stdout.splitlines() if l.startswith(("ok   docs", "FAIL docs")))
    out("B1", f"Check, this repository ({ndocs} controlled documents): median {t_self:.2f} s of 7 runs, "
              f"exit {p.returncode}", f"{t_self:.2f}")
    t0, _ = timed([sys.executable, "-B", "-c", "import yaml, markdown, jinja2"], ROOT, env, 7)
    out("B2", f"Python start-up plus the check's imports alone: {t0:.2f} s, so the checking itself takes about "
              f"{max(t_self - t0, 0) * 1000:.0f} ms", f"{t0:.2f}")
    # scaling: synthetic repositories with 10, 100 and 400 controlled documents
    pts = []
    for n in (10, 100, 400):
        d = make_fixture(tmp / f"scale{n}")
        body = (ROOT / "docs/03-requirements.md").read_text().split("---\n", 2)[2]
        for i in range(n - 4):
            (d / "docs" / f"x{i:03d}.md").write_text(fm(doc_meta(f"FIX-DDR-{i + 1:03d}", f"Record {i}", "Record"), body))
        t, p = timed(check_cmd(), d, env, 3)
        pts.append((n, t))
    slope = (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0])
    out("B3", "Check time against document count: " + ", ".join(f"{n} docs {t:.2f} s" for n, t in pts)
              + f"; slope {slope * 1000:.1f} ms per document; 2 s budget reached at about "
              f"{int((2 - pts[0][1]) / slope + pts[0][0]) if slope > 0 else 0} documents", f"{slope * 1000:.1f}")
    res = {"check_s": t_self, "slope_ms": slope * 1000, "scale": pts}
    # corpus of finished TRL 3 repositories
    if corpus and corpus.is_dir():
        rows = []
        for r in sorted(x for x in corpus.iterdir() if (x / "project.yaml").exists()):
            d = copy_repo(r, tmp / "corpus" / r.name)
            t, p = timed(check_cmd(), d, env, 3)
            nd = sum(1 for l in p.stdout.splitlines() if l.startswith(("ok   ", "FAIL ")) and ".md" in l)
            warns = [l for l in p.stdout.splitlines() if l.startswith("warn")]
            rows.append((r.name, t, p.returncode, nd, warns, p.stdout))
        ts = [x[1] for x in rows]
        fails = [x for x in rows if x[2]]
        out("B4", f"Corpus {corpus}: {len(rows)} repositories at TRL 3, {min(x[3] for x in rows)} to "
                  f"{max(x[3] for x in rows)} controlled documents each; check median {statistics.median(ts):.2f} s, "
                  f"max {max(ts):.2f} s", f"{statistics.median(ts):.2f}")
        out("B5", f"Corpus check failures: {len(fails)} of {len(rows)}"
                  + ("".join(f"\n       {n}: " + " | ".join(l.strip() for l in so.splitlines() if l.startswith(("FAIL", "     -")))
                             for n, _, _, _, _, so in fails)), len(fails))
        wr = [x for x in rows if x[4]]
        out("B6", f"Corpus repositories with warnings: {len(wr)} of {len(rows)}"
                  + "".join(f"\n       {n}: {w[0][5:120]}" for n, _, _, _, w, _ in wr), len(wr))
        kit_same = sum(1 for r in corpus.iterdir() if (r / ".kit/render.py").exists()
                       and all((r / ".kit" / f).read_bytes() == (KIT / f).read_bytes()
                               for f in ("render.py", "drawing.py", "concept.py")))
        std_same = sum(1 for r in corpus.iterdir() if (r / ".kit/STANDARDS.md").exists()
                       and (r / ".kit/STANDARDS.md").read_bytes() == (KIT / "STANDARDS.md").read_bytes())
        pat = r"\|\s([A-Z]{3})\s\|\s[A-Z]"
        ours = set(re.findall(pat, (KIT / "STANDARDS.md").read_text()))
        theirs = set(re.findall(pat, (corpus / rows[0][0] / ".kit/STANDARDS.md").read_text()))
        out("B7", f"Kit drift: kit code identical to this repo's in {kit_same} of {len(rows)} corpus repositories; "
                  f"STANDARDS.md identical in {std_same} of {len(rows)}, although all carry KIT_VERSION "
                  f"{(KIT / 'KIT_VERSION').read_text().strip()}; this repo's standard lists {len(ours - theirs)} project codes "
                  f"that {rows[0][0]}'s does not ({len(theirs - ours)} the other way)", std_same)
        res.update(corpus_n=len(rows), corpus_fail=len(fails), corpus_med=statistics.median(ts), corpus_max=max(ts))
    else:
        out("B4", "Corpus not found; corpus measurements skipped")
    return res


# ---------------------------------------------------------------- section C: PDF render and reproducibility
def pdf_text(pdf: Path) -> str:
    p = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
    return p.stdout


def sec_c(tmp, env, corpus):
    src = corpus / "waterwatch" if corpus and (corpus / "waterwatch").is_dir() else ROOT
    d = copy_repo(src, tmp / "render")
    ts, texts = [], []
    for i in range(2):
        dt, p = run([sys.executable, "-B", ".kit/render.py"], d, env)
        ts.append(dt)
        pdfs = sorted((d / "docs/pdf").glob("*.pdf"))
        texts.append({f.name: pdf_text(f) for f in pdfs})
    n = len(texts[0])
    per = ts[0] / n
    out("C1", f"PDF render, {src.name} copy, {n} controlled documents: {ts[0]:.1f} s and {ts[1]:.1f} s "
              f"(check included); about {per:.2f} s per document, so about {3 * per:.1f} s for three documents",
        f"{3 * per:.1f}")
    pages = sum(int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(f)], capture_output=True, text=True).stdout).group(1))
                for f in (d / "docs/pdf").glob("*.pdf"))
    out("C2", f"Pages rendered: {pages}, about {ts[0] / pages:.2f} s per page", pages)
    same = sum(1 for k in texts[0] if texts[0][k] == texts[1].get(k))
    out("C3", f"Reproducibility: extracted text identical in {same} of {n} PDFs across two renders", same)
    # offline: check and render with no network namespace
    ok_c = ok_r = None
    try:
        _, pc = run(check_cmd(), d, env, netns=True)
        _, pr = run([sys.executable, "-B", ".kit/render.py"], d, env, netns=True)
        ok_c, ok_r = pc.returncode == 0, pr.returncode == 0
        out("C4", f"Offline (network namespace with no interfaces): check {'passes' if ok_c else 'fails'}, "
                  f"render {'passes' if ok_r else 'fails'}", f"{ok_c and ok_r}")
    except FileNotFoundError:
        out("C4", "Offline run not possible here (no unshare)")
    return {"pdf3_s": 3 * per, "repro": (same, n), "offline": (ok_c, ok_r)}


# ---------------------------------------------------------------- section D: concept media
MEDIA_20 = """
import sys; sys.path.insert(0, ".kit")
from build123d import Box, Cylinder, Pos
from concept import Part, render_all
parts = []
for i in range(20):
    x, y = (i % 5) * 160.0, (i // 5) * 160.0
    s = Pos(x, y, 40 + 5 * i) * Box(100 + 3 * i, 90, 80 + 10 * i) - Pos(x, y, 40 + 5 * i) * Cylinder(25, 400)
    s = s + Pos(x + 60, y, 10) * Cylinder(12 + i, 20)
    parts.append(Part(f"Part {i + 1}", s, "#9CA3AF", i + 1, (0, 0, 40 * (i % 4))))
render_all(parts, project="Fixture", title="Twenty-part timing model", dwg_no="FIX-DWG-010",
           key_figures=["timing fixture"], cut=True, scale_figure=True)
"""


def sec_d(tmp, env):
    res = {}
    # 1: this repository's massing, 7 modules plus the laptop context, as concept_media.py renders it
    d = tmp / "media7"
    d.mkdir()
    shutil.copytree(KIT, d / ".kit", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "cad", d / "cad", ignore=shutil.ignore_patterns("step", "stl", "drawings", "__pycache__"))
    (d / "media").mkdir()
    t7, p = run([sys.executable, "-B", "cad/src/concept_media.py"], d, env)
    out("D1", f"Concept media, this repository (7 modules plus laptop, hero, exploded, blueprint, GLB, flow): "
              f"{t7:.1f} s, exit {p.returncode}", f"{t7:.1f}")
    # 2: twenty-part model, all views including cutaway and the 1.75 m figure; twice for reproducibility
    hashes, ts = [], []
    for i in range(2):
        d = tmp / f"media20_{i}"
        d.mkdir()
        shutil.copytree(KIT, d / ".kit", ignore=shutil.ignore_patterns("__pycache__"))
        (d / "m.py").write_text(MEDIA_20)
        t, p = run([sys.executable, "-B", "m.py"], d, env)
        ts.append(t)
        if p.returncode:
            print(p.stderr[-800:])
        hashes.append({f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                       for f in sorted((d / "media").glob("*.png"))})
    same = sum(1 for k in hashes[0] if hashes[0][k] == hashes[1].get(k))
    out("D2", f"Concept media, 20-part model with cutaway and scale figure: {ts[0]:.1f} s and {ts[1]:.1f} s "
              f"(target 60 s)", f"{max(ts):.1f}")
    out("D3", f"Reproducibility: {same} of {len(hashes[0])} PNG images byte-identical across two runs", same)
    res.update(media7=t7, media20=max(ts), img_same=(same, len(hashes[0])))
    return res


# ---------------------------------------------------------------- section E: check coverage by seeded faults
def _edit_front(path: Path, fn):
    t = path.read_text()
    _, head, body = t.split("---\n", 2)
    meta = yaml.safe_load(head)
    fn(meta)
    path.write_text(fm(meta, body))


def _yaml_edit(path: Path, fn):
    y = yaml.safe_load(path.read_text())
    fn(y)
    path.write_text(yaml.safe_dump(y, sort_keys=False))


PRB, REQ = "docs/01-problem.md", "docs/03-requirements.md"
PROBES = [  # (rule in STANDARDS.md, audit claim at TRL 2, seeded fault)
    ("Required front matter fields present", "Yes", lambda d: _edit_front(d / PRB, lambda m: m.pop("author"))),
    ("Document ID matches PRJ-TYP-NNN", "Yes", lambda d: _edit_front(d / PRB, lambda m: m.update(doc_id="FIX-XYZ-01"))),
    ("Document ID unique within the repository", "No",  # a second file reusing the CAL ID; all evidence stays present
     lambda d: (d / "docs/04-calcs/02-extra.md").write_text((d / "docs/04-calcs/01-sizing.md").read_text())),
    ("Version format (quoted, n.n)", "Yes", lambda d: _edit_front(d / PRB, lambda m: (m.update(version="0.1a"), m["revisions"][-1].update(version="0.1a")))),
    ("Version equals newest revision row", "Yes", lambda d: _edit_front(d / PRB, lambda m: m.update(version="0.2"))),
    ("Every revision row complete", "Yes", lambda d: _edit_front(d / PRB, lambda m: m["revisions"][-1].pop("change"))),
    ("Status in the allowed set", "Yes", lambda d: _edit_front(d / PRB, lambda m: m.update(status="Approved"))),
    ("Released documents at 1.0 or later", "Yes", lambda d: _edit_front(d / PRB, lambda m: m.update(status="Released"))),
    ("No em dash anywhere in the repository", "Partly",
     lambda d: (d / "README.md").write_text((d / "README.md").read_text() + f"\nA line {EM} with a dash.\n")),
    ("TRL evidence present for the claimed level", "Yes", lambda d: (d / "docs/04-calcs/01-sizing.md").unlink()),
    ("TRL and target within the phase cap", "Yes", lambda d: _yaml_edit(d / "project.yaml", lambda y: y.update(trl_target=4))),
    ("Required concept media present", "Yes", lambda d: (d / "media/hero.png").unlink()),
    ("Concept media carry the not-for-fabrication label", "No", lambda d: (d / "media/concept-blueprint.png").write_bytes(b"unlabeled")),
    ("BOM numbering matches the exploded view", "No",
     lambda d: (d / "bom/bom.csv").write_text("item,qty,unit_cost_usd\n9 Unmatched part,1,0.00\n")),
    ("BOM fully priced at TRL 3", "Yes", lambda d: (d / "bom/bom.csv").write_text("item,qty,unit_cost_usd\n1 Part,1,\n")),
    ("Evidence files listed in project.yaml exist", "Yes",
     lambda d: _yaml_edit(d / "project.yaml", lambda y: y["trl_evidence"].append("docs/missing.md"))),
    ("Figures and tables numbered and captioned", "No",
     lambda d: (d / PRB).write_text((d / PRB).read_text() + "\n![uncaptioned](x.png)\n\n| a | b |\n| - | - |\n| 1 | 2 |\n")),
    ("Safety note present where hazard keywords appear", "No",
     lambda d: (d / PRB).write_text((d / PRB).read_text() + "\nThe unit runs on mains voltage and lithium cells.\n")),
    ("README sections in the required order", "No",
     lambda d: (d / "README.md").write_text("# Fixture\n\n## Problem\n\n## Concept rationale\n")),
    ("SI unit formatting (space between value and unit)", "No",
     lambda d: (d / PRB).write_text((d / PRB).read_text() + "\nIt draws 12kW at 450C.\n")),
]
GUARD_PROBES = [  # R13: agent guardrails
    ("TRL above the cap", lambda d: _yaml_edit(d / "project.yaml", lambda y: y.update(trl=4, trl_target=4))),
    ("Work beyond the cap (a TST folder)", lambda d: (d / "docs/05-tests").mkdir()),
    ("Decision recorded as made without an owner",
     lambda d: (d / "docs/02-concept.md").write_text((d / "docs/02-concept.md").read_text()
                                                   + "\nDecision: the budget is raised to $900. Approved.\n")),
]


def detected(d: Path, env, before: str) -> bool:
    _, p = run(check_cmd(), d, env)
    warn_new = sum(1 for l in p.stdout.splitlines() if l.startswith("warn")) > before.count("\nwarn")
    return p.returncode != 0 or warn_new


def sec_e(tmp, env):
    base = make_fixture(tmp / "fixture")
    _, p0 = run(check_cmd(), base, env)
    out("E0", f"Fixture repository at TRL 3 passes the unmodified check: {p0.returncode == 0}")
    hits, claimed = [], 0
    for i, (rule, claim, fault) in enumerate(PROBES, 1):
        d = tmp / f"probe{i:02d}"
        shutil.copytree(base, d)
        fault(d)
        hit = detected(d, env, "\n" + p0.stdout)
        hits.append((rule, claim, hit))
        claimed += claim == "Yes"
    n_hit = sum(h for _, _, h in hits)
    mism = [(r, c, h) for r, c, h in hits if (c == "Yes") != h]
    out("E1", f"Seeded faults detected: {n_hit} of {len(PROBES)} rules ({100 * n_hit / len(PROBES):.0f}%); "
              f"TRL 2 audit claimed {claimed}; mismatches with the audit: {len(mism)}"
        + "".join(f"\n       {r}: audit {c}, probe {'caught' if h else 'missed'}" for r, c, h in mism), n_hit)
    for r, c, h in hits:
        print(f"       {'caught' if h else 'MISSED'}  {r}")
    need = -(-90 * len(PROBES) // 100)
    out("E2", f"Rules needed for the 90% target: {need} of {len(PROBES)}; gap {need - n_hit} rules", need - n_hit)
    g = []
    for i, (name, fault) in enumerate(GUARD_PROBES, 1):
        d = tmp / f"guard{i}"
        shutil.copytree(base, d)
        fault(d)
        g.append((name, detected(d, env, "\n" + p0.stdout)))
    out("E3", "Guardrail probes (R13): " + "; ".join(f"{n} {'caught' if h else 'missed'}" for n, h in g),
        sum(h for _, h in g))
    return {"cov": (n_hit, len(PROBES)), "guard": (sum(h for _, h in g), len(g)), "mism": len(mism)}


# ---------------------------------------------------------------- section F: cost, licenses, interop, setup
def sec_f(setup: bool, tmp):
    rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
    total = sum(float(r["unit_cost_usd"]) * float(r["qty"]) for r in rows)
    budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
    unpriced = sum(1 for r in rows if not r["unit_cost_usd"].strip())
    out("F1", f"BOM: {len(rows)} lines, {unpriced} unpriced, total ${total:.2f} against budget_usd ${budget:.2f}", f"{total:.2f}")
    deps = [re.split(r"[<>=]", l)[0].strip() for l in (KIT / "requirements.txt").read_text().splitlines() if l.strip()]
    lic = []
    for p in deps:
        try:
            md = im.metadata(p)
            l = md.get("License-Expression") or next((c.split("::")[-1].strip() for c in md.get_all("Classifier") or []
                                                      if c.startswith("License ::")), None) or (md.get("License") or "?")[:30]
            lic.append((p, md.get("Version"), l))
        except im.PackageNotFoundError:
            lic.append((p, "not installed", "?"))
    out("F2", f"Direct dependencies ({len(lic)}): " + "; ".join(f"{p} {v} {l}" for p, v, l in lic), len(lic))
    copyleft = [p for p, _, l in lic if "GPL" in l]
    out("F3", f"Direct dependencies with a copyleft license: {', '.join(copyleft) or 'none'}; "
              "all are free of charge and OSI-approved or equivalent", len(copyleft))
    y = yaml.safe_load((ROOT / "project.yaml").read_text())
    okh = {"title": bool(y.get("name")), "description": bool(y.get("pitch")),
           "manifest-author name": bool(y.get("author")), "license (SPDX)": bool(y.get("licenses")),
           "project-link or documentation-home": bool(y.get("repository") or y.get("homepage"))}
    out("F4", f"Open Know-How manifest 1.0 required fields available from project.yaml: {sum(okh.values())} of {len(okh)}; "
              "missing: " + ", ".join(k for k, v in okh.items() if not v), sum(okh.values()))
    sheets = len(re.findall(r"^W, H = ", (KIT / "drawing.py").read_text(), re.M))
    out("F5", f"Sheet sizes the drawing generator supports: {sheets} (ANSI B, fixed module constants W, H)", sheets)
    if setup:
        v = tmp / "venv"
        t = time.perf_counter()
        subprocess.run([sys.executable, "-m", "venv", str(v)], check=True)
        p = subprocess.run([str(v / "bin/pip"), "install", "-q", "--disable-pip-version-check", "-r",
                            str(KIT / "requirements.txt")], capture_output=True, text=True)
        dt = time.perf_counter() - t
        sz = sum(f.stat().st_size for f in v.rglob("*") if f.is_file()) / 1e9
        d = copy_repo(ROOT, tmp / "setupcheck")
        _, pc = run([str(v / "bin/python"), "-B", ".kit/render.py", "--check"], d, shim_env(tmp))
        out("F6", f"Fresh virtual environment plus pip install of the kit requirements: {dt:.0f} s, exit {p.returncode}, "
                  f"{sz:.2f} GB installed; check then passes: {pc.returncode == 0} "
                  "(system libraries for WeasyPrint were already present)", f"{dt:.0f}")
    else:
        out("F6", "Setup timing skipped; run with --setup")
    return {"bom_total": total, "budget": budget, "okh": sum(okh.values()), "sheets": sheets}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--setup", action="store_true")
    ap.add_argument("--corpus", default="/home/claude/trl3")
    a = ap.parse_args()
    corpus = Path(a.corpus) if a.corpus else None
    with tempfile.TemporaryDirectory(prefix="rdk-cal-") as t:
        tmp = Path(t)
        env = shim_env(tmp)
        r = {}
        r.update(sec_a())
        r.update(sec_b(tmp, env, corpus))
        r.update(sec_c(tmp, env, corpus))
        r.update(sec_d(tmp, env))
        r.update(sec_e(tmp, env))
        r.update(sec_f(a.setup, tmp))
    with (HERE / "results.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tag", "value", "line"])
        for tag, text, value in RESULTS:
            w.writerow([tag, value, text.split("\n")[0]])
    print(f"wrote {(HERE / 'results.csv').relative_to(ROOT)}")


if __name__ == "__main__":
    main()

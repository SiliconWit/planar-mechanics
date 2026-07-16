"""
Graphical-method diagram generator for the Planar Mechanics course.

Each worked Application in the course is solved graphically first (drawn to
scale with a drawing set) before it is confirmed by calculation and by the
interactive simulator. This script draws the reference figures that the
written construction steps refer to: space (position) diagrams, velocity
polygons, and (later) acceleration polygons.

The figures are plain SVG, so their content is text: readable in a code
editor, diffable in git, and parseable by tools. Every figure carries a white
rounded background plate so its labels stay legible on both light and dark
site themes.

Run from anywhere:
    python3 graphical_diagrams.py
It writes the SVG files into ../images/ (the folder the lessons reference as
./images/...svg).

Conventions
-----------
Colours: crank #2563eb (blue), coupler/rod #d97706 (amber),
follower/piston #059669 (green), ground/neutral #6b7280, points #374151.
All angles in degrees on input; lengths in millimetres.
"""

import os
import re
import numpy as np

IMAGES = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "images"))

COL = {
    "crank": "#2563eb",
    "coupler": "#d97706",
    "rod": "#d97706",
    "follower": "#059669",
    "piston": "#059669",
    "ground": "#6b7280",
    "con": "#9ca3af",
    "pt": "#374151",
}


# ----------------------------------------------------------------------------
# small SVG helpers
# ----------------------------------------------------------------------------
def sub(v, s):
    """A label with a subscript, e.g. sub('v', 'A') -> v with a small A."""
    return f'{v}<tspan baseline-shift="sub" font-size="70%">{s}</tspan>'


def sup(v, s):
    """A label with a superscript, e.g. sup('a', 'n') -> a with a small n."""
    return f'{v}<tspan baseline-shift="super" font-size="70%">{s}</tspan>'


def plate(w, h):
    """White rounded background so dark labels read on any theme."""
    return (f'<rect data-bg="1" x="0" y="0" width="{w:.0f}" height="{h:.0f}" '
            f'rx="8" fill="#ffffff" stroke="#e5e7eb" stroke-width="1"/>')


def arrowheads(colors):
    return "".join(
        f'<marker id="m{c[1:]}" markerWidth="10" markerHeight="10" refX="7.5" '
        f'refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="{c}"/></marker>'
        for c in sorted(set(colors)))


def write(fname, parts):
    path = os.path.join(IMAGES, fname)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    print(f"wrote {fname}  ({os.path.getsize(path)} bytes)")


# ----------------------------------------------------------------------------
# space (position) diagrams
# ----------------------------------------------------------------------------
def slider_crank_space(r, l, theta_deg, fname):
    """Crank OA at theta, connecting rod AB, piston B on the centre-line."""
    th = np.radians(theta_deg)
    O = np.array([0.0, 0.0])
    A = O + r * np.array([np.cos(th), np.sin(th)])
    s = r * np.cos(th) + np.sqrt(l ** 2 - (r * np.sin(th)) ** 2)
    B = np.array([s, 0.0])

    sc, m, cap = 2.4, 46, 20
    xs, ys = [O[0], A[0], B[0]], [O[1], A[1], B[1]]
    xmin, xmax = min(xs) - 12, max(xs) + 16
    ymin, ymax = min(ys) - 12, max(ys) + 16
    W = (xmax - xmin) * sc + 2 * m
    H = (ymax - ymin) * sc + 2 * m + cap
    X = lambda x: m + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def L(p, q, c, w=2.6, dash=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{c}" stroke-width="{w}"{d} stroke-linecap="round"/>')

    def pin(p, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#fff" '
             f'stroke="{COL["pt"]}" stroke-width="2"/>')
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} '
                  f'L {cx+7:.1f} {cy+9:.1f} Z" fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def T(p, txt, c, dx=8, dy=-6, sz=15):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{c}" '
                f'font-size="{sz}" font-family="sans-serif" font-weight="600">{txt}</text>')

    bx, by = X(B[0]), Y(B[1])
    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Slider-crank space diagram with crank at {theta_deg:.0f} degrees">',
         plate(W, H),
         f'<line x1="{X(xmin+4):.1f}" y1="{Y(0):.1f}" x2="{X(xmax-2):.1f}" y2="{Y(0):.1f}" '
         f'stroke="{COL["con"]}" stroke-width="1.2" stroke-dasharray="2 4"/>',
         L(O, A, COL["crank"]), L(A, B, COL["rod"]),
         f'<rect x="{bx-12:.1f}" y="{by-12:.1f}" width="24" height="24" rx="3" fill="none" '
         f'stroke="{COL["piston"]}" stroke-width="2.4"/>',
         pin(O, True), pin(A),
         f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>',
         T((O + A) / 2, "r", COL["crank"], -14, 2), T((A + B) / 2, "l", COL["rod"], 0, -8),
         T(O, "O", COL["pt"], -20, 16), T(A, "A", COL["pt"], -6, -8), T(B, "B", COL["pt"], 12, -8),
         T(A, "&#952;", COL["crank"], -30, -22, 14),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Choose a length scale, e.g. 1 cm = 20 mm. r = {r}, l = {l} mm, '
         f'&#952; = {theta_deg:.0f}&#176;.</text>',
         "</svg>"]
    write(fname, g)


def four_bar_space(a, b, c, d, theta2_deg, theta3_deg, theta4_deg, fname):
    """Ground O2-O4, crank O2-A, coupler A-B, follower O4-B (open assembly)."""
    t2, t3, t4 = np.radians([theta2_deg, theta3_deg, theta4_deg])
    O2, O4 = np.array([0.0, 0.0]), np.array([d, 0.0])
    A = O2 + a * np.array([np.cos(t2), np.sin(t2)])
    B = O4 + c * np.array([np.cos(t4), np.sin(t4)])

    sc, m, cap = 2.3, 46, 20
    xs = [O2[0], O4[0], A[0], B[0]]
    ys = [O2[1], O4[1], A[1], B[1]]
    xmin, xmax = min(xs) - 14, max(xs) + 16
    ymin, ymax = min(ys) - 12, max(ys) + 18
    W = (xmax - xmin) * sc + 2 * m
    H = (ymax - ymin) * sc + 2 * m + cap
    X = lambda x: m + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def L(p, q, col, w=2.6, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{col}" stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def pin(p, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#fff" '
             f'stroke="{COL["pt"]}" stroke-width="2"/>')
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} '
                  f'L {cx+7:.1f} {cy+9:.1f} Z" fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def T(p, txt, col, dx=8, dy=-6, sz=15):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{col}" '
                f'font-size="{sz}" font-family="sans-serif" font-weight="600">{txt}</text>')

    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Four-bar space diagram at crank angle {theta2_deg:.0f} degrees">',
         plate(W, H),
         L(O2, O4, COL["ground"], 2, "6 4"), L(O2, A, COL["crank"]),
         L(A, B, COL["coupler"]), L(O4, B, COL["follower"]),
         pin(O2, True), pin(O4, True), pin(A), pin(B),
         T((O2 + A) / 2, "a", COL["crank"], -14, 2), T((A + B) / 2, "b", COL["coupler"], 0, -8),
         T((O4 + B) / 2, "c", COL["follower"], 8, 2), T((O2 + O4) / 2, "d", COL["ground"], -4, 18),
         T(O2, sub("O", "2"), COL["pt"], -26, 16), T(O4, sub("O", "4"), COL["pt"], 6, 16),
         T(A, "A", COL["pt"], -10, -6), T(B, "B", COL["pt"], 8, -6),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Choose a length scale, e.g. 1 cm = 20 mm. a={a}, b={b}, c={c}, d={d} mm, '
         f'&#952;&#8322;={theta2_deg:.0f}&#176;.</text>',
         "</svg>"]
    write(fname, g)


# ----------------------------------------------------------------------------
# velocity polygon (relative-velocity / vector triangle)
# ----------------------------------------------------------------------------
def velocity_polygon(pts, vectors, caption, fname, aria):
    """pts: {name: (x, y)} in velocity space (math coords, y up).
    vectors: list of (from_name, to_name, colour, label)."""
    import re
    plain = lambda t: len(re.sub(r"&#\d+;", "x", t))
    P = {k: np.array(v, float) for k, v in pts.items()}
    names = list(pts)
    C = np.mean([P[k] for k in names], axis=0)
    sc, pad, cap = 4.6, 10, 22

    pt_lab = {k: P[k] + (P[k] - C) / (np.hypot(*(P[k] - C)) or 1) * 5.0 for k in names}
    vec_lab = []
    for (pn, qn, col, lab) in vectors:
        M = (P[pn] + P[qn]) / 2
        dirv = P[qn] - P[pn]
        perp = np.array([-dirv[1], dirv[0]])
        perp = perp / (np.hypot(*perp) or 1)
        if np.dot(perp, M - C) < 0:
            perp = -perp
        vec_lab.append((M + perp * 4.5, col, lab))

    xs = [P[k][0] for k in names] + [pt_lab[k][0] for k in names] + [m[0][0] for m in vec_lab]
    ys = [P[k][1] for k in names] + [pt_lab[k][1] for k in names] + [m[0][1] for m in vec_lab]
    xmin, xmax = min(xs) - 3, max(xs) + 15
    ymin, ymax = min(ys) - 4, max(ys) + 5
    W = (xmax - xmin) * sc + 2 * pad
    H = (ymax - ymin) * sc + 2 * pad + cap
    W = max(W, plain(caption) * 6.4 + 2 * pad)            # keep the caption inside the frame
    X = lambda x: pad + (x - xmin) * sc
    Y = lambda y: H - pad - cap - (y - ymin) * sc

    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="{aria}"><defs>{arrowheads(v[2] for v in vectors)}</defs>',
         plate(W, H)]
    for (pn, qn, col, lab) in vectors:
        o.append(f'<line x1="{X(P[pn][0]):.1f}" y1="{Y(P[pn][1]):.1f}" '
                 f'x2="{X(P[qn][0]):.1f}" y2="{Y(P[qn][1]):.1f}" stroke="{col}" '
                 f'stroke-width="2.6" marker-end="url(#m{col[1:]})"/>')
    for (lp, col, lab) in vec_lab:
        o.append(f'<text x="{X(lp[0]):.1f}" y="{Y(lp[1]):.1f}" fill="{col}" font-size="15" '
                 f'font-family="sans-serif" font-weight="600" text-anchor="middle" '
                 f'dominant-baseline="middle">{lab}</text>')
    for k in names:
        nm = "o (pole)" if k == "o" else k
        o.append(f'<circle cx="{X(P[k][0]):.1f}" cy="{Y(P[k][1]):.1f}" r="3.6" fill="{COL["pt"]}"/>')
        o.append(f'<text x="{X(pt_lab[k][0]):.1f}" y="{Y(pt_lab[k][1]):.1f}" fill="{COL["pt"]}" '
                 f'font-size="13.5" font-family="sans-serif" font-weight="700" '
                 f'text-anchor="middle" dominant-baseline="middle">{nm}</text>')
    o.append(f'<text x="{pad+2}" y="{H-7:.0f}" fill="{COL["ground"]}" font-size="11.5" '
             f'font-family="sans-serif">{caption}</text>')
    o.append("</svg>")
    write(fname, o)


def vector_polygon(pts, vectors, plabels, caption, fname, aria, sc=4.6):
    """Generic vector polygon (velocity or acceleration). pts: {name:(x,y)} in
    math coords. vectors: list of (from, to, colour, label). plabels: {name:text}
    for the points to label (others stay as plain dots)."""
    import re
    plain = lambda t: len(re.sub(r"&#\d+;", "x", t))
    P = {k: np.array(v, float) for k, v in pts.items()}
    names = list(pts)
    C = np.mean([P[k] for k in names], axis=0)
    pad, cap = 10, 22

    pt_lab = {k: P[k] + (P[k] - C) / (np.hypot(*(P[k] - C)) or 1) * 5.0 for k in plabels}
    vec_lab = []
    for (pn, qn, col, lab) in vectors:
        M = (P[pn] + P[qn]) / 2
        dirv = P[qn] - P[pn]
        perp = np.array([-dirv[1], dirv[0]])
        perp = perp / (np.hypot(*perp) or 1)
        if np.dot(perp, M - C) < 0:
            perp = -perp
        vec_lab.append((M + perp * 5.0, col, lab))

    hw = lambda lab: (plain(lab) * 4.2) / sc          # half label width in math units
    hh = 9.0 / sc
    xs = [P[k][0] for k in names]
    ys = [P[k][1] for k in names]
    for k in plabels:
        xs += [pt_lab[k][0] - hw(plabels[k]), pt_lab[k][0] + hw(plabels[k])]
        ys += [pt_lab[k][1] - hh, pt_lab[k][1] + hh]
    for (lp, col, lab) in vec_lab:
        xs += [lp[0] - hw(lab), lp[0] + hw(lab)]
        ys += [lp[1] - hh, lp[1] + hh]
    xmin, xmax = min(xs) - 3, max(xs) + 3
    ymin, ymax = min(ys) - 3, max(ys) + 3
    W = (xmax - xmin) * sc + 2 * pad
    H = (ymax - ymin) * sc + 2 * pad + cap
    W = max(W, plain(caption) * 6.4 + 2 * pad)
    X = lambda x: pad + (x - xmin) * sc
    Y = lambda y: H - pad - cap - (y - ymin) * sc

    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="{aria}"><defs>{arrowheads(v[2] for v in vectors)}</defs>',
         plate(W, H)]
    for (pn, qn, col, lab) in vectors:
        o.append(f'<line x1="{X(P[pn][0]):.1f}" y1="{Y(P[pn][1]):.1f}" '
                 f'x2="{X(P[qn][0]):.1f}" y2="{Y(P[qn][1]):.1f}" stroke="{col}" '
                 f'stroke-width="2.6" marker-end="url(#m{col[1:]})"/>')
    for (lp, col, lab) in vec_lab:
        o.append(f'<text x="{X(lp[0]):.1f}" y="{Y(lp[1]):.1f}" fill="{col}" font-size="14" '
                 f'font-family="sans-serif" font-weight="600" text-anchor="middle" '
                 f'dominant-baseline="middle">{lab}</text>')
    for k in names:
        o.append(f'<circle cx="{X(P[k][0]):.1f}" cy="{Y(P[k][1]):.1f}" r="3.4" fill="{COL["pt"]}"/>')
        if k in plabels:
            o.append(f'<text x="{X(pt_lab[k][0]):.1f}" y="{Y(pt_lab[k][1]):.1f}" fill="{COL["pt"]}" '
                     f'font-size="13.5" font-family="sans-serif" font-weight="700" '
                     f'text-anchor="middle" dominant-baseline="middle">{plabels[k]}</text>')
    o.append(f'<text x="{pad+2}" y="{H-7:.0f}" fill="{COL["ground"]}" font-size="11.5" '
             f'font-family="sans-serif">{caption}</text>')
    o.append("</svg>")
    write(fname, o)


def four_bar_omega(a, b, c, t2, t3, t4, w2=1.0):
    """Coupler and follower angular velocities from the velocity loop."""
    w3 = a * w2 * np.sin(t4 - t2) / (b * np.sin(t3 - t4))
    w4 = a * w2 * np.sin(t2 - t3) / (c * np.sin(t4 - t3))
    return w3, w4


# ----------------------------------------------------------------------------
# XY plots (cam SVAJ diagrams, pressure-angle curves) and the cam profile
# ----------------------------------------------------------------------------
def xy_plot(curves, xr, yr, xlabel, ylabel, caption, fname, aria, hlines=None):
    """curves: list of (xs, ys, colour, label). xr/yr: (min, max) axis ranges."""
    W, H = 470, 300
    ml, mr, mt, mb = 48, 16, 42, 46
    pw, ph = W - ml - mr, H - mt - mb
    xmin, xmax = xr
    ymin, ymax = yr
    MX = lambda x: ml + (x - xmin) / (xmax - xmin) * pw
    MY = lambda y: (H - mb) - (y - ymin) / (ymax - ymin) * ph
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="{aria}">', plate(W, H)]
    # axes box
    o.append(f'<rect x="{ml}" y="{mt}" width="{pw}" height="{ph}" fill="none" '
             f'stroke="{COL["con"]}" stroke-width="1"/>')
    if ymin < 0 < ymax:                                   # zero line
        o.append(f'<line x1="{ml}" y1="{MY(0):.1f}" x2="{W-mr}" y2="{MY(0):.1f}" '
                 f'stroke="{COL["con"]}" stroke-width="1" stroke-dasharray="3 3"/>')
    for (val, lab) in (hlines or []):                     # horizontal guide lines
        o.append(f'<line x1="{ml}" y1="{MY(val):.1f}" x2="{W-mr}" y2="{MY(val):.1f}" '
                 f'stroke="{COL["pt"]}" stroke-width="1" stroke-dasharray="5 3"/>')
        o.append(f'<text x="{W-mr-2:.0f}" y="{MY(val)-3:.1f}" fill="{COL["pt"]}" font-size="10.5" '
                 f'font-family="sans-serif" text-anchor="end">{lab}</text>')
    for (xs, ys, col, lab) in curves:
        pts = " ".join(f"{MX(x):.1f},{MY(y):.1f}" for x, y in zip(xs, ys))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.4"/>')
    # legend (top, inside plate above the box)
    lx = ml + 6
    for (xs, ys, col, lab) in curves:
        o.append(f'<line x1="{lx:.0f}" y1="{mt-14}" x2="{lx+18:.0f}" y2="{mt-14}" stroke="{col}" stroke-width="2.6"/>')
        o.append(f'<text x="{lx+22:.0f}" y="{mt-10}" fill="{COL["pt"]}" font-size="11.5" font-family="sans-serif">{lab}</text>')
        lx += 26 + len(re.sub(r"&#\d+;|<[^>]+>", "x", lab)) * 6.6
    o.append(f'<text x="{ml+pw/2:.0f}" y="{H-8}" fill="{COL["ground"]}" font-size="11.5" '
             f'font-family="sans-serif" text-anchor="middle">{xlabel}</text>')
    o.append(f'<text x="14" y="{mt+ph/2:.0f}" fill="{COL["ground"]}" font-size="11.5" '
             f'font-family="sans-serif" text-anchor="middle" transform="rotate(-90 14 {mt+ph/2:.0f})">{ylabel}</text>')
    o.append(f'<text x="{ml}" y="{H-26}" fill="{COL["ground"]}" font-size="10.5" '
             f'font-family="sans-serif">{caption}</text>')
    o.append("</svg>")
    write(fname, o)


def cam_profile(Rb, h, beta_deg, fname):
    """Radial-follower cam pitch curve for a cycloidal rise-dwell-fall-dwell
    programme (each segment beta_deg). Pitch radius = Rb + s(theta)."""
    beta = np.radians(beta_deg)
    def cyc(t):
        return h * (t / beta - np.sin(2 * np.pi * t / beta) / (2 * np.pi))
    def s_of(thd):
        t = np.radians(thd) % (2 * np.pi)
        if t < beta: return cyc(t)
        if t < 2 * beta: return h
        if t < 3 * beta: return h - cyc(t - 2 * beta)
        return 0.0
    Rmax = Rb + h
    sc = 120.0 / Rmax
    pad, cap = 30, 22
    span = Rmax * sc
    W = 2 * span + 2 * pad + 70
    H = 2 * span + 2 * pad + cap
    cx, cy = pad + span, pad + span
    PX = lambda r, t: cx + r * sc * np.cos(t)
    PY = lambda r, t: cy - r * sc * np.sin(t)
    o = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Cam pitch profile for a cycloidal rise-dwell-fall-dwell programme">',
         plate(W, H)]
    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{Rb*sc:.1f}" fill="none" '
             f'stroke="{COL["con"]}" stroke-width="1.4" stroke-dasharray="5 4"/>')
    ts = np.radians(np.arange(0, 361, 2))
    pts = " ".join(f"{PX(Rb+s_of(np.degrees(t)),t):.1f},{PY(Rb+s_of(np.degrees(t)),t):.1f}" for t in ts)
    o.append(f'<polyline points="{pts}" fill="none" stroke="{COL["coupler"]}" stroke-width="2.6"/>')
    for thd, lab in [(0, "0&#176;"), (90, "90&#176;"), (180, "180&#176;"), (270, "270&#176;")]:
        t = np.radians(thd); R = Rb + s_of(thd)
        o.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{PX(R,t):.1f}" y2="{PY(R,t):.1f}" '
                 f'stroke="{COL["ground"]}" stroke-width="1" stroke-dasharray="2 3"/>')
        o.append(f'<text x="{PX(R+6,t):.1f}" y="{PY(R+6,t):.1f}" fill="{COL["pt"]}" font-size="11.5" '
                 f'font-family="sans-serif" text-anchor="middle" dominant-baseline="middle">{lab}</text>')
    o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{COL["pt"]}"/>')
    o.append(f'<text x="{cx+Rb*sc*0.35:.1f}" y="{cy-6:.1f}" fill="{COL["con"]}" font-size="11" '
             f'font-family="sans-serif">base circle</text>')
    o.append(f'<text x="{pad}" y="{H-7:.0f}" fill="{COL["ground"]}" font-size="11.5" '
             f'font-family="sans-serif">Pitch curve R = R&#8347; + s(&#952;).  R&#8347; = {Rb:.0f}, h = {h:.0f} mm.</text>')
    o.append("</svg>")
    write(fname, o)


def scissor_space(L, theta_deg, fname):
    """Single-stage symmetric scissor: two crossed arms between base and platform."""
    th = np.radians(theta_deg)
    span, h = L * np.cos(th), L * np.sin(th)
    BL, BR = np.array([0.0, 0.0]), np.array([span, 0.0])
    TL, TR = np.array([0.0, h]), np.array([span, h])
    Cc = np.array([span / 2, h / 2])

    sc, m, cap = 1.55, 50, 20
    xmin, xmax = -18, span + 40
    ymin, ymax = -14, h + 18
    W = (xmax - xmin) * sc + 2 * m
    H = (ymax - ymin) * sc + 2 * m + cap
    X = lambda x: m + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def L_(p, q, col, w=2.6, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{col}" stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def pin(p, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>'
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} L {cx+7:.1f} {cy+9:.1f} Z" '
                  f'fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def T(p, txt, col, dx, dy, sz=14):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{col}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')

    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Single-stage scissor lift at {theta_deg:.0f} degrees">',
         plate(W, H),
         L_(BL, BR, COL["ground"], 3),                     # base
         L_(TL, TR, COL["follower"], 3),                   # platform
         L_(BL, TR, COL["coupler"]), L_(BR, TL, COL["coupler"]),   # crossed arms
         pin(BL, True), pin(BR), pin(TL), pin(TR),
         f'<circle cx="{X(Cc[0]):.1f}" cy="{Y(Cc[1]):.1f}" r="4" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>',
         # vertical height dimension on the right
         f'<line x1="{X(span+26):.1f}" y1="{Y(0):.1f}" x2="{X(span+26):.1f}" y2="{Y(h):.1f}" '
         f'stroke="{COL["pt"]}" stroke-width="1"/>',
         T(np.array([span + 26, h / 2]), "h", COL["pt"], 4, 4),
         T((BL + TR) / 2, "L", COL["coupler"], 6, -4),
         T(BL, "&#952;", COL["pt"], 12, -8),
         T(np.array([span / 2, 0]), "base", COL["ground"], -16, 18, 12),
         T(np.array([span / 2, h]), "platform", COL["follower"], -22, -10, 12),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Choose a length scale, e.g. 1 cm = 40 mm. L = {L} mm, &#952; = {theta_deg:.0f}&#176;, '
         f'h = L sin&#952; = {h:.0f} mm.</text>',
         "</svg>"]
    write(fname, g)


def toggle_skeleton(fname):
    """Schematic four-bar at the over-centre (toggle) position: handle and main
    link collinear. Lengths are representative, chosen to show the geometry."""
    O2, O4 = np.array([0.0, 0.0]), np.array([90.0, 0.0])
    ang = np.radians(70)
    A = O2 + 40 * np.array([np.cos(ang), np.sin(ang)])     # handle pivot to joint A
    B = A + 80 * np.array([np.cos(ang), np.sin(ang)])      # main link, COLLINEAR with handle
    ext = B + 18 * np.array([np.cos(ang), np.sin(ang)])    # dashed collinear extension

    sc, m, cap = 2.0, 50, 20
    xs = [O2[0], O4[0], A[0], B[0]]
    ys = [O2[1], O4[1], A[1], B[1]]
    xmin, xmax = min(xs) - 16, max(xs) + 60
    ymin, ymax = min(ys) - 14, max(ys) + 20
    W = (xmax - xmin) * sc + 2 * m
    H = (ymax - ymin) * sc + 2 * m + cap
    X = lambda x: m + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def L_(p, q, col, w=2.6, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{col}" stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def pin(p, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>'
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} L {cx+7:.1f} {cy+9:.1f} Z" '
                  f'fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def T(p, txt, col, dx, dy, sz=14):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{col}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')

    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Toggle clamp four-bar skeleton at the over-centre position">',
         plate(W, H),
         L_(O2, O4, COL["ground"], 2, "6 4"),               # ground
         L_(B, ext, COL["con"], 1.4, "3 3"),                # collinear extension
         L_(O2, A, COL["crank"]),                           # handle
         L_(A, B, COL["coupler"]),                          # main link (collinear with handle)
         L_(O4, B, COL["follower"]),                        # clamp arm
         pin(O2, True), pin(O4, True), pin(A), pin(B),
         T((O2 + A) / 2, "handle", COL["crank"], -64, 2, 13),
         T((A + B) / 2, "main link", COL["coupler"], 8, -2, 13),
         T((O4 + B) / 2, "clamp arm", COL["follower"], 8, 0, 13),
         T(O2, sub("O", "2"), COL["pt"], -22, 14), T(O4, sub("O", "4"), COL["pt"], 2, 16),
         T(A, "A", COL["pt"], 8, 4), T(B, "B", COL["pt"], 8, -2),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Toggle position: handle and main link are collinear.</text>',
         "</svg>"]
    write(fname, g)


def quick_return_space(r, AC, AP, fname):
    """Crank-and-slotted-lever quick-return (a slider-crank inversion, the shaper drive).

    Fulcrum A (fixed) below, crank centre C (fixed) above it at distance AC, crank radius r.
    The extreme lever positions are the two tangents from A to the crank circle: at each,
    the crank CB is perpendicular to the lever AB (right angle at the tangent point), so
    sin(phi) = r/AC with phi the lever half-swing. The tool arm AP carries the tool end,
    whose two extremes R1, R2 bound the stroke.
    """
    A = np.array([0.0, 0.0])
    C = np.array([0.0, AC])
    phi = np.arcsin(r / AC)
    dR = np.array([np.sin(phi), np.cos(phi)])
    dL = np.array([-np.sin(phi), np.cos(phi)])
    ABlen = AC * np.cos(phi)
    B1, B2 = A + ABlen * dR, A + ABlen * dL          # tangent points (crank pin extremes)
    P1, P2 = A + AP * dR, A + AP * dL                # tool-end extremes R1, R2
    ang_deg = np.degrees(2 * phi)

    sc, m, cap = 0.92, 52, 22
    xs = [P1[0], P2[0], 0]; ys = [0, AP * np.cos(phi), AC + r]
    xmin, xmax = min(xs) - 18, max(xs) + 18
    ymin, ymax = min(ys) - 16, max(ys) + 18
    W = max((xmax - xmin) * sc + 2 * m, 548)
    H = (ymax - ymin) * sc + 2 * m + cap
    xoff = (W - ((xmax - xmin) * sc + 2 * m)) / 2
    X = lambda x: m + xoff + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def L(p, q, col, w=2.6, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{col}" stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def pin(p, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>'
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} L {cx+7:.1f} {cy+9:.1f} Z" '
                  f'fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def T(p, txt, col, dx, dy, sz=14):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{col}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')

    cx, cy, rp = X(C[0]), Y(C[1]), r * sc
    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Quick-return shaper: crank circle and the two extreme lever positions">',
         plate(W, H),
         f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rp:.1f}" fill="none" stroke="{COL["crank"]}" stroke-width="2"/>',
         L(A, C, COL["con"], 1.4, "3 3"),                 # line of centres AC (mean lever)
         L(A, P1, COL["follower"]), L(A, P2, COL["follower"], 2.6, "7 5"),  # extreme lever positions
         L(P1, P2, COL["piston"], 2.4),                   # tool stroke line R1R2
         L(C, B1, COL["crank"], 2.0), L(C, B2, COL["crank"], 2.0, "4 3"),   # crank at the two extremes
         pin(A, True), pin(C, True),
         f'<circle cx="{X(B1[0]):.1f}" cy="{Y(B1[1]):.1f}" r="3.5" fill="{COL["crank"]}"/>',
         f'<circle cx="{X(B2[0]):.1f}" cy="{Y(B2[1]):.1f}" r="3.5" fill="{COL["crank"]}"/>',
         T(A, "A", COL["pt"], -20, 16), T(C, "C", COL["pt"], 8, 4),
         T(B1, sub("B", "1"), COL["pt"], 6, -4), T(B2, sub("B", "2"), COL["pt"], -30, -4),
         T(P1, sub("R", "1"), COL["piston"], 6, -4), T(P2, sub("R", "2"), COL["piston"], -30, -4),
         T((C + B1) / 2, "r", COL["crank"], 6, 2), T((A + C) / 2, "AC", COL["con"], 6, 2, 12),
         T(C, "&#945;", COL["crank"], -6, 34, 15),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Scale: 1 cm = 40 mm.  r = {r:.0f}, AC = {AC:.0f}, AP = {AP:.0f} mm;  '
         f'swing 2&#966; = {ang_deg:.1f}&#176;.</text>',
         "</svg>"]
    write(fname, g)


def _skel_helpers(X, Y):
    def L(p, q, c, w=3.0, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{c}" stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def badge(p, num, col):
        return (f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="9.5" fill="#fff" '
                f'stroke="{col}" stroke-width="2"/><text x="{X(p[0]):.1f}" y="{Y(p[1])+4:.1f}" '
                f'fill="{col}" font-size="12.5" font-family="sans-serif" font-weight="700" '
                f'text-anchor="middle">{num}</text>')

    def joint(p, lab, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.6" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>'
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} L {cx+7:.1f} {cy+9:.1f} Z" '
                  f'fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def jlab(p, lab, dx, dy):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{COL["pt"]}" font-size="12.5" '
                f'font-family="sans-serif" font-weight="700">{lab}</text>')

    def T(p, txt, c, dx, dy, sz=14):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{c}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')
    return L, badge, joint, jlab, T


def four_bar_skeleton(fname):
    """Kinematic skeleton for mobility counting: 4 links, 4 revolute joints."""
    O2, O4 = np.array([0.0, 0.0]), np.array([100.0, 0.0])
    A = O2 + 40 * np.array([np.cos(np.radians(60)), np.sin(np.radians(60))])
    B = O4 + 80 * np.array([np.cos(np.radians(64.94)), np.sin(np.radians(64.94))])
    sc, m, cap = 1.9, 46, 22
    xs, ys = [O2[0], O4[0], A[0], B[0]], [O2[1], O4[1], A[1], B[1]]
    xmin, xmax = min(xs) - 26, max(xs) + 30
    ymin, ymax = min(ys) - 24, max(ys) + 28
    W = max((xmax - xmin) * sc + 2 * m, 560)
    H = (ymax - ymin) * sc + 2 * m + cap
    xoff = (W - ((xmax - xmin) * sc + 2 * m)) / 2
    X = lambda x: m + xoff + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc
    L, badge, joint, jlab, T = _skel_helpers(X, Y)
    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Four-bar kinematic skeleton: four links numbered 1 to 4 and four revolute joints">',
         plate(W, H),
         L(O2, O4, COL["ground"], 3.0, "7 5"), L(O2, A, COL["crank"]),
         L(A, B, COL["coupler"]), L(O4, B, COL["follower"]),
         joint(O2, "R", True), joint(O4, "R", True), joint(A, "R"), joint(B, "R"),
         jlab(O2, "R", -22, -8), jlab(O4, "R", 8, -8), jlab(A, "R", -20, -6), jlab(B, "R", 10, -4),
         badge((O2 + O4) / 2, "1", COL["ground"]), badge((O2 + A) / 2, "2", COL["crank"]),
         badge((A + B) / 2, "3", COL["coupler"]), badge((O4 + B) / 2, "4", COL["follower"]),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Four-bar: 4 links (1 = ground), 4 revolute (R) joints. '
         f'DOF = 3(4-1) - 2(4) = 1.</text>',
         "</svg>"]
    write(fname, g)


def slider_crank_skeleton(fname):
    """Kinematic skeleton: 4 links, 3 revolute joints and 1 prismatic (slider) joint."""
    O = np.array([0.0, 0.0])
    A = 50 * np.array([np.cos(np.radians(60)), np.sin(np.radians(60))])
    s = 50 * np.cos(np.radians(60)) + np.sqrt(150 ** 2 - (50 * np.sin(np.radians(60))) ** 2)
    B = np.array([s, 0.0])
    sc, m, cap = 1.9, 46, 22
    xs, ys = [O[0], A[0], B[0]], [O[1], A[1], B[1]]
    xmin, xmax = min(xs) - 22, max(xs) + 34
    ymin, ymax = min(ys) - 26, max(ys) + 30
    W = max((xmax - xmin) * sc + 2 * m, 570)
    H = (ymax - ymin) * sc + 2 * m + cap
    xoff = (W - ((xmax - xmin) * sc + 2 * m)) / 2
    X = lambda x: m + xoff + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc
    L, badge, joint, jlab, T = _skel_helpers(X, Y)
    bx, by = X(B[0]), Y(B[1])
    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Slider-crank kinematic skeleton: four links, three revolute joints and one prismatic slider joint">',
         plate(W, H),
         f'<line x1="{X(xmin+6):.1f}" y1="{Y(0):.1f}" x2="{X(xmax-4):.1f}" y2="{Y(0):.1f}" '
         f'stroke="{COL["ground"]}" stroke-width="3.0" stroke-dasharray="7 5"/>',
         L(O, A, COL["crank"]), L(A, B, COL["rod"]),
         f'<rect x="{bx-13:.1f}" y="{by-11:.1f}" width="26" height="22" rx="3" fill="none" '
         f'stroke="{COL["piston"]}" stroke-width="2.6"/>',
         joint(O, "R", True), joint(A, "R"),
         f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="4.2" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>',
         jlab(O, "R", -22, 18), jlab(A, "R", -20, -6), jlab(B, "R", -4, -14),
         f'<text x="{bx+18:.1f}" y="{by+5:.1f}" fill="{COL["pt"]}" font-size="12.5" '
         f'font-family="sans-serif" font-weight="700">P</text>',
         badge((O + A) / 2, "2", COL["crank"]), badge((A + B) / 2, "3", COL["rod"]),
         badge((B + np.array([28, 0])), "4", COL["piston"]),
         badge(np.array([(xmin + xmax) / 2, ymin + 8]), "1", COL["ground"]),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Slider-crank: 4 links, 3 revolute (R) + 1 prismatic (P). '
         f'DOF = 3(4-1) - 2(4) = 1.</text>',
         "</svg>"]
    write(fname, g)


def four_bar_accel_polygon(fname):
    """Full four-bar acceleration polygon at theta2 = 120 deg: crank centripetal,
    coupler and follower normals from the pole, and the two tangentials meeting at b'."""
    a, b, c, d = 40.0, 120.0, 80.0, 100.0
    t2, t3, t4 = np.radians(120), np.radians(21.96), np.radians(96.25)
    O2, O4 = np.array([0.0, 0.0]), np.array([d, 0.0])
    A = O2 + a * np.array([np.cos(t2), np.sin(t2)])
    B = O4 + c * np.array([np.cos(t4), np.sin(t4)])
    w3, w4 = four_bar_omega(a, b, c, t2, t3, t4)
    U = lambda v: v / (np.hypot(*v) or 1)
    Mv = np.array([[-b * np.sin(t3), c * np.sin(t4)], [b * np.cos(t3), -c * np.cos(t4)]])
    al3, al4 = np.linalg.solve(Mv, np.array([
        a * np.cos(t2) + b * w3**2 * np.cos(t3) - c * w4**2 * np.cos(t4),
        a * np.sin(t2) + b * w3**2 * np.sin(t3) - c * w4**2 * np.sin(t4)]))
    o = np.array([0.0, 0.0])
    aA = 1.0**2 * a * U(O2 - A)                       # crank centripetal, o -> a'
    n = aA + w3**2 * b * U(A - B)                     # + coupler normal, a' -> n
    perpc = U(np.array([-(B - A)[1], (B - A)[0]]))
    bp = n + al3 * b * perpc                          # + coupler tangential, n -> b'
    m = w4**2 * c * U(O4 - B)                         # follower normal from pole, o -> m

    sc, mg, cap = 7.0, 54, 24
    xs = [o[0], aA[0], n[0], m[0], bp[0]]; ys = [o[1], aA[1], n[1], m[1], bp[1]]
    xmin, xmax = min(xs) - 12, max(xs) + 16
    ymin, ymax = min(ys) - 10, max(ys) + 12
    W = max((xmax - xmin) * sc + 2 * mg, 560)
    H = (ymax - ymin) * sc + 2 * mg + cap
    xoff = (W - ((xmax - xmin) * sc + 2 * mg)) / 2
    X = lambda x: mg + xoff + (x - xmin) * sc
    Y = lambda y: H - mg - cap - (y - ymin) * sc
    cols = [COL["crank"], COL["coupler"], COL["follower"], COL["pt"]]

    def arr(p, q, col, w=2.6, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{col}" stroke-width="{w}"{dd} '
                f'marker-end="url(#m{col[1:]})"/>')

    def dot(p, c=COL["pt"], rr=3.4):
        return f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="{rr}" fill="{c}"/>'

    def T(p, txt, c, dx, dy, sz=13.5):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{c}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')

    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Four-bar acceleration polygon: crank centripetal, coupler and follower normals from the pole, and the two tangentials meeting at b prime">'
         f'<defs>{arrowheads(cols)}</defs>',
         plate(W, H),
         arr(o, bp, COL["pt"], 1.6, "5 4"),                        # resultant a_B (dashed)
         arr(o, aA, COL["crank"]),                                 # crank centripetal
         arr(aA, n, COL["coupler"]),                               # coupler normal (small)
         arr(n, bp, COL["coupler"]),                               # coupler tangential
         arr(o, m, COL["follower"]),                               # follower normal
         arr(m, bp, COL["follower"]),                              # follower tangential
         dot(o), dot(aA), dot(n, COL["coupler"]), dot(m, COL["follower"]), dot(bp),
         T(o, "o&#8242;", COL["pt"], -22, 4), T(aA, "a&#8242;", COL["pt"], 11, 8),
         T(bp, "b&#8242;", COL["pt"], 9, 4), T(m, "m", COL["pt"], -16, 2), T(n, "n", COL["coupler"], -14, 12),
         T((o + aA) / 2, sub("a", "A"), COL["crank"], -26, -2, 13),
         T((o + m) / 2, sup("a", "n"), COL["follower"], -24, 0, 12.5),
         T((m + bp) / 2, sup("a", "t"), COL["follower"], -4, 16, 12.5),
         T((n + bp) / 2, sup("a", "t"), COL["coupler"], 8, 2, 12.5),
         T((aA + n) / 2, sup("a", "n"), COL["coupler"], -20, 6, 12),
         T((o + bp) / 2, sub("a", "B"), COL["pt"], 8, -4, 12.5),
         f'<text x="{mg}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Coupler and follower normals from o&#8242;; the two tangentials '
         f'meet at b&#8242;.  &#952;&#8322; = 120&#176;.</text>',
         "</svg>"]
    write(fname, g)


def _qr_kin(theta_deg, r, AC, AP, w2=1.0):
    """Full velocity and acceleration state of the crank-and-slotted-lever
    quick-return at one crank angle. A fulcrum at origin, C crank centre above."""
    A = np.array([0.0, 0.0]); C = np.array([0.0, AC])
    th = np.radians(theta_deg)
    B = C + r * np.array([np.cos(th), np.sin(th)])
    d = float(np.linalg.norm(B - A)); u = (B - A) / d
    perp = np.array([-u[1], u[0]])
    cz = lambda w, v: np.array([-w * v[1], w * v[0]])
    vBc = cz(w2, B - C)                      # velocity of B as a point on the crank
    wL = float(np.dot(vBc, perp) / d)        # lever angular velocity
    vslip = float(np.dot(vBc, u))            # slip speed of block along the slot
    b3 = wL * cz(1.0, B - A)                 # velocity image of coincident lever point
    P = A + AP * u
    vP = cz(wL, P - A)
    aBc = -w2 ** 2 * (B - C)                 # accel of B on crank (alpha2 = 0)
    aN = -wL ** 2 * (B - A)                  # centripetal of coincident lever point
    cor = 2.0 * wL * cz(1.0, vslip * u)      # Coriolis
    rhs = aBc - aN - cor
    kxBA = cz(1.0, B - A)
    M = np.array([[kxBA[0], u[0]], [kxBA[1], u[1]]])
    alphaL, a_s = np.linalg.solve(M, rhs)
    aT = alphaL * kxBA
    return dict(A=A, C=C, B=B, P=P, d=d, u=u, perp=perp, wL=wL, vslip=vslip,
                vBc=vBc, b3=b3, vP=vP, aBc=aBc, aN=aN, aT=aT, cor=cor,
                a_slip=a_s * u, alphaL=float(alphaL), a_s=float(a_s))


def quick_return_config(theta_deg, r, AC, AP, fname):
    """Shaper drive at one crank angle: crank CB, slotted lever A-P, sliding block at B."""
    k = _qr_kin(theta_deg, r, AC, AP)
    A, C, B, P, u, perp = k["A"], k["C"], k["B"], k["P"], k["u"], k["perp"]
    sc, m, cap = 0.9, 52, 22
    xs = [A[0], C[0] - r, C[0] + r, B[0], P[0]]
    ys = [A[1], C[1] + r, B[1], P[1]]
    xmin, xmax = min(xs) - 20, max(xs) + 90
    ymin, ymax = min(ys) - 16, max(ys) + 20
    W = max((xmax - xmin) * sc + 2 * m, 560)
    H = (ymax - ymin) * sc + 2 * m + cap
    xoff = (W - ((xmax - xmin) * sc + 2 * m)) / 2
    X = lambda x: m + xoff + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def L(p, q, c, w=2.6, dash=""):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" '
                f'y2="{Y(q[1]):.1f}" stroke="{c}" stroke-width="{w}"{dd} stroke-linecap="round"/>')

    def pin(p, fixed=False):
        cx, cy = X(p[0]), Y(p[1])
        t = f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>'
        if fixed:
            t += (f'<path d="M {cx-7:.1f} {cy+9:.1f} L {cx:.1f} {cy:.1f} L {cx+7:.1f} {cy+9:.1f} Z" '
                  f'fill="none" stroke="{COL["pt"]}" stroke-width="1.5"/>'
                  f'<line x1="{cx-10:.1f}" y1="{cy+9:.1f}" x2="{cx+10:.1f}" y2="{cy+9:.1f}" '
                  f'stroke="{COL["pt"]}" stroke-width="1.5"/>')
        return t

    def T(p, txt, c, dx, dy, sz=14):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{c}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')

    # sliding block: small square aligned with the slot
    hu, hp = 9.0 * u, 9.0 * perp
    c1, c2, c3, c4 = B + hu + hp, B + hu - hp, B - hu - hp, B - hu + hp
    block = (f'<path d="M {X(c1[0]):.1f} {Y(c1[1]):.1f} L {X(c2[0]):.1f} {Y(c2[1]):.1f} '
             f'L {X(c3[0]):.1f} {Y(c3[1]):.1f} L {X(c4[0]):.1f} {Y(c4[1]):.1f} Z" '
             f'fill="{COL["rod"]}" fill-opacity="0.25" stroke="{COL["rod"]}" stroke-width="2"/>')
    ram_y = P[1]
    ram_r = np.array([P[0] + 70, ram_y])
    g = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Quick-return shaper at crank angle {theta_deg:.0f} degrees: crank CB, slotted lever A to P, sliding block at B">',
         plate(W, H),
         f'<circle cx="{X(C[0]):.1f}" cy="{Y(C[1]):.1f}" r="{r*sc:.1f}" fill="none" '
         f'stroke="{COL["con"]}" stroke-width="1.4" stroke-dasharray="3 3"/>',
         L(A, P, COL["follower"], 5.0),                       # slotted lever body
         L(A, P, "#ffffff", 1.6, "2 5"),                      # the slot inside it
         L(C, B, COL["crank"], 2.8),                          # crank
         block,
         L(P, ram_r, COL["ground"], 2.0),                     # connector to ram
         f'<rect x="{X(ram_r[0]):.1f}" y="{Y(ram_r[1])-13:.1f}" width="26" height="26" rx="3" '
         f'fill="none" stroke="{COL["ground"]}" stroke-width="2.2"/>',
         f'<line x1="{X(ram_r[0])-6:.1f}" y1="{Y(ram_r[1])+22:.1f}" x2="{X(ram_r[0])+32:.1f}" '
         f'y2="{Y(ram_r[1])+22:.1f}" stroke="{COL["ground"]}" stroke-width="1.6" '
         f'marker-start="url(#mg)" marker-end="url(#mg)"/>',
         f'<defs><marker id="mg" markerWidth="9" markerHeight="9" refX="4" refY="3" orient="auto">'
         f'<path d="M8,0 L0,3 L8,6 Z" fill="{COL["ground"]}"/></marker></defs>',
         pin(A, True), pin(C, True),
         f'<circle cx="{X(B[0]):.1f}" cy="{Y(B[1]):.1f}" r="3.6" fill="{COL["pt"]}"/>',
         f'<circle cx="{X(P[0]):.1f}" cy="{Y(P[1]):.1f}" r="4" fill="#fff" stroke="{COL["pt"]}" stroke-width="2"/>',
         T(A, "A", COL["pt"], -20, 16), T(C, "C", COL["pt"], 8, 4),
         T(B, "B", COL["pt"], 10, 0), T(P, "P", COL["pt"], -6, -8),
         T((C + B) / 2, "r", COL["crank"], 4, -4, 12),
         T(ram_r, "ram", COL["ground"], 2, 34, 12),
         f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11.5" '
         f'font-family="sans-serif">Block B slides in slot A-P; ram driven from P.  '
         f'r = {r:.0f}, AC = {AC:.0f}, AP = {AP:.0f} mm.</text>',
         "</svg>"]
    write(fname, g)


def slider_crank_rod_image(fname):
    """Velocity image of the connecting rod: line a-b, its midpoint g, and the
    least-velocity point q (foot of the perpendicular from the pole o)."""
    r, l, th, w2 = 50.0, 150.0, np.radians(60), 1.0
    cz = lambda w, v: np.array([-w * v[1], w * v[0]])
    A = r * np.array([np.cos(th), np.sin(th)])
    s = r * np.cos(th) + np.sqrt(l ** 2 - (r * np.sin(th)) ** 2)
    B = np.array([s, 0.0])
    vA = cz(w2, A); w3 = -vA[1] / (B - A)[0]; vB = vA + cz(w3, B - A)
    o = np.array([0.0, 0.0]); a = vA; b = vB; ab = b - a
    t = float(np.dot(o - a, ab) / np.dot(ab, ab)); q = a + t * ab; g = (a + b) / 2

    sc, m, cap = 3.6, 48, 24
    xs = [o[0], a[0], b[0]]; ys = [o[1], a[1], b[1]]
    xmin, xmax = min(xs) - 12, max(xs) + 14
    ymin, ymax = min(ys) - 7, max(ys) + 10
    W = max((xmax - xmin) * sc + 2 * m, 516)
    H = (ymax - ymin) * sc + 2 * m + cap
    xoff = (W - ((xmax - xmin) * sc + 2 * m)) / 2
    X = lambda x: m + xoff + (x - xmin) * sc
    Y = lambda y: H - m - cap - (y - ymin) * sc

    def ln(p, qq, c, w=2.6, dash="", arrow=False):
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        mk = f' marker-end="url(#m{c[1:]})"' if arrow else ""
        return (f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(qq[0]):.1f}" '
                f'y2="{Y(qq[1]):.1f}" stroke="{c}" stroke-width="{w}"{dd}{mk} stroke-linecap="round"/>')

    def dot(p, c=COL["pt"], rr=3.6):
        return f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="{rr}" fill="{c}"/>'

    def T(p, txt, c, dx, dy, sz=13.5):
        return (f'<text x="{X(p[0])+dx:.1f}" y="{Y(p[1])+dy:.1f}" fill="{c}" font-size="{sz}" '
                f'font-family="sans-serif" font-weight="600">{txt}</text>')

    cols = [COL["crank"], COL["rod"], COL["follower"]]
    g_ = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" width="100%" xmlns="http://www.w3.org/2000/svg" '
          f'role="img" aria-label="Slider-crank velocity image of the connecting rod with the least-velocity point">'
          f'<defs>{arrowheads(cols)}</defs>',
          plate(W, H),
          ln(o, a, COL["crank"], 2.6, "", True),
          ln(a, b, COL["rod"], 3.0, "", True),
          ln(o, b, COL["follower"], 2.6, "", True),
          ln(o, g, COL["con"], 1.5, "4 3"),
          ln(o, q, COL["pt"], 1.5, "5 3"),
          dot(o), dot(a), dot(b), dot(g, COL["rod"]), dot(q, COL["pt"]),
          T(o, "o (pole)", COL["pt"], -6, 17),
          T(a, "a", COL["pt"], -15, -4), T(b, "b", COL["pt"], -4, 17),
          T(g, "g", COL["rod"], 8, -5), T(q, "q", COL["pt"], -16, 4),
          T((o + a) / 2, sub("v", "A"), COL["crank"], -18, 2, 13),
          T(a + 0.26 * (b - a), sub("v", "B/A"), COL["rod"], 8, -3, 13),
          T((o + b) / 2, sub("v", "B"), COL["follower"], -4, 16, 13),
          f'<text x="{m}" y="{H-6:.0f}" fill="{COL["ground"]}" font-size="11" '
          f'font-family="sans-serif">a b = rod velocity image; g = midpoint, '
          f'q = least-velocity point (v &#8776; 48.7 mm/s).</text>',
          "</svg>"]
    write(fname, g_)


def quick_return_velocity_polygon(theta_deg, r, AC, AP, fname):
    k = _qr_kin(theta_deg, r, AC, AP)
    o, b2, b3 = (0.0, 0.0), tuple(k["vBc"]), tuple(k["b3"])
    vector_polygon(
        {"o": o, "b2": b2, "b3": b3},
        [("o", "b2", COL["crank"], sub("v", "B2")),
         ("o", "b3", COL["follower"], sub("v", "B3")),
         ("b3", "b2", COL["rod"], sub("v", "slip"))],
        {"o": "o", "b2": sub("b", "2"), "b3": sub("b", "3")},
        "Sliding-block triangle: v(B&#8322;) from the crank, v(B&#8323;) of the coincident lever "
        "point, v(slip) along the slot.  &#969;&#8322; = 1 rad/s.",
        fname, "Quick-return velocity polygon with the sliding-block slip vector", sc=3.0)


def quick_return_accel_polygon(theta_deg, r, AC, AP, fname):
    k = _qr_kin(theta_deg, r, AC, AP)
    o = np.array([0.0, 0.0])
    n = k["aN"]; t_end = n + k["aT"]; cor_end = t_end + k["cor"]; b2 = cor_end + k["a_slip"]
    vector_polygon(
        {"o": tuple(o), "n": tuple(n), "t": tuple(t_end), "c": tuple(cor_end), "b2": tuple(b2)},
        [("o", "n", COL["follower"], sup("a", "n")),
         ("n", "t", COL["crank"], sup("a", "t")),
         ("t", "c", "#7c3aed", "2&#969;v"),
         ("c", "b2", COL["ground"], sub("a", "slip"))],
        {"o": "o&#39;", "b2": sub("b", "2") + "&#39;"},
        "Coriolis term 2&#969;v = 70 mm/s&#178; (purple). The chain a&#8319; + a&#7511; + Coriolis "
        "+ a(slip) closes on the crank point acceleration.",
        fname, "Quick-return acceleration polygon showing the Coriolis component", sc=3.2)


# ----------------------------------------------------------------------------
# build every current figure
# ----------------------------------------------------------------------------
def main():
    quick_return_space(120, 300, 450, "l2-quick-return-space-diagram.svg")
    # Lesson 3/4 quick-return (shaper) at crank angle 300 deg
    quick_return_config(300, 120, 300, 450, "l3-quick-return-1-space-diagram.svg")
    quick_return_velocity_polygon(300, 120, 300, 450, "l3-quick-return-2-velocity-polygon.svg")
    quick_return_accel_polygon(300, 120, 300, 450, "l4-quick-return-accel-polygon.svg")
    slider_crank_rod_image("l3-slider-crank-3-rod-image.svg")
    # Lesson 1 mobility skeletons (numbered links, joint types)
    four_bar_skeleton("l1-four-bar-skeleton.svg")
    slider_crank_skeleton("l1-slider-crank-skeleton.svg")
    # Lesson 3, Application 1: slider-crank at theta = 60 deg (r = 50, l = 150)
    r, l, th = 50, 150, np.radians(60)
    slider_crank_space(r, l, 60, "l3-slider-crank-1-space-diagram.svg")
    vA = r * np.array([-np.sin(th), np.cos(th)])
    vB = np.array([-1.0168 * r, 0.0])                      # V_P/(r*omega) = -1.0168 at 60 deg
    velocity_polygon(
        {"o": (0, 0), "a": tuple(vA), "b": tuple(vB)},
        [("o", "a", COL["crank"], sub("v", "A")),
         ("a", "b", COL["rod"], sub("v", "B/A")),
         ("o", "b", COL["piston"], sub("v", "B"))],
        "velocity scale: choose e.g. 1 cm = 10 mm/s  (&#969; = 1 rad/s)",
        "l3-slider-crank-2-velocity-polygon.svg", "Slider-crank velocity polygon")

    # Lesson 3, Application 2: four-bar at theta2 = 120 deg (a40 b120 c80 d100)
    a, b, c, d = 40, 120, 80, 100
    t2, t3, t4 = np.radians(120), np.radians(21.96), np.radians(96.25)
    four_bar_space(a, b, c, d, 120, 21.96, 96.25, "l3-four-bar-1-space-diagram.svg")
    vA = a * np.array([-np.sin(t2), np.cos(t2)])
    w3, w4 = four_bar_omega(a, b, c, t2, t3, t4)
    vB = w4 * c * np.array([-np.sin(t4), np.cos(t4)])
    velocity_polygon(
        {"o": (0, 0), "a": tuple(vA), "b": tuple(vB)},
        [("o", "a", COL["crank"], sub("v", "A")),
         ("a", "b", COL["coupler"], sub("v", "B/A")),
         ("o", "b", COL["follower"], sub("v", "B"))],
        "velocity scale: choose e.g. 1 cm = 10 mm/s  (&#969;&#8322; = 1, &#952;&#8322; = 120&#176;)",
        "l3-four-bar-2-velocity-polygon.svg", "Four-bar velocity polygon at 120 degrees")

    # Lesson 3, Application 3: scissor lift at theta = 30 deg (L = 300, n = 1)
    scissor_space(300, 30, "l3-scissor-1-space-diagram.svg")

    # Lesson 3, Application 4: toggle clamp four-bar skeleton at top-dead-centre
    toggle_skeleton("l3-toggle-1-space-diagram.svg")

    # Lesson 2 (position): space diagrams the student draws to scale and measures
    four_bar_space(40, 120, 80, 100, 60, 18.38, 64.94, "l2-four-bar-space-diagram.svg")
    slider_crank_space(50, 150, 60, "l2-slider-crank-space-diagram.svg")
    scissor_space(300, 30, "l2-scissor-space-diagram.svg")
    toggle_skeleton("l2-toggle-space-diagram.svg")

    # Lesson 4 (acceleration): acceleration polygons (units mm/s^2, omega = 1 rad/s)
    unit = lambda v: v / (np.hypot(*v) or 1)
    aA = sub("a", "A"); aB = sub("a", "B")
    plab = {"o": "o&#8242;", "a": "a&#8242;", "b": "b&#8242;"}

    # crank-slider at theta = 60 deg
    r, l, w, th = 50.0, 150.0, 1.0, np.radians(60)
    O = np.array([0.0, 0.0]); A = r * np.array([np.cos(th), np.sin(th)])
    B = np.array([r * np.cos(th) + np.sqrt(l**2 - (r * np.sin(th))**2), 0.0])
    phi = np.arcsin((r / l) * np.sin(th))
    w3 = (r / l) * np.cos(th) / np.cos(phi) * w
    aA_v = w**2 * r * unit(O - A)               # centripetal of crank pin, A->O
    aBA_n = w3**2 * l * unit(A - B)             # normal of B relative to A, B->A
    aP = -r * w**2 * (np.cos(th) + (r / l) * np.cos(2 * th))
    aB_v = np.array([aP, 0.0])                  # piston accel, along the slide
    vector_polygon(
        {"o": (0, 0), "a": tuple(aA_v), "n": tuple(aA_v + aBA_n), "b": tuple(aB_v)},
        [("o", "a", COL["crank"], aA), ("a", "n", COL["rod"], sup("a", "n")),
         ("n", "b", COL["rod"], sup("a", "t")), ("o", "b", COL["piston"], aB)],
        plab, "acceleration scale: choose e.g. 1 cm = 10 mm/s&#178;  (&#969; = 1 rad/s, &#952; = 60&#176;)",
        "l4-slider-crank-accel-polygon.svg", "Slider-crank acceleration polygon at 60 degrees")

    # four-bar acceleration polygon at theta2 = 120 deg (bespoke, full two-tangential construction)
    four_bar_accel_polygon("l4-four-bar-accel-polygon.svg")

    # Lesson 5 (cam-follower): SVAJ diagram, cam profile, pressure-angle curves
    u = np.linspace(0, 1, 120)
    s_n = u - np.sin(2 * np.pi * u) / (2 * np.pi)
    v_n = (1 - np.cos(2 * np.pi * u)) / 2
    a_n = np.sin(2 * np.pi * u)
    xy_plot([(u, s_n, COL["crank"], "s / h"),
             (u, v_n, COL["follower"], "v / v_max"),
             (u, a_n, COL["coupler"], "a / a_max")],
            (0, 1), (-1.15, 1.15), "cam angle &#952; / &#946;", "normalised",
            "Cycloidal rise: s, v and a are all smooth and begin and end at zero.",
            "l5-svaj-cycloidal.svg", "Cycloidal rise displacement, velocity and acceleration diagram")

    cam_profile(45, 25, 90, "l5-cam-profile.svg")

    hh, bb = 25.0, np.radians(90)
    cyc_s = lambda t: hh * (t / bb - np.sin(2 * np.pi * t / bb) / (2 * np.pi))
    cyc_v = lambda t: (hh / bb) * (1 - np.cos(2 * np.pi * t / bb))
    thd = np.linspace(0, 90, 120)
    thr = np.radians(thd)
    phi30 = np.degrees(np.arctan(cyc_v(thr) / (30 + cyc_s(thr))))
    phi45 = np.degrees(np.arctan(cyc_v(thr) / (45 + cyc_s(thr))))
    xy_plot([(thd, phi30, COL["coupler"], "R_b = 30 mm"),
             (thd, phi45, COL["follower"], "R_b = 45 mm")],
            (0, 90), (0, 42), "cam angle into the rise (deg)", "pressure angle &#966; (deg)",
            "A larger base circle lowers the pressure angle below the 30 degree guide.",
            "l5-pressure-angle.svg", "Pressure angle versus cam angle for two base-circle radii",
            hlines=[(30, "30&#176; guide")])

    # Lesson 6 (force & synthesis): force triangle, transmission angle, actuator force
    Fl = 100 * np.array([np.cos(np.radians(70)), np.sin(np.radians(70))])
    Fp = np.array([0.0, -90.0])
    p1, p2 = Fl, Fl + Fp
    vector_polygon(
        {"o": (0, 0), "p": tuple(p1), "q": tuple(p2)},
        [("o", "p", COL["coupler"], sub("F", "link")),
         ("p", "q", COL["follower"], sub("F", "pad")),
         ("q", "o", COL["ground"], sub("F", "pivot"))],
        {}, "The three forces on a member close into a triangle. Choose a force scale, e.g. 1 cm = 20 N.",
        "l6-force-triangle.svg", "Force triangle for a three-force member", sc=2.0)

    def _fb(th2):
        a, b, c, d = 40.0, 120.0, 80.0, 100.0
        t2 = np.radians(th2)
        K1, K2 = d / a, d / c
        K3 = (a*a - b*b + c*c + d*d) / (2*a*c)
        A = np.cos(t2) - K1 - K2*np.cos(t2) + K3
        B = -2*np.sin(t2)
        C = K1 - (K2 + 1)*np.cos(t2) + K3
        t4 = 2*np.arctan2(-B - np.sqrt(B*B - 4*A*C), 2*A)
        K4 = d / b
        K5 = (c*c - d*d - a*a - b*b) / (2*a*b)
        D = np.cos(t2) - K1 + K4*np.cos(t2) + K5
        E = -2*np.sin(t2)
        F = K1 + (K4 - 1)*np.cos(t2) + K5
        t3 = 2*np.arctan2(-E - np.sqrt(E*E - 4*D*F), 2*D)
        return np.degrees(t3), np.degrees(t4)
    th2s = np.arange(0, 360, 3)
    mus = []
    for x in th2s:
        t3, t4 = _fb(x)
        mu = abs(t4 - t3) % 180
        mus.append(min(mu, 180 - mu))
    xy_plot([(th2s, np.array(mus), COL["follower"], "transmission angle")],
            (0, 360), (0, 90), "crank angle &#952;&#8322; (deg)", "transmission angle &#956; (deg)",
            "Transmission angle dips to about 26 deg twice per turn (poor-force zones).",
            "l6-transmission-angle.svg", "Four-bar transmission angle over a full crank rotation",
            hlines=[(40, "40&#176; guide")])

    ths = np.linspace(10, 85, 120)
    Fa = 500.0 / np.tan(np.radians(ths))
    xy_plot([(ths, Fa, COL["piston"], "actuator force")],
            (0, 90), (0, 3000), "scissor angle &#952; (deg)", "actuator force (N)",
            "Scissor actuator force F = W cot&#952; (W = 500 N): it spikes as the lift nears flat.",
            "l6-actuator-force.svg", "Scissor-lift actuator force versus angle")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Inter-event time distributions of the generated prostate cohort, measured vs. intended.

For each calibrated waiting time, extract the OBSERVED interval from the FHIR bundles
and plot its histogram against the module's intended Triangular density (and, where we
have one, the literature anchor from docs/prostate_zeitachse.md). This is the temporal
counterpart of the Sankey cross-check: it verifies that the emitted timestamps actually
follow the distributions the module claims.

Output: self-contained, theme-aware output/prostate_time_distributions.html (+ static SVG).
Stdlib only. Colors: dataviz default (series-1 blue for observed bars, ink for overlays),
palette validated earlier this session.
"""
import glob
import html
import json
import os
import sys
from datetime import datetime
from statistics import median

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FHIR_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'synthea', 'output', 'fhir')
OUT_HTML = os.path.join(REPO, 'output', 'prostate_time_distributions.html')
OUT_SVG = os.path.join(REPO, 'output', 'prostate_time_distributions.svg')

BLUE_L, BLUE_D = '#2a78d6', '#3987e5'


def dt(x):
    return datetime.fromisoformat(x)


def days(a, b):
    return (dt(b) - dt(a)).total_seconds() / 86400


def extract(bundle):
    """Per-bundle event timestamps needed for the intervals."""
    ev = {}
    meds = []
    for e in bundle.get('entry', []):
        r = e.get('resource', {})
        rt = r.get('resourceType')
        if rt == 'Condition':
            code = (r.get('code', {}).get('coding') or [{}])[0].get('code')
            t = r.get('onsetDateTime')
            if code == '399068003':
                ev.setdefault('dx', t)
            elif code == '1098981000119101':
                ev.setdefault('bcr', t)
        elif rt == 'Procedure':
            code = (r.get('code', {}).get('coding') or [{}])[0].get('code')
            t = (r.get('performedPeriod') or {}).get('start') or r.get('performedDateTime')
            key = {'410006001': 'dre', '429820004': 'trus', '236258004': 'biopsy',
                   '26294005': 'rp', '33195004': 'rt'}.get(code)
            if key and t:
                ev.setdefault(key, t)  # first occurrence
        elif rt == 'CarePlan':
            codes = {(act.get('detail') or {}).get('code', {}).get('coding', [{}])[0].get('code')
                     for act in r.get('activity', [])}
            codes |= {c.get('coding', [{}])[0].get('code') for c in r.get('category', [])}
            if '424313000' in codes:
                ev.setdefault('as_start', (r.get('period') or {}).get('start'))
        elif rt == 'MedicationRequest':
            codes = {c.get('code') for c in (r.get('medicationCodeableConcept') or {}).get('coding', [])}
            t = r.get('authoredOn')
            if t and codes & {'L02AE02'}:
                meds.append(('adt', t))
            if t and codes & {'L02BB04', 'L01CD02', 'L01CD04'}:
                meds.append(('line2', t))
    for kind in ('adt', 'line2'):
        ts = sorted(t for k, t in meds if k == kind)
        if ts:
            ev[kind] = ts[0]
    return ev if 'dx' in ev else None


# (key, title, unit-label, from-event, to-event, scale-to-unit, intended TRIANGULAR
#  in that unit or None, literature anchor (value, label) or None, x-max clip)
PANELS = [
    ('workup', 'Überweisung → Abklärung (DRE → TRUS)', 'Tage', 'dre', 'trus', 1.0,
     (7, 28, 80), None, 120),
    ('treat', 'Diagnose → Therapiebeginn (RP/RT)', 'Tage', 'dx', 'treat', 1.0,
     (5, 18, 45), ('71', 'US-Anker: median 71 d Diagnose→Therapie'), 120),
    ('biopsy_rp', 'Biopsie → Radikale Prostatektomie', 'Tage', 'biopsy', 'rp', 1.0,
     None, ('77', 'Literatur-Anker: median 77 d (IQR 55–107)'), 200),
    ('as_conv', 'Active Surveillance → definitive Therapie', 'Jahre', 'as_start', 'rp', 1 / 365.25,
     (1, 3, 5), None, 6),
    ('bcr', 'Kurative Therapie → biochemisches Rezidiv', 'Jahre', 'treat', 'bcr', 1 / 365.25,
     (1, 2, 4), ('2.5', 'Literatur: median 2,5 J (IQR 0,9–5,5)'), 6),
    ('mcrpc', 'ADT-Start → Zweitlinie (mCRPC-Proxy)', 'Jahre', 'adt', 'line2', 1 / 365.25,
     (1, 1.5, 3), ('1.75', 'Frankfurt-Kohorte: median 21 Mo'), 4),
]


def tri_pdf(x, lo, mode, hi):
    if x < lo or x > hi:
        return 0.0
    if x <= mode:
        return 2 * (x - lo) / ((hi - lo) * (mode - lo)) if mode > lo else 0.0
    return 2 * (hi - x) / ((hi - lo) * (hi - mode)) if hi > mode else 0.0


def collect():
    per_panel = {k: [] for k, *_ in PANELS}
    n = 0
    for f in sorted(glob.glob(os.path.join(FHIR_DIR, '*.json'))):
        name = os.path.basename(f)
        if name.startswith(('hospitalInformation', 'practitionerInformation')):
            continue
        with open(f) as fh:
            ev = extract(json.load(fh))
        if not ev:
            continue
        n += 1
        ev['treat'] = min((t for t in (ev.get('rp'), ev.get('rt')) if t), default=None)
        for key, _, _, src, tgt, scale, *_rest in PANELS:
            a, b = ev.get(src), ev.get(tgt)
            if a and b:
                d = days(a, b) * (1 if scale == 1.0 else 1) * scale
                if d > 0:
                    per_panel[key].append(d)
    return n, per_panel


PW, PH, M = 360, 210, 42  # panel size, margin


def render_panel(idx, spec, values, ink, ink2, blue):
    key, title, unit, _s, _t, _sc, tri, anchor, clip = spec
    x0 = (idx % 3) * (PW + 30)
    y0 = (idx // 3) * (PH + 55)
    min_cut = 1.0 if key == 'workup' else 0.0
    excluded_hi = sum(1 for v in values if v > clip)
    excluded_lo = sum(1 for v in values if v < min_cut)
    values = [v for v in values if min_cut <= v <= clip]
    if not values:
        return f'<g transform="translate({x0},{y0})"><text x="10" y="20" fill="{ink2}">{html.escape(title)}: keine Daten</text></g>'
    vals = values
    hi = clip
    nbins = 24
    w = hi / nbins
    bins = [0] * nbins
    for v in vals:
        bins[min(int(v / w), nbins - 1)] += 1
    peak = max(bins)
    plot_w, plot_h = PW - M - 10, PH - M - 24
    sx = lambda x: M + x / hi * plot_w
    sy = lambda c: 24 + (1 - c / peak) * plot_h
    bars = []
    for i, c in enumerate(bins):
        if not c:
            continue
        bx, bw = sx(i * w) + 1, plot_w / nbins - 2
        bars.append(f'<rect x="{bx:.1f}" y="{sy(c):.1f}" width="{bw:.1f}" '
                    f'height="{24 + plot_h - sy(c):.1f}" rx="2" fill="{blue}">'
                    f'<title>{i*w:.1f}–{(i+1)*w:.1f} {unit}: {c} Pat.</title></rect>')
    overlay = ''
    if tri:
        lo, mode, mx = tri
        pts = []
        steps = 60
        pdf_peak = tri_pdf(mode, lo, mode, mx) or 1
        for j in range(steps + 1):
            x = lo + (min(mx, hi) - lo) * j / steps
            pts.append(f'{sx(x):.1f},{sy(tri_pdf(x, lo, mode, mx) / pdf_peak * peak * 0.9):.1f}')
        overlay = (f'<polyline points="{" ".join(pts)}" fill="none" stroke="{ink}" '
                   f'stroke-width="2" stroke-dasharray="5 3" opacity="0.75">'
                   f'<title>Soll: Triangular({lo}, {mode}, {mx})</title></polyline>')
    anchor_svg = ''
    if anchor:
        av = float(anchor[0])
        if av <= hi:
            anchor_svg = (f'<line x1="{sx(av):.1f}" y1="20" x2="{sx(av):.1f}" y2="{24 + plot_h}" '
                          f'stroke="{ink}" stroke-width="1.5" opacity="0.55"/>'
                          f'<text x="{sx(av) + 4:.1f}" y="32" font-size="10" fill="{ink2}">'
                          f'{html.escape(anchor[1])}</text>')
    med = median(values)
    stats = f'n={len(values)} · median {med:.1f} {unit} · x: {unit}' + (' · gestrichelt = Soll' if tri else '')
    excl = []
    if excluded_hi:
        excl.append(f'>{clip:g} {unit} ausgeblendet: {excluded_hi} (AS-Konvertierer)')
    if excluded_lo:
        excl.append(f'gleichtägig ausgeblendet: {excluded_lo} (benigner Erstworkup)')
    excl_line = (f'<text x="{M}" y="{24 + plot_h + 42}" font-size="10" fill="{ink2}">'
                 f'{html.escape(" · ".join(excl))}</text>') if excl else ''
    axis = (f'<line x1="{M}" y1="{24 + plot_h}" x2="{M + plot_w}" y2="{24 + plot_h}" stroke="{ink2}" stroke-width="1"/>'
            + ''.join(f'<text x="{sx(t):.0f}" y="{24 + plot_h + 14}" font-size="10" text-anchor="middle" '
                      f'fill="{ink2}">{t:g}</text>' for t in axis_ticks(hi)))
    return (f'<g transform="translate({x0},{y0})">'
            f'<text x="{M}" y="12" font-size="12" font-weight="600" fill="{ink}">{html.escape(title)}</text>'
            f'<text x="{M}" y="{24 + plot_h + 30}" font-size="10" fill="{ink2}">{stats}</text>'
            f'{excl_line}'
            f'{"".join(bars)}{overlay}{anchor_svg}{axis}</g>')


def axis_ticks(hi):
    step = {120: 30, 200: 50, 6: 1, 4: 1}.get(hi, max(1, round(hi / 5)))
    out, t = [], 0
    while t <= hi:
        out.append(t)
        t += step
    return out


def render(n, per_panel, dark=False):
    ink = '#ffffff' if dark else '#1a1a19'
    ink2 = '#c3c2b7' if dark else '#5c5b52'
    blue = BLUE_D if dark else BLUE_L
    rows = (len(PANELS) + 2) // 3
    W = 3 * (PW + 30)
    H = rows * (PH + 55)
    panels = ''.join(render_panel(i, spec, per_panel[spec[0]], ink, ink2, blue)
                     for i, spec in enumerate(PANELS))
    bg = f'<rect width="{W}" height="{H}" fill="{"#1a1a19" if dark else "#ffffff"}"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'font-family="system-ui">{bg}{panels}</svg>')


def main():
    n, per_panel = collect()
    if not n:
        sys.exit('no cancer journeys found')
    svg_light = render(n, per_panel, dark=False)
    with open(OUT_SVG, 'w') as f:
        f.write(svg_light)
    doc = f'''<!doctype html><html lang="de"><meta charset="utf-8">
<title>Prostata-Kohorte — Zeitverteilungen</title>
<style>
:root{{color-scheme:light;--surface:#ffffff;--tp:#1a1a19;--ts:#5c5b52}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--surface:#1a1a19;--tp:#ffffff;--ts:#c3c2b7}}}}
:root[data-theme="dark"]{{color-scheme:dark;--surface:#1a1a19;--tp:#ffffff;--ts:#c3c2b7}}
body{{background:var(--surface);color:var(--tp);font-family:system-ui,sans-serif;margin:2rem auto;max-width:1220px;padding:0 1rem}}
h1{{font-size:1.25rem}} p{{color:var(--ts);font-size:.9rem;max-width:70ch}}
.light-only{{display:block}} .dark-only{{display:none}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]) .light-only{{display:none}} :root:not([data-theme="light"]) .dark-only{{display:block}}}}
:root[data-theme="dark"] .light-only{{display:none}} :root[data-theme="dark"] .dark-only{{display:block}}
</style>
<h1>Prostata-Kohorte: gemessene Inter-Event-Zeiten vs. Soll-Verteilungen</h1>
<p>n = {n} Krebs-Journeys (Seed-42-Lauf). Balken = beobachtete Verteilung aus den FHIR-Zeitstempeln;
gestrichelte Kurve = im Modul kodierte Triangular-Verteilung (5-Jahres-Durchschnitte, Jahresfenster
deaktiviert); senkrechte Linie = Literatur-Anker aus <code>docs/prostate_zeitachse.md</code>.
Abweichungen Balken↔Kurve entstehen durch den 7-Tage-Simulationstakt und Pfad-Selektion;
Abweichungen zum Literatur-Anker sind Kalibrierungs-Backlog (z.&nbsp;B. fehlt der Tumorboard-Slot
vor der RP, daher Biopsie→RP schneller als der 77-Tage-Anker).</p>
<div class="light-only">{svg_light}</div>
<div class="dark-only">{render(n, per_panel, dark=True)}</div>
</html>'''
    with open(OUT_HTML, 'w') as f:
        f.write(doc)
    print(f'{n} journeys -> {os.path.relpath(OUT_HTML, REPO)}, {os.path.relpath(OUT_SVG, REPO)}')
    for key, title, unit, *_ in PANELS:
        v = per_panel[key]
        if v:
            print(f'  {title:48} n={len(v):3}  median {median(v):7.2f} {unit}')


if __name__ == '__main__':
    main()

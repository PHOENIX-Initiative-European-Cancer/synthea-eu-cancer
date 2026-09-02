#!/usr/bin/env python3
"""Sankey of the prostate cohort's patient flows, straight from the FHIR bundles.

Stages = the module's calibrated branch points, so the diagram doubles as a visual
cohort cross-check against epidemiology/prostate_calibration.md:

  Detektion -> Risikogruppe -> Primärtherapie -> Verlauf -> Status

Links are colored by EAU risk group (the identity that carries through the whole
journey). Output: self-contained, theme-aware HTML with inline SVG + data table
(output/prostate_sankey.html) and a static light-mode SVG (output/prostate_sankey.svg).

No dependencies beyond the stdlib. Colors: dataviz default categorical slots 1-5,
validated light+dark (validate_palette.js, 2026-09-02).
"""
import glob
import html
import json
import os
import sys
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FHIR_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'synthea', 'output', 'fhir')
OUT_HTML = os.path.join(REPO, 'output', 'prostate_sankey.html')
OUT_SVG = os.path.join(REPO, 'output', 'prostate_sankey.svg')

RISKS = ['Low', 'Intermediate', 'High', 'Lokal fortgeschritten', 'Metastasiert']
# dataviz default categorical palette, slots 1-5 (fixed order, validated both modes)
LIGHT = {'Low': '#2a78d6', 'Intermediate': '#eb6834', 'High': '#1baf7a',
         'Lokal fortgeschritten': '#eda100', 'Metastasiert': '#e87ba4'}
DARK = {'Low': '#3987e5', 'Intermediate': '#d95926', 'High': '#199e70',
        'Lokal fortgeschritten': '#c98500', 'Metastasiert': '#d55181'}

STAGES = [
    ('Detektion', ['Symptomatischer Workup', 'TURP-inzidental']),
    ('Risikogruppe', RISKS),
    ('Primärtherapie', ['Active Surveillance', 'Radikale Prostatektomie',
                        'Radiotherapie (+ADT)', 'Systemtherapie (M1)']),
    ('Verlauf', ['Stabil', 'Rezidiv/Progression']),
    ('Status', ['Lebt', 'Verstorben']),
]

# calibration marginals for the on-chart cross-check (prostate_calibration.md §3)
EXPECTED_RISK = {'Low': 0.32, 'Intermediate': 0.34, 'High': 0.17,
                 'Lokal fortgeschritten': 0.11, 'Metastasiert': 0.06}


def coding_code(codeable):
    for c in (codeable or {}).get('coding', []):
        if c.get('code'):
            return c['code']
    return None


def classify(bundle):
    gleason = None
    ct_val = ''
    m1 = False
    procs, careplans, meds = set(), set(), set()
    recurrent = False
    deceased = False
    has_cancer = False
    for e in bundle.get('entry', []):
        r = e.get('resource', {})
        rt = r.get('resourceType')
        if rt == 'Patient':
            deceased = bool(r.get('deceasedDateTime'))
        elif rt == 'Condition':
            code = coding_code(r.get('code'))
            if code == '399068003':
                has_cancer = True
            elif code == '1098981000119101':
                recurrent = True
        elif rt == 'Observation':
            code = coding_code(r.get('code'))
            if code == '35266-6' and gleason is None:
                gleason = (r.get('valueQuantity') or {}).get('value')
            elif code == '21905-5' and not ct_val:
                vc = r.get('valueCodeableConcept', {})
                ct_val = (vc.get('coding') or [{}])[0].get('display', '')
            elif code == '21907-1':
                vc = r.get('valueCodeableConcept', {})
                if 'M1' in (vc.get('coding') or [{}])[0].get('display', ''):
                    m1 = True
        elif rt == 'Procedure':
            procs.add(coding_code(r.get('code')))
        elif rt == 'CarePlan':
            for act in r.get('activity', []):
                careplans.add(coding_code((act.get('detail') or {}).get('code')))
            for cat in r.get('category', []):
                careplans.add(coding_code(cat))
        elif rt == 'MedicationRequest':
            for c in (r.get('medicationCodeableConcept') or {}).get('coding', []):
                meds.add(c.get('code'))
    if not has_cancer:
        return None

    detektion = 'TURP-inzidental' if ct_val.startswith(('cT1a', 'cT1b')) else 'Symptomatischer Workup'
    if gleason is None:
        risk = 'Low'
    elif gleason <= 6:
        risk = 'Low'
    elif gleason == 7:
        risk = 'Intermediate'
    elif gleason == 8:
        risk = 'High'
    else:
        risk = 'Metastasiert' if m1 else 'Lokal fortgeschritten'

    if risk == 'Metastasiert':
        therapie = 'Systemtherapie (M1)'
    elif '424313000' in careplans:
        therapie = 'Active Surveillance'
    elif '26294005' in procs:
        therapie = 'Radikale Prostatektomie'
    elif '33195004' in procs:
        therapie = 'Radiotherapie (+ADT)'
    else:
        therapie = 'Active Surveillance'

    second_line = meds & {'L02BB04', 'L01CD02', 'L01CD04'}  # enzalutamid, docetaxel, cabazitaxel
    verlauf = 'Rezidiv/Progression' if (recurrent or (m1 and second_line) or
                                        (not m1 and second_line)) else 'Stabil'
    status = 'Verstorben' if deceased else 'Lebt'
    return detektion, risk, therapie, verlauf, status


def main():
    paths = []
    for f in sorted(glob.glob(os.path.join(FHIR_DIR, '*.json'))):
        name = os.path.basename(f)
        if name.startswith(('hospitalInformation', 'practitionerInformation')):
            continue
        with open(f) as fh:
            path = classify(json.load(fh))
        if path:
            paths.append(path)
    n = len(paths)
    if not n:
        sys.exit('no cancer journeys found')

    # link counts between consecutive stages, keyed additionally by risk (= color)
    links = [defaultdict(int) for _ in range(len(STAGES) - 1)]
    node_totals = [Counter() for _ in STAGES]
    for p in paths:
        for i, val in enumerate(p):
            node_totals[i][val] += 1
        for i in range(len(p) - 1):
            links[i][(p[i], p[i + 1], p[1])] += 1

    svg_light = render_svg(node_totals, links, n, LIGHT, static=True)
    svg_themed = render_svg(node_totals, links, n, LIGHT, static=False)
    write_html(svg_themed, node_totals, links, n)
    with open(OUT_SVG, 'w') as f:
        f.write(svg_light)
    print(f'{n} cancer journeys -> {os.path.relpath(OUT_HTML, REPO)}, {os.path.relpath(OUT_SVG, REPO)}')
    obs = {k: v / n for k, v in node_totals[1].items()}
    print('Risiko-Marginale beobachtet vs. kalibriert:')
    for r in RISKS:
        print(f'  {r:22} {obs.get(r, 0):5.1%}  vs. {EXPECTED_RISK[r]:5.1%}')


W, H, PAD, NODE_W, GAP = 1180, 640, 70, 14, 10
LABEL_ROOM = 40


def layout(node_totals, n):
    """x per stage; y-ranges per node, height proportional to count."""
    xs = [PAD + i * (W - 2 * PAD - NODE_W) / (len(STAGES) - 1) for i in range(len(STAGES))]
    usable = H - 2 * PAD
    pos = []
    for i, (_, order) in enumerate(STAGES):
        present = [v for v in order if node_totals[i][v] > 0]
        gaps = GAP * (len(present) - 1)
        scale = (usable - gaps) / n
        y = PAD
        stage_pos = {}
        for v in present:
            h = node_totals[i][v] * scale
            stage_pos[v] = (y, h)
            y += h + GAP
        pos.append(stage_pos)
    return xs, pos


def render_svg(node_totals, links, n, palette, static):
    xs, pos = layout(node_totals, n)
    usable_scale = (H - 2 * PAD - GAP * 4) / n  # ~common scale for ribbon widths
    out_off = [defaultdict(float) for _ in STAGES]
    in_off = [defaultdict(float) for _ in STAGES]
    ribbons, nodes, labels = [], [], []

    for i, stage_links in enumerate(links):
        ordered = sorted(stage_links.items(),
                         key=lambda kv: (STAGES[i][1].index(kv[0][0]),
                                         STAGES[i + 1][1].index(kv[0][1]),
                                         RISKS.index(kv[0][2])))
        for (src, tgt, risk), cnt in ordered:
            h = cnt * (pos[i][src][1] / node_totals[i][src])
            h2 = cnt * (pos[i + 1][tgt][1] / node_totals[i + 1][tgt])
            y0 = pos[i][src][0] + out_off[i][src]
            y1 = pos[i + 1][tgt][0] + in_off[i + 1][tgt]
            out_off[i][src] += h
            in_off[i + 1][tgt] += h2
            x0, x1 = xs[i] + NODE_W, xs[i + 1]
            cx = (x0 + x1) / 2
            path = (f'M{x0:.1f},{y0:.1f} C{cx:.1f},{y0:.1f} {cx:.1f},{y1:.1f} {x1:.1f},{y1:.1f} '
                    f'L{x1:.1f},{y1 + h2:.1f} C{cx:.1f},{y1 + h2:.1f} {cx:.1f},{y0 + h:.1f} {x0:.1f},{y0 + h:.1f} Z')
            tip = f'{src} → {tgt} · {risk}: {cnt} Pat.'
            ribbons.append(f'<path class="link" d="{path}" fill="{palette[risk]}">'
                           f'<title>{html.escape(tip)}</title></path>')

    ink = '#1a1a19' if static else 'var(--text-primary)'
    ink2 = '#5c5b52' if static else 'var(--text-secondary)'
    for i, (stage_name, _) in enumerate(STAGES):
        labels.append(f'<text x="{xs[i] + NODE_W / 2:.0f}" y="{PAD - 28}" text-anchor="middle" '
                      f'class="stage" fill="{ink2}">{html.escape(stage_name)}</text>')
        for v, (y, h) in pos[i].items():
            nodes.append(f'<rect x="{xs[i]:.1f}" y="{y:.1f}" width="{NODE_W}" height="{max(h, 2):.1f}" '
                         f'rx="3" fill="{ink}" fill-opacity="0.82">'
                         f'<title>{html.escape(v)}: {node_totals[i][v]} Pat.</title></rect>')
            anchor, lx = ('start', xs[i] + NODE_W + 8)
            if i == len(STAGES) - 1:
                anchor, lx = 'end', xs[i] - 8
            cnt = node_totals[i][v]
            pct = f' · {cnt / n:.0%}'
            labels.append(f'<text x="{lx:.0f}" y="{y + max(h, 2) / 2 + 4:.0f}" text-anchor="{anchor}" '
                          f'class="lbl" fill="{ink}">{html.escape(v)} '
                          f'<tspan fill="{ink2}">{cnt}{pct}</tspan></text>')

    style = ('<style>.link{opacity:.5}.link:hover{opacity:.85}'
             'text{font-family:system-ui,sans-serif}.lbl{font-size:13px}.stage{font-size:13px;'
             'font-weight:600;letter-spacing:.04em}</style>')
    bg = f'<rect width="{W}" height="{H}" fill="#ffffff"/>' if static else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'font-family="system-ui">{style}{bg}<g>{"".join(ribbons)}</g>'
            f'<g>{"".join(nodes)}</g><g>{"".join(labels)}</g></svg>')


def write_html(svg, node_totals, links, n):
    legend = ''.join(
        f'<span class="key"><i style="background:var(--c{idx})"></i>{html.escape(r)}</span>'
        for idx, r in enumerate(RISKS, 1))
    rows = []
    for r in RISKS:
        obs = node_totals[1][r] / n
        rows.append(f'<tr><td>{html.escape(r)}</td><td>{node_totals[1][r]}</td>'
                    f'<td>{obs:.1%}</td><td>{EXPECTED_RISK[r]:.0%}</td></tr>')
    flow_rows = []
    for i, stage_links in enumerate(links):
        agg = Counter()
        for (src, tgt, _), cnt in stage_links.items():
            agg[(src, tgt)] += cnt
        for (src, tgt), cnt in sorted(agg.items(), key=lambda kv: -kv[1]):
            flow_rows.append(f'<tr><td>{html.escape(src)}</td><td>{html.escape(tgt)}</td>'
                             f'<td>{cnt}</td><td>{cnt / n:.1%}</td></tr>')
    light_vars = ''.join(f'--c{i}:{LIGHT[r]};' for i, r in enumerate(RISKS, 1))
    dark_vars = ''.join(f'--c{i}:{DARK[r]};' for i, r in enumerate(RISKS, 1))
    doc = f'''<!doctype html><html lang="de"><meta charset="utf-8">
<title>Prostata-Kohorte — Patientenflüsse (Sankey)</title>
<style>
:root{{color-scheme:light;--surface:#ffffff;--text-primary:#1a1a19;--text-secondary:#5c5b52;{light_vars}}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--surface:#1a1a19;--text-primary:#ffffff;--text-secondary:#c3c2b7;{dark_vars}}}}}
:root[data-theme="dark"]{{color-scheme:dark;--surface:#1a1a19;--text-primary:#ffffff;--text-secondary:#c3c2b7;{dark_vars}}}
body{{background:var(--surface);color:var(--text-primary);font-family:system-ui,sans-serif;margin:2rem auto;max-width:1220px;padding:0 1rem}}
h1{{font-size:1.25rem}} p,caption{{color:var(--text-secondary);font-size:.9rem}}
.key{{margin-right:1rem;font-size:.85rem}} .key i{{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:.4em;vertical-align:-1px}}
svg text{{fill:var(--text-primary)}}
table{{border-collapse:collapse;margin:1rem 0;font-size:.85rem}} td,th{{padding:.3em .8em;border-bottom:1px solid color-mix(in oklab,var(--text-secondary) 25%,transparent);text-align:left}}
details{{margin:1rem 0}}
</style>
<h1>Prostata-Kohorte: Patientenflüsse durch die kalibrierten Branch-Punkte</h1>
<p>n = {n} Krebs-Journeys (Seed-42-Kohorte, 1000 Männer 50–60). Bandfarbe = EAU-Risikogruppe.
Quelle: FHIR-Bundles nach ECCDM-Postprocessing; Stufen = Kalibrierungspunkte aus
<code>epidemiology/prostate_calibration.md</code>.</p>
<div>{legend}</div>
{svg}
<h2 style="font-size:1rem">Kohorten-Gegenprobe: Risikogruppen-Marginale</h2>
<table><tr><th>Risikogruppe</th><th>n</th><th>beobachtet</th><th>kalibriert (§3)</th></tr>{''.join(rows)}</table>
<p>Erwartete Abweichung: §3 kalibriert die Verteilung <em>im symptomatischen Workup</em>;
die TURP-Inzidentalkarzinome (Kalibrierung §4, 14&nbsp;% der TURP) laufen zusätzlich in den
Low-Ast und heben dessen Gesamtanteil — im Sankey als eigener Eintrittsstrom sichtbar.</p>
<details><summary>Alle Flüsse als Tabelle</summary>
<table><tr><th>von</th><th>nach</th><th>n</th><th>Anteil</th></tr>{''.join(flow_rows)}</table></details>
</html>'''
    with open(OUT_HTML, 'w') as f:
        f.write(doc)


if __name__ == '__main__':
    main()

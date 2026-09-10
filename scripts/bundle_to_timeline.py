#!/usr/bin/env python3
"""Visualize one patient's FHIR bundle as a clinical-journey timeline.

Swimlanes (top to bottom): derived ECCDM EpisodesOfCare, encounters, prostate-relevant
conditions, key procedures, systemic medication, staging/grading markers, and the PSA
curve — the narrative thread of the disease. Only journey-relevant resources are drawn;
the caption reports the full bundle size.

Usage: bundle_to_timeline.py [bundle.json]   (default: richest journey in the cohort)
Output: output/patient_timeline.html (theme-aware) + .svg (static, light).
Stdlib only; colors = dataviz default categorical palette (validated this session).
"""
import glob
import html
import json
import os
import sys
from datetime import datetime, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FHIR_DIR = os.path.join(REPO, 'synthea', 'output', 'fhir')
OUT_HTML = os.path.join(REPO, 'output', 'patient_timeline.html')
OUT_SVG = os.path.join(REPO, 'output', 'patient_timeline.svg')

# validated categorical palette (slots 1-5), light/dark
PAL = {
    'proc': ('#2a78d6', '#3987e5'),   # slot 1 blue  - procedures
    'cond': ('#eb6834', '#d95926'),   # slot 2 orange - conditions
    'med':  ('#1baf7a', '#199e70'),   # slot 3 aqua  - medication
    'eoc':  ('#eda100', '#c98500'),   # slot 4 yellow - episodes of care
    'psa':  ('#e87ba4', '#d55181'),   # slot 5 magenta - PSA curve
}

PROC_LABELS = {
    '410006001': 'DRE', '429820004': 'TRUS', '1144760005': 'mpMRT',
    '236258004': 'Biopsie', '26294005': 'Radikale Prostatektomie',
    '33195004': 'EBRT', '90199006': 'TURP', '1620551000168100': 'PSMA-PET',
}
MED_LABELS = {'L02AE02': 'Leuprorelin', 'L02BB04': 'Enzalutamid', 'L01CD02': 'Docetaxel',
              'L01CD04': 'Cabazitaxel', 'G04CA02': 'Tamsulosin', 'G04CB01': 'Finasterid'}
COND_LABELS = {'266569009': 'BPH', '399068003': 'Prostatakarzinom',
               '1098981000119101': 'Rezidiv (BCR)'}
EOC_LABELS = {'episode-of-care-surveillance-eu-ccm': 'Active Surveillance',
              'episode-of-care-radiotherapy-eu-ccm': 'Radiotherapie',
              'episode-of-care-systematic-treatment-eu-ccm': 'Systemtherapie'}


def dt(x):
    return datetime.fromisoformat(x).replace(tzinfo=None)


def pick_default():
    best = None
    for f in glob.glob(os.path.join(FHIR_DIR, '*.json')):
        with open(f) as fh:
            b = json.load(fh)
        s = 0
        for e in b['entry']:
            r = e['resource']
            code = ((r.get('code') or {}).get('coding') or [{}])[0].get('code')
            if r['resourceType'] == 'Condition' and code == '1098981000119101':
                s += 5
            if r['resourceType'] == 'Procedure' and code == '26294005':
                s += 3
        if s >= 8:
            return f
        best = best if best and best[0] >= s else (s, f)
    return best[1]


def extract(path):
    with open(path) as fh:
        bundle = json.load(fh)
    data = {'encounters': [], 'conds': [], 'procs': [], 'meds': [], 'eocs': [],
            'psa': [], 'stage': [], 'total': 0}
    for e in bundle['entry']:
        r = e['resource']
        rt = r['resourceType']
        data['total'] += 1
        code = ((r.get('code') or {}).get('coding') or [{}])[0].get('code')
        if rt == 'Patient':
            name = r['name'][0]
            data['name'] = f"{' '.join(name.get('given', []))} {name.get('family', '')}"
            data['birth'] = r.get('birthDate')
        elif rt == 'Encounter':
            p = r.get('period', {})
            if p.get('start'):
                data['encounters'].append(dt(p['start']))
        elif rt == 'Condition' and code in COND_LABELS:
            data['conds'].append((dt(r['onsetDateTime']), COND_LABELS[code]))
        elif rt == 'Procedure' and code in PROC_LABELS:
            t = (r.get('performedPeriod') or {}).get('start') or r.get('performedDateTime')
            data['procs'].append((dt(t), PROC_LABELS[code]))
        elif rt == 'MedicationRequest':
            for c in (r.get('medicationCodeableConcept') or {}).get('coding', []):
                if c.get('code') in MED_LABELS and r.get('authoredOn'):
                    data['meds'].append((dt(r['authoredOn']), MED_LABELS[c['code']]))
                    break
        elif rt == 'EpisodeOfCare':
            prof = (r.get('meta', {}).get('profile') or [''])[0].rsplit('/', 1)[-1]
            p = r.get('period', {})
            if prof in EOC_LABELS and p.get('start'):
                data['eocs'].append((dt(p['start']),
                                     dt(p['end']) if p.get('end') else None,
                                     EOC_LABELS[prof]))
        elif rt == 'Observation':
            t = r.get('effectiveDateTime')
            if not t:
                continue
            if code == '2857-1':
                data['psa'].append((dt(t), r.get('valueQuantity', {}).get('value')))
            elif code == '35266-6':
                data['stage'].append((dt(t), f"Gleason {r.get('valueQuantity', {}).get('value'):g}"))
            elif code in ('21905-5', '21906-3', '21907-1', '21899-0', '21900-6'):
                v = ((r.get('valueCodeableConcept') or {}).get('coding') or [{}])[0]
                data['stage'].append((dt(t), v.get('display', '').replace(' (UICC)', '')))
    # merge same-day stage markers into one label
    merged = {}
    for t, lbl in sorted(data['stage']):
        merged.setdefault(t.date(), []).append(lbl)
    data['stage'] = [(datetime.combine(d, datetime.min.time()), ' '.join(ls))
                     for d, ls in sorted(merged.items())]
    return data


W, LANE_LBL = 1240, 150


def render(d, dark=False):
    ink = '#ffffff' if dark else '#1a1a19'
    ink2 = '#c3c2b7' if dark else '#5c5b52'
    surface = '#1a1a19' if dark else '#ffffff'
    ci = 1 if dark else 0
    events = ([t for t, _ in d['conds']] + [t for t, _ in d['procs']] +
              [t for t, _ in d['meds']] + [t for t, _ in d['psa']] +
              [t for t, _, _ in d['eocs']])
    lo = min(events) - timedelta(days=120)
    hi = max(events) + timedelta(days=200)
    span = (hi - lo).days
    x = lambda t: LANE_LBL + (t - lo).days / span * (W - LANE_LBL - 30)

    lanes = [('ECCDM-Episoden', 46), ('Encounter', 26), ('Diagnosen', 40),
             ('Prozeduren', 74), ('Medikation', 40), ('Staging', 40), ('PSA (ng/ml)', 90)]
    y0s, y = {}, 46
    for name, h in lanes:
        y0s[name] = y
        y += h + 14
    H = y + 34
    out = [f'<rect width="{W}" height="{H}" fill="{surface}"/>']

    # year grid
    for yr in range(lo.year, hi.year + 2):
        t = datetime(yr, 1, 1)
        if lo <= t <= hi:
            out.append(f'<line x1="{x(t):.0f}" y1="36" x2="{x(t):.0f}" y2="{H - 26}" '
                       f'stroke="{ink2}" stroke-width="0.5" opacity="0.35"/>')
            out.append(f'<text x="{x(t):.0f}" y="{H - 10}" font-size="11" '
                       f'text-anchor="middle" fill="{ink2}">{yr}</text>')
    for name, h in lanes:
        ly = y0s[name]
        out.append(f'<text x="{LANE_LBL - 10}" y="{ly + h / 2 + 4}" font-size="11" '
                   f'text-anchor="end" font-weight="600" fill="{ink2}">{name}</text>')

    # EOC spans
    ly, lh = y0s['ECCDM-Episoden'], 46
    for i, (s, e, lbl) in enumerate(sorted(d['eocs'])):
        yy = ly + 4 + (i % 3) * 13
        xe = x(e) if e else x(hi) - 6
        open_end = '' if e else f'<polygon points="{xe:.0f},{yy} {xe + 7:.0f},{yy + 4} {xe:.0f},{yy + 8}" fill="{PAL["eoc"][ci]}"/>'
        out.append(f'<rect x="{x(s):.0f}" y="{yy}" width="{max(xe - x(s), 4):.0f}" height="8" rx="3" '
                   f'fill="{PAL["eoc"][ci]}" opacity="0.85"><title>{lbl}</title></rect>{open_end}'
                   f'<text x="{x(s):.0f}" y="{yy - 2}" font-size="10" fill="{ink}">{lbl}'
                   + ('' if e else ' (aktiv)') + '</text>')

    # encounters as ticks
    ly = y0s['Encounter']
    for t in d['encounters']:
        if lo <= t <= hi:
            out.append(f'<line x1="{x(t):.1f}" y1="{ly + 4}" x2="{x(t):.1f}" y2="{ly + 20}" '
                       f'stroke="{ink}" stroke-width="1.4" opacity="0.5">'
                       f'<title>Encounter {t.date()}</title></line>')

    # conditions: onset marker + open-ended line
    ly = y0s['Diagnosen']
    for i, (t, lbl) in enumerate(sorted(d['conds'])):
        yy = ly + 6 + i * 12
        out.append(f'<line x1="{x(t):.0f}" y1="{yy + 4}" x2="{x(hi) - 4:.0f}" y2="{yy + 4}" '
                   f'stroke="{PAL["cond"][ci]}" stroke-width="2" opacity="0.45"/>'
                   f'<circle cx="{x(t):.0f}" cy="{yy + 4}" r="4.5" fill="{PAL["cond"][ci]}">'
                   f'<title>{lbl} · {t.date()}</title></circle>'
                   f'<text x="{x(t) + 8:.0f}" y="{yy + 8}" font-size="10" fill="{ink}">{lbl}</text>')

    # procedures: stagger labels at shared dates
    ly = y0s['Prozeduren']
    slot_of = {}
    for t, lbl in sorted(d['procs']):
        k = t.date()
        slot_of[k] = slot_of.get(k, -1) + 1
        yy = ly + 8 + slot_of[k] * 13
        out.append(f'<rect x="{x(t) - 3.5:.0f}" y="{yy}" width="7" height="7" rx="2" '
                   f'transform="rotate(45 {x(t):.0f} {yy + 3.5})" fill="{PAL["proc"][ci]}">'
                   f'<title>{lbl} · {t.date()}</title></rect>'
                   f'<text x="{x(t) + 8:.0f}" y="{yy + 7}" font-size="10" fill="{ink}">{lbl}</text>')

    # medication
    ly = y0s['Medikation']
    slot_of = {}
    for t, lbl in sorted(d['meds']):
        k = t.date()
        slot_of[k] = slot_of.get(k, -1) + 1
        yy = ly + 8 + slot_of[k] * 13
        out.append(f'<circle cx="{x(t):.0f}" cy="{yy + 3}" r="4" fill="{PAL["med"][ci]}">'
                   f'<title>{lbl} · {t.date()}</title></circle>'
                   f'<text x="{x(t) + 8:.0f}" y="{yy + 7}" font-size="10" fill="{ink}">{lbl}</text>')

    # staging markers
    ly = y0s['Staging']
    for i, (t, lbl) in enumerate(d['stage']):
        yy = ly + 10 + (i % 2) * 16
        out.append(f'<line x1="{x(t):.0f}" y1="{yy - 4}" x2="{x(t):.0f}" y2="{yy + 4}" '
                   f'stroke="{ink}" stroke-width="1.6"/>'
                   f'<text x="{x(t) + 6:.0f}" y="{yy + 4}" font-size="10" fill="{ink}">{lbl}</text>')

    # PSA curve
    ly, lh = y0s['PSA (ng/ml)'], 90
    vals = sorted(d['psa'])
    if vals:
        vmax = max(v for _, v in vals) * 1.25
        py = lambda v: ly + lh - 8 - (v / vmax) * (lh - 20)
        pts = ' '.join(f'{x(t):.0f},{py(v):.0f}' for t, v in vals)
        out.append(f'<polyline points="{pts}" fill="none" stroke="{PAL["psa"][ci]}" stroke-width="2"/>')
        for t, v in vals:
            out.append(f'<circle cx="{x(t):.0f}" cy="{py(v):.0f}" r="4" fill="{PAL["psa"][ci]}" '
                       f'stroke="{surface}" stroke-width="1.5"><title>PSA {v:.1f} ng/ml · {t.date()}</title></circle>'
                       f'<text x="{x(t):.0f}" y="{py(v) - 8:.0f}" font-size="10" '
                       f'text-anchor="middle" fill="{ink}">{v:.1f}</text>')
        out.append(f'<line x1="{LANE_LBL}" y1="{ly + lh - 8}" x2="{W - 30}" y2="{ly + lh - 8}" '
                   f'stroke="{ink2}" stroke-width="1"/>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'font-family="system-ui">{"".join(out)}</svg>'), H


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else pick_default()
    d = extract(path)
    svg_light, _ = render(d, dark=False)
    svg_dark, _ = render(d, dark=True)
    with open(OUT_SVG, 'w') as f:
        f.write(svg_light)
    n_enc = len(d['encounters'])
    doc = f'''<!doctype html><html lang="de"><meta charset="utf-8">
<title>Patient Journey — {html.escape(d.get('name', '?'))}</title>
<style>
:root{{color-scheme:light;--surface:#ffffff;--tp:#1a1a19;--ts:#5c5b52}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{color-scheme:dark;--surface:#1a1a19;--tp:#ffffff;--ts:#c3c2b7}}}}
:root[data-theme="dark"]{{color-scheme:dark;--surface:#1a1a19;--tp:#ffffff;--ts:#c3c2b7}}
body{{background:var(--surface);color:var(--tp);font-family:system-ui,sans-serif;margin:2rem auto;max-width:1280px;padding:0 1rem}}
h1{{font-size:1.25rem}} p{{color:var(--ts);font-size:.9rem;max-width:80ch}}
.light-only{{display:block}} .dark-only{{display:none}}
@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]) .light-only{{display:none}} :root:not([data-theme="light"]) .dark-only{{display:block}}}}
:root[data-theme="dark"] .light-only{{display:none}} :root[data-theme="dark"] .dark-only{{display:block}}
</style>
<h1>Patient Journey: {html.escape(d.get('name', '?'))} (*{html.escape(d.get('birth', '?'))}, synthetisch)</h1>
<p>Ein FHIR-Bundle als klinische Zeitachse — gezeigt sind die prostata-relevanten Ressourcen
({n_enc} Encounter als Striche; das vollständige Bundle enthält {d['total']} Ressourcen).
Gelb: aus dem ECCDM-Postprocessing abgeleitete EpisodesOfCare. Quelle:
<code>{html.escape(os.path.basename(sys.argv[1]) if len(sys.argv) > 1 else 'Seed-42-Kohorte')}</code>.</p>
<div class="light-only">{svg_light}</div>
<div class="dark-only">{svg_dark}</div>
</html>'''
    with open(OUT_HTML, 'w') as f:
        f.write(doc)
    print(f"{d.get('name')} -> {os.path.relpath(OUT_HTML, REPO)}, {os.path.relpath(OUT_SVG, REPO)}")


if __name__ == '__main__':
    main()

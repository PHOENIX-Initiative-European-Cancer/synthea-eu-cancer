#!/usr/bin/env python3
"""Build a PDF report of the prostate module's transition probabilities + sources.

Page 1: probability decision-tree diagram (Graphviz).
Page 2+: table of every calibrated transition probability with source (DOI),
         confidence, and primary-source verification verdict.

Renders an HTML report and prints it to PDF via headless Chrome.
Out: output/prostate_transition_probabilities.pdf
"""
import subprocess, os, html

OUT_DIR = "output"
os.makedirs(OUT_DIR, exist_ok=True)
DOT = os.path.join(OUT_DIR, "_probtree.dot")
SVG = os.path.join(OUT_DIR, "_probtree.svg")
HTML = os.path.join(OUT_DIR, "_calibration_report.html")
PDF = os.path.join(OUT_DIR, "prostate_transition_probabilities.pdf")

# ---------- probability decision-tree (calibrated model) ----------
dot = r'''
digraph P {
  rankdir=TB; bgcolor=white; splines=true;
  node [shape=box style="rounded,filled" fontname="Helvetica" fontsize=11 fillcolor="#eef4fb"];
  edge [fontname="Helvetica" fontsize=10 color="#445"];

  present [label="♂ 50–60, symptomatic\n(100% present — test cohort)" fillcolor="#e8f5e9"];
  workup  [label="Work-up: DRE + PSA + TRUS"];
  bph     [label="BPH" fillcolor="#dbe9f6"];
  elev    [label="Elevated PSA → mpMRI"];
  ca      [label="Prostate cancer" fillcolor="#fde7ea"];

  present -> workup;
  workup -> bph  [label="0.70"];
  workup -> elev [label="0.30"];

  elev -> bph [label="PI-RADS 1–2: 0.40 (benign)"];
  elev -> ca  [label="PI-RADS 3 (0.20)×0.16\n+ 4 (0.25)×0.59\n+ 5 (0.15)×0.85"];
  elev -> bph [label="biopsy benign"];

  // BPH management
  ww   [label="Watchful waiting" fillcolor="#dbe9f6"];
  med  [label="Medical (tamsulosin ± finasteride)" fillcolor="#dbe9f6"];
  turp [label="TURP" fillcolor="#dbe9f6"];
  bph -> ww   [label="0.33"];
  bph -> med  [label="0.52"];
  bph -> turp [label="0.15"];
  turp -> ca  [label="0.14 incidental → low-risk" style=dashed color="#b00020"];

  // cancer risk groups
  low [label="Low"];  inter [label="Intermediate"]; high [label="High"];
  loca [label="Locally advanced"]; met [label="Metastatic (M1)" fillcolor="#fde7ea"];
  ca -> low   [label="0.32"];
  ca -> inter [label="0.34"];
  ca -> high  [label="0.17"];
  ca -> loca  [label="0.11"];
  ca -> met   [label="0.06"];

  as [label="Active surveillance"];
  low -> as [label="preferred"];
  as -> deftx [label="0.50 → treat (5 yr)"];
  deftx [label="Deferred RP / RT"];

  inter -> rp   [label="0.55"]; inter -> ebrtadt [label="0.45"];
  rp [label="Radical prostatectomy"]; ebrtadt [label="EBRT + short ADT"];

  high -> ebrtL [label="0.60"]; high -> rppl [label="0.40"];
  loca -> ebrtL; loca -> rppl;
  ebrtL [label="EBRT + long ADT (2–3y)"]; rppl [label="RP + pelvic LND"];
  ebrtL -> metL [label="0.15 progress"]; rppl -> metL [label="0.15 progress"];
  metL [label="→ systemic (metastatic)" fillcolor="#fde7ea"];

  met -> adt; metL -> adt;
  adt [label="ADT backbone (leuprorelin)" fillcolor="#fde7ea"];
  adt -> arpi [label="0.60"]; adt -> doce [label="0.40"];
  arpi [label="ARPI (enzalutamide)" fillcolor="#fde7ea"]; doce [label="Docetaxel" fillcolor="#fde7ea"];
  arpi -> mcrpc; doce -> mcrpc;
  mcrpc [label="mCRPC → 2nd line\n(cabazitaxel)" fillcolor="#fde7ea"];
  mcrpc -> death [label="0.65 → 2nd line,\nthen 0.55 death"];
  death [label="Prostate-cancer death" fillcolor="#7a0010" fontcolor="white"];
}
'''
open(DOT, "w").write(dot)
subprocess.run(["dot", "-Tsvg", DOT, "-o", SVG], check=True)
svg = open(SVG).read()
svg = svg[svg.find("<svg"):]  # strip xml prolog for clean inline embedding

# ---------- transition-probability + source table ----------
# (decision point, branches/values, source, doi, confidence, verified)
G, A, R = "green", "amber", "red"
rows = [
 ("Symptom presentation", "100% present (selected cohort)", "Cohort-design knob; anchored on UrEpik 19% mod-severe LUTS 50–59", "10.1046/j.1464-410x.2003.04369.x", R, "n/a (design)"),
 ("Work-up → BPH / elevated-PSA", "0.70 / 0.30", "Nordström (symptomatic LUTS cohort, ~67% benign) + EAU 2024 pathway", "10.1016/j.euros.2020.12.004", A, "✓ 67/19/13.7% exact"),
 ("mpMRI → PI-RADS 1–2 / 3 / 4 / 5", "0.40 / 0.20 / 0.25 / 0.15", "Estimate for symptomatic elevated-PSA men; yields ~31% csPCa (matches PRECISION)", "10.1038/s41391-020-00290-4", R, "— (estimate)"),
 ("Biopsy → csPCa | PI-RADS 3 / 4 / 5", "0.16 / 0.59 / 0.85", "Oerther PI-RADS v2.1 meta-analysis, patient-level CDR", "10.1038/s41391-021-00417-1", G, "✓ exact"),
 ("Cancer → risk group (Low/Int/High/LocAdv/Met)", "0.32 / 0.34 / 0.17 / 0.11 / 0.06", "Xie EAU-g 26.6/24.0/36.5/12.9; re-weighted younger (SEER<50 M1 4.2%)", "10.3389/fonc.2021.646073", A, "✓ Xie exact; reweighted"),
 ("Low risk → active surveillance", "1.00 (preferred)", "EAU 2024: AS is the preferred option for low-risk", "10.1016/j.eururo.2024.03.027", G, "✓"),
 ("AS → definitive treatment (5 yr)", "0.50", "HAROW long-term + international AS reviews (median time-to-tx <5 yr)", "10.1007/s00345-020-03471-x", G, "✓ vindicated"),
 ("Intermediate → RP / EBRT+ADT", "0.55 / 0.45", "HAROW real-world (RP-heavy, 56.6%) + EAU 2024", "10.3238/arztebl.2016.0329", A, "✓ HAROW 56.6% RP"),
 ("High / loc-adv → EBRT+longADT / RP+PLND", "0.60 / 0.40", "EAU 2024 (strong vs weak recommendation)", "10.1016/j.eururo.2024.03.027", A, "✓"),
 ("High-risk → late metastasis", "0.15", "Indicative (minority progress on follow-up)", "—", R, "— (indicative)"),
 ("mHSPC → ARPI / docetaxel", "0.60 / 0.40", "EAU 2024 Part II: intensify ADT (doublet)", "10.1016/j.eururo.2024.03.027", A, "✓"),
 ("mCRPC → 2nd line / stable", "0.65 / 0.35", "Indicative progression to castration resistance", "—", R, "— (indicative)"),
 ("mCRPC → prostate-cancer death", "0.55", "Distant-stage 5-yr survival low (~30%), German NRW registry", "10.1016/j.clgc.2024.102289", A, "✓ direction"),
 ("BPH → WW / medical / surgery", "0.33 / 0.52 / 0.15", "Textbook priors (EAU/AUA-aligned)", "—", R, "— (prior)"),
 ("TURP → incidental cancer", "0.14 → low-risk", "Sid Ahmed HoLEP cohort (14.3%, 62% low-grade)", "10.7759/cureus.90916", G, "✓ exact"),
]

def badge(c):
    m = {"green": ("#2e7d32", "high"), "amber": ("#b8860b", "medium"), "red": ("#b00020", "prior/est")}
    col, lab = m[c]
    return f'<span style="background:{col};color:white;padding:1px 7px;border-radius:9px;font-size:11px">{lab}</span>'

trs = ""
for dp, val, src, doi, conf, ver in rows:
    doicell = f'<a href="https://doi.org/{doi}">{doi}</a>' if doi != "—" else "—"
    trs += (f"<tr><td>{html.escape(dp)}</td><td class='v'>{html.escape(val)}</td>"
            f"<td>{html.escape(src)}</td><td class='doi'>{doicell}</td>"
            f"<td>{badge(conf)}</td><td>{html.escape(ver)}</td></tr>")

import base64
vpng = os.path.join(OUT_DIR, "prostate_variants.png")
vb64 = base64.b64encode(open(vpng, "rb").read()).decode() if os.path.exists(vpng) else ""
trace_section = (
    '<div class="tracepage"><h2>Trace overview — variant fingerprint (short → long)</h2>'
    '<div class="sub">Each row = one REAL patient path; left bars = frequency (n, %). '
    'Shows the actual distinct pathways (not a merged graph): short frequent BPH paths on top, '
    'long rare cancer / mCRPC paths at the bottom.</div>'
    f'<img class="trace" src="data:image/png;base64,{vb64}"></div>') if vb64 else ""

report = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: A4 landscape; margin: 13mm; }}
@page portraitpage {{ size: A4 portrait; margin: 12mm; }}
body {{ font-family: Helvetica, Arial, sans-serif; color:#222; }}
h1 {{ font-size:20px; margin:0 0 2px; }}
h2 {{ font-size:15px; margin:2px 0 6px; color:#334; }}
.sub {{ color:#666; font-size:12px; margin-bottom:10px; }}
table {{ border-collapse:collapse; width:100%; font-size:11px; }}
th,td {{ border:1px solid #ccd; padding:5px 7px; text-align:left; vertical-align:top; }}
th {{ background:#eef4fb; }}
td.v {{ font-weight:bold; white-space:nowrap; }}
td.doi {{ font-family:monospace; font-size:10px; }}
.foot {{ color:#888; font-size:10px; margin-top:10px; }}
.diagrampage {{ page-break-before: always; text-align:center; }}
.diagrampage svg {{ max-width:100%; height:auto; }}
.tracepage {{ page: portraitpage; page-break-before: always; text-align:center; }}
.trace {{ max-width:100%; max-height:245mm; height:auto; }}
</style></head><body>
<h1>Prostate pathway — transition probabilities &amp; sources</h1>
<div class="sub">synthea-eu-cancer · modules/adult/prostate.json · calibrated to EAU 2024 + German S3/ZfKD.
Confidence: <b>high</b> = exact from primary source · <b>medium</b> = sourced, transferability caveat ·
<b>prior/est</b> = modelling prior. Full trace: epidemiology/prostate_calibration.md.</div>
<table>
<tr><th>Decision point</th><th>Probabilities</th><th>Source</th><th>DOI</th><th>Confidence</th><th>Verified vs primary source</th></tr>
{trs}
</table>
<div class="foot">Primary-source verification (2026-07): 5 core arrows + ~19/20 remaining sources confirmed exact or directional
(4 background agents). Citation fixes: Xie (not Zhou), Egevad (not Epstein). AS→treatment 0.50 vindicated.</div>
<div class="diagrampage"><h2>Probability decision tree</h2>{svg}</div>
{trace_section}
</body></html>"""
open(HTML, "w").write(report)

chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                "--virtual-time-budget=3000",
                f"--print-to-pdf={os.path.abspath(PDF)}",
                "file://" + os.path.abspath(HTML)], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("wrote", PDF, "(", os.path.getsize(PDF), "bytes )" if os.path.exists(PDF) else "MISSING")

#!/usr/bin/env python3
"""Event log (CSV) -> Directly-Follows Graph in Graphviz DOT, rendered to PNG/SVG.

Usage: python3 scripts/eventlog_to_dfg.py [eventlog_csv] [out_basename]
Defaults: output/prostate_eventlog.csv -> output/prostate_dfg(.dot/.png/.svg)
Needs the `dot` CLI (graphviz) on PATH for rendering.
"""
import csv, sys, os, subprocess
from collections import defaultdict, Counter

csv_path = sys.argv[1] if len(sys.argv) > 1 else "output/prostate_eventlog.csv"
base = sys.argv[2] if len(sys.argv) > 2 else "output/prostate_dfg"

rows = list(csv.DictReader(open(csv_path)))
traces = defaultdict(list)
for r in rows:
    traces[r["case_id"]].append((r["timestamp"], r["activity"]))

node_freq = Counter()
edge_freq = Counter()
start_freq = Counter()
end_freq = Counter()
for case, evs in traces.items():
    evs.sort(key=lambda x: x[0])
    acts = [a for _, a in evs]
    for a in acts:
        node_freq[a] += 1
    if acts:
        start_freq[acts[0]] += 1
        end_freq[acts[-1]] += 1
    for a, b in zip(acts, acts[1:]):
        edge_freq[(a, b)] += 1

max_e = max(edge_freq.values()) if edge_freq else 1

def esc(s):
    return s.replace('"', '\\"')

def node_id(a):
    return '"' + esc(a) + '"'

lines = ['digraph DFG {', '  rankdir=TB;', '  bgcolor="white";',
         '  node [shape=box style="rounded,filled" fillcolor="#eef4fb" fontname="Helvetica" fontsize=11];',
         '  edge [fontname="Helvetica" fontsize=9 color="#556"];',
         '  START [shape=circle fillcolor="#2e7d32" style=filled fontcolor=white label="START" width=0.6];',
         '  END [shape=doublecircle fillcolor="#37474f" style=filled fontcolor=white label="END\\n(alive /\\ncensored)" width=0.6];']

# color cancer-branch nodes differently
cancer = {"mpMRI", "PI-RADS", "Prostate biopsy", "Diagnosis: Prostate cancer",
          "Biochemical recurrence", "PSMA-PET",
          "Gleason score", "Radical prostatectomy", "Radiotherapy (EBRT)",
          "Active surveillance", "Med: leuprorelin (ADT)", "Med: enzalutamide (ARPI)",
          "Med: docetaxel", "Med: cabazitaxel"}
for a, n in node_freq.items():
    if a == "Death (prostate cancer)":
        fill, fc = "#7a0010", "white"
    elif a == "Death (other cause)":
        fill, fc = "#9e9e9e", "black"
    elif a in cancer:
        fill, fc = "#fde7ea", "black"
    else:
        fill, fc = "#eef4fb", "black"
    lines.append(f'  {node_id(a)} [label="{esc(a)}\\n({n})" fillcolor="{fill}" fontcolor="{fc}"];')

for a, n in start_freq.items():
    lines.append(f'  START -> {node_id(a)} [label="{n}" penwidth={1+4*n/max_e:.1f}];')
for (a, b), n in edge_freq.items():
    pw = 1 + 5 * n / max_e
    lines.append(f'  {node_id(a)} -> {node_id(b)} [label="{n}" penwidth={pw:.1f}];')
for a, n in end_freq.items():
    lines.append(f'  {node_id(a)} -> END [label="{n}" penwidth={1+4*n/max_e:.1f} style=dashed];')

n_cases = len(traces)
n_events = len(rows)
n_var = len(set(tuple(a for _, a in sorted(evs)) for evs in traces.values()))
lines.append('  subgraph cluster_legend {')
lines.append('    label="Legend"; fontname="Helvetica"; fontsize=12; style="rounded"; color="#999";')
lines.append('    legend [shape=plaintext label=<')
lines.append('      <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">')
lines.append(f'      <TR><TD COLSPAN="2"><B>Prostate pathway &#8212; {n_cases} cases, {n_events} events, {n_var} variants</B></TD></TR>')
lines.append('      <TR><TD BGCOLOR="#eef4fb">activity (n)</TD><TD ALIGN="LEFT">BPH / diagnostic step &#8212; n = occurrences</TD></TR>')
lines.append('      <TR><TD BGCOLOR="#fde7ea">activity (n)</TD><TD ALIGN="LEFT">cancer branch</TD></TR>')
lines.append('      <TR><TD BGCOLOR="#9e9e9e">Death (other cause)</TD><TD ALIGN="LEFT">competing-risk death (non-prostate)</TD></TR>')
lines.append('      <TR><TD BGCOLOR="#7a0010"><FONT COLOR="white">Death (prostate cancer)</FONT></TD><TD ALIGN="LEFT">PCa-specific death (metastatic branch)</TD></TR>')
lines.append('      <TR><TD BGCOLOR="#2e7d32"><FONT COLOR="white">START</FONT></TD><TD ALIGN="LEFT">trace entry (first recorded event)</TD></TR>')
lines.append('      <TR><TD BGCOLOR="#37474f"><FONT COLOR="white">END</FONT></TD><TD ALIGN="LEFT">trace end &#8212; alive / censored at sim end (NOT death)</TD></TR>')
lines.append('      <TR><TD>edge number</TD><TD ALIGN="LEFT">directly-follows frequency (thicker = more frequent)</TD></TR>')
lines.append('      </TABLE>>];')
lines.append('  }')
lines.append("}")
dot = "\n".join(lines)
open(base + ".dot", "w").write(dot)
for fmt in ("png", "svg"):
    try:
        subprocess.run(["dot", f"-T{fmt}", base + ".dot", "-o", base + "." + fmt], check=True)
        print(f"wrote {base}.{fmt}")
    except Exception as e:
        print(f"render {fmt} failed: {e}")
print(f"cases={len(traces)} activities={len(node_freq)} edges={len(edge_freq)}")

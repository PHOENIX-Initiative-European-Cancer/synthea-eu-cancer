#!/usr/bin/env python3
"""Trace-variant view (fingerprint) from the event log.

Each row = one distinct trace variant (a REAL patient path, not a DFG merge).
Rows are sorted SHORT -> LONG by trace length. A left-hand horizontal histogram
shows each variant's absolute count and percentage. Complements the DFG.

Usage: python3 scripts/variant_view.py [eventlog_csv] [out_png] [max_variants]
Defaults: output/prostate_eventlog.csv -> output/prostate_variants.png, all variants
"""
import csv, sys, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

csv_path = sys.argv[1] if len(sys.argv) > 1 else "output/prostate_eventlog.csv"
out = sys.argv[2] if len(sys.argv) > 2 else "output/prostate_variants.png"
cap = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9

rows = list(csv.DictReader(open(csv_path)))
traces = collections.defaultdict(list)
for r in rows:
    traces[r["case_id"]].append((r["timestamp"], r["activity"]))
variants = collections.Counter()
for evs in traces.values():
    evs.sort(key=lambda x: x[0])
    variants[tuple(a for _, a in evs)] += 1

total = sum(variants.values())
# sort SHORT -> LONG (length asc), ties by frequency desc; keep the most frequent `cap`
shown = sorted(variants.items(), key=lambda kv: (len(kv[0]), -kv[1]))
if len(shown) > cap:
    keep = set(dict(variants.most_common(cap)).keys())
    shown = [(v, n) for v, n in shown if v in keep]
M = len(shown)

# stable color per activity (first appearance)
acts = []
for var, _ in shown:
    for a in var:
        if a not in acts:
            acts.append(a)
cmap = plt.get_cmap("tab20")
color = {a: cmap(i % 20) for i, a in enumerate(acts)}

maxlen = max(len(v) for v, _ in shown)
maxn = max(n for _, n in shown)
fig_h = max(4, 0.40 * M + 1.8)
fig_w = max(11, 0.72 * maxlen + 6)
fig = plt.figure(figsize=(fig_w, fig_h))
gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 3.0], wspace=0.03)
axh = fig.add_subplot(gs[0])
axt = fig.add_subplot(gs[1], sharey=axh)

for i, (var, n) in enumerate(shown):
    axh.barh(i, n, height=0.78, color="#5b8db8", edgecolor="white")
    axh.text(n + maxn * 0.02, i, f"{n} ({100.0*n/total:.1f}%)",
             va="center", ha="left", fontsize=7.5)
    for j, a in enumerate(var):
        axt.add_patch(Rectangle((j, i - 0.39), 1, 0.78, facecolor=color[a],
                                edgecolor="white", linewidth=1.1))

axh.set_xlim(0, maxn * 1.32)
axh.set_ylim(-0.6, M - 0.4)
axh.invert_yaxis()              # shortest trace on top
axh.set_xlabel("cases (n)")
axh.set_yticks([])
axh.set_title("frequency", fontsize=10)
for s in ("top", "right", "left"):
    axh.spines[s].set_visible(False)

axt.set_xlim(0, maxlen)
axt.set_xticks([x + 0.5 for x in range(maxlen)])
axt.set_xticklabels([str(i + 1) for i in range(maxlen)], fontsize=8)
axt.set_xlabel("activity position in trace  (rows sorted short → long)")
axt.set_yticks([])
for s in ("top", "right", "left"):
    axt.spines[s].set_visible(False)

fig.suptitle(f"Prostate pathway — trace variants (short→long), {M} of {len(variants)} variants, "
             f"{total} cases — each row = one REAL patient path", fontsize=11, y=0.995)
legend = [Line2D([0], [0], marker="s", color="w", markerfacecolor=color[a],
                 markersize=11, label=a) for a in acts]
axt.legend(handles=legend, loc="center left", bbox_to_anchor=(1.01, 0.5),
           fontsize=8, frameon=False, title="activity")
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"wrote {out}  |  {len(variants)} variants, {total} cases, showing {M}")

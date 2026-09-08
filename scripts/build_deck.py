#!/usr/bin/env python3
"""Build the SYNDERAI prostate-prototype deck — compressed 8-slide (SHORT) version.
Run: python3 scripts/build_deck.py  ->  output/SYNDERAI_prostate_short.pptx
Full 15-slide version: scripts/build_deck_full.py -> output/SYNDERAI_prostate_full.pptx
Style: plain navy content layout (no swoosh), red accent bar + white descriptive
title, one lead sentence, single-line statement points (bold head - short tail).
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from PIL import Image
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = "/Users/thome/.claude/skills/bih-presentation/assets/templates/BIH_16x9.pptx"
base = os.path.join(HERE, "output") + "/"

prs = Presentation(TPL)
sldIdLst = prs.slides._sldIdLst
for sid in list(sldIdLst):
    prs.part.drop_rel(sid.get(qn('r:id'))); sldIdLst.remove(sid)
L = {x.name.strip(): x for x in prs.slide_layouts}
TITLE = L["Titelfolie"]; PLAIN = L["Text einspaltig 02"]

W = RGBColor(0xFF, 0xFF, 0xFF); R = RGBColor(0xE6, 0x00, 0x2d); M = RGBColor(0xC3, 0xCE, 0xD8)
NV = RGBColor(0x0b, 0x3d, 0x5c); DK = RGBColor(0x22, 0x22, 0x22); LK = RGBColor(0x8f, 0xc1, 0xe3)
GR = RGBColor(0x3f, 0xb9, 0x50)


def new():
    sl = prs.slides.add_slide(PLAIN)
    for s in list(sl.shapes):
        if s.is_placeholder:
            s._element.getparent().remove(s._element)
    return sl


def box(sl, x, y, w, h):
    tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.text_frame.word_wrap = True
    return tb.text_frame


def run(p, t, s, c, b=False):
    r = p.add_run(); r.text = t; r.font.size = Pt(s); r.font.color.rgb = c; r.font.bold = b
    r.font.name = "Fira Sans"
    return r


def header(sl, title, tsize=28):
    bar = sl.shapes.add_shape(1, Inches(1.0), Inches(0.95), Inches(1.6), Inches(0.06))
    bar.fill.solid(); bar.fill.fore_color.rgb = R; bar.line.fill.background()
    run(box(sl, 1.0, 1.15, 11.4, 1.0).paragraphs[0], title, tsize, W, b=True)


def marker(sl, y, x=1.05, col=R):
    m = sl.shapes.add_shape(1, Inches(x), Inches(y + 0.09), Inches(0.16), Inches(0.16))
    m.fill.solid(); m.fill.fore_color.rgb = col; m.line.fill.background()


def points(sl, pts, y0=4.0, step=0.86, w=10.7):
    y = y0
    for head, txt in pts:
        marker(sl, y); tf = box(sl, 1.45, y - 0.05, w, 0.9); p = tf.paragraphs[0]
        run(p, head, 17, W, b=True)
        if txt:
            run(p, "  —  " + txt, 17, M)
        y += step
    return y


def substantive(title, lead, pts, closing=None, y0=4.0, step=0.86, lead_y=2.5):
    sl = new(); header(sl, title)
    if lead:
        run(box(sl, 1.0, lead_y, 11.2, 1.1).paragraphs[0], lead, 21, W)
    endy = points(sl, pts, y0=y0, step=step)
    if closing:
        run(box(sl, 1.0, max(endy + 0.15, 6.7), 11.2, 0.6).paragraphs[0], closing, 14, M)
    return sl


def two_col(title, lead, left_head, left_items, right_head, right_items,
            left_glyph="✓", right_glyph="→", left_col=GR, right_col=R):
    sl = new(); header(sl, title)
    if lead:
        run(box(sl, 1.0, 2.35, 11.3, 1.0).paragraphs[0], lead, 18, W)

    def col(x, ch, gl, items, gcol):
        run(box(sl, x, 3.55, 5.3, 0.5).paragraphs[0], ch, 18, W, b=True)
        u = sl.shapes.add_shape(1, Inches(x + 0.02), Inches(4.05), Inches(1.1), Inches(0.045))
        u.fill.solid(); u.fill.fore_color.rgb = gcol; u.line.fill.background()
        y = 4.3
        for head, tail in items:
            tf = box(sl, x, y, 5.8, 0.6); p = tf.paragraphs[0]
            run(p, gl + "  ", 14, gcol, b=True)
            run(p, head, 14.5, W, b=True)
            if tail:
                run(p, "  " + tail, 14.5, M)
            y += 0.58
    col(1.0, left_head, left_glyph, left_items, left_col)
    col(6.9, right_head, right_glyph, right_items, right_col)
    return sl


def table_slide(title, data, widths, fs=14, vbold=True, cap=None):
    sl = new(); header(sl, title)
    gf = sl.shapes.add_table(len(data), len(widths), Inches(1.0), Inches(2.25),
                             Inches(sum(widths)), Inches(4.2)); tbl = gf.table
    for i, wd in enumerate(widths):
        tbl.columns[i].width = Inches(wd)
    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            c = tbl.cell(ri, ci); c.text = val; pa = c.text_frame.paragraphs[0]
            pa.font.name = "Fira Sans"; pa.font.size = Pt(fs); c.fill.solid()
            if ri == 0:
                c.fill.fore_color.rgb = NV; pa.font.bold = True; pa.font.color.rgb = W
            else:
                c.fill.fore_color.rgb = W; pa.font.color.rgb = DK
                if vbold and ci == 1:
                    pa.font.bold = True
    if cap:
        run(box(sl, 1.0, 6.65, 11.4, 0.8).paragraphs[0], cap, 13, M)
    return sl


def image_points(title, lead, pts, img):
    sl = new(); header(sl, title, tsize=25)
    if lead:
        run(box(sl, 1.0, 2.05, 11.3, 0.7).paragraphs[0], lead, 17, M)
    y = 3.15
    for head, txt in pts:
        marker(sl, y, x=1.05); tf = box(sl, 1.45, y - 0.05, 4.5, 1.3); p = tf.paragraphs[0]
        run(p, head, 16, W, b=True)
        if txt:
            q = tf.add_paragraph(); run(q, txt, 14, M)
        y += 1.2
    iw, ih = Image.open(img).size; ar = iw / ih; bw, bh = 6.3, 4.6; ox, oy = 6.4, 2.4
    (w, h) = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
    sl.shapes.add_picture(img, Inches(ox + (bw - w) / 2), Inches(oy + (bh - h) / 2), Inches(w), Inches(h))
    return sl


# ── 1 · Title ────────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(TITLE); ph = {s.placeholder_format.idx: s for s in sl.shapes if s.is_placeholder}
if 0 in ph:
    ph[0].text_frame.text = "Synthetic Data for Cancer Research"
if 1 in ph:
    tf = ph[1].text_frame; tf.clear()
    tf.paragraphs[0].text = "A Phoenix Initiative prototype — prostate cancer pathways"
    for r in tf.paragraphs[0].runs:
        r.font.size = Pt(22)
    p = tf.add_paragraph(); p.text = "Thomas Debertshäuser · Charité / BIH · HL7 Europe SYNDERAI"
    for r in p.runs:
        r.font.size = Pt(16)

# ── 2 · Why + prototype ──────────────────────────────────────────────────────
substantive("Synthetic cancer cohorts — a prostate prototype",
    "Real registry data is privacy-locked and carries no ground truth. We generate calibrated, shareable cohorts instead — starting with prostate cancer.",
    [("Shareable & PII-free", "no data-access agreements, no ethics gates"),
     ("Known ground truth", "the care process is designed, not inferred"),
     ("The prototype", "Synthea pathway, males 50–60: symptoms → BPH or cancer → metastatic"),
     ("Standards-native", "FHIR R4 · SNOMED · LOINC · dual ATC")],
    "SYNDERAI delivers this for the EHDS; the Phoenix Initiative is the cancer flavour.",
    y0=3.7, step=0.78, lead_y=2.35)

# ── 3 · Evidence (+ worked example as the takeaway) ──────────────────────────
table_slide("Every transition is calibrated on evidence",
    [("Effect (transition)", "Value", "Source"),
     ("PI-RADS 3 / 4 / 5 → cancer", "16 / 59 / 85 %", "Oerther 2021"),
     ("Treatment: RP / RT / AS", "57 / 16 / 16 %", "HAROW (Herden 2016)"),
     ("Incidental cancer at TURP", "14 %", "Sid Ahmed 2025"),
     ("EAU risk groups (low/int/high/adv)", "27 / 24 / 37 / 13 %", "Xie 2021 (SEER)"),
     ("Biochemical recurrence (high / low)", "40 / 20 %", "S3 Ch. 7"),
     ("De-novo M1 (age 50–60)", "6 %", "SEER (Mali 2025)")],
    (5.1, 2.9, 3.5),
    cap="Worked example — the guideline gives no number for PI-RADS→cancer; ours (16/59/85 %, Oerther 2021, "
        "patient-level) is full-text verified: exact. ~40 arrows traced this way · 25 sources · ESMO converges.")

# ── 4 · FHIR cohort + process mining ─────────────────────────────────────────
image_points("A real FHIR cohort — and you can mine it",
    "1,112 seed-pinned FHIR R4 patients; the designed process is the ground truth you validate against.",
    [("Reproducible", "seed-pinned, with FHIR provenance"),
     ("Real timeline", "diagnosis → recurrence → salvage over years"),
     ("Process mining", "directly-follows graph from the synthetic traces")],
    base + "prostate_dfg.png")

# ── 5 · EHDS gap → CCDM ballot ───────────────────────────────────────────────
sl = substantive("EHDS moves the data; the Common Cancer Model adds the content",
    "EHDS defines the exchange infrastructure and generic document types — but no disease-specific cancer content.",
    [("Generic priority categories", "patient summary, prescription, labs, imaging, discharge"),
     ("No cancer data points", "staging, treatment response, progression not modelled"),
     ("HL7 Europe Common Cancer Model", "minimal cancer model, mapped to FHIR + OMOP"),
     ("In STU1 ballot now", "1 Jul – 31 Aug 2026 · comments via HL7 Jira")],
    y0=3.4, step=0.72, lead_y=2.35)
y = 6.35
l = sl.shapes.add_shape(1, Inches(1.1), Inches(y + 0.16), Inches(10.6), Inches(0.03))
l.fill.solid(); l.fill.fore_color.rgb = M; l.line.fill.background()
for dx, lab in [(1.1, "Feb 2025 · Phoenix"), (4.4, "Jun 2026 · build"),
                (7.0, "Jul–Aug 2026 · ballot"), (10.0, "~2027 · EHDS acts")]:
    d = sl.shapes.add_shape(9, Inches(dx), Inches(y), Inches(0.26), Inches(0.26))
    d.fill.solid(); d.fill.fore_color.rgb = R; d.line.fill.background()
    run(box(sl, dx - 0.1, y + 0.34, 2.9, 0.5).paragraphs[0], lab, 11, W)

# ── 6 · Bridge + status ──────────────────────────────────────────────────────
two_col("Making the model testable — without real data",
    "The model has no FHIR profiles yet. Synthetic cohorts are the foundation to validate it today — and let vendors build without a real-data project.",
    "Here today",
    [("Calibrated generator", "module weights + states"),
     ("Evidence-traced", "~40 transitions to source"),
     ("EU terminology", "SNOMED · LOINC · dual ATC"),
     ("FHIR R4 output", "reproducible cohort per run"),
     ("Process mining", "DFG + trace variants")],
    "Still missing",
    [("Temporal axis", "how long between events"),
     ("", "time-to-treatment · BCR-free · time-to-mets"),
     ("Progression hazards", "flat, not time-dependent yet"),
     ("S3 v8.1 depth", "PSA screening · PSMA-PET · PARP"),
     ("EU demographics", "still US incidence · CCDM mapping")])

# ── 7 · Caveat ───────────────────────────────────────────────────────────────
substantive("In context — one of many projects",
    "Synthetic data is a foundation, not the whole answer.",
    [("Part of an ecosystem", "alongside IDEA4RC, mCODE, national cancer-data initiatives"),
     ("Complements, does not replace", "real-world validation stays essential"),
     ("The value", "shareable, PII-free, available today")])

# ── 8 · Appendix · sources ───────────────────────────────────────────────────
sl = new(); header(sl, "Appendix · sources & traceability")


def lo(d):
    return (d, d.split("//")[1]) if d.startswith("http") else ("https://doi.org/" + d, "doi.org/" + d)


left = [("Guidelines & consensus", [("EAU 2024", "10.1016/j.eururo.2024.03.027"), ("S3-Leitlinie v8.1 (2025)", "https://www.leitlinienprogramm-onkologie.de/leitlinien/prostatakarzinom"), ("ISUP grading, Egevad 2016", "10.1111/apm.12533")]),
        ("Diagnostic pathway", [("Oerther 2021 (PI-RADS meta)", "10.1038/s41391-021-00417-1"), ("PRECISION-type MRI 2020", "10.1038/s41391-020-00290-4"), ("Nordström 2021 (LUTS→PCa)", "10.1016/j.euros.2020.12.004"), ("Irish PSA 2012", "10.5402/2012/832109"), ("Taiwanese PSA 2023", "10.1371/journal.pone.0283040"), ("Grey-zone PSAD 2021", "10.1186/s12885-021-08216-6")]),
        ("Grading & staging", [("Xie 2021 (SEER risk groups)", "10.3389/fonc.2021.646073"), ("NCDB grade migration 2023", "10.1093/jncics/pkad018"), ("SEER <50, Mali 2025", "10.1002/hsr2.70414"), ("Mathieu 2017 (ISUP validation)", "10.3389/fmed.2017.00157")])]
right = [("Treatment & outcome", [("HAROW, Herden 2016", "10.3238/arztebl.2016.0329"), ("HAROW-AS, Herden 2020", "10.1007/s00345-020-03471-x"), ("Sid Ahmed 2025 (incidental TURP)", "10.7759/cureus.90916"), ("NRW survival 2024", "10.1016/j.clgc.2024.102289"), ("DE vs US survival, Winter 2016", "10.1111/bju.13537")]),
         ("Epidemiology & detection", [("Lower-Saxony incidence 2021", "10.3389/fonc.2021.681006"), ("UrEpik, Boyle 2003", "10.1046/j.1464-410x.2003.04369.x"), ("EPIC LUTS, Irwin 2009", "10.1016/j.eururo.2009.02.026"), ("BPH epidemiology 2017", "10.1016/j.ajur.2017.06.004"), ("LUTS & PSA, BJGP 2018", "10.3399/bjgp18X699689"), ("NCDA screen-detected 2024", "10.3399/BJGP.2024.0376")])]


def colf(x, groups):
    tf = box(sl, x, 2.3, 6.15, 5.0); first = True
    for head, items in groups:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False; p.space_before = Pt(4)
        run(p, head, 13, W, b=True)
        for label, doi in items:
            url, disp = lo(doi); q = tf.add_paragraph(); q.level = 1
            run(q, "•  " + label + " — ", 10.5, W)
            rb = run(q, disp, 10.5, LK); rb.hyperlink.address = url


colf(0.55, left); colf(6.85, right)

out = os.path.join(HERE, "output", "SYNDERAI_prostate_short.pptx")
prs.save(out)
print("saved:", len(prs.slides), "slides ->", out)

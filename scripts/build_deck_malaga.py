#!/usr/bin/env python3
"""Build the ECCM/Málaga-prep deck — synthetic data for the European Common Cancer Model.
Run: python3 scripts/build_deck_malaga.py  ->  output/ECCM_Malaga_prep.pptx
21 talk slides + appendix backup. Audience: OHDSI Europe, FHIR-community view.
Style: plain navy content layout, red accent bar + white descriptive title,
one lead sentence, single-line statement points (bold head - tail).
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_CONNECTOR
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
GR = RGBColor(0x3f, 0xb9, 0x50); PANEL = RGBColor(0x14, 0x4a, 0x6b)


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
        run(box(sl, 1.0, 2.35, 11.3, 1.0).paragraphs[0], lead, 19, W)

    def col(x, ch, gl, items, gcol):
        run(box(sl, x, 3.35, 5.3, 0.5).paragraphs[0], ch, 18, W, b=True)
        u = sl.shapes.add_shape(1, Inches(x + 0.02), Inches(3.85), Inches(1.1), Inches(0.045))
        u.fill.solid(); u.fill.fore_color.rgb = gcol; u.line.fill.background()
        y = 4.1
        for head, tail in items:
            tf = box(sl, x, y, 5.8, 0.6); p = tf.paragraphs[0]
            run(p, gl + "  ", 14, gcol, b=True)
            run(p, head, 14.5, W, b=True)
            if tail:
                run(p, "  " + tail, 14.5, M)
            y += 0.6
    col(1.0, left_head, left_glyph, left_items, left_col)
    col(6.9, right_head, right_glyph, right_items, right_col)
    return sl


def table_slide(title, data, widths, fs=14, vbold=True, cap=None):
    sl = new(); header(sl, title)
    gf = sl.shapes.add_table(len(data), len(widths), Inches(1.0), Inches(2.35),
                             Inches(sum(widths)), Inches(4.3)); tbl = gf.table
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
        run(box(sl, 1.0, 6.75, 11.4, 0.7).paragraphs[0], cap, 13, M)
    return sl


def divider(kicker, title):
    sl = new()
    bar = sl.shapes.add_shape(1, Inches(1.0), Inches(2.7), Inches(1.6), Inches(0.08))
    bar.fill.solid(); bar.fill.fore_color.rgb = R; bar.line.fill.background()
    run(box(sl, 1.0, 2.95, 11.0, 0.6).paragraphs[0], kicker, 18, M, b=True)
    run(box(sl, 1.0, 3.5, 11.4, 1.6).paragraphs[0], title, 40, W, b=True)
    return sl


def chip(sl, x, y, w, txt, col=NV, tcol=None, h=0.52, fs=13, bold=True):
    s = sl.shapes.add_shape(5, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = col; s.line.fill.background()
    tf = s.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.06); tf.margin_top = tf.margin_bottom = Inches(0.03)
    from pptx.enum.text import PP_ALIGN
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, txt, fs, tcol or W, b=bold)
    return s


def image2_slide(title, img1, lab1, img2, lab2, cap=None):
    sl = new(); header(sl, title, tsize=25)
    for img, lab, x in [(img1, lab1, 0.75), (img2, lab2, 6.85)]:
        iw, ih = Image.open(img).size; ar = iw / ih; bw, bh = 5.75, 3.95
        (w, h) = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
        sl.shapes.add_picture(img, Inches(x + (bw - w) / 2), Inches(2.35 + (bh - h) / 2), Inches(w), Inches(h))
        run(box(sl, x, 2.35 + bh + 0.12, bw, 0.45).paragraphs[0], lab, 13, W, b=True)
    if cap:
        run(box(sl, 1.0, 7.0, 11.4, 0.5).paragraphs[0], cap, 13, M)
    return sl


def image_slide(title, img, cap=None, box_h=4.9):
    sl = new(); header(sl, title, tsize=25)
    iw, ih = Image.open(img).size; ar = iw / ih; bw, bh = 11.4, box_h
    (w, h) = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
    sl.shapes.add_picture(img, Inches(0.95 + (bw - w) / 2),
                          Inches(2.25 + (bh - h) / 2), Inches(w), Inches(h))
    if cap:
        run(box(sl, 1.0, 2.25 + box_h + 0.1, 11.4, 0.6).paragraphs[0], cap, 13, M)
    return sl


# ═════════════════════════════ TALK — 21 slides ══════════════════════════════

# ── 1 · Title ────────────────────────────────────────────────────────────────
sl = prs.slides.add_slide(TITLE); ph = {s.placeholder_format.idx: s for s in sl.shapes if s.is_placeholder}
if 0 in ph:
    ph[0].text_frame.text = "Synthetic Data for the European Common Cancer Model"
if 1 in ph:
    tf = ph[1].text_frame; tf.clear()
    tf.paragraphs[0].text = "Draft profiles · first implementation feedback · a FHIR-community view for OHDSI Europe"
    for r in tf.paragraphs[0].runs:
        r.font.size = Pt(22)
    p = tf.add_paragraph(); p.text = "Thomas Debertshäuser · Charité / BIH · HL7 Europe SYNDERAI · Phoenix Initiative"
    for r in p.runs:
        r.font.size = Pt(16)

# ── 2 · Agenda ───────────────────────────────────────────────────────────────
substantive("The route",
    None,
    [("Part I — The rails", "EHDS, EEHRxF and the HL7 Europe specification stack"),
     ("Part II — The model", "the European Common Cancer Model up close — and its OMOP leg"),
     ("Part III — The test", "a calibrated synthetic prostate cohort, validated against the draft profiles")],
    y0=3.2, step=1.05)

# ── 3 · Why synthetic ────────────────────────────────────────────────────────
substantive("Why synthetic cancer cohorts",
    "Real cancer-registry data is privacy-locked, slow to share, and offers no ground truth to validate against.",
    [("We cannot wait", "another round of consortial data-sharing agreements, DPIAs and ethics votes takes years"),
     ("Shareable & PII-free", "no agreements, no gates — send it to anyone, today"),
     ("EU-conformant", "SNOMED CT · LOINC · dual ATC"),
     ("Known ground truth", "the care process is designed, not inferred")],
    "SYNDERAI delivers this for the European Health Data Space; the Phoenix Initiative is the cancer flavour.",
    y0=3.7, step=0.8)

# ── 4 · EHDS: law + clock ────────────────────────────────────────────────────
sl = new(); header(sl, "The EHDS — one law, two pillars, one clock")
run(box(sl, 1.0, 2.2, 11.2, 0.9).paragraphs[0],
    "Regulation (EU) 2025/327, in force since March 2025 — primary use (care, Ch. II) and secondary use (research, Ch. IV).", 19, W)
run(box(sl, 1.0, 3.1, 11.2, 0.6).paragraphs[0],
    "The six priority categories (Art. 14) arrive in two waves:", 17, M)
y = 4.3
l = sl.shapes.add_shape(1, Inches(1.1), Inches(y + 0.16), Inches(11.0), Inches(0.03))
l.fill.solid(); l.fill.fore_color.rgb = M; l.line.fill.background()
for dx, date, lab in [
        (1.1, "26 Mar 2025", "in force"),
        (3.3, "26 Mar 2027", "applies · EEHRxF\nimplementing acts due"),
        (5.7, "26 Mar 2029", "wave 1: summaries, eP/eD\n+ secondary use (Ch. IV)"),
        (8.1, "26 Mar 2031", "wave 2: imaging, labs,\ndischarge · genomic data"),
        (10.5, "26 Mar 2035", "third countries join\nHealthData@EU")]:
    d = sl.shapes.add_shape(9, Inches(dx), Inches(y), Inches(0.3), Inches(0.3))
    d.fill.solid(); d.fill.fore_color.rgb = R; d.line.fill.background()
    run(box(sl, dx - 0.25, y + 0.5, 2.5, 0.45).paragraphs[0], date, 16, W, b=True)
    tf = box(sl, dx - 0.25, y + 0.95, 2.5, 1.3)
    for i, line in enumerate(lab.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run(p, line, 13, M)
run(box(sl, 1.0, 6.85, 11.4, 0.5).paragraphs[0],
    "The Art. 15 implementing acts (EEHRxF technical specifications) are the big open item — due 26 March 2027.", 14, M)

# ── 5 · EEHRxF: syntax by law, semantics by the stack ────────────────────────
substantive("EEHRxF — syntax by law, semantics by the stack",
    "The exchange format is what Article 15 tells the Commission to lay down — one format for all six categories.",
    [("Mainly syntax, little semantics", "it standardises structure and format — terminology and clinical depth stay thin"),
     ("The stack fills the semantics", "eHN guidelines → Xt-EHR logical models v1.0.0 → HL7 Europe FHIR IGs"),
     ("Note the pattern", "logical model first, serializations second — the Common Cancer Model works the same way")],
    "Syntax alone does not analyse — the FHIR layer is where meaning gets bound.")

# ── 6 · What FHIR is ─────────────────────────────────────────────────────────
substantive("FHIR — more than a wire format",
    "For this room: FHIR is an exchange language, and it is four things at once.",
    [("A data model", "resources — Patient, Condition, Observation — constrained by profiles"),
     ("An exchange format", "JSON / XML over a REST API — the wire syntax the EEHRxF rides on"),
     ("A technical ecosystem", "servers, validators, SDKs, terminology services — open source, off the shelf"),
     ("A community", "connectathons, working groups, ballots — specifications are grown, not decreed")],
    "The last one is the point this talk relies on: the feedback loop is a community feature.",
    y0=3.7, step=0.8)

# ── 7 · IGs in practice ──────────────────────────────────────────────────────
image2_slide("This is what they actually look like",
    base + "ig_laboratory.png", "Laboratory Report · STU 2.0 · published",
    base + "ig_eps.png", "European Patient Summary · STU1 ballot",
    cap="One family at hl7.eu/fhir — four IGs published, five in ballot · the full landscape table is in the appendix.")

# ── 8 · One format, both use cases ───────────────────────────────────────────
substantive("One structured format for both use cases",
    "What we want: FHIR as the de facto output of clinical software — for primary and secondary use alike.",
    [("Primary use is FHIR", "the EEHRxF specifications are FHIR IGs — structured at the source, not scanned PDFs"),
     ("Bindings add what the format lacks", "profiles bind SNOMED CT, LOINC, ATC, UCUM — semantics the bare syntax does not mandate"),
     ("Secondary use inherits both", "structure and coded meaning — access bodies can only serve what care recorded"),
     ("The payoff for this room", "SNOMED and LOINC in FHIR are already OMOP standard concepts — the ETL shrinks")],
    y0=3.7, step=0.8)

# ── 9 · Secondary use + SYNDERAI teaser ──────────────────────────────────────
substantive("Secondary use — where this room comes in",
    "Chapter IV builds a research access layer over the same data, applying from March 2029.",
    [("Access bodies + HealthData@EU", "permits replace per-project negotiations · pilot ran 2022–2024"),
     ("Cancer was already a use case", "the pilot tested genomic signatures in colorectal cancer"),
     ("The analytics gap", "turning exchange data into analysis-ready OMOP is our shared job"),
     ("SYNDERAI — data to practise on", "1,000+ synthetic lab reports · ~1,000 patient summaries · and a cancer arm: Part II")],
    y0=3.7, step=0.8)

# ── 10 · Thesis ──────────────────────────────────────────────────────────────
substantive("Top-down alone will not produce quality data",
    "You can mandate a format and a deadline. You cannot mandate that the data inside is right.",
    [("Top-down", "regulation → format → dates — necessary, but it standardises containers, not content"),
     ("Bottom-up, complementary", "build the disease model, implement it, generate data, validate, feed back"),
     ("Where they meet", "the ECCM runs exactly this loop: model → profiles → test data → feedback")],
    "The rest of this talk is the bottom-up loop in action.")

# ── 11 · Model landscape ─────────────────────────────────────────────────────
table_slide("The starting point — no existing model carries Europe",
    [("Cancer data model / initiative", "FHIR?", "Why it does not generalise"),
     ("mCODE / CodeX (US)", "yes", "US Core baseline — US context, terminologies, identifiers"),
     ("IDEA4RC (EU)", "yes", "rare cancers & sarcomas — not representative"),
     ("PanCareSurPass (EU)", "yes", "paediatric cancer survivorship — a niche"),
     ("oBDS (German cancer registries)", "not yet", "strong national dataset — no FHIR layer"),
     ("OSIRIS (INCa, France)", "yes", "a specification without available data"),
     ("CanDLE · Genomic Data Infrastructure", "no", "strong domains — project-funded, built beside the EHR rails")],
    (3.9, 1.3, 6.2), fs=13.5, vbold=True,
    cap="The gap: minimal, cancer-agnostic, European, on FHIR — with data to test it. Standards outlive projects.")

# ── 12 · ECCM status + timeline ──────────────────────────────────────────────
sl = substantive("The Common Cancer Model — from ballot to draft profiles",
    "A minimal, cancer-agnostic model by HL7 Europe under the Phoenix working group — now growing its FHIR layer.",
    [("Logical model balloted", "STU1 · Jul–Aug 2026 · comment resolution under way"),
     ("13 draft FHIR profiles", "condition · stage · histology · treatments · progression · follow-up"),
     ("One model, two legs", "the logical model maps to FHIR (exchange) and OMOP (analytics) · hl7.eu/fhir/cancer-common")], y0=3.55)
y = 6.35
l = sl.shapes.add_shape(1, Inches(1.1), Inches(y + 0.16), Inches(10.6), Inches(0.03))
l.fill.solid(); l.fill.fore_color.rgb = M; l.line.fill.background()
for dx, lab in [(1.1, "Feb 2025 · Phoenix"), (3.9, "Jun 2026 · build"),
                (6.4, "Jul–Aug 2026 · ballot"), (9.6, "Málaga · discuss & iterate")]:
    d = sl.shapes.add_shape(9, Inches(dx), Inches(y), Inches(0.26), Inches(0.26))
    d.fill.solid(); d.fill.fore_color.rgb = R; d.line.fill.background()
    run(box(sl, dx - 0.1, y + 0.34, 2.9, 0.5).paragraphs[0], lab, 11, W)

# ── 13 · Two years in + value streams ────────────────────────────────────────
substantive("Two years in — and what we do from now on",
    "The first ballot delivered little community feedback. Why? A conceptual / logical model is hard to test.",
    [("Nothing to run, nothing to find", "no profiles, no data, no validator — reading a spec surfaces few defects"),
     ("Implementation delivered a lot", "profiles + synthetic data + validator → a full findings list within weeks"),
     ("So every iteration now ships runnable", "SYNDERAI-Cancer cohorts, CC0 — the preview of European cancer data"),
     ("Plus the useful extras", "medication & regimen definitions · terminology and mapping support")],
    "Hand people something to run, not only something to read.",
    y0=3.5, step=0.78)

# ── 14 · Anatomy ─────────────────────────────────────────────────────────────
sl = new(); header(sl, "Anatomy of the model — eleven entities, one journey")
run(box(sl, 1.0, 2.0, 11.4, 0.5).paragraphs[0],
    "Everything hangs off the condition at diagnosis — the model describes a cancer journey, not a document.", 17, W)


def panel(x, y, w, h, label, chips, ccol=NV):
    pn = sl.shapes.add_shape(5, Inches(x), Inches(y), Inches(w), Inches(h))
    pn.fill.solid(); pn.fill.fore_color.rgb = PANEL; pn.line.color.rgb = M; pn.line.width = Pt(0.75)
    run(box(sl, x + 0.15, y + 0.06, w - 0.3, 0.4).paragraphs[0], label, 13, LK, b=True)
    cw = (w - 0.3 - 0.1 * (2 - 1)) / 2
    for i, c in enumerate(chips):
        cx = x + 0.15 + (i % 2) * (cw + 0.1); cy = y + 0.52 + (i // 2) * 0.62
        chip(sl, cx, cy, cw, c, col=ccol, fs=12.5)
    return pn


chip(sl, 0.7, 3.35, 2.5, "Cancer Patient", col=NV, fs=14, h=0.55)
chip(sl, 0.7, 4.35, 2.5, "Condition at Diagnosis", col=R, fs=14, h=0.75)
ln = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(1.95), Inches(3.9), Inches(1.95), Inches(4.35))
ln.line.color.rgb = M; ln.line.width = Pt(1.5)
panel(3.9, 2.75, 4.25, 1.85, "DISEASE & EXTENT",
      ["Cancer Stage", "Histology / Behaviour", "Clinical Progression"])
panel(8.35, 2.75, 4.25, 1.85, "TREATMENT",
      ["Surgery", "Radiotherapy", "Systemic Treatment", "Active Surveillance"])
panel(3.9, 4.8, 4.25, 1.25, "OUTCOME",
      ["Treatment Response", "Last Follow-Up"])
panel(8.35, 4.8, 4.25, 1.25, "CONTEXT",
      ["Imaging", "Comorbidities"])
for tx, ty in [(3.9, 3.65), (3.9, 5.4)]:
    ln = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(3.2), Inches(4.7), Inches(tx), Inches(ty))
    ln.line.color.rgb = M; ln.line.width = Pt(1.5)
run(box(sl, 1.0, 6.55, 11.4, 0.5).paragraphs[0],
    "11 logical entities · every one carries a reference back to the condition at diagnosis (and, where relevant, to a progression).", 13, M)

# ── 15 · OMOP vs FHIR strengths ──────────────────────────────────────────────
two_col("Different strengths — deliberately so",
    "Not competitors: one is built for analysis, the other for care — and care includes the future tense.",
    "OMOP CDM — built for analysis",
    [("Retrospective by design", "records what happened"),
     ("Harmonised concept space", "one vocabulary, clean cohorts"),
     ("Population-scale evidence", "the analytics home turf")],
    "FHIR — built for care, incl. planning",
    [("The future tense", "request vs. event — orders, plans, schedules"),
     ("Workflow components", "CarePlan · ServiceRequest · Task"),
     ("Executable knowledge", "PlanDefinition/$apply — see the outlook")],
    left_glyph="▪", right_glyph="▪", left_col=LK, right_col=R)

# ── 16 · Medication coding ───────────────────────────────────────────────────
substantive("Medication coding — where EU reality meets OMOP",
    "Drugs are the hardest crosswalk in the room: Europe classifies, OMOP standardises on products.",
    [("ATC", "what EU source data carries — substance-level classification with DDDs · our cohort: dual WHO + ATC-DE"),
     ("RxNorm (+ Extension)", "OMOP's standard drug vocabulary — product level, US-rooted · no IDMP link today"),
     ("The mapping is lossy by design", "finasteride = G04CB01 or D11AX10 by indication · combinations n:m · curated maps disagree"),
     ("IDMP is the bridge being built", "EMA SPOR live · PMS product API in beta 2026 · PhPID assignment not yet operational")],
    "Thesis: OMOP need not adopt IDMP — one global PhPID → RxNorm(+Extension) adapter would do. Who builds it?",
    y0=3.7, step=0.8)

# ── 16b · Medication: plan vs. reality, class vs. product ────────────────────
sl = new(); header(sl, "Planned is not given — and recommended is a class")
run(box(sl, 1.0, 1.95, 11.4, 0.6).paragraphs[0],
    "Recommendations speak in drug classes, care happens in products — and reality deviates from the plan.", 17, W)
cols = [
    ("RECOMMENDED", "“an ARPI”", "drug-class level", "guideline · ATC class / ValueSet"),
    ("PLANNED", "enzalutamide", "160 mg / day", "PlanDefinition → CarePlan"),
    ("ORDERED · DISPENSED", "product & pack", "the concrete drug", "MedicationRequest · Dispense"),
    ("GIVEN", "what actually happened", "reduced · switched · stopped", "Administration / Statement"),
]
for i, (kick, l1, l2, res) in enumerate(cols):
    x = 0.8 + i * 2.98
    pn = sl.shapes.add_shape(5, Inches(x), Inches(2.85), Inches(2.75), Inches(2.35))
    pn.fill.solid(); pn.fill.fore_color.rgb = PANEL; pn.line.color.rgb = M; pn.line.width = Pt(0.75)
    from pptx.enum.text import PP_ALIGN
    tf = box(sl, x + 0.1, 3.0, 2.55, 0.4); p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, kick, 11, LK, b=True)
    tf = box(sl, x + 0.1, 3.55, 2.55, 1.0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; run(p, l1, 15, W, b=True)
    p = tf.add_paragraph(); p.alignment = PP_ALIGN.CENTER; run(p, l2, 13, W)
    tf = box(sl, x + 0.1, 4.65, 2.55, 0.5); p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run(p, res, 10.5, M)
    if i < 3:
        from pptx.enum.shapes import MSO_SHAPE
        ar = sl.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.76), Inches(3.88), Inches(0.24), Inches(0.22))
        ar.fill.solid(); ar.fill.fore_color.rgb = R; ar.line.fill.background()
brk = sl.shapes.add_shape(1, Inches(3.85), Inches(5.35), Inches(8.7), Inches(0.03))
brk.fill.solid(); brk.fill.fore_color.rgb = R; brk.line.fill.background()
run(box(sl, 3.85, 5.45, 8.7, 0.4).paragraphs[0],
    "plan → given: the deviation is the adherence signal — analysable only if both sides are recorded", 12, R)
points(sl, [
    ("OMOP's DRUG_EXPOSURE sees only the last column", "plan, intent and deviation live upstream — in FHIR"),
    ("Class-level recommendations need class-aware terminology", "bind ATC classes / ValueSets, resolve at order time")],
    y0=6.1, step=0.62, w=11.0)

# ── 17 · Prostate test bed + pipeline ────────────────────────────────────────
substantive("The test bed — a synthetic prostate cohort on the draft profiles",
    "Built on open-source Synthea for males aged 50–60, from first symptoms to metastatic disease.",
    [("Symptom-triggered, full journey", "LUTS → work-up → diagnosis → treatment → recurrence → metastatic"),
     ("Reproducible scale", "1,000-patient cohort per run · 115 cancer journeys · FHIR R4, EU terminology"),
     ("Evidence-calibrated", "~40 transitions traced to 25 primary sources — table in the appendix"),
     ("Post-processed onto the 13 draft profiles", "derives cTNM / pTNM, histology, episodes, progression, follow-up"),
     ("Validator gate: 0 errors", "HL7 Java validator against the pinned draft build")],
    "To our knowledge the first end-to-end implementation of the drafts — that is where the feedback comes from.",
    y0=3.45, step=0.68)

# ── 18 · Sankey ──────────────────────────────────────────────────────────────
image_slide("The cohort at a glance — 115 synthetic cancer journeys",
    base + "prostate_sankey_en_crop.png", box_h=4.55,
    cap="Nodes = calibrated branch points · colours = EAU risk group · a visual cross-check against the calibration targets")

# ── 19 · Feedback ────────────────────────────────────────────────────────────
substantive("Implementing the drafts — findings & feedback",
    "Six substantive comments filed, several already fixed — and three things that are cheap now, breaking later.",
    [("TNM component binding", "deprecated PhenX LOINC in the example — recommend SNOMED UICC-8 qualifiers (AJCC is licensed)"),
     ("Underspecified corners", "no pathological-stage example · mixed topography axes · no pT1 in prostate"),
     ("Breaking-if-fixed typos", "'systematic-treatemmt-*' leaks into instance extension URLs — fix before instances exist"),
     ("Offer: a synthetic test corpus", "journeys as IG examples / ballot test data — CC0, SYNDERAI-tagged")],
    y0=3.7, step=0.8)

# ── 20 · Outlook: foundational layer + HemOnc ────────────────────────────────
substantive("The foundational layer — knowledge, not just data",
    "How do we support cancer care and research below the data level? Four pillars — all FHIR-native, all reusable.",
    [("Represent clinical knowledge", "local, national, European guidelines as computable artefacts — PlanDefinition · Library"),
     ("Terminology guidance", "catalogues, bindings, validation support — terminology services instead of Excel lists"),
     ("Computable, reusable CDS", "actionable logic written once, run anywhere — CQL + PlanDefinition/$apply"),
     ("Computable eligibility", "study in-/exclusion criteria as shared expressions — the bridge to your cohort definitions")],
    "Already running: HemOnc — OMOP's regimen vocabulary — served as PlanDefinition/$apply → CarePlan with computed doses.",
    y0=3.5, step=0.8)

# ── 20b · The wider architecture ─────────────────────────────────────────────
sl = new(); header(sl, "The wider architecture — one picture")
run(box(sl, 1.0, 1.95, 11.4, 0.5).paragraphs[0],
    "Four layers — and a synthetic test harness that runs through all of them.", 17, W)


def layer(y, label, chips, hilite=None):
    pn = sl.shapes.add_shape(5, Inches(0.8), Inches(y), Inches(10.3), Inches(0.98))
    pn.fill.solid(); pn.fill.fore_color.rgb = PANEL; pn.line.color.rgb = M; pn.line.width = Pt(0.75)
    run(box(sl, 0.95, y + 0.04, 9.9, 0.32).paragraphs[0], label, 10.5, LK, b=True)
    n = len(chips); gap = 0.12
    cw = (10.0 - gap * (n - 1)) / n
    for i, c in enumerate(chips):
        col = R if (hilite is not None and i == hilite) else NV
        chip(sl, 0.95 + i * (cw + gap), y + 0.4, cw, c, col=col, fs=12, h=0.46)


layer(2.55, "RAILS — THE EHDS", ["Regulation (EU) 2025/327", "EEHRxF (Art. 15)", "MyHealth@EU", "HealthData@EU"])
layer(3.63, "SPECIFICATIONS", ["eHN guidelines", "Xt-EHR logical models", "HL7 Europe FHIR IGs", "Common Cancer Model"], hilite=3)
layer(4.71, "KNOWLEDGE", ["Terminology — SNOMED · LOINC · ATC", "Regimens — HemOnc → PlanDefinition", "CDS & eligibility — CQL"])
layer(5.79, "DATA & USE", ["Clinical software — FHIR out", "Primary use — exchange", "Secondary use — FHIR→OMOP → analytics"])
harness = sl.shapes.add_shape(5, Inches(11.25), Inches(2.55), Inches(1.35), Inches(4.22))
harness.fill.solid(); harness.fill.fore_color.rgb = NV; harness.line.color.rgb = R; harness.line.width = Pt(1.5)
tb = sl.shapes.add_textbox(Inches(10.35), Inches(4.3), Inches(3.15), Inches(0.7))
tb.rotation = 270; tb.text_frame.word_wrap = False
from pptx.enum.text import PP_ALIGN
p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
run(p, "SYNDERAI — synthetic data", 13, W, b=True)
p2 = tb.text_frame.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
run(p2, "tests every layer", 12, M)
run(box(sl, 0.8, 6.95, 11.4, 0.45).paragraphs[0],
    "Cancer is the first disease vertical on these rails — the pattern generalises to every domain.", 13, M)

# ── 21 · The point ───────────────────────────────────────────────────────────
substantive("The point",
    "The European Health Data Space does not happen to us — we have to form it.",
    [("The model", "ECCM draft profiles, in active development"),
     ("The test bed", "shareable, PII-free synthetic journeys — conformant today, 0 validation errors"),
     ("The loop", "implement → feed back → iterate — that is what we bring to Málaga"),
     ("The invitation", "take the cohort, run your FHIR→OMOP ETL against it, tell both communities what breaks")],
    "Top-down sets the rails; quality grows bottom-up — and a model becomes real the moment someone can test it.",
    y0=3.7, step=0.78)

# ═════════════════════════════ APPENDIX ══════════════════════════════════════

divider("APPENDIX", "Backup slides & tables")

# ── A1 · HL7 Europe IG landscape ─────────────────────────────────────────────
table_slide("Appendix · The HL7 Europe specification landscape",
    [("Implementation guide", "Status (Sept 2026)"),
     ("Base & Core Profiles — incl. patient-eu", "published · STU 2.0"),
     ("Extensions", "published · STU 1.3"),
     ("Laboratory Report", "published · STU 2.0"),
     ("Medication Prescription & Dispense", "published · STU 1.0 (R4 + R5)"),
     ("European Patient Summary (EPS)", "STU1 ballot · IPS-aligned · Xt-EHR-supported"),
     ("Imaging Report · Hospital Discharge Report", "ballot (v1.0.0 · v0.1.0)"),
     ("EU Health Data API", "ballot v1.0.0"),
     ("Common Cancer Model", "ballot v1.0.0")],
    (6.0, 5.5), fs=13.5, vbold=False,
    cap="hl7.eu/fhir — one family. The Common Cancer Model reuses its base profiles (patient-eu).")

# ── A2 · ECCM CI build ───────────────────────────────────────────────────────
image_slide("Appendix · The ECCM guide — live in the FHIR CI build", base + "ig_cancer_common.png", box_h=4.55,
    cap="build.fhir.org/ig/hl7-eu/cancer-common · 1.0.0-ballot — the scope names both mappings: HL7 FHIR and OMOP.")

# ── A3 · CANDLE view (drop the shared slide as output/candle_achievement.png) ─
if os.path.exists(base + "candle_achievement.png"):
    image_slide("Appendix · The same landscape, seen from CANDLE", base + "candle_achievement.png", box_h=4.55,
        cap="CANDLE 'Achievement Year 1': the NCDN network around UNCAN.eu — HL7 Europe's cancer data model is one of its working groups. Slide kindly provided by the CANDLE project.")

# ── A4 · What the model captures ─────────────────────────────────────────────
table_slide("Appendix · What the model captures — the element level",
    [("Entity", "Key elements (from the logical models)"),
     ("Patient", "birth date · sex at birth · gender · comorbidities at diagnosis"),
     ("Condition at Diagnosis", "topography · histology & behaviour · grade · visit / biopsy / imaging / lab dates"),
     ("Cancer Stage", "staging system + stage code/value · clinical vs pathological · evidence reference"),
     ("Clinical Progression", "disease status · extent · loco-regional + metastatic sites · asserted date"),
     ("Surgery · RT · Systemic", "intent · setting · start / end date · body site · ongoing flag"),
     ("Response · Last Follow-Up", "response type · vital status · evidence of disease · cause / date of death")],
    (3.6, 8.4), fs=13.5, vbold=False,
    cap="Minimal by design: the common denominator registries and studies actually share — not an mCODE-scale maximal model.")

# ── A5 · Logical → FHIR ──────────────────────────────────────────────────────
table_slide("Appendix · From logical model to FHIR — deliberately conventional",
    [("ECCM logical entity", "FHIR R4 profile"),
     ("Cancer Patient", "Patient — built on the HL7 Europe base (patient-eu)"),
     ("Condition at Diagnosis", "Condition"),
     ("Stage · Histology · Progression · Imaging", "Observation — one profile each"),
     ("Response · Follow-Up · Comorbidities", "Observation — one profile each"),
     ("Surgery", "Procedure"),
     ("Radiotherapy · Systemic · Active Surveillance", "EpisodeOfCare — period, not point event")],
    (5.6, 6.0), fs=14, vbold=False,
    cap="13 profiles + 21 extensions (intent, setting, sites, stage evidence, vital status) · mapped to OMOP in parallel · SUSHI build: 0 errors")

# ── A6 · Design choices ──────────────────────────────────────────────────────
substantive("Appendix · Four design choices worth knowing",
    "Reading the drafts as an implementer, these are the decisions that shape everything downstream.",
    [("One spine", "every entity references the condition at diagnosis — queries follow the journey, not documents"),
     ("Treatments are episodes", "EpisodeOfCare with period, intent, setting — the same shape as OMOP's EPISODE table"),
     ("Cancer semantics live in extensions", "21 extensions carry intent, setting, metastatic sites, stage evidence, vital status"),
     ("Stage is evidence-linked", "clinical stage references imaging, pathological stage references the surgery")],
    y0=3.75, step=0.8)

# ── A7 · Evidence table ──────────────────────────────────────────────────────
table_slide("Appendix · Every transition is calibrated on evidence",
    [("Effect (transition)", "Value", "Source"),
     ("PI-RADS 3 / 4 / 5 → cancer", "16 / 59 / 85 %", "Oerther 2021"),
     ("Treatment: RP / RT / AS", "57 / 16 / 16 %", "HAROW (Herden 2016)"),
     ("Incidental cancer at TURP", "14 %", "Sid Ahmed 2025"),
     ("EAU risk groups (low/int/high/adv)", "27 / 24 / 37 / 13 %", "Xie 2021 (SEER)"),
     ("Biochemical recurrence (high / low)", "40 / 20 %", "S3 Ch. 7"),
     ("Salvage durable control (5 yr)", "55 %", "early salvage RT"),
     ("De-novo M1 (age 50–60)", "6 %", "SEER (Mali 2025)")],
    (5.1, 2.9, 3.5),
    cap="25 primary sources · full-text cross-checked (5 core arrows exact, ~19/20 confirmed) · ESMO converges")

# ── A8 · Actively developing ─────────────────────────────────────────────────
two_col("Appendix · Actively developing — what comes next",
    "The generator is the shareable artifact; each track below widens what the model can be tested against.",
    "In progress",
    [("Temporal axis (prostate v4)", "delays · follow-up chain"),
     ("", "recurrence as a per-visit hazard"),
     ("Time-to-event calibration", "GENIE BPC distributions"),
     ("Breast module", "women 50–60 · concept done"),
     ("", "3,000-line evidence base, sourced")],
    "On the horizon",
    [("EU epidemiology", "country-level incidence (ECIS/ENCR)"),
     ("EU demographics", "names, addresses, identifier systems"),
     ("More entities", "melanoma, pancreatic, hematologic"),
     ("Biomarker profiles", "an ECCDM gap surfaced by breast"),
     ("Pediatric oncology", "modules planned")])

# ── A9 · ECCM coverage ───────────────────────────────────────────────────────
table_slide("Appendix · every ECCM entity is already covered",
    [("ECCM draft profiles", "Prostate pipeline produces"),
     ("Cancer Patient · Condition at Diagnosis", "Patient · prostate-cancer diagnosis"),
     ("Cancer Stage (clinical / pathological TNM)", "Gleason / ISUP · cTNM + pTNM (Partin)"),
     ("Clinical Cancer Progression", "biochemical recurrence · metastasis"),
     ("Surgery · Radiotherapy · Systemic Treatment", "RP / TURP · EBRT · ADT / ARPI / chemo"),
     ("Overall Treatment Response · Last Follow-Up", "outcome · vital status / death"),
     ("Active Surveillance · Imaging", "AS episode of care · mpMRI / PSMA-PET")],
    (5.9, 5.6), fs=15, vbold=False,
    cap="Validated against the pinned draft build with the HL7 Java validator — 0 errors across the sampled bundles.")

# ── A10 · Sources ────────────────────────────────────────────────────────────
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

out = os.path.join(HERE, "output", "ECCM_Malaga_prep.pptx")
prs.save(out)
print("saved:", len(prs.slides), "slides ->", out)

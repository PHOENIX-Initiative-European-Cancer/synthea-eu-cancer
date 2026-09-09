#!/usr/bin/env python3
"""Build the ECCM/Málaga-prep deck — synthetic data for the European Common Cancer Model.
Run: python3 scripts/build_deck_malaga.py  ->  output/ECCM_Malaga_prep.pptx
Style: same as SYNDERAI decks — plain navy content layout, red accent bar + white
descriptive title, one lead sentence, single-line statement points (bold head - tail).
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
    p = tf.paragraphs[0]; p.alignment = 2  # will be reset below; 2=right — set center
    from pptx.enum.text import PP_ALIGN
    p.alignment = PP_ALIGN.CENTER
    run(p, txt, fs, tcol or W, b=bold)
    return s


def image_slide(title, img, cap=None, box_h=4.9):
    sl = new(); header(sl, title, tsize=25)
    iw, ih = Image.open(img).size; ar = iw / ih; bw, bh = 11.4, box_h
    (w, h) = (bw, bw / ar) if bw / ar <= bh else (bh * ar, bh)
    pic = sl.shapes.add_picture(img, Inches(0.95 + (bw - w) / 2),
                                Inches(2.25 + (bh - h) / 2), Inches(w), Inches(h))
    if cap:
        run(box(sl, 1.0, 2.25 + box_h + 0.1, 11.4, 0.6).paragraphs[0], cap, 13, M)
    return sl


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

# ── 1b · Agenda ──────────────────────────────────────────────────────────────
substantive("The route",
    None,
    [("Part I — The rails", "EHDS, EEHRxF and the HL7 Europe specification stack"),
     ("Part II — The model", "the European Common Cancer Model up close — and its OMOP leg"),
     ("Part III — The test", "a calibrated synthetic prostate cohort, validated against the draft profiles")],
    y0=3.2, step=1.05)

# ── 2 · Why ──────────────────────────────────────────────────────────────────
substantive("Why synthetic cancer cohorts",
    "Real cancer-registry data is privacy-locked, slow to share, and offers no ground truth to validate against.",
    [("Shareable & PII-free", "no data-access agreements, no ethics gates"),
     ("EU-conformant", "SNOMED CT · LOINC · dual ATC"),
     ("Known ground truth", "the care process is designed, not inferred")],
    "SYNDERAI delivers this for the European Health Data Space; the Phoenix Initiative is the cancer flavour.")

divider("PART I", "The rails: EHDS, EEHRxF & the HL7 Europe specifications")

# ── EHDS · overview ──────────────────────────────────────────────────────────
substantive("The EHDS in one slide",
    "Regulation (EU) 2025/327 — in force since 26 March 2025, applying in stages from 2027.",
    [("One law, two pillars", "primary use (care, Chapter II) and secondary use (research & policy, Chapter IV)"),
     ("Primary use", "citizens access & share their EHR data · MyHealth@EU participation becomes mandatory"),
     ("Secondary use", "health data access bodies · HealthData@EU · permits instead of per-project contracts"),
     ("Why this room cares", "the pipeline from care data to research data becomes law")],
    y0=3.7, step=0.8)

# ── EHDS · timeline ──────────────────────────────────────────────────────────
sl = new(); header(sl, "The EHDS clock")
run(box(sl, 1.0, 2.3, 11.2, 0.8).paragraphs[0],
    "Staged application (Art. 105) — the dates that structure everyone's roadmap.", 19, W)
y = 4.1
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
    run(box(sl, dx - 0.25, y + 0.5, 2.4, 0.4).paragraphs[0], date, 13, W, b=True)
    tf = box(sl, dx - 0.25, y + 0.85, 2.4, 1.2)
    for i, line in enumerate(lab.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run(p, line, 11, M)
run(box(sl, 1.0, 6.8, 11.4, 0.5).paragraphs[0],
    "The Art. 15 implementing acts (EEHRxF technical specifications) are the big open item — due 26 March 2027.", 13, M)

# ── EHDS · priority categories ───────────────────────────────────────────────
substantive("Six priority categories (Art. 14)",
    "The primary-use core: six categories of electronic health data every member state must make exchangeable.",
    [("Wave 1 · 2029", "patient summaries · ePrescriptions · eDispensations"),
     ("Wave 2 · 2031", "imaging studies & reports · test / lab results & reports · discharge reports"),
     ("Extensible", "the Commission can add categories by delegated act")],
    "Cancer data is not a category of its own — it has to travel inside these generic ones.")

# ── EHDS · EEHRxF ────────────────────────────────────────────────────────────
substantive("EEHRxF — the format the law prescribes",
    "The European EHR Exchange Format is what Article 15 tells the Commission to lay down in implementing acts.",
    [("Technical specs for all six categories", "one exchange format, uniform across the EU"),
     ("Mainly syntax, little semantics", "it standardises structure and format — terminology bindings and clinical depth stay thin"),
     ("Not yet adopted", "the Art. 15 implementing acts are due by 26 March 2027 — the big open item"),
     ("Not from scratch", "builds on the 2019 EEHRxF recommendation and the eHN guidelines")],
    "Syntax alone does not analyse — filling in the semantics is the work of the specification stack on the next slides.",
    y0=3.7, step=0.8)

# ── EHDS · what FHIR is ──────────────────────────────────────────────────────
substantive("FHIR — more than a wire format",
    "For this room: FHIR is an exchange language, and it is four things at once.",
    [("A data model", "resources — Patient, Condition, Observation — constrained by profiles"),
     ("An exchange format", "JSON / XML over a REST API — the wire syntax the EEHRxF rides on"),
     ("A technical ecosystem", "servers, validators, SDKs, terminology services — open source, off the shelf"),
     ("A community", "connectathons, working groups, ballots — specifications are grown, not decreed")],
    "The last one is the point this talk relies on: the feedback loop is a community feature.",
    y0=3.7, step=0.8)

# ── EHDS · who writes the stack ──────────────────────────────────────────────
substantive("Who writes the stack — from guidelines to FHIR",
    "Three layers feed the implementing acts — and HL7 Europe writes the FHIR layer.",
    [("eHN guidelines", "the clinical content agreements per priority category"),
     ("Xt-EHR Joint Action (2023–26)", "EHDS Logical Information Models v1.0.0 — the semantic backbone"),
     ("HL7 Europe implementation guides", "FHIR profiles turning the logical models into wire format")],
    "Note the pattern — logical model first, serializations second. The Common Cancer Model works the same way.",
    y0=3.75)

# ── EHDS · HL7 Europe IG landscape ───────────────────────────────────────────
table_slide("The HL7 Europe specification landscape",
    [("Implementation guide", "Status (Sept 2026)"),
     ("Base & Core Profiles — incl. patient-eu", "published · STU 2.0"),
     ("Extensions", "published · STU 1.3"),
     ("Laboratory Report", "published · STU 2.0"),
     ("Medication Prescription & Dispense", "published · STU 1.0 (R4 + R5)"),
     ("European Patient Summary (EPS)", "STU1 ballot · IPS-aligned · Xt-EHR-supported"),
     ("Imaging Report · Hospital Discharge Report", "ballot (v1.0.0 · v0.1.0)"),
     ("EU Health Data API", "ballot v1.0.0"),
     ("Common Cancer Model", "ballot v1.0.0 — Part II of this talk")],
    (6.0, 5.5), fs=13.5, vbold=False,
    cap="hl7.eu/fhir — one family. The Common Cancer Model reuses its base profiles (patient-eu).")

# ── EHDS · MyHealth@EU ───────────────────────────────────────────────────────
substantive("MyHealth@EU — the network that already runs",
    "Cross-border exchange is not hypothetical — services have been live since 2019.",
    [("Live today", "ePrescription / eDispensation and patient summaries · over a dozen member states"),
     ("In the pipeline", "lab results piloting · imaging & discharge reports planned"),
     ("EHDS raises the bar", "participation becomes mandatory — all 27 member states by March 2029")])

# ── EHDS · secondary use ─────────────────────────────────────────────────────
substantive("Secondary use — where this room comes in",
    "Chapter IV builds a research access layer over the same data, applying from March 2029.",
    [("Health data access bodies", "one per member state · permits replace per-project negotiations"),
     ("HealthData@EU", "cross-border requests through one infrastructure · pilot ran 2022–2024"),
     ("Cancer was already a use case", "the pilot tested genomic signatures in colorectal cancer"),
     ("The analytics gap", "the law mandates access — turning exchange data into analysis-ready OMOP is our shared job")],
    y0=3.7, step=0.8)

# ── EHDS · FHIR for both pillars ─────────────────────────────────────────────
substantive("One structured format for both use cases",
    "FHIR is where the two pillars meet: data structured once, at the point of care, serves care and research alike.",
    [("Primary use is FHIR", "the EEHRxF specifications are FHIR IGs — structured at the source, not scanned PDFs"),
     ("Bindings add what the format lacks", "profiles bind SNOMED CT, LOINC, ATC, UCUM — semantics the bare syntax does not mandate"),
     ("Secondary use inherits both", "structure and coded meaning — access bodies can only serve what care recorded"),
     ("The payoff for this room", "SNOMED and LOINC in FHIR are already OMOP standard concepts — the ETL shrinks")],
    y0=3.7, step=0.8)

# ── EHDS · SYNDERAI & xShare ─────────────────────────────────────────────────
substantive("Synthetic data for the format — SYNDERAI & xShare",
    "You cannot test an exchange format without data that is legal to share. That is SYNDERAI's job.",
    [("SYNDERAI", "1,000+ synthetic EU lab reports · ~1,000 patient summaries · conformant to the HL7 Europe IGs"),
     ("Built for testing", "connectathons, vendor implementation, education — no ethics gates"),
     ("xShare Yellow Button", "citizen one-click sharing in EEHRxF — its adopters need test data too"),
     ("The cancer flavour", "our synthetic cancer cohorts are SYNDERAI's Phoenix arm — the rest of this talk")],
    y0=3.7, step=0.8)

# ── 3 · EHDS gap (bridge) ────────────────────────────────────────────────────
substantive("EHDS moves the data — but not the disease content",
    "The European Health Data Space defines the exchange infrastructure and generic priority categories.",
    [("Priority categories are generic", "summaries, ePrescription / eDispensation, imaging, labs, discharge"),
     ("No cancer-specific data points", "staging, treatment response, progression absent"),
     ("Disease content needs a disease model", "exactly the gap the Common Cancer Model fills")])

# ── EHDS · the thesis: top-down needs bottom-up ──────────────────────────────
substantive("Top-down alone will not produce quality data",
    "You can mandate a format and a deadline. You cannot mandate that the data inside is right.",
    [("Top-down", "regulation → format → dates — necessary, but it standardises containers, not content"),
     ("Bottom-up, complementary", "build the disease model, implement it, generate data, validate, feed back"),
     ("Where they meet", "the ECCM runs exactly this loop: model → profiles → test data → feedback")],
    "The rest of this talk is the bottom-up loop in action.")

divider("PART II", "The European Common Cancer Model — a closer look")

# ── ECCM · why a new model ───────────────────────────────────────────────────
table_slide("The starting point — no existing model carries Europe",
    [("Cancer data model", "FHIR?", "Why it does not generalise"),
     ("mCODE / CodeX (US)", "yes", "US Core baseline — US context, terminologies, identifiers"),
     ("IDEA4RC (EU)", "yes", "rare cancers & sarcomas — not representative"),
     ("PanCareSurPass (EU)", "yes", "paediatric cancer survivorship — a niche"),
     ("oBDS (German cancer registries)", "not yet", "strong national dataset — no FHIR layer"),
     ("OSIRIS (INCa, France)", "yes", "a specification without available data")],
    (3.9, 1.3, 6.2), fs=14, vbold=True,
    cap="The gap: minimal, cancer-agnostic, European, on FHIR — with data to test it. That pairing is the ECCM + synthetic cohorts.")

# ── 4 · ECCM status + timeline ───────────────────────────────────────────────
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

# ── ECCM · how the work happens ──────────────────────────────────────────────
substantive("Two years in — where feedback actually comes from",
    "Two years of Phoenix: one model, conceptual and logical, and a first ballot just behind us.",
    [("Open working group", "HL7 Europe / Phoenix — model first, serializations second"),
     ("The ballot delivered little", "few community comments — why? a conceptual / logical model is hard to test"),
     ("Nothing to run, nothing to find", "no profiles, no data, no validator — reading a spec surfaces few defects"),
     ("Implementation delivered a lot", "profiles + synthetic data + validator → a full findings list within weeks")],
    "The lesson for both communities: hand people something to run, not only something to read.",
    y0=3.5, step=0.78)

# ── ECCM · value streams from now on ─────────────────────────────────────────
substantive("So this is what we do from now on — our value streams",
    "Every iteration of the model ships with something you can run.",
    [("Iterate the model", "profiles + comment resolution — implementation-driven, every draft testable"),
     ("Synthetic cohorts", "CC0, SYNDERAI-tagged — the preview of what European cancer data will look like"),
     ("Medication & regimen definitions", "dual-coded ATC · the HemOnc catalog as PlanDefinition / CarePlan"),
     ("Mapping support", "terminology and ConceptMap work across SNOMED · LOINC · ATC · ICD")],
    "Take them as the reference: a pipeline that handles the preview will handle the real thing.",
    y0=3.5, step=0.78)

# ── ECCM explainer A · anatomy ───────────────────────────────────────────────
from pptx.enum.shapes import MSO_CONNECTOR
PANEL = RGBColor(0x14, 0x4a, 0x6b)
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


pat = chip(sl, 0.7, 3.35, 2.5, "Cancer Patient", col=NV, fs=14, h=0.55)
con = chip(sl, 0.7, 4.35, 2.5, "Condition at Diagnosis", col=R, fs=14, h=0.75)
ln = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(1.95), Inches(3.9), Inches(1.95), Inches(4.35))
ln.line.color.rgb = M; ln.line.width = Pt(1.5)
p1 = panel(3.9, 2.75, 4.25, 1.85, "DISEASE & EXTENT",
           ["Cancer Stage", "Histology / Behaviour", "Clinical Progression"])
p2 = panel(8.35, 2.75, 4.25, 1.85, "TREATMENT",
           ["Surgery", "Radiotherapy", "Systemic Treatment", "Active Surveillance"])
p3 = panel(3.9, 4.8, 4.25, 1.25, "OUTCOME",
           ["Treatment Response", "Last Follow-Up"])
p4 = panel(8.35, 4.8, 4.25, 1.25, "CONTEXT",
           ["Imaging", "Comorbidities"])
for tx, ty in [(3.9, 3.65), (3.9, 5.4)]:
    ln = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(3.2), Inches(4.7), Inches(tx), Inches(ty))
    ln.line.color.rgb = M; ln.line.width = Pt(1.5)
run(box(sl, 1.0, 6.55, 11.4, 0.5).paragraphs[0],
    "11 logical entities · every one carries a reference back to the condition at diagnosis (and, where relevant, to a progression).", 13, M)

# ── ECCM explainer B · what it captures ──────────────────────────────────────
table_slide("What the model captures — the element level",
    [("Entity", "Key elements (from the logical models)"),
     ("Patient", "birth date · sex at birth · gender · comorbidities at diagnosis"),
     ("Condition at Diagnosis", "topography · histology & behaviour · grade · visit / biopsy / imaging / lab dates"),
     ("Cancer Stage", "staging system + stage code/value · clinical vs pathological · evidence reference"),
     ("Clinical Progression", "disease status · extent · loco-regional + metastatic sites · asserted date"),
     ("Surgery · RT · Systemic", "intent · setting · start / end date · body site · ongoing flag"),
     ("Response · Last Follow-Up", "response type · vital status · evidence of disease · cause / date of death")],
    (3.6, 8.4), fs=13.5, vbold=False,
    cap="Minimal by design: the common denominator registries and studies actually share — not an mCODE-scale maximal model.")

# ── ECCM explainer C · logical → FHIR ────────────────────────────────────────
table_slide("From logical model to FHIR — deliberately conventional",
    [("ECCM logical entity", "FHIR R4 profile"),
     ("Cancer Patient", "Patient — built on the HL7 Europe base (patient-eu)"),
     ("Condition at Diagnosis", "Condition"),
     ("Stage · Histology · Progression · Imaging", "Observation — one profile each"),
     ("Response · Follow-Up · Comorbidities", "Observation — one profile each"),
     ("Surgery", "Procedure"),
     ("Radiotherapy · Systemic · Active Surveillance", "EpisodeOfCare — period, not point event")],
    (5.6, 6.0), fs=14, vbold=False,
    cap="13 profiles + 21 extensions (intent, setting, sites, stage evidence, vital status) · mapped to OMOP in parallel · SUSHI build: 0 errors")

# ── ECCM explainer D · design choices ────────────────────────────────────────
substantive("Four design choices worth knowing",
    "Reading the drafts as an implementer, these are the decisions that shape everything downstream.",
    [("One spine", "every entity references the condition at diagnosis — queries follow the journey, not documents"),
     ("Treatments are episodes", "EpisodeOfCare with period, intent, setting — the same shape as OMOP's EPISODE table"),
     ("Cancer semantics live in extensions", "21 extensions carry intent, setting, metastatic sites, stage evidence, vital status"),
     ("Stage is evidence-linked", "clinical stage references imaging, pathological stage references the surgery")],
    y0=3.75, step=0.8)

# ── ECCM explainer E · FHIR ↔ OMOP ───────────────────────────────────────────
substantive("Two legs of one model — where FHIR meets OMOP",
    "The communities meet in the middle: exchange happens in FHIR, analysis happens in OMOP — the ECCM is designed for both.",
    [("FHIR leg", "13 profiles for primary-use exchange — EEHRxF-style, built on the HL7 Europe base"),
     ("OMOP leg", "the same logical entities map onto the CDM — episodes, measurements, conditions"),
     ("The bridge in practice", "FHIR-native cancer journeys are exactly what a FHIR→OMOP ETL needs as input"),
     ("Known ground truth", "synthetic cohorts let you validate the ETL — the true counts are known by construction")],
    y0=3.75, step=0.8)

# ── ECCM explainer E2 · different strengths ──────────────────────────────────
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

# ── ECCM explainer F · medication coding ─────────────────────────────────────
substantive("Medication coding — where EU reality meets OMOP",
    "Drugs are the hardest crosswalk in the room: Europe classifies, OMOP standardises on products.",
    [("ATC", "what EU source data carries — substance-level classification with DDDs · our cohort: dual WHO + ATC-DE"),
     ("RxNorm (+ Extension)", "OMOP's standard drug vocabulary — product level, US-rooted · no IDMP link today"),
     ("The mapping is lossy by design", "finasteride = G04CB01 or D11AX10 by indication · combinations n:m · curated maps disagree"),
     ("IDMP is the bridge being built", "EMA SPOR live · PMS product API in beta 2026 · PhPID assignment not yet operational")],
    "Thesis: OMOP need not adopt IDMP — one global PhPID → RxNorm(+Extension) adapter would do. Who builds it?",
    y0=3.7, step=0.8)

divider("PART III", "Testing the model — a synthetic prostate cohort")

# ── 5 · Prototype ────────────────────────────────────────────────────────────
substantive("A prostate-cancer pathway model as the test bed",
    "Built on the open-source Synthea simulator for males aged 50–60, from first symptoms to metastatic disease.",
    [("Symptom-triggered", "urinary symptoms → work-up → BPH or cancer"),
     ("The full journey", "diagnosis → risk groups → treatment → recurrence → salvage → metastatic"),
     ("Standards-native", "every patient a FHIR R4 bundle, EU terminology"),
     ("Reproducible scale", "1,000-patient cohort per run · 115 cancer journeys")],
    y0=3.8, step=0.8)

# ── 6 · Evidence ─────────────────────────────────────────────────────────────
table_slide("Every transition is calibrated on evidence",
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

# ── 7 · Sankey ───────────────────────────────────────────────────────────────
image_slide("The cohort at a glance — 115 synthetic cancer journeys",
    base + "prostate_sankey_en_crop.png", box_h=4.55,
    cap="Nodes = calibrated branch points · colours = EAU risk group · a visual cross-check against the calibration targets")

# ── 8 · Pipeline ─────────────────────────────────────────────────────────────
substantive("From Synthea output to the ECCM draft profiles",
    "A post-processing pipeline reshapes every journey onto the 13 draft profiles — with a validator gate to keep it honest.",
    [("Derives what the model asks for", "clinical + pathological TNM, histology, episodes of care, progression, last follow-up"),
     ("Validator gate: 0 errors", "HL7 Java validator against the pinned draft build"),
     ("Reproducible pin", "vendored profile build · canonical parameterized against pre-ballot drift")],
    "To our knowledge the first end-to-end implementation of the draft profiles — and that is where the feedback comes from.")

# ── 9 · Feedback (substantive) ───────────────────────────────────────────────
substantive("Implementing the drafts — what came back",
    "Conformance findings only surface when someone actually implements. Six substantive comments filed; several already fixed.",
    [("TNM component binding", "example uses deprecated PhenX LOINC — recommend SNOMED UICC-8 qualifiers (AJCC is licence-encumbered)"),
     ("Pathological stage underspecified", "no example instance · stage-code semantics ('TNM' — in which system?) unclear"),
     ("One topography axis, please", "surgery example ICD-O-3 vs. condition ICD-10 — mixed axes fragment analytics"),
     ("Domain edge cases", "there is no pT1 in prostate — TURP-incidental carcinoma is clinical cT1a/b")],
    "Already fixed after re-pin: evidence reference split imaging/surgery · single-value stage systems (FIGO) · focus 1..1.",
    y0=3.75, step=0.78)

# ── 10 · To discuss in Málaga ────────────────────────────────────────────────
substantive("What we are feeding back to the model team",
    "Three things are cheap to fix now and breaking later — plus an offer.",
    [("Extension URL typos", "'systematic-treatemmt-*' leaks into instance URLs — breaking once instances exist"),
     ("Names & canonical", "'HitsologyBehaviour' · 'CinicalOrPathological' · decide the canonical before ballot"),
     ("Deprecated codes in examples", "PhenX TNM LOINC codes are all flagged deprecated"),
     ("Offer: a synthetic test corpus", "contribute journeys as IG examples / ballot test data — CC0, SYNDERAI-tagged")],
    y0=3.7, step=0.8)

# ── 11 · Active development ──────────────────────────────────────────────────
two_col("Actively developing — what comes next",
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

# ── Outlook · HemOnc regimens → CarePlan ─────────────────────────────────────
substantive("Outlook — regimens: HemOnc's OMOP groundwork, served as FHIR",
    "For treatment protocols, OHDSI is ahead: HemOnc is already an OMOP vocabulary. We are building the FHIR leg.",
    [("HemOnc in OMOP", "the regimen knowledge base behind OMOP Oncology's treatment episodes"),
     ("Projected into FHIR", "PlanDefinition · ActivityDefinition · MedicationKnowledge · CodeSystem / ConceptMap"),
     ("Executable, not just descriptive", "PlanDefinition/$apply → a patient CarePlan with computed doses (Calvert AUC · mg/m² × BSA)"),
     ("Closing the loop", "synthetic journeys following named regimens — the same regimen identity in EPISODE and CarePlan")],
    "Draft IG in development with HemOnc.org, the OHDSI oncology community, HL7-EU Phoenix and MII Onkologie · CC BY 4.0.",
    y0=3.7, step=0.8)

# ── 12 · Closing ─────────────────────────────────────────────────────────────
substantive("The point",
    "Top-down sets the rails; quality grows bottom-up — a model becomes real the moment someone can test it.",
    [("The model", "ECCM draft profiles, in active development"),
     ("The test bed", "shareable, PII-free synthetic journeys — conformant today, 0 validation errors"),
     ("The loop", "implement → feed back → iterate — that is what we bring to Málaga"),
     ("The invitation", "take the cohort, run your FHIR→OMOP ETL against it, tell both communities what breaks")])

# ── 13 · Appendix · CCDM mapping ─────────────────────────────────────────────
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

# ── 14 · Appendix · sources ──────────────────────────────────────────────────
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

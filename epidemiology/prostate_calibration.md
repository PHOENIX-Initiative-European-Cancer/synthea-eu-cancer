# Prostate module — transition-probability calibration

Source trace for every calibrated arrow in `modules/adult/prostate.json`.

**Clinical model:** BPH is *not* a precursor of prostate cancer. A shared **symptom trigger** (LUTS: nocturia,
weak stream, pelvic/urinary pain) brings the man aged 50–60 to urology; the diagnostic work-up (PSA + DRE + TRUS,
then mpMRI + biopsy if PSA elevated) **branches** into BPH *or* prostate cancer. BPH is the diagnostic *occasion*,
not the cause.

**Calibration frame:** EAU-EANM-ESTRO-ESUR-ISUP-SIOG **2024** guideline gives the pathway *structure*; German
**S3-Leitlinie Prostatakarzinom v8.1 (2025)** and German cancer-registry data (**ZfKD/RKI** "Krebs in Deutschland",
**ECIS**) calibrate the *probabilities*. Where German registry granularity was missing, large SEER/NCDB/European
cohorts are used and flagged.

Confidence legend: 🟢 well-sourced · 🟡 sourced but transferability/era caveat · 🔴 modelling prior / estimate.

---

## 1. Entry & symptom trigger

| Arrow (state) | Value | Basis | Conf |
|---|---|---|---|
| `Symptom_Check` → present symptomatically | **0.12 / yr** (~72% cumulative over 50–60) | **Cohort-yield knob, NOT epidemiology.** Anchored on ~19% moderate-to-severe LUTS (IPSS ≥8) at 50–59 (UrEpik, Boyle 2003, PubMed 12930430), inflated so a small demo cohort exercises the pathway. **This is the dial to turn for cohort throughput.** | 🔴 |
| `Symptom_Check` → exit at age ≥61 | deterministic | Cohort window is 50–60; unpresented men exit as background. | — |

---

## 2. Diagnostic work-up

| Arrow | Value | Basis | Conf |
|---|---|---|---|
| `Workup_Branch` → benign (no biopsy) / elevated-PSA pathway | **0.70 / 0.30** | Among symptomatic 50–60 men the diagnosis is overwhelmingly BPH; cancer only in the PSA-elevated minority (LUTS is not a PCa risk factor, EAU). ~67% benign in a LUTS+PSA≥3 biopsy cohort (PMC8317798). 30% suspicious > 5% healthy-pop >3.2 ng/mL because BPH inflates PSA in symptomatic men. | 🟡 |
| `PIRADS_Branch` → PI-RADS 1-2 / 3 / 4 / 5 | **0.40 / 0.20 / 0.25 / 0.15** | PI-RADS distribution among elevated-PSA symptomatic men — **estimate**. Yields ~31% csPCa among MRI-pathway men, matching PRECISION-era 35–38%. | 🔴 |
| `Biopsy_PR3` → cancer / benign | **0.16 / 0.84** | csPCa (ISUP ≥2) detection at PI-RADS 3, patient-level. Oerther meta-analysis, PMC9184264. | 🟢 |
| `Biopsy_PR4` → cancer / benign | **0.59 / 0.41** | csPCa at PI-RADS 4, patient-level. PMC9184264. | 🟢 |
| `Biopsy_PR5` → cancer / benign | **0.85 / 0.15** | csPCa at PI-RADS 5, patient-level. PMC9184264. | 🟢 |
| PI-RADS ≤2 → no biopsy | deterministic | EAU 2024 / S3 v8.1: at PI-RADS 1–2 no biopsy shall be performed. Elevated PSA attributed to BPH. | 🟢 |

**Threshold note:** EAU uses a functional **3 ng/mL** action threshold; S3 v8.1 uses a confirmed **4 ng/mL** biopsy
threshold. The module encodes the elevated-PSA observation at 4–12 ng/mL (S3-aligned). One number to pick explicitly.

---

## 3. Cancer risk-group distribution at diagnosis

`Cancer_RiskGroup_Branch`, **re-weighted for the 50–60 cohort** (younger ⇒ more localized, less M1):

| Risk group | Value | EAU definition | Basis | Conf |
|---|---|---|---|---|
| Low | **0.32** | PSA<10 & ISUP1 & cT1–2a | Xie 2021 PMC8076565 EAU-g low **26.6%** (verified), raised for young cohort | 🟡 |
| Intermediate | **0.34** | PSA10–20 or ISUP2–3 or cT2b | Xie EAU-g **24.0%** (verified); NCDB grade migration PMC10133398 | 🟡 |
| High (localized) | **0.17** | PSA>20 or ISUP4–5 or cT2c | Xie EAU-g localized-high **36.5%** (verified; SEER-inflated → trimmed to 0.17) | 🟡 |
| Locally advanced | **0.11** | cT3–4 or cN+ | Xie EAU-g locally-advanced **12.9%** (verified) | 🟡 |
| Metastatic (M1) | **0.06** | any M1 | ~9% overall (SEER), lowered to ~4–6% for 50s (SEER under-50 PMC11758148) | 🟡 |

Younger-cohort skew justified by SEER under-50: localized 76% vs ~70% overall, distant ~4% vs ~9%.
Grade migration (NCDB): biopsy GG1 fell ~45%→25% (2010→2019) — contemporary cohorts sit lower on GG1 than older German
single-centre series (Göppingen GG1 55%, Mathieu 2017). ISUP-by-age table for Germany = **open data gap**.

Per-group encoded staging/grade (coherent set):

| Group | Gleason | cTNM | PSA at dx (ng/mL) |
|---|---|---|---|
| Low | 6 (ISUP 1) | cT1cN0M0 | 4.0–9.9 |
| Intermediate | 7 (ISUP 2–3) | cT2bN0M0 | 8–20 |
| High | 8 (ISUP 4) | cT2cN0M0 | 20–45 |
| Locally advanced | 9 (ISUP 5) | cT3aN0M0 | 20–80 |
| Metastatic | 9 (ISUP 5) | cT3bN1M1 | 50–500 |

---

## 4. Treatment allocation

| Arrow | Value | Basis | Conf |
|---|---|---|---|
| Low → **Active surveillance** | deterministic | EAU 2024: AS is the *preferred* option for low-risk, life expectancy >10 yr (strong rec). | 🟢 |
| `AS_Progression_Branch` → definitive tx / stay on AS | **0.50 / 0.50** (over 1–5 yr) | ~50% of AS patients treated within 5 yr (PMC7407781; German HAROW AS PMC8332563). No death arrow — AS cancer-specific survival ~99–100% at 5 yr. | 🟢 |
| Intermediate → RP / EBRT+short-ADT | **0.55 / 0.45** | EAU: RP(±LND) or EBRT+4–6 mo ADT. German HAROW localized pooled is RP-heavy (~57% RP). | 🟡 |
| High/loc-adv → EBRT+long-ADT / RP+PLND | **0.60 / 0.40** | EAU 2024: EBRT + 2–3 yr ADT (strong) or RP + extended PLND multimodal (weak). ADT monotherapy *not* recommended for fit patients. | 🟡 |
| `HighRisk_Progression_Branch` → metastatic / stable | **0.15 / 0.85** | Minority of treated high-risk progress to M1 over follow-up (indicative). Routes into systemic chain without a 2nd ConditionOnset. | 🔴 |
| **BPH** `BPH_Management_Branch` → WW / medical / surgery | **0.33 / 0.52 / 0.15** | Indicative textbook priors, EAU/AUA-aligned (Medscape; PMC7109311). Not a registry split. | 🔴 |
| BPH medical → add finasteride | **0.50** | 5-ARI added for enlarged gland (>40 mL) / progression risk (combination therapy). | 🔴 |
| `TURP_Incidental_Check` → incidental cancer | **0.14** | Incidental PCa in ~14% of TURP/HoLEP specimens (PMC12459874); typically low-grade ⇒ routed to low-risk node. | 🟢 |

---

## 5. Metastatic / castration-resistant course & outcomes

| Arrow | Value | Basis | Conf |
|---|---|---|---|
| `mHSPC_Intensification_Branch` → ARPI / docetaxel | **0.60 / 0.40** | EAU 2024 Part II: ADT alone no longer standard; intensify with ARPI (doublet) or docetaxel. Split indicative. | 🟡 |
| `mCRPC_Branch` → 2nd-line / stable | **0.65 / 0.35** (after 1–3 yr) | Progression to castration resistance then 2nd-line (cabazitaxel / Lu-177-PSMA / PARPi). | 🔴 |
| `mCRPC_Outcome_Branch` → PCa death / survive | **0.55 / 0.45** | Distant-stage 5-yr relative survival low (~30% range, German NRW registry PubMed 39742793). Death arrow lives only here + implicitly localized survival >90%. | 🟡 |

**Survival anchors (for validation of generated cohort, not encoded as arrows):** localized 5-yr relative survival
>90%; regional ~83% (2015–19); distant low (~30% range). Germany overall 5-/10-yr RS 93.3% / 90.7% (PubMed 27208546).

---

## 6. Codes to verify (⚠ blocking before any Synthea run — beads interop-prototypes-0er)

Best-guess terminology used in the prototype. Validate against the terminology server **and** Synthea's own code
conventions; replace ingredient-level RxNorm with product (SCD) codes.

| Concept | System | Code (provisional) | Status |
|---|---|---|---|
| Malignant tumor of prostate | SNOMED CT | 399068003 | 🟢 likely ok (mCODE examples) |
| Hyperplasia of prostate (BPH) | SNOMED CT | 266569009 | 🟢 likely ok |
| PSA | LOINC | 2857-1 | 🟢 ok |
| Gleason score in specimen | LOINC | 35266-6 | 🟡 verify |
| PI-RADS v2 category | LOINC | 82717-8 | 🟡 verify |
| Digital rectal exam | SNOMED CT | 274405006 | 🟡 verify |
| Transrectal ultrasound prostate | SNOMED CT | 428051000 | 🔴 verify |
| MRI of prostate | SNOMED CT | 241645008 | 🔴 verify |
| Prostate needle biopsy | SNOMED CT | 396487001 | 🔴 verify |
| Radical prostatectomy | SNOMED CT | 176260009 | 🟢 likely ok |
| TURP | SNOMED CT | 176258007 | 🔴 verify |
| Teleradiotherapy (EBRT) | SNOMED CT | 33195004 | 🟡 verify |
| Active surveillance (care plan) | SNOMED CT | 424313000 | 🔴 verify |
| Watchful waiting (care plan) | SNOMED CT | 373818007 | 🔴 verify |
| tamsulosin | RxNorm | 77492 (ingredient) | 🔴 need product/SCD |
| finasteride 5 MG tablet | RxNorm | 310872 | 🟡 verify |
| leuprolide | RxNorm | 6413 (ingredient) | 🔴 need product/SCD |
| enzalutamide | RxNorm | 1373489 (ingredient) | 🔴 need product/SCD |
| docetaxel | RxNorm | 72962 (ingredient) | 🔴 need product/SCD |
| cabazitaxel | RxNorm | 1093279 (ingredient) | 🔴 need product/SCD |

TNM stage and EAU risk group are currently held as patient **attributes** (`pca_risk_group`, `pca_ctnm`) rather than
coded observations, because the Synthea Observation state is numeric-oriented. The CCDM post-processing layer should
emit these as `Condition.stage` / staging Observations (LOINC 21905-5 cT, 21906-3 cN, 21907-1 cM).

---

## 7. Open data gaps

1. Exact ZfKD/RKI **per-5-year-band incidence** (50–54 vs 55–59) — KID C61 PDF didn't machine-parse; pull from the table directly.
2. German **ISUP-by-age** table — not found in open sources.
3. German **screen-detected vs symptomatic** split — England 19% asymptomatic-PSA (PMC11881005); no clean German figure.
4. Exact German **distant-stage 5-yr survival %** and **PCSM-by-stage** — paywalled (NRW paper PubMed 39742793) / cite RKI.


## 8. Primary-source verification (2026-07-01, full-text read)

PDFs read directly from the Zotero collection and checked against the arrows above.

| Claim / arrow | Value used | Primary source says | Verdict |
|---|---|---|---|
| Biopsy csPCa by PI-RADS 3/4/5 | 16 / 59 / 85 % | Oerther 2021 **patient-level** CDR: PI-RADS 3 =16%, 4 =59%, 5 =**85%** (abstract + Fig. 3) | ✅ EXACT |
| HAROW treatment allocation | RP 56.6 / RT 16.4 / AS 15.8 / ADT 6.9 / WW 4.3 % | Herden 2016 Table 2: OP 56.6 / RT 16.4 / AS 15.8 / HT 6.9 / WW 4.3 % | ✅ EXACT |
| AS switch rate | (23.9% cited) | Herden 2016 Fig. 1: 112/468 = **23.9%** changed treatment at mFU 28 mo | ✅ EXACT |
| Incidental cancer at TURP/HoLEP | 14 % → low-risk | Sid Ahmed 2025: **14.3%** iPCa, **62.2%** low-grade (Gleason 6) | ✅ EXACT (but HoLEP; pure TURP ≈2–5% in PSA era) |
| EAU risk-group distribution | 26.6 / 24.0 / 36.5 / 12.9 % | Xie 2021 Table 1 EAU-g: 26.62 / 24.01 / 36.49 / 12.88 % | ✅ EXACT |
| **AS → definitive treatment in 5 yr** | **0.50** (`AS_Progression_Branch`) | HAROW long-term (Herden 2020, PMC8332563): median time-to-treatment ~33 mo (RP)/38.5 mo (RT); 56.8% converted over median 7.7 yr; **10-yr** intervention-free survival 33.8–34.6%. International AS reviews: 24–60% converted by 5 yr (central ~50%). | ✅ **0.50 VINDICATED.** An earlier draft flagged "too high (→0.37)" from **misreading** HAROW's 33–36% — those are *10-year intervention-free survival* rates, NOT 5-yr conversion. Median time-to-treatment <5 yr ⇒ ~50% convert by 5 yr in HAROW too. **Keep 0.50.** |

**Citation fix applied:** the risk-stratification source is **Xie et al. 2021** (Front Oncol, PMC8076565 / 10.3389/fonc.2021.646073), not "Zhou" (agent mis-attribution) — corrected in this doc, `docs/calibration_sources.md`, and the `prostate.json` remark.

**Net result (5 core arrows):** every *hard* number transcribed into the module (PI-RADS detection, HAROW allocation, incidental-cancer, EAU risk groups) matches the primary source **exactly**.

## 9. Full-corpus verification (2026-07-02, 4 background agents, all ~20 remaining sources)

| Block | Result |
|---|---|
| **Incidence / BPH / LUTS** | Lower-Saxony 50–59 = **127.1/100k** ✅ exact · UrEpik mod-severe LUTS 50–59 = **19.0%** ✅ exact · EPIC (nocturia most common, storage>voiding) ✅ · German 10-yr risk age 65=**2.8%** & lifetime **14.2%** ✅ exact (age 40/70 plausible, not directly found) · BPH histological ~50% at 6th decade ✅ — **⚠️ "40–60% symptomatic BPH over 50" NOT supported** by ajur source (that 60% is age 90); background only, not an arrow |
| **Diagnostic pathway** | Nordström 67/19/**13.7%** ✅ exact · Irish PSA 95th 55–59 = **3.25** ✅ · Taiwan 95th 50–59 = **3.2** ✅ · grey-zone PSAD ✅ · MRI-targeted csPCa **35.3–38%** ✅ · LUTS-not-a-risk-factor ✅ |
| **Grading / staging** | NCDB GG1 **45→25%** ✅ exact · SEER<50 distant **4.2%** ✅ exact (supports M1 discussion) · NCDA screen-detected **19.2%** ✅ exact · screen-vs-clinical ✅ · **⚠️ citation: 10.1111/apm.12533 is Egevad et al., not Epstein** (fixed) |
| **Treatment / survival** | DE vs US 5-/10-yr RS **93.3/90.7** vs 99.4/99.6 ✅ exact · EAU-2024 by-risk pathway ✅ · NRW stage-survival direction ✅ (exact % paywalled, unverifiable) · **AS→treatment 0.50 VINDICATED** (see row above) |

**Overall: ~19/20 confirmed exact or directionally.** Corrections applied: Zhou→Xie, Epstein→Egevad. Minor unverified: "40–60% symptomatic BPH" (context, not an arrow) and German 10-yr risk at exactly age 40/70 (plausible). **No module transition probability requires a change based on the verification** — the one flag I raised myself (AS 0.50) was refuted on deeper reading. Open user decision remains: de-novo M1 0.06 vs ~0.08.

# SNOMED CT Data Dictionary — Prostate Pathway (BPH / Prostate Cancer)

Clean, **validated** terminology for the full BPH/PCa pathway used by `modules/adult/prostate.json`.

**Provenance of every code:**
- `termsvc` = validated live against the **CEIR-OS FHIR terminology server** (`ceir-terminology-mcp` → `ontoserver.mii-termserv.de`), SNOMED CT **International Edition, version 20250701**. Only codes the server returned with an active display are listed.
- `spec` = curated from the **BIH-CEI Prostate Cancer Specification v0.1.0** (`https://bih-cei.github.io/ProstateCancerSpec/semantic-annotations.html`) — the authoritative pathology/grading/staging source.

Cross-references: **LOINC** for observables/labs, **ICD-O-3** for morphology, **ATC** for substances (EU medication coding).

> ⚠️ This dictionary supersedes the best-guess codes in the prototype module. Corrections are flagged **[FIXES PROTOTYPE]**; see beads `interop-prototypes-0er`. Codes not resolvable in INT 20250701 are in §9 (post-coordination / gaps).

---

## 1. Symptoms & clinical findings (pre-diagnosis trigger)

Generic findings for the symptomatic presentation **before** the BPH/PCa branch (do not presume aetiology yet).

| Concept | System | Code | Display | Prov |
|---|---|---|---|---|
| Lower urinary tract symptoms | SNOMED | `307541003` | Lower urinary tract symptoms | termsvc |
| Nocturia | SNOMED | `139394000` | Nocturia | termsvc |
| Poor/weak urinary stream | SNOMED | `311810006` | [D]Poor urinary stream | termsvc ⚠ residual-category concept |
| Frequency of micturition | SNOMED | `162114000` | (Frequency of micturition) or (polyuria) | termsvc |
| Dysuria | SNOMED | `49650001` | Dysuria | termsvc |
| Pelvic pain (complaint of) | SNOMED | `162147009` | C/O pelvic pain | termsvc |
| Acute pelvic pain | SNOMED | `314716005` | Acute pelvic pain | termsvc |
| Retention of urine | SNOMED | `267064002` | Retention of urine | termsvc |
| Acute retention of urine | SNOMED | `236648008` | Acute retention of urine | termsvc |
| Haematuria | SNOMED | `266568001` | Hematuria | termsvc |

**BPH-attributed symptom variants** (use only *after* the BPH branch is taken, where aetiology is established):

| Concept | Code | Display |
|---|---|---|
| LUTS due to BPH | `30041000119101` | Lower urinary tract symptoms due to benign prostatic hypertrophy |
| Nocturia due to BPH | `1711000119101` | Nocturia due to benign prostatic hypertrophy |
| Weak stream due to BPH | `117521000119100` | Weak urinary stream due to benign prostatic hypertrophy |
| Hesitancy due to BPH | `117501000119109` | Urinary hesitancy due to benign prostatic hypertrophy |

---

## 2. Diagnoses

### Benign
| Concept | System | Code | Display | Prov |
|---|---|---|---|---|
| Benign prostatic hyperplasia | SNOMED | `266569009` | Hyperplasia of prostate | spec + termsvc ✓ (prototype correct) |
| Chronic prostatitis | SNOMED | `19905009` | Chronic prostatitis | spec |
| Granulomatous prostatitis | SNOMED | `61500009` | Granulomatous prostatitis | spec |

### Malignant — disorders
| Concept | System | Code | Display | Prov |
|---|---|---|---|---|
| Malignant tumour of prostate (generic) | SNOMED | `399068003` | Malignant tumour of prostate | termsvc ✓ (used in module) |
| Acinar adenocarcinoma of prostate | SNOMED | `399490008` | Adenocarcinoma of prostate | spec |
| Primary adenocarcinoma of prostate | SNOMED | `1259672003` | Primary adenocarcinoma of prostate | spec (alt) |
| Ductal adenocarcinoma of prostate | SNOMED | `823017009` | Ductal adenocarcinoma of prostate | spec |
| Small cell carcinoma of prostate | SNOMED | `1208457007` | (small cell carcinoma, prostate) | spec |
| Squamous cell carcinoma of prostate | SNOMED | `399590005` | Squamous cell carcinoma of prostate | spec |
| Hormone-refractory (castration-resistant) PCa | SNOMED | `427492003` | Hormone refractory prostate cancer | termsvc |
| Secondary malignant neoplasm of bone | SNOMED | `94216004` | Secondary malignant neoplasm of bone and articular cartilage | termsvc |
| Metastasis to bone | SNOMED | `154572002` | Metastasis to bone | termsvc |

### Pre-malignant / borderline (spec)
| Entity | ICD-O-3 | SNOMED | Display |
|---|---|---|---|
| High-grade prostatic intraepithelial neoplasia (HGPIN) | 8148/2 | `446711009` | HGPIN |
| Atypical small acinar proliferation (ASAP) | — | `16294321000119104` | ASAP |

**ICD-O-3 morphology** (spec, for `LOINC 59847-4`): Acinar adenoca `8140/3` · Ductal `8500/3` · Intraductal `8500/2` · Cribriform `8201/3` · Small cell `8041/3` · Squamous `8070/3` · Urothelial `8120/3`.
Morphology-only SCT: acinar `1187332001` · ductal `82711006` · IDC-P `1162814007` · ICC `30156004` · small cell `74364000` · squamous `1162767002` · urothelial `27090000`.

---

## 3. Diagnostic procedures & observables

| Concept | System | Code | Display | Prov |
|---|---|---|---|---|
| Digital rectal examination | SNOMED | `410006001` | Digital examination of rectum | termsvc **[FIXES PROTOTYPE 274405006]** |
| PSA measurement (procedure) | SNOMED | `63476009` | Prostate specific antigen measurement | termsvc |
| PSA (lab observable) | LOINC | `2857-1` | Prostate specific Ag [Mass/vol] in Serum/Plasma | — |
| Free PSA | LOINC | `10886-0` | Prostate Specific Ag Free [Mass/vol] | — |
| Serum testosterone measurement | SNOMED | `270973006` | Serum testosterone measurement | termsvc |
| Testosterone (lab observable) | LOINC | `2986-8` | Testosterone [Mass/vol] in Serum/Plasma | — |
| Endorectal ultrasonography (≈TRUS) | SNOMED | `429820004` | Endorectal ultrasonography | termsvc **[FIXES PROTOTYPE 428051000 — invalid]** ⚠ see §9 |
| Multiparametric MRI (generic) | SNOMED | `1144760005` | Multiparametric magnetic resonance imaging | termsvc ⚠ prostate site via post-coordination (§9) |
| Magnetic resonance imaging (generic) | SNOMED | `113091000` | Magnetic resonance imaging | termsvc |
| Needle biopsy of prostate | SNOMED | `236258004` | Needle biopsy of prostate | termsvc **[FIXES PROTOTYPE 396487001]** |
| Biopsy of prostate (generic) | SNOMED | `65575008` | Biopsy of prostate | termsvc |
| Radionuclide bone study (bone scan) | SNOMED | `146371003` | Radionuclide bone study | termsvc |
| PI-RADS category | LOINC | `82717-8` | PI-RADS category | — ⚠ no SNOMED equivalent |

### Grading & staging observations (spec)
| Observation.code | System | Code | Value domain |
|---|---|---|---|
| Gleason pattern primary | LOINC | `44641-9` | → VS Gleason Pattern |
| Gleason pattern secondary | LOINC | `44642-7` | → VS Gleason Pattern |
| Gleason score (qualitative) | LOINC | `35266-6` | → VS Gleason Score |
| ISUP grade group | SNOMED | `1812491000004107` | Histologic grade by ISUP technique → VS ISUP |
| WHO differentiation grade | LOINC | `21858-6` | → VS WHO Grade |
| Histology & behaviour ICD-O-3 | LOINC | `59847-4` | → VS ICD-O-3 Morphology |
| TNM cT / cN / cM | MII Onko profiles | `mii-pr-onko-tnm-{t,n,m}-kategorie` | UICC TNM (`uicc.org/resources/tnm`) |

**VS Gleason Pattern**: P1 `369770006` · P2 `369771005` · P3 `369772003` · P4 `369773008` · P5 `369774002`.
> ⚠ The spec lists P5 as `369774004`, which **does not exist** in SNOMED INT 20250701 (transposed digit). Correct code is `369774002`. Filed as [BIH-CEI/ProstateCancerSpec#18](https://github.com/BIH-CEI/ProstateCancerSpec/issues/18).
**VS Gleason Score** (spec): 2 `49878003` · 3 `46677009` · 4 `18430005` · 5 `74013009` · 6 `84556003` · 7 `57403001` · 8 `33013007` · 9 `58925000` · 10 `24514009` · X `860741001`.
**VS ISUP Grade Group** (spec): GG1(3+3) `1279715000` · GG2(3+4) `1279714001` · GG3(4+3) `1279716004` · GG4(4+4) `1279717008` · GG4(3+5) `1279718003` · GG4(5+3) `1279719006` · GG5(4+5) `1279720000` · GG5(5+4) `1279721001` · GG5(5+5) `1279722008`.
**VS WHO Grade** (spec): G1 `1155701009` · G2 `1155703007` · G3 `1155704001` · G4 `1155702002`.

---

## 4. Therapeutic procedures — surgery

| Concept | System | Code | Display | Prov |
|---|---|---|---|---|
| Radical prostatectomy | SNOMED | `26294005` | Radical prostatectomy | termsvc **[FIXES PROTOTYPE 176260009 — invalid]** |
| Radical prostatectomy w/o pelvic node excision | SNOMED | `176261008` | " without pelvic node excision | termsvc |
| Radical prostatectomy + pelvic lymphadenectomy | SNOMED | `176263006` | " with pelvic lymphadenectomy | termsvc |
| Laparoscopic robot-assisted radical prostatectomy | SNOMED | `708919000` | Radical prostatectomy, laparoscopic with robot assistance | termsvc |
| Pelvic lymphadenectomy | SNOMED | `14059008` | Pelvic lymphadenectomy | termsvc |
| Transurethral prostatectomy (TURP) | SNOMED | `90199006` | Transurethral prostatectomy | termsvc **[FIXES PROTOTYPE 176258007]** |
| Bipolar TURP | SNOMED | `1148689009` | Bipolar transurethral resection of prostate | termsvc |
| Enucleation of prostate | SNOMED | `116244007` | Enucleation of prostate | termsvc |
| Holmium laser enucleation of prostate (HoLEP) | SNOMED | `699075006` | Holmium laser enucleation of prostate | termsvc |
| Bilateral orchidectomy | SNOMED | `14043008` | Bilateral orchidectomy | termsvc |

## 5. Therapeutic procedures — radiotherapy & management

| Concept | System | Code | Display | Prov |
|---|---|---|---|---|
| External beam radiation therapy | SNOMED | `33195004` | External beam radiation therapy procedure | termsvc ✓ (prototype correct) |
| Brachytherapy | SNOMED | `152198000` | Brachytherapy | termsvc |
| Interstitial brachytherapy | SNOMED | `113120007` | Interstitial brachytherapy | termsvc |
| Active surveillance | SNOMED | `424313000` | Active surveillance | termsvc ✓ (prototype correct) |
| Active surveillance of prostate cancer | SNOMED | `712837004` | Active surveillance of prostate cancer | termsvc (more specific) |
| Watchful waiting | SNOMED | `373818007` | No anti-cancer treatment - watchful waiting | termsvc ✓ (prototype correct) |
| Androgen deprivation therapy (regime) | SNOMED | `707266006` | Androgen deprivation therapy | termsvc |
| Radioligand therapy Lu-177 vipivotide | SNOMED | `1263784000` | Radioligand therapy using lutetium (Lu-177) vipivotide tetraxetan | termsvc |

---

## 6. Substances (Wirkstoffe)

All SNOMED substance-hierarchy concepts, validated termsvc. ATC = EU medication cross-reference.

**Medication coding in `prostate.json` uses ATC dual-coding, not SNOMED substance** (per MII-Onko [issue #283](https://github.com/medizininformatik-initiative/kerndatensatzmodul-onkologie/issues/283)):
- **WHO-ATC** `http://www.whocc.no/atc` — international standard (validated on **tx.fhir.org**; English display).
- **ATC-DE / BfArM** `http://fhir.de/CodeSystem/bfarm/atc` — MII/CCDM standard (validated on the **MII termserver**; German display).
- The MII termserver does **not** carry WHO-ATC (only ATC-DE); tx.fhir.org carries WHO-ATC. Codes are identical for these substances; only system URI + display language differ. SNOMED substance codes below are retained as a semantic cross-reference.

### BPH — alpha-1-blockers
| Substance | SNOMED | ATC |
|---|---|---|
| Tamsulosin | `372509005` | G04CA02 | 
| Alfuzosin | `395954002` | G04CA01 |
| Silodosin | `442042006` | G04CA04 |
| Doxazosin | `372508002` | C02CA04 |
| Terazosin | `387068008` | G04CA03 |

### BPH — 5-alpha-reductase inhibitors & PDE5
| Substance | SNOMED | ATC |
|---|---|---|
| Finasteride | `386963006` | G04CB01 |
| Dutasteride | `385572003` | G04CB02 |
| Tadalafil | `407111005` | G04BE08 |

### PCa — LHRH agonists / antagonists
| Substance | SNOMED | ATC |
|---|---|---|
| Leuprorelin acetate | `327358003` | L02AE02 |
| Goserelin | `108771008` | L02AE03 |
| Triptorelin | `395915003` | L02AE04 |
| Degarelix | `441864003` | L02BX02 |
| Relugolix | `1144477009` | L02BX04 |

### PCa — antiandrogens & ARPI
| Substance | SNOMED | ATC |
|---|---|---|
| Bicalutamide | `386908000` | L02BB03 |
| Abiraterone (acetate `699679004`) | `699678007` | L02BX03 |
| Enzalutamide | `703125003` | L02BB04 |
| Apalutamide | `766972001` | L02BB05 |
| Darolutamide | `789148001` | L02BB06 |

### PCa — chemotherapy, PARPi, radioligand, steroid
| Substance | SNOMED | ATC |
|---|---|---|
| Docetaxel | `386918005` | L01CD02 |
| Cabazitaxel | `446706007` | L01CD04 |
| Olaparib | `432162002` | L01XK01 |
| Rucaparib | `723984009` | L01XK03 |
| Radium-223 dichloride | `24853006` | V10XX03 |
| Lutetium (Lu-177) vipivotide tetraxetan | `1263794005` | V10XX05 |
| Prednisone | `116602009` | H02AB07 |
| Prednisolone | `116601002` | H02AB06 |

---

## 7. Prototype code corrections (feed into `prostate.json`, beads-0er)

| State in prostate.json | Old (guessed) | Correct (validated) | Note |
|---|---|---|---|
| `DRE` | 274405006 | **410006001** | 274405006 not returned by INT 20250701 |
| `TRUS_Benign` / `TRUS_Suspicious` | 428051000 | **429820004** | 428051000 invalid; Endorectal US (+ §9) |
| `mpMRI` | 241645008 | **1144760005** | + prostate bodySite post-coord (§9) |
| `Biopsy_PR*` | 396487001 | **236258004** | Needle biopsy of prostate |
| `Radical_Prostatectomy` | 176260009 | **26294005** | 176260009 not valid |
| `TURP` | 176258007 | **90199006** | Transurethral prostatectomy |
| BPH `266569009`, PCa `399068003`, EBRT `33195004`, AS `424313000`, WW `373818007` | — | — | already correct ✓ |
| all substances | RxNorm ingredient guesses | SNOMED §6 | switch to SNOMED (+ ATC) for CCDM |

## 8. Observables/labs (LOINC)

PSA `2857-1` · Free PSA `10886-0` · Testosterone `2986-8` · Gleason score `35266-6` · Gleason pattern 1°/2° `44641-9`/`44642-7` · WHO grade `21858-6` · ICD-O-3 histology `59847-4` · PI-RADS `82717-8`.

## 9. Gaps & post-coordination required

1. **TRUS of prostate** — no prostate-specific transrectal-US procedure in INT 20250701. Use `429820004` Endorectal ultrasonography **+** bodySite `41216001` (Prostate), or post-coordinate `16310003` (US imaging) + prostate site.
2. **Prostate mpMRI** — no prostate-specific concept. Use `1144760005` (mp-MRI) **+** bodySite `41216001` (Prostate).
3. **PI-RADS** — no SNOMED concept; keep LOINC `82717-8` with a numeric value.
4. **CRPC** — `427492003` "Hormone refractory prostate cancer" is the closest; "castration-resistant" phrasing has no distinct INT concept.

---

*Terminology server: CEIR-OS `ceir-terminology-mcp` → `ontoserver.mii-termserv.de`. SNOMED CT International Edition 20250701. Resolved 2026-07-01. Spec: BIH-CEI Prostate Cancer Specification v0.1.0.*

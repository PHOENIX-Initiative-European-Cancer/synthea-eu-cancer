# Calibration sources — prostate module

The high-value literature behind the transition probabilities in `modules/adult/prostate.json`
(traced arrow-by-arrow in `epidemiology/prostate_calibration.md`). Imported into Zotero collection
**"Prostate Synthea Calibration"** (personal library, key `JUMTDTVK`).

DOIs resolved & verified via NCBI ID Converter / eutils (2026-07-01).

## Guidelines & consensus
| DOI | Source | Calibrates |
|---|---|---|
| 10.1016/j.eururo.2024.03.027 | EAU-EANM-ESTRO-ESUR-ISUP-SIOG Guidelines on Prostate Cancer 2024, Part I | Diagnostic pathway structure, risk groups, treatment |
| 10.1111/apm.12533 | Egevad et al. — ISUP grading / grade groups (this DOI is Egevad et al.; the Epstein grade-group consensus is a separate paper, PMID 26492179) | ISUP grade-group definitions |

## Incidence, BPH & LUTS epidemiology
| DOI | Source | Calibrates |
|---|---|---|
| 10.3389/fonc.2021.681006 | Lower-Saxony vs Groningen incidence | Age-specific PCa incidence 50–59 |
| 10.1016/j.ajur.2017.06.004 | Epidemiology of clinical BPH | BPH prevalence by age |
| 10.1046/j.1464-410x.2003.04369.x | UrEpik (Boyle) — LUTS prevalence | Moderate-severe LUTS (IPSS≥8) at 50–59 → symptom-trigger knob |
| 10.1016/j.eururo.2009.02.026 | EPIC study — LUTS prevalence/bother | LUTS prevalence cross-check |
| 10.1016/j.euros.2020.12.004 | Identifying PCa among men with LUTS | Workup_Branch benign/cancer split |
| 10.3399/bjgp18X699689 | LUTS & PSA testing | Presentation/testing behaviour |

## Diagnostic pathway (PSA / MRI / biopsy)
| DOI | Source | Calibrates |
|---|---|---|
| 10.5402/2012/832109 | Irish PSA reference profiles | Age-specific PSA distribution |
| 10.1371/journal.pone.0283040 | Taiwanese PSA distribution | PSA percentiles cross-check |
| 10.1186/s12885-021-08216-6 | Gray-zone PSA + PSAD | PSA-tier biopsy yield |
| 10.1038/s41391-021-00417-1 | Oerther et al. — PI-RADS v2.1 meta-analysis | csPCa detection per PI-RADS (Biopsy_PR3/4/5 = 16/59/85%) |
| 10.1038/s41391-020-00290-4 | MRI-pathway cohort (PRECISION-type) | MRI-pathway csPCa yield ~35–38% |

## Grading, staging & risk-group distribution
| DOI | Source | Calibrates |
|---|---|---|
| 10.3389/fmed.2017.00157 | Mathieu et al. — ISUP grade-group validation | German Gleason/ISUP distribution |
| 10.1093/jncics/pkad018 | NCDB grade migration | GG1 decline 2010→2019 |
| 10.3389/fonc.2021.646073 | Xie et al. — risk-group stratification (SEER) | EAU risk-group proportions (verified: EAU-g 26.6/24.0/36.5/12.9) |
| 10.1002/hsr2.70414 | SEER under-50 prostate cancer | Younger-cohort stage skew (M1 ~4%) |
| 10.3399/BJGP.2024.0376 | National Cancer Diagnosis Audit | Screen-detected vs symptomatic |
| 10.1186/1471-2407-5-27 | Clinical vs screen diagnosis | Detection mode |
| 10.7759/cureus.90916 | Incidental PCa at TURP/HoLEP | TURP_Incidental_Check = 14% |

## Treatment allocation & outcomes
| DOI | Source | Calibrates |
|---|---|---|
| 10.3238/arztebl.2016.0329 | HAROW study | German real-world treatment allocation |
| 10.5173/ceju.2020.0167 | Active surveillance outcomes | AS→treatment ~50% in 5 yr |
| 10.1007/s00345-020-03471-x | HAROW active-surveillance long-term | AS conversion (German) |
| 10.1016/j.clgc.2024.102289 | Incidence & survival NRW registry | Survival by stage |
| 10.1111/bju.13537 | Germany vs USA PCa survival | Stage-adjusted survival |

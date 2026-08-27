# synthea-eu-cancer

Synthetic cancer patient cohorts for the **HL7 Europe Common Cancer Data Model (CCDM)**, generated via [Synthea](https://github.com/synthetichealth/synthea) with EU-specific epidemiology and post-processing into CCDM-conformant FHIR.

## ⚠️ Disclaimer — synthetic data

**This repository contains synthetic (computer-generated) data and a synthetic-data generator. It contains no real patient data.**

- **No real persons.** The data does not describe, and is not derived from, any real individual. Any resemblance to an actual person, living or dead, is coincidental.
- **Not for medical use or medical research.** This data must not be used to derive, support, or validate any clinical, epidemiological, statistical, or other medical or scientific finding, nor for diagnosis, treatment, or any decision affecting the care of any person. The transition probabilities are calibrated to published literature **for plausibility only** and do not constitute medical evidence.
- **Intended purpose.** The sole purpose of this project is to provide interoperable example data for the testing, development, validation, demonstration, and education of European health-data sharing and analysis projects — in particular the European Health Data Space (EHDS) and the HL7 Europe Common Cancer Data Model.
- **No warranty.** The data and code are provided "as is", without warranty of any kind, express or implied. Use is at your own risk.

## Cooperation

Developed in cooperation with:
- **Phoenix Initiative** — HL7 Europe Cancer Common Model working group (see beads `interop-prototypes-5vv`)
- **SYNDERAI** — "Synthetic Data for the European Health Data Space" (a.k.a. *Synthetic Data Examples – Realistic – using AI*), HL7 Europe initiative around synthetic datasets for testing, validation, education, and vendor implementation support. xShare project participation; speakers from Charité and Founda Health. HL7 Europe webinar: 2026-07-16. Thomas Debertshäuser presents *"Synthetic data for cancer research: the Phoenix Initiative."*

> See: https://hl7europe.eu/synderai-synthetic-data-for-the-european-health-data-space/

## Why

Synthea ships realistic patient simulation but is US-centric: epidemiology, demographics, identifiers, and FHIR profile baseline (US Core / mCODE) all assume US context. The HL7-EU CCDM needs cohorts that are:

1. Demographically European (country-level distributions, names, addresses, identifier systems)
2. Epidemiologically European (incidence/prevalence per ECIS / ENCR registry data)
3. Profile-conformant to **HL7 Europe CCDM** (not US Core / mCODE)
4. Coverage broader than Synthea's built-in oncology modules (breast, lung, colorectal, prostate)

## Scope

| Area | Status |
|------|--------|
| Wrapper to run upstream Synthea | TODO |
| EU epidemiology configs (incidence overrides per country) | TODO |
| Demographics localization (DE, FR, IT, ES, NL, … ) | TODO |
| New cancer modules (melanoma, pancreatic, hematologic, …) | TODO |
| Pediatric oncology modules | TODO |
| Synthea-FHIR → HL7-EU CCDM mapping | **DONE (draft)** — `scripts/postprocess_ccdm.py` reshapes prostate bundles to the 13 ECCDM draft profiles (stage/EOC/progression/follow-up derived; pinned draft build in `profiles/eccdm/`) |
| Validation against CCDM IG | **DONE (draft)** — `scripts/validate_ccdm.sh` gates a bundle sample against the vendored package |
| TNM staging emission (UICC-8, clinical + pathological) | **DONE** — module v3, calibration `epidemiology/prostate_calibration.md` §11 (Partin matrix, M1a/b/c split) |

## Repo layout

```
synthea-eu-cancer/
├── modules/         # Custom Synthea disease modules (JSON state machines)
│   ├── adult/       # Adult oncology modules
│   └── pediatric/   # Pediatric oncology modules
├── epidemiology/    # EU registry data (ECIS/ENCR), per-country incidence tables
├── mappings/        # Synthea-FHIR → HL7-EU CCDM transformations
├── profiles/eccdm/  # Vendored local build of the ECCDM draft profiles (pinned commit, see README there)
├── scripts/         # Run scripts, post-processing pipelines (incl. postprocess_ccdm.py, validate_ccdm.sh)
└── docs/            # Design notes, CCDM mapping decisions
```

## Approach

Upstream Synthea is added as a git submodule (not forked) so we stay in lockstep with releases. EU customization layers on top via:

1. **Custom modules** loaded via `--module-dir` flag
2. **Properties overrides** for country/locale
3. **Post-processing** transforms output bundles to CCDM profiles (separate pipeline, doesn't fight Synthea internals)

## Related work in this monorepo

- `oncology-regimens/` — MII Onkologie Protokoll-Catalog (FHIR knowledge layer)
- beads `interop-prototypes-5vv` — PHOENIX engagement on CCDM catalog extension
- beads `interop-prototypes-5d9` — Phase 2 EU extension of MII Onko catalog

## Status

Scaffold only. See beads `interop-prototypes-dve` for tracking.

## Terminology attribution & license

This repository — the code and the Synthea module — is offered under **CC0 1.0 Universal**, matching the HL7 Europe Common Cancer Model (`hl7-eu/cancer-common`) it targets.

The module and the generated data reference standard terminologies. These are **not** covered by CC0; they remain the property of their respective owners and may require a licence in your jurisdiction:

- **SNOMED CT®** — © SNOMED International. Used by permission; SNOMED and SNOMED CT are registered trademarks of SNOMED International. Use of SNOMED CT requires a valid SNOMED CT Affiliate Licence in the applicable territory (in Germany administered nationally by BfArM). <https://www.snomed.org>
- **LOINC®** — this material contains content from LOINC (<http://loinc.org>), copyright © 1995–2024 Regenstrief Institute, Inc. and the LOINC Committee, available at no cost under the LOINC license (<http://loinc.org/license>). LOINC® is a registered trademark of Regenstrief Institute, Inc.
- **ATC / DDD** — © WHO Collaborating Centre for Drug Statistics Methodology (WHOCC), Oslo (<https://www.whocc.no>). The German ATC version (ATC-DE) is published by BfArM (`http://fhir.de/CodeSystem/bfarm/atc`).

See also the [synthetic-data disclaimer](#️-disclaimer--synthetic-data) above: this data is not for medical use or research.

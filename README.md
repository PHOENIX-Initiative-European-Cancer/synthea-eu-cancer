# synthea-eu-cancer

Synthetic cancer patient cohorts for the **HL7 Europe Common Cancer Data Model (CCDM)**, generated via [Synthea](https://github.com/synthetichealth/synthea) with EU-specific epidemiology and post-processing into CCDM-conformant FHIR.

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
| Synthea-FHIR → HL7-EU CCDM mapping | TODO |
| Validation against CCDM IG | TODO |

## Repo layout

```
synthea-eu-cancer/
├── modules/         # Custom Synthea disease modules (JSON state machines)
│   ├── adult/       # Adult oncology modules
│   └── pediatric/   # Pediatric oncology modules
├── epidemiology/    # EU registry data (ECIS/ENCR), per-country incidence tables
├── mappings/        # Synthea-FHIR → HL7-EU CCDM transformations
├── scripts/         # Run scripts, post-processing pipelines
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

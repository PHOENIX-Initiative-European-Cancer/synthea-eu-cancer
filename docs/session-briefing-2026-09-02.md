# Session-Briefing (Stand 2026-09-02)

Einstieg für die nächste Session in `~/code/interop-prototypes/synthea-eu-cancer`.
`bd prime` läuft automatisch; `bd ready` zeigt die entsperrte Arbeit. Die wichtigsten
Erkenntnisse liegen als bd-Memories (`bd memories eccdm`, `bd memories synderai`).

## Wo das Projekt steht

**Prostata (fertig, validiert):** Modul v3 emittiert klinisches + pathologisches TNM
(SNOMED-UICC-8-Werte, Partin-Matrix), Histologie, alle Codes serverbestätigt. 1000er-Kohorte
(Seed 42) → `scripts/postprocess_ccdm.py` formt die 115 Krebs-Journeys auf die **ECCDM-Draft-
Profile** um (Pin: Fork `ValhallasCat/cancer-common@c020f19`, gevendort in `profiles/eccdm/`).
Validator-Gate `scripts/validate_ccdm.sh`: **0 Errors**. Feedback-Liste ans Profil-Team:
`docs/eccdm_draft_feedback.md` (offene Extension-URL-Typos = Breaking-if-fixed!).

**Mamma (Konzept + Evidenz fertig, Umsetzung offen):** Kohorte **Frauen 50–60** (entschieden),
DCIS ja, BRCA schlank (Population 0,35 %!), Biomarker unprofiliert (ECCDM-Lücke).
- `docs/breast_module_concept.md` — Architektur, evidenz-korrigiert (Detektionsmix **44/18/38**;
  BI-RADS ist im dt. Screening **nicht erhoben** → nur Emissions-Artefakt; pCR = `ypT0/is ypN0`)
- `epidemiology/breast_calibration.md` — 3.081 Zeilen Evidenz, Teile A/B/C, jeder Wert mit
  Quelle + Confidence-Flag. Bei pCR-Überlappung gilt Teil C §3.

## Entsperrte nächste Schritte (bd ready)

1. **`synthea-eu-cancer-c0v`** (AP-T): Brustkrebs-Codes validieren (SNOMED/LOINC/OPS, ~15
   Substanzen dual WHO-ATC + ATC-DE) → `terminology/breast_data_dictionary.md`. **Entsperrt den
   Modulbau `5h3`** (Kette: 5h3→qoc→1s7→{io5,dba}→0wh→aij; dazu dbq Feedback, xb3 optional).
2. **`synthea-eu-cancer-bp2`**: GENIE BPC (Prostate + BRCA 1.0-public) → TTNT-/PFS-Verteilungen
   für die Zeit-Pfeile. ⚠️ Braucht einmalige **Synapse-Registrierung durch Thomas**; danach
   R-Paket `{genieBPC}`. Kalibriert u. a. `mCRPC_Delay` (heute uniform 1–3 J).
3. **`synpros-6n1`** (Prostata v4, Zeitkomponente): Workup mit Prozess-Delays entzerren
   (poln. Fast-Track-Paper PMC12153762: 19,6/27,7/14/18,3 Tage), S3-Nachsorgekette
   (PSA q3 Mo J1–2, q6 Mo J3–4, jährlich ab J5) mit **BCR als per-Visit-Hazard** (emergente
   Zeit-bis-BCR statt Uniform-Draw). Details in den Bead-Notes.
4. **`synthea-eu-cancer-4uk`**: Sankey-Visualisierung der Kohorten-Flüsse (plotly aus
   `prostate_eventlog.csv`; Knoten = kalibrierte Branch-Punkte → visuelle Gegenprobe).
   Vorher `dataviz`-Skill lesen.

## Fallen & Konventionen (Kurzfassung — Details in bd memories)

- ECCDM-Canonical `http://hl7.eu/fhir/cancer-common` kann sich vor Ballot ändern →
  `postprocess_ccdm.py --base` ist parametrisiert; Pin-Wechsel = SUSHI-Rebuild + tgz-Tausch
  (Anleitung in `profiles/eccdm/README.md`).
- SNOMED-TNM: **UICC-Codes, nie AJCC** (Lizenz); Morphologie 35917007 ist inaktiv → 1187332001.
- Kein pT1 bei Prostata; TURP-Inzidental = cT1a/b (klinisch!).
- meta.security = HTEST+TRAIN (SYNTH existiert nicht und vergiftet die ganze Validierung).
- Synthea: `ConditionOnset` mit `target_encounter`, der nie wiederkommt, manifestiert nie.
- Session-Ende: Commit + `bd dolt push` + `git push` (CLAUDE.md-Protokoll).

## Sonstiges

- Web-Search-Budget global auf 1000/Session erhöht (`~/.claude/settings.json`) — gilt ab
  Session-Start, die Recherche-Subagents teilen sich das Budget.
- Bewährtes Muster dieser Tage: Konzept-/Evidenz-Arbeit an benannte Hintergrund-Agenten
  delegieren (parallel), Ergebnisse mergen, bd-Issues vom Hauptthread pflegen. Antworten
  von Sub-Sub-Agenten landen gelegentlich bei main → einfach an den Ziel-Agenten weiterleiten.
- Dieses Briefing nach Gebrauch gern löschen oder überschreiben.

# Konzept: Synthea-Brustkrebs-Modul (Frauen 50–60)

Analogon zu `modules/adult/prostate.json` + `epidemiology/prostate_calibration.md`. Dieses Papier legt das
klinische Modell, die Stratifizierungsachsen, die Emissionscodes und die Arbeitspakete fest — **es ist noch keine
Kalibrierungsdoku**. Die Zahlen unten sind bereits recherchiert und bequellt, wandern aber beim Umsetzen in
`epidemiology/breast_calibration.md` (Epic `synthea-eu-cancer-4w3`), damit dieses Dokument als Architekturentscheid
lesbar bleibt.

**Kohortenfenster: Frauen 50–60** (Entscheid, spiegelt die Prostata-Kohorte 50–60). Das ist ein Screening-Fenster
mit ~5–6 Einladungsrunden im 2-Jahres-Takt und hat mehrere nicht-triviale Konsequenzen für die Kalibrierung —
siehe **§1.2**, das den Altersband-Effekt an einer Stelle bündelt.

> ⚠️ **Quellenlage zum Altersband.** Fast alle deutschen Auswertungen zum Mammakarzinom sind auf das
> Screening-Anspruchsalter **50–69** geschnitten (RKI-Stadienverteilung, TRM-Subtypen, Braun 2018,
> OnkoZert-Kennzahlen). Nur wenige Quellen liefern 50–54/55–59-Bänder (KoopMammo-Kennzahlen, TRM-M1-Anteil,
> RKI-Überleben). **Konvention in diesem Dokument:** wo eine 50–59-Zahl existiert, wird sie verwendet und mit
> 🟢/🟡 geführt; wo nur 50–69 vorliegt, wird die 50–69-Zahl beibehalten, mit **„Quelle 50–69"** markiert und die
> Confidence um eine Stufe abgesenkt (🟢→🟡, 🟡→🔴), weil die Übertragung auf 50–60 unbelegt ist.
> Die Richtung der Verzerrung ist meist bekannt und wird jeweils angegeben.

**Confidence-Legende** (identisch zum Prostata-Modul): 🟢 gut belegt (deutsches/EU-Register oder große Primärstudie,
genau die gefragte Zahl) · 🟡 belegt, aber Übertragbarkeits-/Ära-Vorbehalt · 🔴 Modellierungsprior / Schätzung.

### Entschiedener Scope für v1

| Thema | Entscheidung | Detail |
|---|---|---|
| Kohortenfenster | **Frauen 50–60** | §1.2 |
| **DCIS** | **JA, verbindlich mitmodelliert** — eigener Ast, kein Subtyp | §3.3 |
| **Hochrisiko-/BRCA-Arm** | **JA, aber ausdrücklich schlank** — Minimalvariante in v1, Vollvariante v2 | §1.4.1 / §1.4.2 |
| **Biomarker + Grading (FHIR-Profilierung)** | **unprofilierte LOINC-Observations**; TNM voll ECCDM-profiliert; Lücke als Feedback ans Phoenix-Team; **kein SenologieOnFHIR-Tagging in v1** | §8.3 Punkt 3 |
| Ki-67-Cutoff | 14 % (St. Gallen 2013) als bewusste Modellkonvention | §3.1 |
| BI-RADS | Emissions-Artefakt statt steuernder Branch (Option 1) | §2 |
| Ausgeschlossen in v1 | bilaterale Karzinome, männliches Mamma-Ca, B3/ADH, Rekonstruktion, Psychoonkologie, Studienteilnahme | §10.2 |

**Leitlinien-Frame:** S3-Leitlinie Mammakarzinom **AWMF 032-045OL, Version 5.1 (Juni 2026)** gibt die *Struktur*;
**AGO Kommission Mamma 2026.1D** die Therapie-Feinheiten; **RKI/ZfKD "Krebs in Deutschland 2021–2023" (KID 2025)**,
**Tumorregister München (TRM)**, **Kooperationsgemeinschaft Mammographie (KoopMammo) Jahresbericht Evaluation 2023**
und der **DKG/OnkoZert-Jahresbericht Brustkrebszentren 2025** kalibrieren die *Wahrscheinlichkeiten*.
Klassifikationsrahmen für Staging: **UICC TNM 8. Auflage**.

---

## 0. Was vom Prostata-Modul übernommen wird — und was nicht

| Baustein | Prostata v3 | Mamma (Vorschlag) |
|---|---|---|
| Wurzel-Trigger | *ein* Symptom-Trigger (LUTS), 100 % der Kohorte | **drei Eintrittspfade** (Screening / Intervall / symptomatisch), Anteile epidemiologisch belegt |
| Bildgebungs-Score im Workup | PI-RADS (LOINC 82717-8) → biopsierate-steuernd | **BI-RADS** (LOINC 72018-2, SNOMED-Werte) → identische Rolle |
| Haupt-Branch nach Diagnose | EAU-Risikogruppe (5 Klassen) | **Surrogat-Subtyp** (5 Klassen) — aber als *abgeleitete*, nicht als primäre Größe (§3.2) |
| Zweite Stratifizierungsachse | — | **Detektionsmodus** (bedingt Stadium, Grading, Subtyp) — §1.3 |
| Staging-Emission | LOINC 21905-5/21906-3/21907-1 + 21899-0/21900-6, SNOMED-UICC-8-Werte | **unverändert übernehmbar** (§5.4) + neu `yp`-Kategorien |
| Histologie | ein Wert (8140/3) | Verteilung über 4–5 ICD-O-Morphologien inkl. `/2` für DCIS |
| Rezidiv-Pfad | BCR (PSA-getrieben) → Salvage | **Lokalrezidiv / Fernmetastasierung** (subtyp-abhängige Hazard-Form) — §7 |
| Neoadjuvanz | existiert nicht | **neu und tragend**: pCR-Branch mit `ypTNM` — §6.2 |
| Biomarker | keine (Gleason ist ein Score, kein Biomarker) | **ER/PR/HER2/Ki-67 als kohärentes Observation-Set** — §4, zugleich die größte ECCDM-Lücke |

**Wiederverwendbar ohne Änderung:** `scripts/postprocess_atc_de.py`, `scripts/postprocess_synthetic_tag.py`,
`scripts/make_provenance_fhir.py`, `scripts/fhir_to_eventlog.py` + `eventlog_to_dfg.py` (Process Mining),
`scripts/validate_ccdm.sh`. `scripts/postprocess_ccdm.py` braucht eine Entitäts-Abstraktion (§8.3).

---

## 1. Klinisches Modell — Eintrittspfade

### 1.1 Die Wurzelentscheidung: Detektionsmodus

Beim Prostata-Modul war der Eintritt trivial (ein Symptom-Trigger, alle Männer). Beim Mammakarzinom ist der
**Detektionsmodus die analytisch wertvollste Variable überhaupt**, weil das deutsche
Mammographie-Screening-Programm (MSP) eine große, gut vermessene Teilpopulation erzeugt, deren Tumoren
systematisch kleiner, nodal-negativer und besser differenziert sind. Der Modus gehört deshalb an die *Wurzel*
und wird als Patientenattribut (`bc_detection_mode`) durch das gesamte Modul getragen.

| Eintrittspfad | Anteil | Basis | Conf |
|---|---|---|---|
| **Screening-detektiert** (MSP) | **0.45** | Braun 2018 (Münster MSP 2006–2012, n=1.531): 46,6 %; national gegengerechnet ~50 %. **Quelle 50–69** | 🟡 (eine Region + Altersband) |
| **Intervallkarzinom** (nach negativem Screening) | **0.11** | Braun 2018: 10,4 %; Programmsensitivität 69,9–71,7 % (Kaiser 2023, PMC10496211) ⇒ ~28 % Intervallanteil unter Teilnehmerinnen. **Quelle 50–69** | 🟡 |
| **Symptomatisch / Nicht-Teilnehmerin** | **0.44** | Braun 2018: 42,9 %. **Quelle 50–69** | 🟡 |
| **Hochrisiko / IFNP** (BRCA & Co.) | **0.03** *zusätzlich, überlagernd* | gBRCA1/2 in unselektierter BC 1,8 % (LIBRO-1, PMC6320715); Altersgradient >50 J. 3,3 % (PMC3240809). Im Fenster **50–60** höher als in 50–69, weil nur 26 % der BRCA1- und 33 % der BRCA2-Trägerinnen ≥60 J. bei Diagnose sind (LIBRO-1) | 🔴 |

**Richtung der Altersband-Verzerrung** für die drei Detektionsmodi: im Fenster 50–60 verschiebt sich der Mix
**weg vom Screening**, weil (a) die Hintergrundinzidenz mit dem Alter steigt (259/100.000 bei 50–54 gegen
350/100.000 bei 65–69, KoopMammo 2023) 🟢, die Detektionsrate im Screening also niedriger ist, während der
symptomatische Arm relativ an Gewicht gewinnt, und (b) Intervallkarzinome bei dichterem Drüsengewebe jüngerer
Frauen häufiger sind. Belegt ist diese Verschiebung **nicht** — Braun 2018 publiziert den Detektionsmix nicht
nach Altersband. Der 45/11/44-Split bleibt deshalb der Startwert; er ist ein **Kalibrier-Kandidat für
`synthea-eu-cancer-51w`** und keine gesetzte Größe.

**Modellierungshinweis Screening-Teilnahme:** die Teilnahme ist stark „klebrig" und darf **nicht** als i.i.d.
52-%-Münzwurf modelliert werden. KoopMammo 2023 liefert die Markov-Kette direkt: Ersteinladung **45,9 %**,
Wiedereinladung nach Teilnahme **86,3 %**, nach Nicht-Teilnahme **15,3 %** (Gesamtteilnahme 52,1 %) 🟢.
Das ist der Mechanismus, der die 45/11/44-Aufteilung *erzeugt*, statt sie zu postulieren — und er ist mit einer
`Delay` + `complex_transition`-Schleife auf einem Attribut `msp_last_attended` in Synthea sauber abbildbar.

### 1.2 Kohorten-Fenster 50–60 — Programmparameter und Altersband-Effekte

Anspruchsberechtigt ist **50–69 J.**, seit 01.07.2024 **50–75 J.** (G-BA-Beschluss 21.09.2023; 70–75 derzeit nur
auf Selbsteinladung) 🟢. Einladungsintervall **24 Monate**, regulär 22–30 Monate 🟢. Das **Kohortenfenster des
Moduls ist 50–60**: Einladung mit 50, 52, 54, 56, 58, 60 ⇒ **6 Einladungen / ~5 Intervalle**. Die
Teilnahme-Markov-Kette (§1.1) bleibt davon unberührt — sie ist ohnehin rundenbasiert und nicht altersparametrisiert.

Vier Effekte folgen aus dem schmaleren, jüngeren Fenster und müssen in der Kalibrierung explizit behandelt werden:

**(a) Die Erstrunden-Prävalenzspitze fällt vollständig in die Kohorte.** Programmweit sind nur 16 % aller
Untersuchungen Erstuntersuchungen; in einer 50–60-Kohorte durchläuft dagegen **jede Teilnehmerin ihre
Erstuntersuchung mit ~50 Jahren** — also innerhalb des Beobachtungsfensters. Erstuntersuchungen unterscheiden
sich massiv von Folgeuntersuchungen (KoopMammo 2023, alle 🟢):

| Kennzahl | Erstuntersuchung | reguläre Folgeuntersuchung |
|---|---|---|
| Wiedereinbestellungsrate | **10,8 %** (50–54: 10,9 %) | **2,6 %** (50–54: 3,2 %; 55–59: 2,4 %) |
| Detektionsrate (CDR) | **8,7 ‰** (50–54: **7,6 ‰**) | 5,3 ‰ (50–54: **3,8 ‰**) |
| DCIS-Anteil | 22 % | 18 % |
| invasiv ≤10 mm | 29 % | 36 % |
| nodal-negativ | 76 % | 82 % |
| UICC II+ | 26 % | 21 % |

Das Modul muss Erst- und Folgeuntersuchung deshalb als **getrennte Zustände** führen (Attribut
`msp_round_index`), nicht als eine gemittelte Screening-Runde. In einer 50–69-Kohorte hätte man das mit dem
Programmmittel wegmitteln können; in 50–60 wäre das ein systematischer Fehler.

**(b) Die Fallzahl pro Kohortenkopf sinkt deutlich.** Die CDR bei 50–54 liegt in Folgeuntersuchungen bei
**3,8 ‰** gegenüber 7,0 ‰ bei 65–69 🟢; das mediane Erkrankungsalter in Deutschland ist **65 Jahre**, und nur
15 % aller Fälle treten vor 50 auf 🟢. Ein 50–60-Fenster liegt also auf der **ansteigenden Flanke** der
Inzidenzkurve. Für die Kohortengenerierung heißt das: entweder große `-p`-Zahlen oder — wie beim Prostata-Modul
mit dem LUTS-Trigger von 0,12/Jahr — ein bewusst überhöhter **Durchsatz-Stellknopf**, der als solcher
gekennzeichnet wird (🔴 „Kohorten-Ausbeute, NICHT Epidemiologie") und nicht mit den kalibrierten Arrows
vermischt wird.

**(c) Der Subtyp-Mix verschiebt sich leicht ins Aggressivere.** Der Altersgradient ist im TRM quantifiziert
(§3.1): TNBC <50 J. **12,2 %** gegen 50–69 J. 8,7 % (RR 1,40), Luminal A <50 J. 26,3 % gegen 50–69 J. 35,7 % 🟢.
Ein 50–60-Fenster liegt zwischen beiden Bändern, also näher am 50–69-Wert, aber mit erkennbarer Drift: **TNBC
etwas höher, Luminal A etwas niedriger** als die 50–69-Marginale. Da die TRM-Publikation keine 50–59-Spalte
enthält, bleibt die Größe der Drift 🔴.

**(d) Der Spättail der luminalen Rezidive entfaltet sich nicht.** Dies ist das direkte Analogon zur
Prostata-Notiz „in einem 50–60-Querschnitt entfaltet sich der BCR/Salvage-Tail nur für früh diagnostizierte
Patienten". Bei ER+-Tumoren treten Fernrezidive über **Jahre 5–20** mit konstant 1–2 %/Jahr auf (Pan 2017) 🟢 —
eine mit 58 diagnostizierte Frau erreicht im Modell nur ~2 Nachbeobachtungsjahre. Konsequenz: die
Rezidiv-Statistik der generierten Kohorte ist **strukturell nach TNBC verschoben** (früher Hazard-Gipfel bei
2–3 Jahren, der ins Fenster fällt). Das ist keine Fehlkalibrierung, sondern eine Eigenschaft des Fensters — sie
gehört als Einschränkung in `README.md` und in die Validierung (§10), damit niemand die Kohorten-Rezidivrate
gegen Registerzahlen hält. Wer den luminalen Spättail braucht, muss das Endalter anheben.

### 1.3 Warum der Detektionsmodus konditionierend wirkt

Braun 2018 (PMID 30149831) publiziert die **gemeinsame Verteilung** von Detektionsmodus mit Stadium, Grading und
Subtyp in derselben Population — das ist der Grund, warum diese Achse nicht nur kosmetisch ist.
**Quelle 50–69** (Münster MSP-Teilnehmerinnen 2006–2012); nach Altersband ist die Tabelle nicht aufgeschlüsselt,
alle Zeilen daher für 50–60 um eine Stufe abgewertet:

| Merkmal | screen-detektiert (n=714) | Intervall (n=160) | Nicht-Teilnehmerin (n=657) | Conf (50–60) |
|---|---|---|---|---|
| DCIS-Anteil | **26,3 %** | 8,1 % | 12,8 % | 🟡 |
| T1 (der Invasiven) | **78,3 %** | 58,5 % | 54,8 % | 🟡 |
| N0 / N+ | **75,5 / 23,4 %** | 59,9 / 32,0 % | 61,3 / 30,7 % | 🟡 |
| G1 / G2 / G3 | 34,6 / 48,7 / **16,5 %** | 21,1 / 51,0 / 27,9 % | 19,9 / 52,4 / 27,2 % | 🟡 |
| Triple-negativ | **6,1 %** | 11,6 % | 12,0 % | 🟡 (in 50–60 eher höher, §1.2c) |
| HR+/HER2− | 78,0 % | 70,1 % | 67,7 % | 🟡 |
| HER2+ | 15,0 % | 17,7 % | 18,9 % | 🟡 |
| BET-Rate (inkl. DCIS) | 75,2 % | 67,5 % | 61,5 % | 🟡 |

Programmweite Gegenprobe (KoopMammo 2023, Folgeuntersuchungen) 🟢: DCIS 18 %, invasiv ≤10 mm 36 %,
nodal-negativ 82 %, UICC II+ **21 %** — gegen die Prä-Screening-Zielpopulation 2000–2005: DCIS 7 %, ≤10 mm 14 %,
N0 57 %, UICC II+ **56 %**. Die Screening-vs-symptomatisch-Spreizung ist also groß und gut belegt; ein Modul, das
sie ignoriert, erzeugt eine unrealistisch homogene Kohorte.

### 1.4 Hochrisiko-Arm (IFNP)

> ✅ **ENTSCHIEDEN:** der Hochrisiko-Arm wird mitmodelliert, aber **ausdrücklich schlank**. Verbindlich für v1 ist
> die Minimalvariante in **§1.4.1**; alles darüber hinaus ist v2 (**§1.4.2**). Die fachliche Herleitung unten
> bleibt als Begründung und als Vorrat für v2 stehen.

Der Arm des **Deutschen Konsortiums Familiärer Brust- und Eierstockkrebs** ist klein, aber strukturell eigenständig
und liefert die Aufhänger für `FamilyMemberHistory` + Checkliste:

- Einschluss über die **DKG/GC-HBOC-Checkliste** (V1_28.07.2020): Risiko-Score = A + max(B, C), hereditäre
  Belastung ab **Score ≥ 3**; Gentest ab empirischer Mutationsdetektionswahrscheinlichkeit **≥ 10 %**
  (Kast 2016, 21.401 Familien) 🟢. Für die 50–60-Kohorte relevante Gewichte: uni-/bilaterales Mamma-Ca **nach**
  dem 51. Geburtstag = 1 Punkt, TNBC vor 50 = 3, Ovarial-Ca vor 80 = 3. Die Indexpatientin selbst bringt in
  diesem Altersfenster also nur **1 Punkt** mit — der Score ≥3 entsteht fast ausschließlich aus der
  Familienanamnese (B/C-Zweige). Das ist ein wichtiger Modellierungshinweis: ohne belegte
  `FamilyMemberHistory` erreicht in 50–60 praktisch niemand die Checklisten-Schwelle.
- **IFNP-Inhalt:** jährliches Kontrast-MRT, Mammographie (inkl. Tomosynthese) alle 1–2 J. ab 40, Sonographie bei
  jedem Termin 🟢. Programmsensitivität **89,6 %**, **84,5 %** der entdeckten Karzinome Stadium 0 oder I
  (Bick 2019, n=4.573) 🟢. Detektionsrate im Regelbetrieb **1,53 %** (DKG FBREK-Jahresbericht 2025) 🟢.
- **Subtyp-Skew:** BRCA1-Tumoren sind zu **~69–71 %** triple-negativ, BRCA2 nur zu ~16–23 % (CIMBA 2012,
  PMID 22144499) 🟢. Altersverschiebung BRCA1 ≈ −22 bis −25 J., BRCA2 ≈ −18 bis −20 J. gegenüber dem
  deutschen Median von 65 J. 🔴; nur 26 % der BRCA1- und 33 % der BRCA2-Trägerinnen sind bei Diagnose ≥60 J.
  (LIBRO-1) 🟢. Das Fenster **50–60** trifft BRCA-Trägerinnen damit **besser** als 50–69 — der Hochrisiko-Arm
  ist hier relativ stärker besetzt (§1.1) — aber immer noch weit rechts vom Erkrankungsgipfel
  (BRCA1 30–40 J., BRCA2 40–50 J., Kuchenbaecker 2017) 🟢. Empfehlung unverändert: den Hochrisiko-Arm als
  **eigenes Alters-Guard ab ~35 J.** neben dem 50–60-Screening-Guard führen, nicht als Unterast davon. Wird der
  Arm auf 50–60 beschnitten, entstehen fast nur BRCA2-/Moderate-Risk-Journeys und praktisch keine typische
  BRCA1-TNBC-Journey — das wäre klinisch irreführend.

#### 1.4.1 Minimalvariante — verbindlich für v1

Ziel: der Arm soll **erkennbar** sein (Kohorte enthält Hochrisiko-Journeys mit plausibler Bildgebung und
Subtyp-Skew), aber **keinen eigenen Zustandsbaum** aufziehen. Er kostet damit ~8–10 zusätzliche Zustände statt
der ~40, die die Vollvariante bräuchte.

| Element | Umsetzung in v1 | Wert | Conf |
|---|---|---|---|
| Zugehörigkeit | **ein Attribut** `bc_high_risk` (boolean), gesetzt im `Initial`-Bereich | **0.02** der Kohorte | 🔴 (Spanne 1,5–2,5 %, §1.1) |
| Familienanamnese | **eine** `FamilyMemberHistory` (Mutter oder Schwester, Mamma-Ca), pauschal bei `bc_high_risk` | SCT 254837009, `onset` = Erkrankungsalter | 🟢 (Codes) |
| Checkliste | **eine** Observation SCT 445039002, `valueBoolean = true`, Komponente `score` = 3–5 | — | 🟢 (Codes) |
| Früherkennung | **intensivierte Bildgebung statt MSP**: jährliches Mamma-MRT (LOINC 30794-2) + Mammographie, ersetzt die 2-Jahres-Screening-Schleife | jährlich statt 2-jährlich | 🟢 (IFNP-Inhalt) |
| Detektionsvorteil | höherer Anteil Stadium 0/I | **84,5 %** Stadium 0 oder I (Bick 2019) | 🟢 |
| Subtyp-Skew | Umgewichtung des `Subtype_Branch` **auf demselben Branch**, nicht als eigener Ast | TNBC-Anteil **~40 %** statt ~9 % (gemischt BRCA1/BRCA2/Nicht-Trägerinnen; reine BRCA1-Kohorten liegen bei 69–71 %) | 🔴 |
| Genetik | **eine** Observation LOINC 69548-6 mit `gene-studied` BRCA1/BRCA2 (LOINC 48018-6, HGNC) | — | 🟢 (Codes) |

**Ausdrücklich NICHT in v1:** prophylaktische Mastektomie/Adnexektomie, kontralaterale Zweitkarzinome,
Kaskadentestung von Angehörigen, TruRisk-Panel jenseits BRCA1/2, differenzierte BRCA1-vs-BRCA2-Journeys,
Risikoberechnung nach BOADICEA, Score-Berechnung aus einer echten Familienanamnese-Struktur. Der
Checklisten-Score wird **gesetzt, nicht gerechnet**.

**Konsequenz für das Alters-Guard:** die Minimalvariante läuft im **normalen 50–60-Fenster** mit. Das erzeugt
zwar überwiegend BRCA2-/Moderate-Risk-typische Journeys (§1.4 oben) — akzeptiert, weil ein zweites Alters-Guard
ab 35 J. eine eigene Kohortenpopulation und damit genau die Komplexität bedeutet, die vermieden werden soll.
Diese Einschränkung gehört in `README.md`: **die Kohorte enthält keine typische junge BRCA1-TNBC-Journey.**

#### 1.4.2 Vollvariante — v2

Eigenes Alters-Guard ab ~35 J., getrennte BRCA1-/BRCA2-Pfade mit den publizierten Altersverteilungen und
kumulativen Risiken (BRCA1 72 % / BRCA2 69 % bis 80 J., Kuchenbaecker 2017 🟢; deutsche prospektive Werte bis
60 J.: BRCA1 61,8 % / BRCA2 43,2 %, Engel 2020 🟢), prophylaktische Chirurgie, kontralaterale Karzinome
(BRCA1 25,1 % @10 J., Engel 2020 🟢), Moderate-Risk-Gene (PALB2, CHEK2, ATM — BRIDGES-ORs, Dorling 2021 🟢).
Erst dann lohnt sich der Aufwand, weil die Journey-Vielfalt dann tatsächlich abgebildet wird.

---

## 2. Workup — BI-RADS als PI-RADS-Analogon

Kaskade: **Mammographie → (Sonographie / MRT) → Stanz- oder Vakuumbiopsie**. Strukturell identisch zum
`PIRADS_Branch` → `Biopsy_PR{3,4,5}`-Muster des Prostata-Moduls: ein ordinaler Bildgebungs-Score steuert die
Biopsierate, und die Malignitätswahrscheinlichkeit hängt an der Score-Stufe.

KoopMammo veröffentlicht Wiedereinbestellung und CDR **nach 5-Jahres-Altersband**. Diese Arrows sind daher die
einzigen im ganzen Dokument, die direkt auf 50–60 kalibriert werden können — sie sollten unbedingt
altersbandspezifisch kodiert werden statt mit dem Programmmittel.

| Arrow | Wert für 50–60 | Programmmittel (Referenz) | Basis | Conf |
|---|---|---|---|---|
| `MSP_Exam` → Wiedereinbestellung, **Erstuntersuchung** | **0.109** (50–54) / 0.103 (55–59) | 0.108 | KoopMammo 2023, Tab. 4 | 🟢 |
| `MSP_Exam` → Wiedereinbestellung, **reguläre Folge** | **0.032** (50–54) / **0.024** (55–59) | 0.026 | ebd. | 🟢 |
| Detektionsrate (CDR), **Erstuntersuchung** | **7,6 ‰** (50–54) | 8,7 ‰ | ebd. §9 | 🟢 |
| Detektionsrate (CDR), **reguläre Folge** | **3,8 ‰** (50–54) | 5,3 ‰ | ebd. §9 (Anstieg auf 7,0 ‰ bei 65–69) | 🟢 |
| Hintergrundinzidenz (Nenner der relativen CDR) | **259/100.000** (50–54) | — | ebd. §9 (350/100.000 bei 65–69) | 🟢 |
| Wiedereinbestellung → Abklärung wahrgenommen | **0.98** | 0.98 | ebd. | 🟢 (altersunabhängig) |
| Abklärung → Biopsieindikation | **1,1 %** aller Untersuchten | dito | ebd. | 🟡 (nicht nach Alter berichtet) |
| **PPV I** (Karzinom unter Wiedereinbestellten) | **0.16** | dito | ebd. | 🟡 (nicht nach Alter berichtet; in 50–54 wegen höherer Recall- und niedrigerer Detektionsrate rechnerisch **niedriger**) |
| **PPV II** (Karzinom unter nicht-invasiv Abgeklärten) | **0.56** | dito | ebd. | 🟡 |
| Präoperativ histologisch gesichert | **0.95** | dito | ebd. | 🟢 |
| `BIRADS_Branch` → 1–2 / 3 / 4 / 5 | **Modellierungsprior**, muss PPV I und die altersband-spezifische CDR reproduzieren | — | keine deutsche BI-RADS-Verteilung im Abklärungskollektiv publiziert | 🔴 |

Die PPV-Werte sind programmweit berichtet, nicht nach Alter. Da bei 50–54 die Wiedereinbestellungsrate *höher*
und die CDR *niedriger* ist als im Programmmittel, muss der PPV I in dieser Altersgruppe rechnerisch unter
0,16 liegen. Wer die drei Größen (Recall, CDR, PPV) gleichzeitig aus dem Programmmittel übernimmt, erzeugt eine
**inkonsistente Kette**. Empfehlung: Recall und CDR altersbandspezifisch setzen (beide 🟢) und den PPV daraus
**ableiten** statt ihn zu setzen — das ist zugleich die Konsistenzprüfung für `synthea-eu-cancer-51w`.

**Der eine bewusst zu wählende Schwellenwert** (Analogon zur PSA-3-vs-4-Notiz im Prostata-Modul): das
Prostata-Modul steuert die Biopsie über PI-RADS-*Stufen* mit publizierten stufenspezifischen Detektionsraten
(Oerther 2021). Für BI-RADS existiert **keine gleichwertige deutsche Stufen-Detektionsrate** 🔴. Zwei Optionen:

1. **BI-RADS als Emissions-Artefakt** — Biopsie und Malignität direkt aus PPV I / PPV II ziehen, BI-RADS
   *rückwärts* konsistent setzen (BI-RADS 4 bei Biopsie, 5 bei hoher Malignitätswahrscheinlichkeit).
   Vorteil: alle Arrows bleiben 🟢, nichts wird erfunden.
2. **BI-RADS als steuernder Branch** — analog PI-RADS, aber mit 🔴-Prior für die Stufenverteilung.

**Empfehlung: Option 1.** Sie hält den Anteil roter Arrows niedrig und nutzt aus, dass die deutsche
Screening-Kette anders als die Prostata-Kette an ihren *Ergebnis*-Kennzahlen (PPV, CDR) vermessen ist,
nicht an ihren Zwischenstufen. Der BI-RADS-Wert wird trotzdem emittiert — er ist ein Pflicht-Datenelement in
SenologieOnFHIR und ein wichtiges Testartefakt.

Der symptomatische Arm überspringt das Screening und geht über `Tastbefund` → `Diagnostische Mammographie +
Sonographie` → Biopsie; hier ist die Malignitätsrate deutlich höher, aber ohne publizierte deutsche Zahl 🔴 —
sie wird stattdessen implizit über die Kohortenzusammensetzung (§1.1) gesteuert.

---

## 3. Subtypen-Stratifizierung

### 3.1 Verteilung

Die einzige belastbare deutsche populationsbezogene Quelle mit dem vollständigen 5-Wege-Split ist das
**Tumorregister München** (Schrodi/Eckel/Schubert-Fritschle/Engel, DKK-Poster 02/2016, n=8.228 invasive BC,
Diagnose 2000–2014, Surrogat-IHC nach St. Gallen 2013):

| Surrogat-Subtyp | <50 J. | **50–69** *(Startwert)* | Drift-Richtung für 50–60 | Definition (St. Gallen 2013) | Conf (50–60) |
|---|---|---|---|---|---|
| Luminal A-like | 26,3 % | **35,7 %** | ↓ etwas niedriger | HR+, HER2−, Ki-67 <14 % **und** PR+ | 🟡 |
| Luminal B-like HER2− | 42,8 % | **40,8 %** | ≈ unverändert | HR+, HER2−, Ki-67 ≥14 % **oder** PR− | 🟡 |
| Luminal B-like HER2+ | 14,3 % | **10,5 %** | ↑ etwas höher | HR+, HER2+ (Ki-67 beliebig) | 🟡 |
| HER2-enriched (nicht-luminal) | 4,3 % | **4,2 %** | ≈ unverändert | ER−, PR−, HER2+ | 🟡 |
| Triple-negativ | 12,2 % | **8,7 %** | ↑ etwas höher | ER−, PR−, HER2− | 🟡 |

**Quelle 50–69** — die TRM-Auswertung publiziert keine 50–59-Spalte 🔴. Die Drift-Spalte ist aus dem
<50-vs-50–69-Kontrast abgeleitet (TNBC RR 1,40, Luminal A 26,3 → 35,7 %) und zeigt nur die *Richtung*; die
Größe des Effekts im Fenster 50–60 ist unbekannt. **Startwert bleibt die 50–69-Spalte**; die Justierung ist
Aufgabe von `synthea-eu-cancer-0m8`. Ein plausibler erster Ansatz ist eine lineare Interpolation zwischen der
<50- und der 50–69-Marginale mit Gewicht ~0,25 auf der jüngeren Spalte (⇒ TNBC ~9,6 %, Luminal A ~33,4 %) 🔴 —
explizit als Modellprior zu kennzeichnen.

Einzelmarker zur Gegenprobe: ER+ **85,4 %**, PR+ 77,7 %, HER2+ **15 %** (bester nationaler Wert: Lacruz 2025,
Sci Rep, n=239.527, PMID 39920241) 🟢 (alle Alter). RKI KID 2025 nennt national ER+/PR+ 74 %, TNBC **10 %** 🟢.
Zum Alterseffekt gibt es einen belastbaren Extremwert als Plausibilitätsschranke: in Schweden liegt der
TNBC-Anteil bei <40-Jährigen bei **26 %** (Gkekos 2026, n=89.322) 🟢 — die Alterskurve ist also monoton und
steil, was die Drift-Richtung oben stützt.

> ⚠️ **Definitions-Artefakt — die wichtigste Fallstricknotiz dieses Kapitels.** Der Luminal-A-Anteil ist keine
> biologische Konstante, sondern schwankt vollständig mit der Definition: St. Gallen 2013 → **31,3 %** (TRM);
> nur Ki-67 ≥14 → **44,7 %** (Hennigs 2016, PMID 27634735); 4-Marker-IHC → **48,4 %** (Inwald 2015,
> PMID 26369534); Grading-Surrogat ohne Ki-67 → 56 % (NL) / 59 % (SE). **Erst die Definition festlegen, dann den
> Prior.** Eine populationsbezogene deutsche **PAM50**-Verteilung existiert nicht 🔴; alle Zahlen sind Surrogat-IHC.
> Die S3 warnt explizit, dass Surrogat ≠ intrinsischer Subtyp ist.

**Entscheidung:** St.-Gallen-2013-Definition mit **Ki-67-Cutoff 14 %** verwenden, weil nur dafür eine deutsche
populationsbezogene 5-Wege-Verteilung *und* die passenden Grading-/M1-Kreuztabellen vorliegen. Der Cutoff wird
als Modul-Konstante `bc_ki67_cutoff` dokumentiert. Wichtig für die Kalibrierungsdoku: die **S3 v5.1 weigert sich
ausdrücklich, einen Luminal-A/B-Cutoff zu definieren** („die Frage nach dem optimalen Grenzwert für Ki67 … [ist]
nicht beantwortet"); sie kennt nur >25 % = erhöhtes Rezidivrisiko und <10 % = niedriges Risiko (Statement 4.85) 🟢.
Die AGO 2026.1D nennt ebenfalls keinen Cutoff. Der IKWG-Standard 2021 lautet ≤5 % niedrig / ≥30 % hoch
(Nielsen 2021, PMID 33369635) 🟢. Der 14-%-Cutoff ist damit eine **bewusst gewählte, leitlinienfremde
Modellkonvention** — genau wie die PSA-4-Wahl im Prostata-Modul, und ebenso explizit zu kennzeichnen.

### 3.2 Design-Entscheidung: Subtyp ist *abgeleitet*, nicht primär

Beim Prostata-Modul ist die EAU-Risikogruppe die primäre latente Variable, und Gleason/PSA/cT werden aus ihr
gezogen. Für das Mammakarzinom wäre das falsch herum: der Subtyp **ist** definitionsgemäß eine Funktion von
ER/PR/HER2/Ki-67. Wenn das Modul den Subtyp zieht und die Marker unabhängig davon, entstehen inkonsistente
Bundles (z. B. „Luminal A" mit Ki-67 60 %), die jeder nachgelagerte Analyse-Use-Case sofort aufdeckt.

**Vorgehen (zweistufig, mit Konsistenz-Guard):**

1. `Subtype_Branch` zieht den Subtyp aus der Verteilung §3.1, **konditioniert auf `bc_detection_mode`**
   (Braun-2018-Spalten aus §1.3; die Marginale muss die in `synthea-eu-cancer-0m8` festgelegte
   50–60-Zielverteilung reproduzieren — Startwert ist die TRM-50–69-Spalte, §3.1. Das ist eine
   Kalibrieraufgabe, keine freie Wahl).
2. Je Subtyp-Ast werden ER-%, PR-%, HER2-IHC-Score und Ki-67-% aus subtyp-bedingten Verteilungen (§4.2) gezogen,
   **so parametrisiert, dass die St.-Gallen-2013-Regel den gezogenen Subtyp zurückgibt**.
3. Ein Validierungs-Check im Postprocessor (nicht im Modul) prüft die Rückrechnung auf allen Bundles und
   bricht bei Inkonsistenz ab — analog zum bestehenden `validate_ccdm.sh`-Gate.

### 3.3 DCIS als eigener Ast

> ✅ **ENTSCHIEDEN:** DCIS wird mitmodelliert. Dieser Ast ist verbindlich für v1 — er ist der Grund, warum der
> Screening-Arm überhaupt realistisch aussieht (18–26 % der screen-detektierten Fälle, §1.2a), und er ist
> billig: kein Systemtherapie-Baum, kein Rezidiv-Hazard nach Subtyp, ~15 Zustände.

DCIS ist **kein Subtyp**, sondern eine eigene Entität (`Tis`, ICD-O `/2`, ICD-10-GM D05.1) mit eigenem
Therapiepfad und ohne Systemtherapie. Anteil stark detektionsmodus-abhängig:

| Population | DCIS-Anteil | Quelle | Conf (50–60) |
|---|---|---|---|
| screen-detektiert, **Erstuntersuchung** | **22 %** | KoopMammo 2023 | 🟢 (nicht altersstratifiziert, aber Rundenart ist der dominante Faktor) |
| screen-detektiert, **reguläre Folgeuntersuchung** | **18 %** | ebd. | 🟢 |
| screen-detektiert (Münster) | 26,3 % | Braun 2018, Quelle 50–69 | 🟡 |
| Intervallkarzinome | 8,1 % | Braun 2018, Quelle 50–69 | 🟡 |
| Nicht-Teilnehmerinnen | 12,8 % | Braun 2018, Quelle 50–69 | 🟡 |
| alle deutschen Mamma-Neubildungen | ~8 % | RKI KID 2025 (alle Alter) | 🟢 |
| DKG-Zentren, Primärfälle | 9,6 % | OnkoZert JB 2025 (alle Alter) | 🟢 |

Weil in der 50–60-Kohorte jede Teilnehmerin die Erstrunde durchläuft (§1.2a), liegt der DCIS-Anteil im
Screening-Arm **am oberen Rand** dieser Spanne — die 22-%-Zeile ist für die frühen Runden der relevantere Wert.

Grading beim DCIS läuft über **Van Nuys / Kerngrading**, nicht Elston-Ellis: Kerngrad niedrig 11,6 % /
intermediär 26,1 % / hoch 33,3 % (TRM Tab. 25, 28,9 % ohne Angabe) 🟢.

---

## 4. Biomarker-Emission

### 4.1 Codes (aus SenologieOnFHIR übernommen, gegen CEIR-OS/LOINC 2.83 geprüft)

| Konzept | System | Code | Display (verifiziert) | Wert | Status |
|---|---|---|---|---|---|
| Östrogenrezeptor | LOINC | **40556-3** | Estrogen receptor Ag [Presence] in Tissue by Immune stain | LA6576-8 Positive / LA6577-6 Negative | 🟡 gegen Termserver prüfen |
| Progesteronrezeptor | LOINC | **85339-0** | *Progesterone receptor Ag [Presence] in **Breast cancer specimen** by Immune stain* | dito | 🟢 verifiziert (LOINC 2.83) — Achtung: SenologieOnFHIR gibt das Display abweichend an |
| HER2 (IHC) | LOINC | **48676-1** | HER2 [Interpretation] in Tissue | Leitlinien-Slice: positiv/`low`/`ultralow`/negativ/equivocal | 🟡 prüfen |
| HER2 IHC-Score | LOINC-Antwortcodes | LA26333-6 (1+), LA11841-6 (2+) | — | bzw. MII-MTB-CS `mii-cs-mtb-her2-ihc-score` 0/1/2/3 | 🟡 |
| HER2 ISH/FISH | LOINC-Panel | **74885-5** | (MII-MTB-Profil, via `Observation.hasMember`) | Ratio + Kopienzahl | 🟡 |
| **Ki-67-Proliferationsindex** | LOINC | **29593-1** | Cells.Ki-67 nuclear Ag/cells in Tissue by Immune stain | Quantity, `%` (UCUM) | 🟢 verifiziert (LOINC 2.83) |
| PD-L1 CPS / TPS | NCIt | **C176582** / **C184941** | PD-L1 Combined Positive Score / Tumor Proportion Score | Quantity `{score}` bzw. `%` | 🟡 |
| Grading | LOINC | **33732-9** | Histology grade [Identifier] in Cancer specimen | SNOMED 54102005 G1 / 1663004 G2 / 61026006 G3 | 🟡 |
| Genexpressions-Score | lokales BIH-CS | `cs-senologie-genexpressionstest#oncotype-dx` | — | Quantity 0–100 | ⚠ **lokales CodeSystem**, kein LOINC |
| Recurrence-Score-Risikoklasse | RiskAssessment | `risk-probability#low\|moderate\|high` | — | + `probabilityDecimal` | 🟢 |

⚠ **Lokale CodeSystems in SenologieOnFHIR**, die ein EU-Modul *nicht* übernehmen sollte, ohne die Lücke zu melden:
`cs-senologie-biomarker` (IRS-/Allred-Score), `cs-senologie-genexpressionstest`, `bildgebung-custom`,
`clinical-findings-custom`, `tumorboard-empfehlung`, `cs-senologie-follow-up`. Für ein EU-Datenmodell sind das
Kandidaten für Standardisierung — siehe §8.4.

### 4.2 Kohärente Marker-Sets je Subtyp

**Deutsche S3-Konvention für ER/PR** (Empfehlung 4.72, mod. 2025, wörtlich): Prozentsatz positiver Tumorzellkerne
**und** durchschnittliche Färbeintensität angeben; **negativ <1 % · gering positiv 1–10 % · positiv >10 %** 🟢.
Der **IRS nach Remmele/Stegner** ist in S3 v5.1 ausdrücklich als *optional und ohne klinische oder prognostische
Relevanz* eingestuft („lediglich historische Bedeutung") — er sollte also allenfalls als sekundäre Observation
emittiert werden, obwohl SenologieOnFHIR ihn prominent führt und die Beispielfälle ihn durchgängig benutzen 🟢.

**HER2** (S3 Empfehlung 4.73, GR A / EL 1): IHC-Score 0/1+/2+/3+ **und** den scoredefinierenden Prozentsatz
angeben; **Reflex-ISH bei jedem 2+** 🟢.

| Größe | Lum A | Lum B HER2− | Lum B HER2+ | HER2-enriched | TNBC | Conf |
|---|---|---|---|---|---|---|
| ER (%) | 80–100 (Modus ~90) | 60–100 | 50–100 | 0 (Tail 1–10 in ~2–3 %) | 0 (dito) | 🔴 |
| PR (%) | 50–95 | 0–60 (PR− in 30–40 %) | 0–70 | 0 | 0 | 🔴 |
| HER2 IHC | 0/1+ | 0/1+ | 3+ oder 2+/ISH+ | 3+ oder 2+/ISH+ | 0/1+ | 🟢 (Definition) |
| Ki-67 Median (IQR) | 10 (6–13) | 25 (18–35) | 30 (20–45) | 40 (25–55) | 60 (40–80) | 🔴 |
| Grading G1/G2/G3 | **31,5 / 65,9 / 2,7** | 7,2 / 69,7 / 22,9 | 2,9 / 52,8 / 44,3 | 0,8 / 34,0 / 65,2 | **1,4 / 25,4 / 73,2** | 🟢 (TRM 2016) |
| M1 bei Erstdiagnose | **2,6 %** | 7,2 % | 10,1 % | **13,2 %** | 6,0 % | 🟢 (TRM 2016) |

Kalibrier-Anker für die Ki-67-Priors (deutsche Marginalen, die reproduziert werden müssen): Mittelwert
**20,3 ± 18,1 %**, Median **15 %**, Bins <10 % 22,0 / 10–14 % 23,2 / 15–24 % 26,1 / ≥25 % 28,4 %
(Inwald 2013, Krebsregister Regensburg, n=3.658, PMID 23674192) 🟢; Ki-67 ≥14 % in **64,1 %** (TRM) 🟢;
G1/G2/G3-Mittelwerte 9,7 / 16,2 / 37,4 % 🟢. Eine Ki-67-Verteilung **pro Subtyp** ist in keiner deutschen
Quelle publiziert 🔴 — die Priors oben sind so gewählt, dass sie diese Marginalen und den 36/64-Split am
Cutoff 14 reproduzieren.

**HER2-IHC-Score-Verteilung:** keine deutsche Quelle 🔴. Bester Ersatz ist das dänische Nationalregister
(Nielsen 2023, n=48.382, PMC10636935): 0: 26,8 / 1+: 45,5 / 2+: 16,4 / 3+: 11,6 % 🟢, mit
**P(ISH+ | IHC 2+) = 0,144** 🟢. Vorschlag: auf den deutschen HER2+-Anteil von 15 % reskalieren →
**0: 26 %, 1+: 44 %, 2+: 17 %, 3+: 13 %**, P(ISH+|2+) = 0,15 🔴.
Robustheitswarnung aus derselben Quelle: der HER2-low-Anteil schwankte zwischen dänischen Pathologien von
**46,3 % bis 71,8 %** — Interlabor-Varianz ist hier größer als jeder Modellierungsfehler.

**HER2-low** (S3 v5.1 Tab. 30 nach Tarantino 2023): deutscher Nationalwert **42 %** aller BC
(Lacruz 2025, n=239.527), davon 91 % HR+ 🟢; **51,8 %** der HR+/HER2-negativen und **37,5 %** der TNBC 🟢.
HER2-ultralow hat keinen belastbaren deutschen Primärwert 🔴 → als *abgeleitetes* Attribut modellieren,
nicht als gezogene Größe.

---

## 5. TNM / Staging

### 5.1 cTNM bei Diagnose, konditioniert auf Detektionsmodus

Abgeleitet aus KoopMammo 2023 (Größen-/N-Klassen) kreuzgerechnet mit der TRM-pT-Feinverteilung
(≤10 mm auf T1a:T1b im Verhältnis 21:79; >20 mm auf T2:T3:T4 im Verhältnis 80:11:9):

| pT (invasiv, bekannte Größe) | screen-detektiert | symptomatisch | Conf |
|---|---|---|---|
| T1a | ~7,6 % | ~3,2 % | 🟡 abgeleitet |
| T1b | ~28,8 % | ~11,9 % | 🟡 |
| T1c | ~45,0 % | ~37,6 % | 🟡 |
| **T1 gesamt** | **~81 %** | **~53 %** | 🟡 |
| T2 | ~14,9 % | ~37,7 % | 🟡 |
| T3 | ~2,1 % | ~5,1 % | 🟡 |
| T4 | ~1,8 % | ~4,5 % | 🟡 |

Nodalstatus: **N0 / N+ = 75,5 / 23,4 %** (screen), **59,9 / 32,0 %** (Intervall), **61,3 / 30,7 %**
(symptomatisch) — Braun 2018, **Quelle 50–69** 🟡. Die N+-Fälle werden mit der TRM-Marginalen
**N1 : N2 : N3 = 70 : 19 : 11** aufgeteilt 🔴 (kein detektionsmodus- und kein altersspezifischer Split publiziert).

UICC-Gesamtstadium zur Gegenprobe (RKI KID 2025, gültige Werte, Frauen **50–69**): **I 51 / II 35 / III 7 / IV 7 %**
— **Quelle 50–69**, RKI stratifiziert nicht feiner 🟡. Richtung für 50–60: der Stadienmix wird durch die
Erstrunden-Spitze (§1.2a: UICC II+ 26 % statt 21 %) leicht **ungünstiger** als die 50–69-Marginale.
Registry-Realismus: **26 % der deutschen C50-Fälle haben unbekanntes UICC-Stadium** 🟢 — optional als
`dataAbsentReason`-Variante emittierbar, wenn Registerdaten nachgebildet werden sollen.

**De-novo-M1 — hier existiert eine echte 50–59-Zahl:** TRM (n=60.479) berichtet pM1 bei Erstdiagnose für
**50–59 J.: 6,2 %** und 60–69 J.: 7,2 % 🟢. Für die 50–60-Kohorte ist damit **6,2 %** der belegte Wert
(statt der 7 % aus dem RKI-50–69-Band 🟡). Da das MSP kein M-Staging vornimmt und screen-detektierte Karzinome
praktisch nie M1 sind, folgt bedingt auf „nicht screen-detektiert" ein M1-Anteil von **~11 %** 🔴
(6,2 % / 0,55 Nicht-Screening-Anteil). Metastasenlokalisation bei Erstmanifestation hat **keine
deutsche/europäische Tabelle** 🔴; SEER-Prior: Knochen 50,7 / Lunge 23,9 / Leber 19,7 / Hirn 5,7 % 🟢 (US),
subtypabhängig (TNBC lungenbetont, HER2+ leber-/hirnbetont).

### 5.2 pTNM nach Operation, Sentinel vs. Axilladissektion

Anders als beim Prostata-Modul ist der pN-Status **nicht optional**: fast jede invasive Patientin bekommt eine
axilläre Diagnostik. DKG-Kennzahlen 2023 🟢:

| Arrow | Wert | Basis | Conf |
|---|---|---|---|
| pN0-Patientinnen mit **SLNB allein** (ohne präoperative Systemtherapie) | **0.931** | OnkoZert KZ 20a (26.156/28.098; Soll ≥80 %) | 🟢 |
| ⇒ ALND (oder SLNB+ALND) bei pN0 | 0.069 | abgeleitet | 🟢 |
| Nodalstatus überhaupt bestimmt (invasiv) | 0.966 | OnkoZert KZ 19 | 🟢 |
| Axilläre LK-Entfernung bei DCIS (soll vermieden werden) | 0.025 | OnkoZert KZ 18 | 🟢 |
| Axilläre Therapie bei pN1mi (soll vermieden werden) | 0.073 | OnkoZert KZ 23 | 🟢 |

Staging-Guardrails (analog zur „kein pT1 beim Prostata-Ca"-Notiz): pN erfordert eine Lymphknoten-Entnahme;
`(sn)`-Suffix nur nach Sentinel-Biopsie (SNOMED hat dafür eigene Werte, §5.4); DCIS ist **pTis(DCIS)**, nie pT1;
nach neoadjuvanter Therapie sind **alle** Kategorien mit `y` zu präfigieren, auch die klinischen.

### 5.3 ypTNM und pCR — der strukturell neue Teil

Das Prostata-Modul kennt keine Neoadjuvanz. Für das Mammakarzinom ist sie tragend (§6.2) und braucht eine
eigene Staging-Emission: **pCR = ypT0 ypN0**. SNOMED hält die vollständige `yp`-Hierarchie bereit (verifiziert,
SNOMED INT 20260501) — u. a. **ypT0 1352650002**, **ypTis(DCIS) 1352633004**, **ypN0 1352797005**. Damit ist
sowohl `ypT0 ypN0` (strenge pCR) als auch `ypT0/is ypN0` (weiche pCR) sauber kodierbar; das Modul sollte die
**strenge** Definition verwenden (bessere prognostische Trennschärfe: HR(DFS) 0,446 vs. 0,523).

### 5.4 Emissionscodes (SNOMED UICC-8, alle verifiziert gegen SNOMED INT 20260501)

**Wichtigster Terminologie-Befund dieses Konzepts:** die im Prostata-Modul verwendeten SNOMED-Werte sind
**nicht organspezifisch** — `1352973007` hat den FSN *"Union for International Cancer Control cT1c
(qualifier value)"*. Die gesamte UICC-Wertehierarchie ist damit **ohne Änderung wiederverwendbar**; für das
Mammakarzinom kommen nur zusätzliche Kategorien hinzu. Kategorie-Observations (LOINC 21905-5 cT, 21906-3 cN,
21907-1 cM, 21899-0 pT, 21900-6 pN) bleiben unverändert.

| cT | Code | | cN | Code | | pT | Code | | pN | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| cTis(DCIS) | 1352965003 | | cN0 | 1353041009 | | pTis(DCIS) | 1352535003 | | pN0 | 1352621009 |
| cT1mi | 1352979006 | | cN0(sn) | 1356757005 | | pT1mi | 1352562006 | | pN0(i+) | 1352624001 |
| cT1a | 1352983006 | | cN1 | 1353043007 | | pT1a | 1352560003 | | pN1mi | 1352620005 |
| cT1b | 1352968001 | | cN1mi | 1353045000 | | pT1b | 1352543008 | | pN1a | 1352619004 |
| cT1c | 1352973007 | | cN2a | 1353050006 | | pT1c | 1352537006 | | pN1a(sn) | 1352615005 |
| cT2 | 1352993004 | | cN2b | 1353055001 | | pT2 | 1352545001 | | pN2a | 1352608002 |
| cT3 | 1352966002 | | cN3a | 1353057009 | | pT3 | 1352533005 | | pN3a | 1352618007 |
| cT4b | 1352960008 | | cN3b | 1353054002 | | pT4b | 1352561004 | | pN3b | 1352623007 |
| cT4d (inflammatorisch) | 1352963005 | | cN3c | 1353051005 | | pT4d | 1352557005 | | pN3c | 1352606003 |
| cM0 / cM1 | 1352512001 / **1352513006** | | | | | | | | |

`yp`-Kategorien (neoadjuvant): **ypT0 1352650002**, ypTis(DCIS) 1352633004, ypT1mi 1352637003,
ypT1a 1352644007, ypT1b 1352639000, ypT1c 1352641004, ypT2 1352635006, ypT3 1352657004, ypT4 1352649002;
**ypN0 1352797005**, ypN0(i+) 1352798000, ypN1mi 1352796001, ypN1a 1352795002, ypN2a 1352805002,
ypN3a 1352804003.

Beachte: der Prostata-Pfad nutzt `cM1a/b/c`; für das Mammakarzinom ist **cM1 (1352513006)** ohne Subkategorie
korrekt — UICC 8 kennt beim Mamma-Ca keine M1-Untergliederung.

### 5.5 Histologie (ICD-O-3 + SNOMED-Morphologie)

WHO-konformer Prior (TRM-Rohdaten mit der deutschen Kodierpraxis korrigiert — deutsche Register kodieren
gemischte/spezielle Karzinome überwiegend als 8500/3 und blähen NST dadurch auf ~80 % auf) 🔴:

| Morphologie | ICD-O-3 | Anteil (invasiv) | deutscher Registerwert (TRM ≥2007, renormiert) | Conf |
|---|---|---|---|---|
| Invasives Karzinom NST | **8500/3** | ~73 % | 80,6 % | 🟢 (Register) / 🔴 (WHO-Korrektur) |
| Invasiv-lobulär | **8520/3** | ~12 % | 13,5 % | 🟢 |
| Gemischt duktal-lobulär | 8522/3 | ~6 % | (in NST enthalten) | 🔴 |
| Muzinös | 8480/3 | ~2 % | 1,5 % (rein) | 🟢 |
| Tubulär | 8211/3 | ~1,5 % | 1,1 % (rein) | 🟢 |
| **DCIS** | **8500/2** | (eigener Ast, §3.3) | ~85–95 % aller In-situ-Fälle | 🟡 |
| LCIS | 8520/2 | (eigener Ast) | ~5–15 % aller In-situ-Fälle | 🟡 |

SNOMED-Morphologien für `observation-histology-behaviour-eu-ccm` (aus SenologieOnFHIR VS
`vs-senologie-histologie-typ`): invasives Ca NST **82711006**, invasiv-lobuläres Ca **443451005**,
DCIS **109889007** 🟡 — vor Modulbau gegen den Termserver validieren, analog zur Prostata-Notiz zum
inaktivierten 35917007.

Condition-Codes: SNOMED **254837009** *Malignant neoplasm of breast*, DCIS **109889007**; ICD-10-GM C50.0–C50.9
bzw. **D05.1** (DCIS) / D05.0 (LCIS) 🟡.

---

## 6. Therapiepfade

### 6.1 Lokale Therapie

| Arrow | Wert | Basis | Conf |
|---|---|---|---|
| BET bei **cT1N0M0** | **0.862** | OnkoZert JB 2025 (n=25.753) | 🟢 |
| BET bei **cT2N0M0** | **0.705** | ebd. (n=11.856) | 🟢 |
| BET bei cT3N0M0 / cT4N0M0 | 0.311 / 0.272 | ebd. | 🟢 |
| BET bei **N+ (jedes T) M0** | **0.575** | ebd. (n=14.448) | 🟢 |
| BET bei **DCIS** | **0.793** | ebd. (n=6.824) | 🟢 |
| BET bei M1 | 0.361 | ebd. | 🟢 |
| BET gesamt (operierte Fälle) | 0.737 | ebd. | 🟢 |
| **Radiatio nach BET, invasiv** | **0.978** | OnkoZert KZ 4 (LL-QI) | 🟢 |
| **Radiatio nach BET, DCIS** | **0.784** | OnkoZert KZ 5 | 🟢 |
| Primärfälle **nicht operiert** | 0.161 gesamt (M1: 0.846; cT1N0M0: 0.072) | OnkoZert JB 2025 | 🟢 |
| Revisionsoperation | 0.024 | OnkoZert KZ 22 | 🟢 |

**Design-Entscheidung:** die BET-Wahrscheinlichkeit **auf das Stadium konditionieren, nicht aufs Alter** — der
Alterseffekt ist klein (50–69: 75,8 % gegen 69,6 % über alle Alter, Heinig 2022, PMID 35109813) 🟡, der
Stadieneffekt dagegen groß (86 % → 27 %). Damit ist auch die Verschmälerung auf 50–60 unkritisch: die
OnkoZert-Kennzahlen sind zwar **nicht altersstratifiziert** (alle Alter, 96,9 % weiblich) 🟡, aber weil das
Modul über das Stadium konditioniert und der Stadienmix altersband-korrekt gezogen wird (§5.1), trägt sich der
Alterseffekt implizit durch. Das ist der Grund, die Kennzahlen stadien- und nicht altersbezogen anzusetzen.

Bestrahlung: Zielvolumina aus SenologieOnFHIR (`vs-senologie-rt-zielvolumen`, SNOMED): ganze Brust 76752008,
Thoraxwand 78904004, axilläre LK 68171009, supraklavikuläre LK 76838003, parasternale LK 245282001 🟡.
Typische Dosis 50 Gy + 10–16 Gy Boost (aus den Senologie-Beispielfällen); moderne Hypofraktionierung
40 Gy / 2,5 Gy Einzeldosis ist im OncoBox-Testfall belegt.

### 6.2 Neoadjuvanz und pCR-Branch

Anteil neoadjuvant behandelter Patientinnen, **alle Primärfälle 2023: 21,4 %** (OnkoZert) 🟢; nach klinischem
Stadium cT1N0M0 18,9 / cT2N0M0 32,7 / N+M0 29,5 % 🟢. Nach Subtyp liegt nur eine ältere deutsche
Realwelt-Auswertung vor (Ortmann 2022, 55 DKG-Zentren, 2007–2018, n=94.638) 🟢: TNBC 31,8 %, HR−/HER2+ 31,9 %,
HR+/HER2+ 26,5 %, HR+/HER2− 5,8 % — bei einer damaligen Gesamtrate von 11,0 %, die sich seither auf 21,4 %
verdoppelt hat.

⚠️ **Ära-Vorbehalt.** Diese Subtyp-Anteile reproduzieren die heutige Gesamtrate nicht. Vorgeschlagene
Reskalierung auf 2023 (post-KEYNOTE-522 / post-KATHERINE), so gewählt, dass sie gewichtet mit den deutschen
Subtyp-Prävalenzen die beobachteten 21,4 % ergibt: **TNBC 60–70 %, HR−/HER2+ ~60 %, HR+/HER2+ 45–50 %,
HR+/HER2− ~10 %** 🔴. Das ist der wichtigste rote Arrow im Therapieteil.

pCR-Raten (ypT0 ypN0), deutsche Realwelt (Ortmann 2022) 🟢: HR+/HER2− **12 %**, HR+/HER2+ **36 %**,
HR−/HER2+ **53 %**, TNBC **38 %**. Moderne Regime-Anker: KEYNOTE-522 (TNBC + Pembrolizumab) **64,8 %** 🟢,
NeoSphere (HER2+, Docetaxel+Trastuzumab+Pertuzumab) **45,8 %** 🟢, GeparOcto TNBC 48,5/51,7 % 🟢.
Vorschlag als Modellprior 🔴: TNBC **60 %** (Pembro-Backbone) bzw. 38 % (nur Chemo), HER2+/HR− 60 %,
HER2+/HR+ 40 %, Luminal B HER2− 12 %, Luminal A 6 %.

Prognostische Nuance, die das Modul abbilden sollte (von Minckwitz 2012, PMID 22508812, n=6.377): pCR ist
prognostisch bei Luminal B/HER2−, HER2+ nicht-luminal und TNBC — **nicht** bei Luminal A (p=0,39) und nicht bei
Luminal B/HER2+ (p=0,45) 🟢. Der pCR-Zustand darf also nur in den ersten drei Ästen auf den Rezidiv-Hazard wirken.

**Post-neoadjuvante Eskalation:** HER2+ mit Resttumor → T-DM1 (KATHERINE: 3-J-iDFS 88,3 % vs. 77,0 %,
HR 0,50) 🟢; TNBC mit Resttumor → Capecitabin bzw. Olaparib bei gBRCA. Anteil der HER2+ mit Resttumor
= 1 − pCR ≈ 40–50 % 🔴.

### 6.3 Systemtherapie je Subtyp

| Subtyp | Rückgrat | Anker | Conf |
|---|---|---|---|
| **Luminal A** | endokrin 5(–10) J., Chemo nur ausnahmsweise; Genexpressionstest als Entscheidungshilfe | ET-Empfehlung bei HR+ **96,8 %** (OnkoZert KZ 7) | 🟢 |
| **Luminal B HER2−** | endokrin + Chemo bei N+/hohem Risiko; CDK4/6 adjuvant bei monarchE-Kriterien | Chemo bei HR+ **und** N+: **60,8 %** (OnkoZert KZ 6) | 🟢 |
| **Luminal B HER2+** | Chemo + duale HER2-Blockade + endokrin | Trastuzumab ≥1 J. bei HER2+ ≥pT1c: **95,0 %** (KZ 8) | 🟢 |
| **HER2-enriched** | (neo)adjuvante Chemo + Trastuzumab/Pertuzumab, ggf. T-DM1 | dito | 🟢 |
| **TNBC** | neoadjuvante Platin-/Taxan-Chemo + Pembrolizumab (bei CPS≥10 bzw. Stadium II/III), Olaparib bei gBRCA | KEYNOTE-522 | 🟢 |
| **DCIS** | keine Systemtherapie; Tamoxifen optional bei ER+ | S3 | 🟢 |

Endokrine Details: **AI 54,9 % vs. Tamoxifen 45,1 %** bei Therapiebeginn in Deutschland über alle Alter
(Jacob/Kostev 2023, IQVIA LRx, n=284.383, PMID 36149512) 🟢. Die Mittelwerte der beiden Gruppen (AI 69,0 J.,
TAM 59,1 J.) zeigen die starke Altersabhängigkeit — und weisen darauf hin, dass die **50–60-Kohorte deutlich
Tamoxifen-lastiger** ist als eine 50–69-Kohorte: der TAM-Mittelwert von 59,1 J. liegt mitten im Fenster.
Der zuvor für 50–69 vorgeschlagene Split AI 75–85 % ist für 50–60 daher zu AI-lastig; Vorschlag **AI ~55–65 % /
TAM ~35–45 %** 🔴, zusätzlich konditioniert auf den Menopausenstatus (im Fenster 50–60 sind nicht alle Frauen
postmenopausal — Tamoxifen bzw. AI+GnRH ist dort die leitliniengerechte Wahl). **Persistenz nach 5 Jahren (90-Tage-Lücke):
AI 35,1 %, TAM 32,5 %** 🟢 — das ist ein schön modellierbarer Abbruch-Pfad, den kein anderes synthetisches
Mamma-Dataset abbildet, und er ist direkt aus deutschen Verordnungsdaten belegt.

CDK4/6-Inhibitoren im metastasierten HR+/HER2−-Setting: 38,5 % → 62,7 % in den ersten zwei Jahren nach
Zulassung (PRAEGNANT-Register, Fasching 2020, PMID 32956934) 🟢; für 2023 extrapoliert ~80–85 % 🔴.
Adjuvant (monarchE-Kriterien) betrifft ~13 % der HR+/HER2−-Frühfälle (dänische DBCG-Kohorte) 🟡 —
kein deutscher Wert 🔴.

Genexpressionstest: seit **20.06.2019** ist Oncotype DX für HR+/HER2−, nodal-negativ GKV-erstattet 🟢;
die tatsächliche Nutzung liegt laut Experteneinschätzung bei **~20 % der Berechtigten** 🟡 — es gibt keine
publizierte deutsche Nutzungsstudie 🔴, u. a. weil der Test **nicht** unter den 23 DKG-Qualitätsindikatoren ist 🟢.

---

## 7. Rezidiv und Metastasierung (Analogon zu BCR → Salvage)

Beim Prostata-Modul ist der PSA-Anstieg ein sauberer, laborgetriebener Trigger. Beim Mammakarzinom gibt es kein
Analogon — das Rezidiv wird direkt als Hazard gezogen, **subtypabhängig in Höhe *und Form***. Das ist der
strukturell interessanteste Teil des Moduls.

> ⚠️ **Fensterabhängigkeit — siehe §1.2d.** In einer 50–60-Kohorte entfaltet sich nur der *frühe* Teil dieser
> Hazard-Kurven. Eine mit 52 diagnostizierte Frau erreicht ~8 Nachbeobachtungsjahre, eine mit 58 diagnostizierte
> nur ~2. Der TNBC-Gipfel bei 2–3 Jahren fällt fast immer ins Fenster, der luminale Spättail (Jahre 5–20)
> praktisch nie. Die Zahlen unten sind trotzdem vollständig anzugeben — sie kalibrieren die Hazard-*Funktion*,
> aus der Synthea nur das im Fenster liegende Stück zieht.

| Größe | Wert | Basis | Conf |
|---|---|---|---|
| Lokalrezidiv, deutsche Population (kumulative Inzidenz, Tod konkurrierend) | **5,2 % @5J / 8,2 % @10J**; regionär nodal 2,2 / 3,2 % ⇒ locoregionär ≈7,4 / 11,4 % | TRM Survival C50, Tab. 5b (n=58.903, 1998–2020) | 🟢 |
| Fernmetastasierung (M0 bei Diagnose) | **11,0 % @5J / 16,6 % @10J / 19,4 % @15J** | ebd. | 🟢 |
| jede Progression | 16,3 / 24,0 / 28,7 % | ebd. | 🟢 |
| Rezidiv-Hazard ER+ vs ER−, Jahre 0–5 | 9,9 %/J vs 11,5 %/J | Colleoni 2016, IBCSG I–V, PMID 26786933 | 🟢 (Ära-Vorbehalt) |
| Jahre 5–10 / 10–15 | ER+ 5,4 / 2,9 %/J; ER− 3,3 / 1,3 %/J | ebd. | 🟢 |
| **TNBC-Hazard-Form** | Gipfel bei ~3 J., danach steiler Abfall; kaum Rezidive nach ~8 J. | Dent 2007, PMID 17671126 | 🟢 |
| ER+-Hazard-Form | konstanter Spättail 1–2 %/J über 20 J. hinaus | Pan 2017, NEJM, PMID 29117498 (88 Studien, 62.923 Frauen) | 🟢 |
| ER+ Fernrezidiv Jahre 5–20, nach Stadium | T1N0 **13 %** · T1N1-3 20 % · T2N0 19 % · T2N1-3 26 % · T1N4-9 34 % | ebd. | 🟢 |
| Überleben **nach** Fernmetastasierung (modern, DE) | 1-J 69,3 % · 2-J 52,2 % · **5-J 23,8 %** · 10-J 10,7 % | TRM Survival Tab. 5f (n=8.811, ≥2007) | 🟢 |
| Medianes Überleben nach Metastasierung je Subtyp | Lum A 2,2 J · Lum B 1,6 J · Lum/HER2 1,3 J · HER2-enriched 0,7 J · basal 0,5 J | Kennecke 2010, PMID 20498394 | 🟢 (alte Kohorte) |
| Kontralaterales Mamma-Ca, BRCA1 @10J | 25,1 % (BRCA2 6,6 %, Nicht-Trägerinnen 4,6 %) | Engel 2020, PMID 31081934 | 🟢 |

**Vorgeschlagene Hazard-Formen** 🔴 (aus Colleoni + Pan + Dent synthetisiert): TNBC — Weibull mit Gipfel
2–3 J. bei ~8–10 %/J, <2 %/J ab J. 5, <1 %/J ab J. 8 · Luminal A — ~1,5–2 %/J flach bis J. 20 ·
Luminal B — ~3–4 %/J J. 0–5, ~2,5 %/J J. 5–15 · HER2+ (behandelt) — ~4 %/J J. 0–5, ~1,5 %/J danach.

Synthea kann keine kontinuierlichen Hazards; die Umsetzung ist eine **`Delay` + `complex_transition`-Schleife
mit stückweise konstanten Jahresraten je Subtyp** — dieselbe Mechanik wie `PSA_Followup` → `BCR_Check`, nur
mit mehreren Zeitfenstern. Das ist der Grund, warum das Modul deutlich mehr Zustände braucht als das
Prostata-Modul (§9).

Überlebens-Validierungsanker (nicht als Arrows kodiert): 5-J-relatives Überleben nach UICC-Stadium
**I 101 % · II 95 % · III 76 % · IV 31 %** (RKI KID 2025) 🟢; nach pTNM (TRM, 5-/10-J):
pT1N0M0 100,8/98,7 · pT2N0M0 95,4/88,2 · pT1N+M0 94,8/86,6 · pT2N+M0 85,3/71,3 · M1 28,3/13,7 🟢.
National: 5-J 88 %, 10-J 83 %, medianes Erkrankungsalter 65 J. 🟢.

**Altersband-spezifische Anker (RKI/TRM liefern hier 50–59 direkt)** — die richtigen Zielwerte für die
Kohorten-Validierung in `synthea-eu-cancer-6r8`: 5-J-relatives Überleben **50–59 J.: 92 %** (60–69: 90 %,
RKI KID 2025) 🟢; 15-J-relatives Überleben **50–59 J.: 80,7 %** (TRM Survival Tab. 3c) 🟢. Die generierte Kohorte
muss gegen **92 %** validiert werden, nicht gegen die 88 % des nationalen Alle-Alter-Werts.

---

## 8. Mapping: SenologieOnFHIR ↔ ECCDM ↔ Synthea-Emission

### 8.1 Abgedeckt (ECCDM-Profil vorhanden, Postprocessor erweiterbar)

| Datenelement | SenologieOnFHIR-Profil | ECCDM-Profil | Synthea muss emittieren |
|---|---|---|---|
| Diagnose | `senologie-diagnose-maligne` (SCT 254837009 + ICD-10-GM + ICD-11) | `cancer-condition-at-diagnosis-eu-ccm` | `ConditionOnset` SCT 254837009 / 109889007 + bodySite Brust |
| Histologie | `senologie-pathologie-befund` (LOINC 60568-3) | `observation-histology-behaviour-eu-ccm` | Observation LOINC 59847-4, value = ICD-O + SCT-Morphologie |
| cTNM | MII `mii-pr-onko-tnm-klassifikation` (in Senologie nur als `Condition.stage.summary` **Freitext**!) | `observation-cancer-stage-eu-ccm` (clinical) | LOINC 21905-5/21906-3/21907-1 + SCT-UICC-Werte (§5.4) |
| pTNM / ypTNM | dito | `observation-cancer-stage-eu-ccm` (pathological) | LOINC 21899-0/21900-6 + SCT-UICC-`p`/`yp`-Werte |
| Brust-OP | `senologie-operation` (SCT-Kategorie + **OPS**-Code) | `procedure-surgery-eu-ccm` | Procedure + `surgery-intent` + bodySite (Profil fordert bodySite 1..1) |
| Strahlentherapie | `senologie-strahlentherapie` (OPS 8-522.x) | `episode-of-care-radiotherapy-eu-ccm` | Procedure SCT 1287742003 → EOC im Postprocessor |
| Systemtherapie | `senologie-systemtherapie-procedure` + `-medikation` | `episode-of-care-systematic-treatment-eu-ccm` | MedicationRequests (ATC, dual-kodiert WHO + ATC-DE) → EOC |
| Rezidiv / Progression | `senologie-follow-up` (SCT 396432002 + MII-Verlaufs-CS) | `observation-clinical-cancer-progression-eu-ccm` | Rezidiv-`ConditionOnset` → Progression-Observation |
| Follow-up / Vitalstatus | `senologie-follow-up`, `Patient.deceased[x]` | `observation-last-follow-up-eu-ccm` | bereits generisch im Postprocessor |

### 8.2 SenologieOnFHIR-Elemente ohne ECCDM-Entsprechung — **die Lückenliste**

| Datenelement | SenologieOnFHIR | ECCDM | Bewertung |
|---|---|---|---|
| **ER-Status** | `senologie-er-status` (LOINC 40556-3) | ✗ **kein Biomarker-Profil** | ⛔ **Hauptlücke.** Ohne Rezeptorstatus ist ein Mamma-Datensatz im ECCDM klinisch nicht interpretierbar |
| **PR-Status** | `senologie-pr-status` (LOINC 85339-0) | ✗ | ⛔ dito |
| **HER2-Status + IHC-Score + ISH** | `senologie-her2-status` (LOINC 48676-1, ISH via MII-MTB-Panel 74885-5) | ✗ | ⛔ dito; therapiedeterminierend |
| **Ki-67** | `senologie-ki67-proliferationsindex` (LOINC 29593-1) | ✗ | ⛔ subtypdefinierend |
| **PD-L1** | `senologie-pdl1-status` (NCIt CPS/TPS) | ✗ | ⚠ prädiktiv für Immuntherapie |
| **Grading** | MII `MII_PR_Onko_Grading` (LOINC 33732-9) | ✗ (nur Histologie/Behaviour) | ⚠ Grading ist in *jedem* Register Pflichtfeld |
| **Genexpressionstest + Recurrence Score** | `senologie-genexpressions-score` + `-genexpressionstest` (RiskAssessment) | ✗ | ⚠ steuert die Chemo-Entscheidung |
| **Tumorboard-Empfehlung** | `senologie-tumorboard-empfehlung` (CarePlan, 12 activity-Slices) | ✗ | ⚠ zentraler Prozessschritt; für Process Mining wertvoll |
| **Nebenwirkung** | `senologie-nebenwirkung` (AdverseEvent, MedDRA + CTCAE) | ✗ | ⚠ |
| **Erbliche Belastung / Checkliste** | `senologie-checkliste-erbliche-belastung` (SCT 445039002) + FamilyMemberHistory | ✗ | ⚠ Einstieg in den Hochrisiko-Arm |
| **Neoadjuvanz / `yp`-Staging** | über MII-TNM abbildbar | ⚠ Profil vorhanden, aber **keine Aussage zu `y`-Präfix** | ⚠ Dokumentationslücke |
| **Seitenlokalisation / bilateral** | `senologie-tumorlokalisation` (BodyStructure, Quadrant, Uhrzeit) | ⚠ nur `bodySite` | ⚠ synchron bilateral = 3,04 % der Fälle (OnkoZert) |

**Empfehlung:** die Zeilen mit ⛔ als konkretes Feedback ans ECCDM-Team formulieren, im gleichen Stil und in
derselben Datei wie `docs/eccdm_draft_feedback.md`, mit dem bereits etablierten Angebot, die generierten Bundles
als IG-Beispiele beizusteuern. Das Argument ist stark: das ECCDM ist tumorartübergreifend, aber vier der fünf
Mamma-Subtypen sind ohne Biomarker-Observations schlicht nicht darstellbar — und dieselbe Lücke trifft
Lungen-Ca (EGFR/ALK/PD-L1) und Kolorektal-Ca (RAS/BRAF/MSI) genauso. Ein generisches
`observation-tumor-biomarker-eu-ccm` (Code aus einem LOINC-basierten VS, Wert ordinal + optionale
quantitative Komponente) würde alle drei auf einmal lösen.

### 8.3 Was der Postprocessor braucht

`scripts/postprocess_ccdm.py` ist heute prostata-hartverdrahtet: `PCA_CODE`, `RP_CODE`, `EBRT_CODES`,
`ADT_ATC` etc. sind Modulkonstanten, und `find_cancer_condition()` sucht genau eine SNOMED-Nummer.
Erforderlicher Umbau (AP-P):

1. **Entitäts-Registry** statt Konstanten: ein Dict pro Tumorentität (Condition-Code, bodySite, Surgery-Codes,
   RT-Codes, Systemtherapie-ATC-Gruppen, Rezidiv-Code), Auswahl per CLI-Flag oder Autodetektion.
2. **Stage-Emission um `yp` erweitern** — heute unterscheidet `stage_obs()` nur clinical/pathological über die
   `CinicalorPathological`-Extension; das `y`-Präfix steckt nur im Wertcode. Zusätzlich muss die
   `EvidenceReference` bei ypTNM auf die **Post-Neoadjuvanz-OP** zeigen.
3. **Biomarker-Passthrough** — ✅ **ENTSCHIEDEN, so umsetzen:**
   - **ER, PR, HER2, Ki-67 und Grading** werden als **unprofilierte LOINC-Observations** emittiert
     (40556-3 / 85339-0 / 48676-1 / 29593-1 / 33732-9, §4.1) — korrekt kodiert, aber **ohne `meta.profile`**.
     Sie bleiben im Bundle, werden nicht gelöscht und nicht auf ein Fremdprofil gezwungen.
   - **TNM wird voll ECCDM-profiliert** (`observation-cancer-stage-eu-ccm`, clinical/pathological/`yp`) — dort
     existiert ein Profil, dort wird es genutzt.
   - **Kein SenologieOnFHIR-Tagging in v1.** Die Senologie-Profile werden als *fachliche Blaupause* für die
     Codeauswahl verwendet, aber **nicht** als `meta.profile` gesetzt: das IG hängt an MII-KDS-Abhängigkeiten
     (Onkologie 2026.0.3, Patho, MTB, ISiK) und an 12+ lokalen BIH-CodeSystems (§8.4), die ein
     EU-CCDM-Datensatz nicht mitschleppen soll. Ein Senologie-Konformitätslauf wäre ein eigenes Projekt.
   - Das **Validierungs-Gate darf daran nicht scheitern**: `validate_ccdm.sh` prüft nur profilierte Ressourcen;
     die unprofilierten Biomarker-Observations müssen die Basis-FHIR-Validierung bestehen, mehr nicht.
   - Die Lücke geht als **Feedback ans Phoenix-Team** (AP-F, §8.2) — mit dem Vorschlag eines generischen
     `observation-tumor-biomarker-eu-ccm`. Sobald ein solches Profil existiert, ist der Umbau ein Einzeiler
     pro Observation, weil die Codes dann bereits stimmen. **Das ist der eigentliche Grund für diese
     Entscheidung:** korrekt kodiert und unprofiliert ist die einzige Variante, die später ohne Datenmigration
     nachprofiliert werden kann.
4. **Bilaterale Fälle**: `find_cancer_condition()` gibt heute die *erste* Condition zurück. Für synchron
   bilaterale Karzinome (3 %) müssen zwei unabhängige Journeys pro Patientin zusammengeführt werden —
   oder bilateral wird in v1 bewusst ausgeschlossen (Empfehlung: **ausschließen**, als bekannte Einschränkung
   dokumentieren, in v2 nachziehen).

### 8.4 Terminologische Vorarbeit

SenologieOnFHIR mischt Standard-Terminologien mit **12+ lokalen BIH-CodeSystems**. Für ein EU-Modul gilt:
lokale Codes **nicht** übernehmen, sondern (a) einen Standardcode suchen, (b) wenn keiner existiert, das
Element in v1 weglassen und als Standardisierungsbedarf melden. Das ist die terminologische Kehrseite der
Entscheidung aus §8.3 Punkt 3: **Senologie ist Blaupause, nicht Zielprofil** — wir übernehmen die
LOINC-/SNOMED-Codeauswahl, aber weder die lokalen CodeSystems noch die `meta.profile`-Kanonicals. Betroffen sind vor allem der
Genexpressionstest-Typ, die Tumorboard-Beschlusszustände, IRS/Allred und die Nachsorge-Art.
Positiv: SenologieOnFHIR liefert 10 ConceptMaps (SCT→oBDS, SCT→ICD-O-3-Topographie, Medikation SCT→ATC/ASK)
und 12 SQL-on-FHIR-ViewDefinitions, die als Validierungswerkzeug direkt nachnutzbar sind.

---

## 9. Modulgröße und Zustandsökonomie

Das Prostata-Modul hat 167 Zustände bei **einer** Stratifizierungsachse (5 Risikogruppen). Das Mamma-Modul hat
**zwei orthogonale Achsen** (3 Detektionsmodi × 5 Subtypen) plus den DCIS-Ast (§3.3, entschieden) und den
schlanken Hochrisiko-Arm (§1.4.1, entschieden). Naiv ausmultipliziert wären das >500 Zustände — nicht wartbar.

**Gegenmaßnahmen:**

- Detektionsmodus als **Attribut** (`bc_detection_mode`) setzen, nicht als Zustandskette duplizieren; die
  Konditionierung erfolgt über `complex_transition` an den vier Stellen, wo sie wirkt (Subtyp-Branch, cT-Split,
  cN-Split, Grading).
- Ebenso die Screening-Rundenart (`msp_round_index`, §1.2a): Erst- und Folgeuntersuchung unterscheiden sich nur
  in vier Zahlen (Recall, CDR, DCIS-Anteil, Stadienmix) — das ist ein `complex_transition` auf einem Attribut,
  **keine zweite Zustandskette**. Die Screening-Schleife selbst bleibt damit bei ~10 Zuständen, obwohl sie im
  Fenster 50–60 sechsmal durchlaufen wird.
- Staging-Emission als **eine gemeinsame Kette** mit `complex_transition` je Kategorie — statt wie beim
  Prostata-Modul pro Risikogruppe eine eigene `Obs_cT_*`-Kette. Das Prostata-Muster (`CT_Split_Low`,
  `CT_Split_Intermediate`, …) skaliert bei 2 Achsen nicht mehr.
- Therapie-Bausteine (BET, Mastektomie, SLNB, ALND, RT, endokrin, Chemo, Anti-HER2) als **wiederverwendete
  Zustände** mit attributgesteuerten Übergängen.

Realistische Schätzung: **220–280 Zustände**. Die Zusammenführung der Staging-Ketten ist zugleich ein
Refactoring-Kandidat für das Prostata-Modul (dort ließen sich ~40 Zustände einsparen) — aber getrennt, um die
validierte v3-Kohorte nicht zu invalidieren.

---

## 10. Arbeitspakete

Aufwände in Personentagen (PT), Erfahrungswert aus dem Prostata-Modul (dort ~12 PT von Kalibrierung bis
validiertem ECCDM-Output). Reihenfolge ist eine Abhängigkeitskette; innerhalb der Kalibrierungs-Recherche sind
die fünf Pakete parallelisierbar, ebenso später AP-6/AP-7.

### 10.1 Kalibrierungs-Recherche — Epic `synthea-eu-cancer-4w3`

Ergebnis des Epics ist **eine** Datei: `epidemiology/breast_calibration.md` im Format von
`prostate_calibration.md` (jeder Arrow mit Quelle + Confidence-Flag). Die fünf Kinder decken die Kapitel
dieses Konzepts ab. **Querschnittsauflage für alle fünf:** jede übernommene Zahl bekommt den Vermerk, ob sie
für **50–60** gilt oder aus einer 50–69-Quelle stammt (dann „Quelle 50–69" + abgesenkte Confidence, §1.2).

| Bead | Inhalt | deckt ab | Aufwand |
|---|---|---|---|
| **`synthea-eu-cancer-51w`** | **Eintritt & Detektion** — Screening-Markov-Kette (45,9/86,3/15,3), Detektionsmodus-Split 45/11/44 inkl. Altersband-Prüfung, Erst-vs-Folgerunden-Kennzahlen (50–54/55–59), BI-RADS-Entscheidung (Option 1 vs. 2), PPV-Konsistenzprüfung, Hochrisiko-/IFNP-Arm **nur in der Minimalvariante** (§1.4.1 — Anteil, Bildgebungsfrequenz, TNBC-Umgewichtung; keine Vollvariante) | §1, §2 | **1,5 PT** |
| **`synthea-eu-cancer-0m8`** | **Subtypen & Stadien bei Diagnose** — Ki-67-Cutoff-Entscheidung + Dokumentation der S3-Weigerung, 5-Wege-Subtypverteilung inkl. 50–60-Drift, kohärente ER/PR/HER2/Ki-67-Sets, HER2-IHC-/HER2-low-Priors, cTNM nach Detektionsmodus, UICC-Gegenprobe, Grading, Histologie-Mix, DCIS-Ast | §3, §4, §5.1, §5.5 | **2 PT** |
| **`synthea-eu-cancer-98b`** | **pTNM / Sentinel / pCR** — SLNB-vs-ALND-Allokation, pTNM-Übergangsmatrix (Analogon zur Partin-Matrix), Staging-Guardrails, `yp`-Kategorien und pCR-Definition (ypT0 ypN0 streng) | §5.2, §5.3, §5.4 | **1,5 PT** |
| **`synthea-eu-cancer-t3f`** | **Therapie-Allokation** — BET/Mastektomie nach Stadium, RT nach BET, Neoadjuvanz-Anteile inkl. Ära-Reskalierung (der wichtigste 🔴-Arrow), pCR-Raten je Subtyp, endokrine Therapie inkl. AI/TAM-Split für 50–60 und Persistenz, Chemo/Anti-HER2/CDK4/6, Genexpressionstest | §6 | **2 PT** |
| **`synthea-eu-cancer-6r8`** | **Verlauf & Outcomes** — subtypabhängige Rezidiv-Hazards (Höhe *und* Form), Fernmetastasierung, Überleben nach Metastasierung, Validierungsanker inkl. der 50–59-Werte (5-J-RS 92 %, 15-J-RS 80,7 %), Dokumentation der Fenster-Trunkierung (§1.2d) | §7 | **1,5 PT** |

**Summe Epic 4w3: ~8,5 PT.**

### 10.2 Umsetzung

Beads-Issues angelegt (2026-08-31), Abhängigkeiten verdrahtet: Recherche-Beads + AP-T entsperren AP-M1; Kette M1→M2→M3→{M4,M5}→AP-P→AP-V; AP-F hängt an M2, AP-C an M5.

| AP | Inhalt | Ergebnis | Aufwand | Abhängig von |
|---|---|---|---|---|
| **AP-T** (`synthea-eu-cancer-c0v`) | Terminologie-Validierung: alle Codes aus §4.1, §5.4, §5.5, §6.1 gegen CEIR-OS (SNOMED INT + LOINC 2.83) prüfen; OPS-Codes gegen BfArM; ATC für die 15+ Substanzen (Tamoxifen, AI, Trastuzumab, Pertuzumab, T-DM1, Pembrolizumab, CDK4/6, Anthrazykline, Taxane, Platine, Capecitabin, Olaparib, Zoledronat) dual-kodiert WHO-ATC + ATC-DE | `terminology/breast_data_dictionary.md` | **2 PT** | 4w3 |
| **AP-M1** (`synthea-eu-cancer-5h3`) | Modulbau: Screening-Markov-Kette + Eintrittspfade + Workup | `modules/adult/breast.json` v0.1 | **2 PT** | 51w, AP-T |
| **AP-M2** (`synthea-eu-cancer-qoc`) | Modulbau: Subtyp-Branch + kohärente Biomarker-Emission inkl. Konsistenz-Guard | v0.2 | **2 PT** | 0m8, AP-M1 |
| **AP-M3** (`synthea-eu-cancer-1s7`) | Modulbau: cTNM / pTNM / ypTNM inkl. SLNB-vs-ALND-Logik und DCIS-Sonderregeln | v0.3 | **2 PT** | 98b, AP-M2 |
| **AP-M4** (`synthea-eu-cancer-io5`) | Modulbau: Therapiepfade je Subtyp inkl. Neoadjuvanz + pCR-Branch + post-neoadjuvanter Eskalation | v0.4 | **3 PT** | t3f, AP-M3 |
| **AP-M5** (`synthea-eu-cancer-dba`) | Modulbau: Rezidiv-/Metastasierungs-Pfad mit stückweise konstanten Hazards + endokrine Persistenz-Abbrüche | v1.0 | **2 PT** | 6r8, AP-M3 |
| **AP-P** (`synthea-eu-cancer-0wh`) | `postprocess_ccdm.py` auf Entitäts-Registry umbauen, `yp`-Staging, Biomarker-Passthrough (§8.3) | erweiterter Postprocessor, Prostata-Regression grün | **3 PT** | AP-M4, AP-M5 |
| **AP-V** (`synthea-eu-cancer-aij`) | Validierung: `validate_ccdm.sh` auf Mamma-Bundles; Kohorten-Gegenprobe gegen die Anker (Subtypmarginale, BET-Raten, M1 6,2 %, **5-J-RS 92 %**); Process-Mining-DFG über `fhir_to_eventlog.py`; Fenster-Einschränkungen (§1.2d) in `README.md` dokumentieren | Validierungsreport, Kohorte n=1000 | **2 PT** | AP-P |
| **AP-F** (`synthea-eu-cancer-dbq`) | ECCDM-Feedback zu den Biomarker-Lücken (§8.2) in `docs/eccdm_draft_feedback.md` ergänzen; Vorschlag `observation-tumor-biomarker-eu-ccm` skizzieren | Feedback-Abschnitt + ggf. Issue im `hl7-eu/cancer-common`-Tracker | **1 PT** | AP-M2 |
| **AP-C** (optional, `synthea-eu-cancer-xb3`) | Abgleich gegen die 14 SenologieOnFHIR-Beispielfälle: kann das Modul jede Journey erzeugen? | Abdeckungsmatrix, Lückenliste | **1,5 PT** | AP-M5 |

**Summe Umsetzung: ~17,5 PT** (ohne AP-C: 16 PT). **Gesamt ~26 PT** — etwa das Doppelte des Prostata-Moduls,
plausibel angesichts der zweiten Stratifizierungsachse, der Neoadjuvanz und der Biomarker-Schicht.

Hinweis zu AP-C: sieben der 14 Senologie-Beispielfälle liegen außerhalb des 50–60-Fensters (Lena Hoffmann 44,
Julia Fischer 37, Kathrin Müller 47, Christina Becker 42, Hannah Klein 33, Renate Vogel 43, Sabine Weber 71) und
zwei sind männlich. Die Abdeckungsmatrix muss deshalb zwischen „Modul kann das prinzipiell nicht" und „liegt nur
außerhalb des Kohortenfensters" unterscheiden.

**Bewusste Ausschlüsse für v1** (als bekannte Einschränkungen in `README.md` zu dokumentieren): synchron
bilaterale Karzinome (3,04 %), männliches Mammakarzinom (0,82 %), B3-Läsionen/ADH, Rekonstruktion/Implantate
(IRegG), Psychoonkologie/Sozialdienst, Studienteilnahme — alle in SenologieOnFHIR modelliert und v2-Kandidaten —
sowie die **Vollvariante des Hochrisiko-Arms** (§1.4.2: prophylaktische Chirurgie, kontralaterale Karzinome,
Moderate-Risk-Gene, eigenes Alters-Guard ab 35 J.) und die **Profilierung der Biomarker-/Grading-Observations**
(§8.3 Punkt 3 — erst wenn das ECCDM ein Profil hat).

**Nicht ausgeschlossen, sondern verbindlich:** DCIS (§3.3) und der schlanke Hochrisiko-Arm (§1.4.1).

---

## 11. Offene Datenlücken

0. **Das Altersband 50–60 selbst ist die größte strukturelle Lücke.** Die deutsche Mamma-Literatur ist auf das
   Screening-Anspruchsalter **50–69** geschnitten; eine 50–59-Aufschlüsselung liefern nur KoopMammo
   (Recall, CDR, Hintergrundinzidenz), TRM (M1-Anteil 6,2 %) und RKI/TRM (Überleben 92 % / 80,7 %) 🟢.
   Für Detektionsmix (Braun 2018), Subtypverteilung (TRM/Schrodi), UICC-Stadienmix (RKI) und alle
   OnkoZert-Therapiekennzahlen gibt es **keine** feinere Stratifizierung 🔴 — diese Zahlen sind im Dokument
   als „Quelle 50–69" markiert und um eine Confidence-Stufe abgesenkt. Wo die Richtung der Verzerrung bekannt
   ist (TNBC ↑, Luminal A ↓, Stadienmix leicht ungünstiger durch die Erstrunden-Spitze), ist sie angegeben;
   die *Größe* ist durchweg unbelegt. **Das ist die wichtigste offene Frage für Epic `synthea-eu-cancer-4w3`.**
   Ein möglicher Ausweg für einzelne Größen: Sonderauswertung beim Tumorregister München anfragen — die
   TRM-Faktenblätter enthalten 5-Jahres-Altersbänder, sie sind nur in der Subtypen-Publikation zu 50–69
   aggregiert.
1. **Ki-67-Verteilung pro Surrogat-Subtyp** — in keiner deutschen Quelle publiziert 🔴. Die Priors in §4.2 sind
   an die Regensburger Marginalen und den TRM-36/64-Split angepasst, aber nicht direkt belegt.
2. **HER2-IHC-Score-Verteilung für Deutschland** 🔴 — nur die dänische Nationalregister-Verteilung existiert.
   Interlabor-Varianz (46,3–71,8 % HER2-low) ist größer als der Modellierungsfehler.
3. **BI-RADS-Stufenverteilung im deutschen Abklärungskollektiv** 🔴 — kein Analogon zu Oerther 2021 (PI-RADS).
   Deshalb die Entscheidung für Option 1 in §2.
4. **Neoadjuvanz-Anteil je Subtyp für 2023** 🔴 — Ortmann 2022 endet 2018, die Gesamtrate hat sich seither
   verdoppelt. Der wichtigste rote Arrow im Therapieteil.
5. **UICC-Vierwege-Split für screen-detektierte Karzinome** 🔴 — KoopMammo berichtet nur „0+I" vs. „II+".
6. **N1/N2/N3-Split nach Detektionsmodus** 🔴 — Braun 2018 gibt nur N0/N+.
7. **Metastasenlokalisation für Deutschland/Europa** 🔴 — es existiert keine Tabelle; nur SEER.
8. **Genexpressionstest-Nutzungsrate** 🔴 — nur eine Kongress-Experteneinschätzung (~20 %), keine Registerzahl;
   der Test ist kein DKG-Qualitätsindikator, also gibt es keinen Nenner.
9. **monarchE-Anteil und Pertuzumab-/Bisphosphonat-Uptake in Deutschland** 🔴 — nicht publiziert.
10. **Erweiterte endokrine Therapie (>5 J.) Uptake** 🔴 — nicht publiziert.
11. **Detektionsmix nach Altersband** 🔴 — Braun 2018 publiziert den 45/11/44-Split nicht nach Alter, obwohl
    Hintergrundinzidenz und Mammadichte im Fenster 50–60 klar gegen den 50–69-Mittelwert sprechen (§1.1).
    (Die Screening-Erweiterung auf 70–75 ist für dieses Kohortenfenster gegenstandslos, für spätere
    Fensterweitungen aber weiterhin ohne Evaluationsdaten.)
12. **Populationsbezogene deutsche PAM50-Verteilung** 🔴 — existiert nicht; alle Subtypzahlen sind Surrogat-IHC.

Eine zirkulierende Angabe „Lum B HER2− 55,4 % / Lum A 22,0 %" mit TRM-Zuschreibung ließ sich **nicht** auf eine
Primärquelle zurückführen — **nicht verwenden**. Ebenso „Deutschland 15,9 % HER2-ultralow" (keine Zitatkette).

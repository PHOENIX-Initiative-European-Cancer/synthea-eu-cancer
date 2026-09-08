# Konzept: Synthea-Brustkrebs-Modul (Frauen 50–60)

Analogon zu `modules/adult/prostate.json` + `epidemiology/prostate_calibration.md`. Dieses Papier legt das
klinische Modell, die Stratifizierungsachsen, die Emissionscodes und die Arbeitspakete fest — **es ist keine
Kalibrierungsdoku**.

> 📐 **Die kanonischen Zahlen leben in [`epidemiology/breast_calibration.md`](../epidemiology/breast_calibration.md)**
> (3.081 Zeilen, Teile A/B/C aus Epic `synthea-eu-cancer-4w3`, Stand 2026-08-31). Dieses Konzept nennt nur noch die
> Zahlen, an denen eine **Design-Entscheidung** hängt, und verweist im Übrigen dorthin. Bei Abweichungen zwischen
> beiden Dokumenten **gilt die Kalibrierungsdatei** — sie ist gegen die Primärquellen verifiziert, dieses Papier
> nicht.
>
> Die Evidenzrunde vom 2026-08-31 hat dieses Konzept an **19 Stellen korrigiert** (A §0: 6, B §8: 4, C §0: 9).
> Alle Korrekturen sind unten eingearbeitet und mit „**korrigiert**" plus Fundstelle markiert. Die tragenden vier:
> **(1)** Detektionsmix 44/18/38 statt 45/11/44 · **(2)** das deutsche MSP erhebt **kein BI-RADS** ·
> **(3)** `bc_high_risk` ist eine Populations-, keine Patientinnengröße (0,35 % statt 2 %) ·
> **(4)** die Rezidiv-Hazards müssen nicht mehr geschätzt werden — das TRM publiziert gemessene Jahresraten.

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
| BI-RADS | Emissions-Artefakt statt steuernder Branch — **alternativlos**, das MSP erhebt kein BI-RADS | §2 |
| pCR-Definition | **`ypT0/is ypN0`** (korrigiert von „streng ypT0 ypN0") | §5.3 |
| pCR-Wirkung auf Rezidiv | nur **TNBC- und HER2+-Ast** (S3-konform) | §6.2 |
| Ausgeschlossen in v1 | bilaterale Karzinome, männliches Mamma-Ca, B3/ADH, Rekonstruktion, Psychoonkologie, Studienteilnahme | §10.2 |

> ⚠️ **Offener Punkt zur S3-Version (Kalibrierung A §0).** Dieses Papier zitiert durchgängig **v5.1 (Juni 2026)**;
> der lokale AWMF-Korpus, gegen den die Kalibrierung verifiziert wurde, enthält **v5.0 (Dezember 2025,
> AWMF-Freigabe 23.01.2026)**. **Alle Empfehlungsnummern in der Kalibrierungsdatei sind gegen v5.0 verifiziert.**
> Vor Modulbau ist abzugleichen, ob v5.1 die Nummerierung geändert hat — das betrifft u. a. die im Text
> genannten Empf. 4.72, 4.73, 4.85, 4.138–4.161.

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
| Bildgebungs-Score im Workup | PI-RADS (LOINC 82717-8) → biopsierate-steuernd | **BI-RADS** (LOINC 72018-2) → nur **Emissions-Artefakt**; Steuerung über MSP-Prozesskennzahlen (§2) |
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

> ✏️ **korrigiert (Kalibrierung A §7, §8.1).** Der ursprüngliche Split 45/11/44 stützte sich auf Braun 2018
> (Münster, n=1.531). Es gibt eine 45-fach größere deutsche Quelle: **Buschmann 2024** (Krebsregister NRW,
> alle Frauen 50–69 mit inzidentem C50 2006–2014, n=**68.230**, PMID 38287392). Braun 2018 bleibt für die
> *bedingten* Merkmalsverteilungen (§1.3) unverzichtbar — Buschmann liefert diese Tabelle nicht — aber **nicht
> mehr für die Marginale**.

| Eintrittspfad | Anteil | Basis | Conf |
|---|---|---|---|
| **Screening-detektiert** (MSP) | **0.44** | Buschmann 2024, NRW, **2014er Steady-State** (die Gesamtperiode 2006–2014 ist durch die Rollout-Jahre nach unten verzerrt). **Quelle 50–69** | 🟡 |
| **Intervallkarzinom** (nach negativem Screening) | **0.18** | ebd. — der bisherige Wert 0,11 war **um Faktor ~1,6 zu niedrig** | 🟡 |
| **Symptomatisch / Nicht-Teilnehmerin** | **0.38** | ebd. | 🟡 |
| **Hochrisiko / IFNP** (gBRCA1/2) | **0.0035** *auf Populationsebene* — siehe §1.4.1 | CARRIERS (n=32.544 Kontrollen) + BRIDGES (n=53.461): **0,353 % / 0,361 %** | 🟢 |

**Warum der neue Split nicht nur „eine größere Studie" ist — die interne Konsistenzprüfung entscheidet.**
Der Intervallanteil *unter Teilnehmerinnen* beträgt bei 44/18 gerechnet 18/(44+18) = **28,6 %**, also eine
implizierte Programmsensitivität von **71,4 %**. Das deckt sich mit **Heinze 2023** (BARMER-Abrechnungsdaten,
n=1,99 Mio. Folgescreenings: IC-Anteil 27,6 %, PS 69,9–71,7 %) aus einer völlig unabhängigen Datenquelle 🟢.
Der alte Split 45/11 ergibt dagegen 11/56 = 19,6 %, also **PS 80,4 %** — das ist der Erstrunden-Wert und für
eine Dauerteilnehmerinnen-Kohorte im Fenster 50–60 nachweislich zu optimistisch. **Der alte Split war mit der
Programmsensitivität, die dasselbe Modul an anderer Stelle verwendet, nicht vereinbar.** Genau diese
Widerspruchsfreiheit ist das Argument, nicht die Stichprobengröße.

> ✏️ **Zitatkorrektur (A §0.2):** die Programmsensitivität 69,9–71,7 % stammt von **Heinze F et al.**,
> *BMC Cancer* 2023;23:855, **PMID 37697304** — nicht von „Kaiser", wie eine frühere Fassung dieses Papiers
> angab. Der Zahlenwert war korrekt, der Erstautor falsch.

**Design-Empfehlung: den Modus erzeugen statt setzen.** Die sauberste Umsetzung lässt `bc_detection_mode` aus
der Teilnahme-Markov-Kette + Programmsensitivität + altersbandspezifischer Detektionsrate **emergieren** und
benutzt 44/18/38 nur als **Validierungsziel**. Das ist exakt dasselbe Argument, mit dem §3.2 den Subtyp aus den
Biomarkern ableitet statt ihn zu ziehen — und es hat hier einen zusätzlichen Vorteil: der resultierende Mix ist
dann automatisch konsistent mit den Erstrunden-Effekten des schmalen Fensters (§1.2a), die man sonst doppelt
einrechnen müsste.

**Modellierungshinweis Screening-Teilnahme:** die Teilnahme ist stark „klebrig" und darf **nicht** als i.i.d.
52-%-Münzwurf modelliert werden. KoopMammo 2023 liefert die Markov-Kette direkt: Ersteinladung **45,9 %**,
Wiedereinladung nach Teilnahme **86,3 %**, nach Nicht-Teilnahme **15,3 %** (Gesamtteilnahme 52,1 %) 🟢.
Das ist der Mechanismus, der den Detektionsmix *erzeugt*, statt ihn zu postulieren — abbildbar als
`Delay` + `complex_transition`-Schleife auf einem Attribut `msp_last_attended`.

**Richtung der Altersband-Verzerrung:** im Fenster 50–60 verschiebt sich der Mix **weg vom Screening**, weil die
Hintergrundinzidenz niedriger und die Programmsensitivität bei 50–54 am schlechtesten ist — der Intervallanteil
ist also eher am oberen Rand anzusetzen. Belegt ist das nicht; **keine deutsche Quelle publiziert den
Detektionsmix nach Altersband** 🔴. Der 44/18/38-Split bleibt Startwert und Kalibrier-Kandidat für
`synthea-eu-cancer-51w`, keine gesetzte Größe.

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
`msp_round_index`), nicht als eine gemittelte Screening-Runde.

> ✏️ **korrigiert und quantifiziert (Kalibrierung A §3.5).** Die ursprüngliche Formulierung „die Kohorte ist
> erstrundenlastig" war in dieser Schärfe falsch. **Auf Untersuchungsebene** hat eine Frau mit allen 6
> Einladungen 1 Erst- und 5 Folgeuntersuchungen = 16,7 % — praktisch identisch zum Programmmittel von 16 %.
> Der Effekt sitzt allein auf **Karzinomebene**, weil die Erstrunde die doppelte Detektionsrate hat:
> `7,6 + 5 × 4,16 = 28,4` Karzinome je 1.000 Frauen, davon `7,6/28,4 =` **26,8 % aus der Erstrunde**
> (programmweit 22,1 %). Daraus folgt ein gewichteter **DCIS-Anteil im Screening-Arm von ~19 %** —
> nicht die 22 %, die eine frühere Fassung dieses Papiers als „oberen Rand" ansetzte. Der Erstrunden-Effekt
> ist real und rechtfertigt getrennte Zustände, aber er ist beim DCIS-Anteil ein **1-Punkt-Effekt, kein
> 4-Punkte-Effekt.** (Die Rechnung unterstellt vollständige Teilnahme; mit der Markov-Kette verschiebt sich
> der Anteil leicht nach oben, weil Wiedereinsteigerinnen erneut in erstrundennahe Konstellationen geraten 🟡.)

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
- **Prävalenz — korrigierte Quellenbasis (Kalibrierung A §0.3, §8.1):** die frühere Fassung stützte sich auf
  LIBRO-1 (1,8 %) und einen Altersgradienten von „3,3 % bei >50 J." Beides ist ersetzt: LIBRO-1 ist eine
  **schwedische** Kohorte, und die 3,3 % waren **2 Ereignisse bei 60 Patientinnen** aus einer Athener Serie
  (95 %-KI 0,4–11,5 %) — als Altersevidenz unbrauchbar und **gestrichen**. Maßgeblich sind jetzt zwei
  Großkohorten, die auf 0,05 Prozentpunkte übereinstimmen: **CARRIERS** (Hu/Hart 2021, PMID 33471974,
  n=32.247 Fälle) **2,15 %** und **BRIDGES/BCAC** (Dorling 2021, PMID 33471991, n=60.466) **2,10 %** — jeweils
  **unter Brustkrebs-Patientinnen** 🟢. In der Allgemeinbevölkerung sind es **0,353 % / 0,361 %** (Kontrollen
  beider Kohorten) 🟢. Der klassisch zitierte Bereich 1:400–1:800 stammt aus Segregationsanalysen der 1990er
  und ist **zu niedrig**.
- **Subtyp-Skew:** BRCA1-Tumoren sind zu **~69–71 %** triple-negativ, BRCA2 nur zu ~16–23 % (CIMBA 2012,
  PMID 22144499) 🟢. BRCA2 dominiert BRCA1 im Verhältnis **2:1** und im Fenster 50–60 noch stärker, weil
  BRCA2-Trägerinnen 5–8 Jahre später erkranken (CARRIERS: mittleres Diagnosealter BRCA1 50,3–50,9 J.,
  BRCA2 55,4–58,6 J.) 🟢; nur 26 % der BRCA1- und 33 % der BRCA2-Trägerinnen sind bei Diagnose ≥60 J.
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

> ✏️ **korrigiert (Kalibrierung A §0.4, §8.1) — der folgenreichste Zahlenfehler des Konzepts.** Die frühere
> Fassung setzte `bc_high_risk = 0.02`. Die 2,1 % gelten aber **unter Brustkrebs-Patientinnen**; Synthea setzt
> das Attribut im `Initial`-Bereich, also auf **Populationsebene** — dort sind es **0,35 %**. Ein Faktor 6.
>
> **Umsetzung v1:** `bc_high_risk = 0.0035` auf Populationsebene **plus** ein erhöhter Erkrankungs-Hazard für
> Trägerinnen, sodass sich die 2,1 % unter den Erkrankten **ergeben**. Das ist etwas mehr Arbeit als ein fixer
> Anteil, aber die einzige Variante, die *beide* publizierten Marginalen trifft — und sie passt zur
> Grundlinie dieses Moduls, abgeleitete Größen abzuleiten statt zu setzen (§1.1, §3.2). Wird stattdessen der
> bequeme Weg gewählt, muss in `README.md`: **die Kohorte überschätzt den BRCA-Anteil unter den
> Nicht-Erkrankten um Faktor 6** — für ein Demo-Dataset vertretbar, für jede Prävalenzauswertung tödlich.

| Element | Umsetzung in v1 | Wert | Conf |
|---|---|---|---|
| Zugehörigkeit | **ein Attribut** `bc_high_risk` (boolean), gesetzt im `Initial`-Bereich | **0.0035** (Populationsebene) ⇒ **~2,1 %** unter den Erkrankten | 🟢 (CARRIERS + BRIDGES) |
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

## 2. Workup — das BI-RADS-Analogon trägt nicht, und das ist der Befund

> ✏️ **korrigiert, strukturell (Kalibrierung A §4).** Die Überschrift dieses Kapitels lautete
> „BI-RADS als PI-RADS-Analogon". Die Recherche hat den Vergleich **widerlegt**:
>
> **Das deutsche MSP erhebt keine BI-RADS-Kategorien.** Die Befundung ist **binär** („unauffällig" vs.
> „Konsensuskonferenz erforderlich"); danach entscheidet die Konsensuskonferenz über den Abklärungsbedarf.
> Die einzige verpflichtende Kategorisierung im Programm ist die **B-Klassifikation B1–B5** der Histologie
> (BMV-Ä Anlage 9.2 — BI-RADS kommt im gesamten Anlagentext nicht vor). Auch die **S3 v5.0 knüpft in keiner
> einzigen Empfehlung eine Handlungskonsequenz an eine BI-RADS-Kategorie**; der Term erscheint im
> 497-seitigen Langtext genau einmal, als Literaturstelle. Die Leitlinie steuert über
> **Befundkonstellationen** (Herdbefund / Mikrokalk / Dichte / Diskordanz), nicht über eine Suspicion-Skala.
>
> Eine deutsche BI-RADS-Stufenverteilung mit Karzinomraten je Stufe ist damit nicht „zufällig nicht
> publiziert", sondern **strukturell nicht erhebbar**. Damit ist die frühere „Option 1" nicht mehr die
> pragmatischere von zwei Wahlmöglichkeiten, sondern **die einzige fachlich haltbare** — die Abwägung unten
> entfällt.

Kaskade im Screening-Arm, gesteuert über die deutschen Prozess-Kennzahlen statt über eine Score-Stufe:

`MSP_Exam → (binär) Recall → Stufe-1-Abklärung → Biopsieindikation → Biopsie → B-Klassifikation → Karzinom`

Der BI-RADS-Wert wird **rückwärts konsistent gesetzt** (4 bei Biopsieindikation, 5 bei hoher
Malignitätswahrscheinlichkeit) — er bleibt als Emissions-Artefakt im Bundle, weil er ein Pflicht-Datenelement
in SenologieOnFHIR und ein wichtiges Testartefakt ist, steuert aber nichts.

**Im symptomatischen Arm ist BI-RADS dagegen real im Gebrauch** (ACR BI-RADS 5th ed., Fachkonsens
Müller-Schimpfle 2016) 🟢. Nur dort lohnt sich eine Stufenlogik — mit US-/NL-Proxy-PPVs
(4A 7,6 % · 4B 22,0 % · 4C 69,3 % · 5 92,9 %), die in der Kalibrierungsdatei stehen und als Proxy markiert
sind 🟡. **Achtung beim Import:** der deutsche PPV II liegt mit 55,6 % fast doppelt so hoch wie der US-PPV3
(~29 %), weil die zweistufige Abklärung filtert, bevor die Nadel kommt — ein 1:1-Import US-amerikanischer
BI-RADS-4-PPVs würde die Biopsierate im Modell massiv überschätzen.

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
| Abklärung → Biopsieindikation | **0.011** aller Untersuchten | dito | ebd. | 🟡 (nicht nach Alter berichtet) |
| Recall → Biopsie (abgeleitet) | **0.279** | dito | ebd., eigene Rechnung | 🟡 |
| **PPV I**, **Erstuntersuchung** | **0.070** (50–54) / 0.101 (55–59) | **0.083** | abgeleitet `CDR / Recall` | 🟢 |
| **PPV I**, **reguläre Folge** | **0.119** (50–54) / **0.183** (55–59) | **0.206** | dito | 🟢 |
| **PPV II** (Karzinom je Biopsieindikation) | **0.556** | dito | ebd. | 🟡 (nicht nach Alter berichtet) |
| Präoperativ histologisch gesichert | **0.952** | dito | ebd. | 🟢 |
| Kontrolluntersuchung statt Abklärung (dt. Analogon zu BI-RADS 3) | **0.005** aller Untersuchten | — | ebd. | 🟢 |

> ✏️ **korrigiert (Kalibrierung A §0.5, §3.3).** Die frühere Fassung führte **einen** PPV I von 0,16. Das ist
> der bundesweite *Mischwert*; nach Untersuchungsart trennt der Bericht in **Erst 8,3 %** und **reguläre Folge
> 20,6 %**. Ein pauschaler 0,16 ist damit **in beide Richtungen um Faktor ~2 falsch** — für die Erstrunde bei
> 50–54 sogar um Faktor 2,3.

**Die im Konzept vorgeschlagene Ableitung ist durchgerechnet und schließt sich.** `PPV I = CDR / Recall` ergibt
untersuchungsgewichtet **8,19 % (Erst)** und **20,80 % (Folge)** gegen die publizierten **8,3 %** und
**20,6 %** — eine Abweichung von 0,1–0,2 Prozentpunkten. Damit ist bewiesen, dass Recall, CDR und PPV I aus
demselben Bericht arithmetisch kohärent sind und die abgeleiteten Bandwerte belastbar. **Das ist das
Konsistenz-Gate für `synthea-eu-cancer-51w`:** jede spätere Änderung an Recall oder CDR muss diese Rechnung
erneut bestehen.

Bemerkenswert und für die Kohorte relevant: der PPV I ist bei **50–54 in der Erstrunde mit 7,0 % der
schlechteste Wert des gesamten Programms** — hoher Recall trifft auf niedrige Inzidenz. Genau dieser Punkt
liegt im Kohortenfenster, und zwar bei jeder Teilnehmerin.

Nur ~28 % der Wiedereinbestellten werden überhaupt biopsiert; drei Viertel werden in der nicht-invasiven Stufe 1
(Palpation, Zusatzaufnahmen, Sonographie, ggf. MRT) entlastet. Das ist der Grund für den hohen deutschen PPV II
— und die Warnung gegen den Import von US-BI-RADS-PPVs oben.

Der symptomatische Arm überspringt das Screening und geht über `Tastbefund` → `Diagnostische Mammographie +
Sonographie` → Biopsie; die Karzinomwahrscheinlichkeit bei symptomatischer Vorstellung steht in der
Kalibrierungsdatei (Teil A §6).

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
Screening-Arm über dem Folgerunden-Wert von 18 % — der **gewichtete Zielwert ist ~19 %** (Herleitung §1.2a).
Die frühere Formulierung „am oberen Rand, 22 %" nahm den reinen Erstrunden-Wert und überschätzte den Effekt
(korrigiert, Kalibrierung A §3.5).

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
| PR (%) | 50–95 | 0–60 (**PR− in ~10–15 %**, korrigiert von 30–40 %) | 0–70 | 0 | 0 | 🔴 |
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
(symptomatisch) — Braun 2018, **Quelle 50–69** 🟡.

> ✏️ **korrigiert (Kalibrierung B §5.2, §8).** Der 🔴-Prior „N1 : N2 : N3 = 70 : 19 : 11" ist **ersetzt**: die
> NCDB-Auswertung liefert für cN0-Patientinnen die gemessene Feinverteilung
> **pN1mi 20,1 / pN1 63,7 / pN2 11,7 / pN3 4,5 %**. Damit fällt einer der roten Arrows weg. Zusätzlich neu
> erschlossen und im Konzept bisher gar nicht vorgesehen: eine vollständige **cN0 → pN+ Übergangsmatrix**
> (das Mamma-Analogon zur Partin-Matrix des Prostata-Moduls, §5.2) und eine **cT → pT-Upstaging-Tabelle**.
> Beide stehen in der Kalibrierungsdatei Teil B §5.4 / §5.7.

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

**Das Partin-Analogon existiert jetzt.** Beim Prostata-Modul ist die Partin-Matrix (cT/PSA/Gleason → pT/pN) das
Herzstück der pathologischen Staging-Emission. Für das Mammakarzinom hat die Kalibrierungsrunde das Gegenstück
**neu erschlossen** — eine `cN0 → pN+`-Übergangsmatrix aus NCDB (17,9 %) und INSEMA (17,0 %), plus
cT→pT-Upstaging (Kalibrierungsdatei Teil B §5.4/§5.7). Damit hat das Mamma-Modul an dieser Stelle **dieselbe
Belegtiefe wie das Prostata-Modul**, was beim Schreiben dieses Konzepts noch nicht absehbar war.

### 5.3 ypTNM und pCR — der strukturell neue Teil

Das Prostata-Modul kennt keine Neoadjuvanz. Für das Mammakarzinom ist sie tragend (§6.2) und braucht eine
eigene Staging-Emission. SNOMED hält die vollständige `yp`-Hierarchie bereit (verifiziert, SNOMED INT
20260501) — u. a. **ypT0 1352650002**, **ypTis(DCIS) 1352633004**, **ypN0 1352797005**. Damit sind beide
pCR-Definitionen sauber kodierbar.

> ✏️ **korrigiert (Kalibrierung C §0 K11, §3.5).** Die frühere Fassung wählte die **strenge** Definition
> `ypT0 ypN0` mit dem Argument der besseren Trennschärfe (HR 0,446 vs. 0,523). Das kehrt sich um: die S3 ist
> **in sich inkonsistent** — das Pathologiekapitel und die RT-Tabelle 8 definieren `ypT0/is ypN0`, nur
> Empfehlung 4.111 schreibt `ypT0 und ypN0`. Maßgeblich ist die Mehrheitsschreibweise, und vor allem: sie
> entspricht der Definition **aller Zulassungsstudien** (KEYNOTE-522, TRYPHAENA, KATHERINE), aus denen die
> pCR-Raten stammen, die das Modul verwendet.
>
> **Modellkonvention: durchgängig `ypT0/is ypN0`** (DCIS im Resektat zulässig). Andernfalls würden gemessene
> pCR-Raten gegen eine strengere Definition gezogen, als die Studien sie erhoben haben — ein systematischer
> Fehler zugunsten zu niedriger pCR-Häufigkeit.

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
| Radiatio nach BET, invasiv — **Indikation** | 0.978 | OnkoZert KZ 4 (LL-QI) | 🟢 |
| **Radiatio nach BET, invasiv — Durchführung** | **~0.91** | Heinig 2022, PMID 35109813 (Dx-Jahr 2008) | 🟡 |
| **Radiatio nach BET, DCIS — begonnen** | **0.784** | OnkoZert KZ 5 | 🟢 |
| Primärfälle **nicht operiert** | 0.161 gesamt (M1: 0.846; cT1N0M0: 0.072) | OnkoZert JB 2025 | 🟢 |
| Revisionsoperation | 0.024 | OnkoZert KZ 22 | 🟢 |

**Design-Entscheidung:** die BET-Wahrscheinlichkeit **auf das Stadium konditionieren, nicht aufs Alter** — der
Alterseffekt ist klein (50–69: 75,8 % gegen 69,6 % über alle Alter, Heinig 2022, PMID 35109813) 🟡, der
Stadieneffekt dagegen groß (86 % → 27 %). Damit ist auch die Verschmälerung auf 50–60 unkritisch: die
OnkoZert-Kennzahlen sind zwar **nicht altersstratifiziert** (alle Alter, 96,9 % weiblich) 🟡, aber weil das
Modul über das Stadium konditioniert und der Stadienmix altersband-korrekt gezogen wird (§5.1), trägt sich der
Alterseffekt implizit durch. Das ist der Grund, die Kennzahlen stadien- und nicht altersbezogen anzusetzen.

> ✏️ **korrigiert (Kalibrierung C §0 K4).** Die frühere Fassung las die 97,8 % als Durchführungsrate. OnkoZert
> KZ 4 misst aber den Anteil, **denen eine Radiatio *empfohlen* wurde** — eine Indikations-, keine
> Durchführungskennzahl. Für ein Modul, das Procedures emittiert, ist die Durchführung die relevante Größe.
> KZ 5 (DCIS) misst dagegen tatsächlich „begonnen" und bleibt unverändert.

Bestrahlung: Zielvolumina aus SenologieOnFHIR (`vs-senologie-rt-zielvolumen`, SNOMED): ganze Brust 76752008,
Thoraxwand 78904004, axilläre LK 68171009, supraklavikuläre LK 76838003, parasternale LK 245282001 🟡.
**Hypofraktionierung ist heute Standard** (Details und Dosisschemata: Kalibrierungsdatei Teil C §2.2) — das
im OncoBox-Testfall belegte Schema 40 Gy / 2,5 Gy ist also der Normalfall, nicht die Ausnahme; die 50 Gy +
10–16 Gy Boost der Senologie-Beispielfälle sind das ältere Schema.

### 6.2 Neoadjuvanz und pCR-Branch

Anteil neoadjuvant behandelter Patientinnen, **alle Primärfälle 2023: 21,4 %** (OnkoZert, 15.699/73.505) 🟢;
nach klinischem Stadium cT1N0M0 18,9 / cT2N0M0 32,7 / N+M0 29,5 % 🟢 (alle drei exakt bestätigt).

> ✏️ **präzisiert (Kalibrierung C §0 K5).** Zwei Fallstricke: **(a) Nenner.** Der parallel kursierende Wert
> 25,45 % ist derselbe Zähler auf dem Nenner *operierte* Primärfälle (61.675) — beide korrekt, zwei Nenner.
> Das Modul muss den Nenner explizit festlegen. **(b) Kategoriename.** OnkoZert zählt „neoadjuvant **oder
> präoperativ systemisch**", was breiter ist als reine Chemotherapie. **(c) Altersband:** für 50–60 kommt ein
> belegter Multiplikator **1,28** hinzu ⇒ **0,25–0,28** statt 0,214.

Nach Subtyp: Ortmann 2023 (55 DKG-Zentren, 2007–2018, n=94.638) 🟢 — TNBC 31,8 %, HR−/HER2+ 31,9 %,
HR+/HER2+ 26,5 %, HR+/HER2− 5,8 %, alle vier exakt bestätigt. Die Ära-Reskalierung auf 2023, die dieses Konzept
als „wichtigsten roten Arrow" markiert hatte, ist in der Kalibrierungsdatei (Teil C §3.3) **hergeleitet** statt
geschätzt — dort nachschlagen statt hier duplizieren.

> ✏️ **Zitatkorrektur (C §0 K13):** **Ortmann O et al., *J Cancer Res Clin Oncol* 2023;149(3):1195–1209,
> PMID 35380257 / PMC9984341** (online first 04/2022). Das Konzept zitierte durchgängig „Ortmann 2022".

**pCR-Raten** (jetzt `ypT0/is ypN0`, §5.3), deutsche Realwelt (Ortmann 2023) 🟢: HR+/HER2− **12 %**,
HR+/HER2+ **36 %**, HR−/HER2+ **53 %**, TNBC **38 %**. Moderne Regime-Anker: KEYNOTE-522 **64,8 %** 🟢,
GeparOcto TNBC 48,5/51,7 % 🟢.

> ✏️ **korrigiert (C §0 K9, B §8).** **NeoSphere (45,8 %) ist als HER2+-Anker unbrauchbar** — die Studie misst
> **pCR in der Brust allein**, ohne Nodalstatus, ist also gegenüber `ypT0/is ypN0` nach oben verzerrt und mit
> KEYNOTE-522 nicht vergleichbar. Ersatz: **TRYPHAENA (45–52 %)** oder TRAIN-2.
>
> ✏️ **korrigiert (B §8):** die Modellpriors Luminal A **6 %** / Luminal B HER2− **12 %** reproduzieren
> Ortmanns HR+/HER2−-Mischwert von 12 % nicht. Korrigiert auf **5 % / 18 %**.

Prognostische Nuance (von Minckwitz 2012, PMID 22508812, n=6.377): pCR ist prognostisch bei Luminal B/HER2−,
HER2+ nicht-luminal und TNBC — nicht bei Luminal A (p=0,39) und nicht bei Luminal B/HER2+ (p=0,45) 🟢.

> ✏️ **vereinfacht (C §0 K12).** Die S3 ist enger als von Minckwitz: *„Nur bei triple-negativen und
> HER2-positiven Mammakarzinomen wird die pCR derzeit als Surrogatmarker … anerkannt."* ⇒ **der pCR-Effekt
> wirkt nur im TNBC- und im HER2+-Ast** — leitlinienkonform **und** einfacher als die bisherige Drei-Äste-Regel.

**Verzweigungsbedingung Pembrolizumab — korrigiert (C §0 K10, §3.4):** die frühere Fassung schrieb
„Pembrolizumab bei CPS≥10 bzw. Stadium II/III". **S3 Empfehlung 4.154 (neu 2025) nennt ausschließlich
> 2 cm oder N+ — es gibt keinen PD-L1-/CPS-Cutoff.** Das entspricht KEYNOTE-522, wo der pCR-Vorteil
unabhängig von der PD-L1-Expression war; die CPS-Abhängigkeit gilt **nur metastasiert** (KEYNOTE-355) 🟢.
Ebenso leitliniengesteuert ist die HER2+-Weiche: **> 2 cm und/oder N+** → neoadjuvant mit dualer Blockade
(Empf. 4.161), **≤ 2 cm und cN0** → primäre OP mit De-Eskalation auf Paclitaxel + Trastuzumab 12 Wochen
(Empf. 4.160). Das ersetzt einen flachen Subtyp-Prior durch eine **stadienabhängige Verzweigung** — die
vollständige Entscheidungstabelle steht in der Kalibrierungsdatei Teil C §3.4.

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

> ✏️ **korrigiert, Vorzeichenwechsel (Kalibrierung C §0 K1, §4.1).** Die frühere Fassung schätzte für 50–60
> **AI ~55–65 % / TAM ~35–45 %** 🔴. Die altersstratifizierte Rekonstruktion aus Kostev 2023 (IQVIA LRx,
> n=284.383, PMID 36149512) ergibt für **51–60 Jahre: AI 46,4 % / Tamoxifen 53,6 %** 🟢.
> **Der Split kippt — Tamoxifen ist in diesem Fenster die Mehrheit.** Der Konzeptvorschlag war 10–19
> Prozentpunkte zu AI-lastig, und der Wert steigt von 🔴 auf 🟢.

Endokrine Details: **AI 0,46 / Tamoxifen 0,54** für 50–60 🟢 (Gesamtmarkt über alle Alter: 54,9/45,1).
Die **primäre latente Variable ist der Menopausenstatus, nicht das Alter** — und im Fenster 50–60 liegt
genau der Übergang (Median Menopausenalter DE 50 J., IQR 47–53): bei 50 J. rund die Hälfte postmenopausal,
bei 60 J. ~97 %. Das Modul braucht zusätzlich einen **Statuswechsel-Arm nach Chemotherapie**
(chemotherapie-induzierte Amenorrhoe), keinen fixen Baseline-Status — S3 Empf. 4.142 verlangt dafür
Hormonstatus-Monitoring.

**Persistenz nach 5 Jahren (90-Tage-Lücke): AI 35,1 %, TAM 32,5 %** 🟢 — ein schön modellierbarer Abbruch-Pfad,
den kein anderes synthetisches Mamma-Dataset abbildet, direkt aus deutschen Verordnungsdaten belegt.

> ✏️ **korrigiert (C §0 K2).** Das Konzept unterstellte implizit „jüngere brechen häufiger ab". Kostev 2023
> zeigt einen **U-förmigen** Verlauf: ≤50 J. HR 1,08, **51–60 J. HR 0,92**, 61–70 J. HR 0,89 (Referenz >70 J.).
> **Die Zielgruppe 50–60 hat also unterdurchschnittliches Abbruchrisiko.** Stärkster Prädiktor ist ohnehin
> nicht das Alter, sondern der **Verordner** (Hausarzt HR 1,24) — was für das Modul bedeutet, dass der
> Abbruch-Arm an der Versorgungsstruktur hängen sollte, nicht am Geburtsdatum.

CDK4/6-Inhibitoren im metastasierten HR+/HER2−-Setting: 38,5 % → 62,7 % in den ersten zwei Jahren nach
Zulassung (PRAEGNANT-Register, Fasching 2020, PMID 32956934) 🟢; für 2023 extrapoliert ~80–85 % 🔴.
Adjuvant (monarchE-Kriterien) betrifft ~13 % der HR+/HER2−-Frühfälle (dänische DBCG-Kohorte) 🟡 —
kein deutscher Wert 🔴.

> ✏️ **korrigiert (C §0 K3).** Der Genexpressionstest-Stand des Konzepts („seit 20.06.2019 Oncotype DX für
> HR+/HER2−, N0") gilt nur für 2019–2020. Aktuell: seit **15.10.2020 vier Tests** (Oncotype, EndoPredict,
> MammaPrint, Prosigna); seit **17.07.2025 Oncotype auch bei N1** — dafür **alle vier eingeschränkt auf
> postmenopausal** (oder prämenopausal mit Ovarialsuppression).
>
> Das ist mehr als eine Aktualisierung: der Testzugang ist ab 2025 **menopausenstatusabhängig**, und in einer
> 50–60-Kohorte mit gemischtem Status wird daraus ein **echter Verzweigungspunkt** statt eines pauschalen
> Nutzungsanteils. Die Nutzungsrate selbst bleibt unbelegt (~20 % Experteneinschätzung 🟡, keine deutsche
> Studie 🔴 — der Test ist keiner der 23 DKG-Qualitätsindikatoren, es gibt also keinen Nenner).

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
| Fernmetastasierung (M0 bei Diagnose) | **≈8,4 % @5J / ≈13,1 % @10J** (⚠ nicht 11,0/16,6 — siehe Kasten) | TRM-Spezialauswertung `RisikoM0`, n=46.418, Dx 2002–2020 | 🟢 |
| jede Progression | 16,3 / 24,0 / 28,7 % | TRM Survival Tab. 5b | 🟢 |
| Rezidiv-Hazard ER+ vs ER−, Jahre 0–5 | 9,9 %/J vs 11,5 %/J | Colleoni 2016, IBCSG I–V, PMID 26786933 | 🟢 (Ära-Vorbehalt) |
| Jahre 5–10 / 10–15 | ER+ 5,4 / 2,9 %/J; ER− 3,3 / 1,3 %/J | ebd. | 🟢 |
| **TNBC-Hazard-Form** | Gipfel bei ~3 J., danach steiler Abfall; kaum Rezidive nach ~8 J. | Dent 2007, PMID 17671126 | 🟢 |
| ER+-Hazard-Form | konstanter Spättail 1–2 %/J über 20 J. hinaus | Pan 2017, NEJM, PMID 29117498 (88 Studien, 62.923 Frauen) | 🟢 |
| ER+ Fernrezidiv Jahre 5–20, nach Stadium | T1N0 **13 %** · T1N1-3 20 % · T2N0 19 % · T2N1-3 26 % · T1N4-9 34 % | ebd. | 🟢 |
| Überleben **nach** Fernmetastasierung (modern, DE) | 1-J 69,3 % · 2-J 52,2 % · **5-J 23,8 %** · 10-J 10,7 % | TRM Survival Tab. 5f (n=8.811, ≥2007) | 🟢 |
| Medianes Überleben nach Metastasierung je Subtyp | Lum A 2,2 J · Lum B 1,6 J · Lum/HER2 1,3 J · HER2-enriched 0,7 J · basal 0,5 J | Kennecke 2010, PMID 20498394 | 🟢 (alte Kohorte) |
| Kontralaterales Mamma-Ca, BRCA1 @10J | 25,1 % (BRCA2 6,6 %, **Nicht-Trägerinnen 3,6 %** — korrigiert von 4,6 %) | Engel 2020, PMID 31081934 | 🟢 |

> ✏️ **korrigiert (Kalibrierung C §0 K6).** Es gibt **zwei TRM-Tabellen mit zwei Werten** für die
> Fernmetastasierung: Survival Tab. 5b (11,0 / 16,6 %) und die Spezialauswertung `RisikoM0` (≈8,4 / ≈13,1 %).
> **Nicht mischen.** Die Auflösung steht in der Kalibrierungsdatei Teil C §6.2. Ebenso korrigiert: das
> kontralaterale Risiko der Nicht-Trägerinnen ist **3,6 %**, nicht 4,6 % (Zahlendreher im Konzept).

> ⭐ **Die wichtigste Einzelkorrektur der ganzen Recherche (C §0 K8).** Dieses Kapitel schlug vor, die
> Hazard-Formen aus Colleoni + Pan + Dent zu **synthetisieren** — ein 🔴-Konstrukt aus drei internationalen
> KM-Kurven verschiedener Ären. Das ist nicht mehr nötig: **das TRM publiziert eine gemessene
> Hazard-Rate-Spalte pro Jahresintervall** (Spezialauswertung `RisikoM0`, Tab. 21–24, Deutschland,
> Dx 2002–2020, konkurrenzrisikokorrigiert).
>
> Damit werden die Rezidiv-Hazards von einem geschätzten zu einem **gemessenen deutschen Parameter** — der
> zentrale Mechanismus des Rezidiv-Pfades steht nicht mehr auf einem Modellprior. Die konsolidierten
> Jahresraten je Subtyp stehen in der Kalibrierungsdatei Teil C §6.3 und ersetzen die früher hier
> vorgeschlagenen Weibull-Näherungen vollständig.

Synthea kann keine kontinuierlichen Hazards; die Umsetzung bleibt eine **`Delay` + `complex_transition`-Schleife
mit stückweise konstanten Jahresraten je Subtyp** — dieselbe Mechanik wie `PSA_Followup` → `BCR_Check`, nur mit
mehreren Zeitfenstern. Die TRM-Jahresintervalle passen zu dieser Mechanik sogar besser als eine stetige
Verteilung, weil sie bereits in der benötigten Granularität vorliegen.

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

### 10.1 Kalibrierungs-Recherche — Epic `synthea-eu-cancer-4w3` ✅ **abgeschlossen (2026-08-31)**

Ergebnis: **`epidemiology/breast_calibration.md`**, 3.081 Zeilen, Teile A/B/C im Format von
`prostate_calibration.md` (jeder Arrow mit Quelle + Confidence-Flag). Die Querschnittsauflage — jede Zahl mit
Vermerk „[50–60]" / „[Quelle 50–69]" / „[alle Alter]" und entsprechend abgesenkter Confidence — ist umgesetzt.

| Bead | Inhalt | deckt ab | Status |
|---|---|---|---|
| **`synthea-eu-cancer-51w`** | **Eintritt & Detektion** — Screening-Markov-Kette, Detektionsmodus-Split, Erst-vs-Folgerunden-Kennzahlen, BI-RADS-Frage, PPV-Konsistenzkette, Hochrisiko-Arm (Minimalvariante) | §1, §2 | ✅ Teil A |
| **`synthea-eu-cancer-0m8`** | **Subtypen & Stadien bei Diagnose** — Ki-67-Cutoff, 5-Wege-Subtypverteilung, kohärente Marker-Sets, HER2-IHC/HER2-low, cTNM nach Detektionsmodus, Grading, Histologie, DCIS | §3, §4, §5.1, §5.5 | ✅ Teil B |
| **`synthea-eu-cancer-98b`** | **pTNM / Sentinel / pCR** — SLNB-vs-ALND, **cN0→pN+-Matrix (Partin-Analogon)**, cT→pT-Upstaging, Staging-Guardrails, `yp`-Kategorien, pCR-Definition | §5.2, §5.3, §5.4 | ✅ Teil B |
| **`synthea-eu-cancer-t3f`** | **Therapie-Allokation** — BET/Mastektomie, RT, Neoadjuvanz inkl. hergeleiteter Ära-Reskalierung, pCR je Subtyp, endokrine Therapie, Chemo/Anti-HER2/CDK4/6, Genexpressionstest | §6 | ✅ Teil C |
| **`synthea-eu-cancer-6r8`** | **Verlauf & Outcomes** — **gemessene TRM-Jahres-Hazards**, Fernmetastasierung, Überleben nach Metastasierung, altersband-spezifische Validierungsanker, Fenster-Trunkierung | §7 | ✅ Teil C |

**Ertrag über die reine Bestätigung hinaus:** 19 Korrekturen an diesem Konzept (Kopf des Dokuments), **vier
neu erschlossene Tabellenblöcke**, die hier gar nicht vorgesehen waren (pT/pN je Subtyp, cN0→pN+-Matrix,
cT→pT-Upstaging, gemessene Rezidiv-Hazards), und **sechs geschlossene 🔴-Lücken** (§11). Von den nachgeprüften
Konzeptwerten waren die große Mehrheit exakt bestätigt — die Korrekturen konzentrieren sich auf Stellen, an
denen das Konzept aus Mangel an deutschen Daten geschätzt hatte und inzwischen eine Primärquelle vorliegt.

### 10.2 Umsetzung

Beads-Issues angelegt (2026-08-31), Abhängigkeiten verdrahtet: Recherche-Beads + AP-T entsperren AP-M1; Kette M1→M2→M3→{M4,M5}→AP-P→AP-V; AP-F hängt an M2, AP-C an M5.

| AP | Inhalt | Ergebnis | Aufwand | Abhängig von |
|---|---|---|---|---|
| **AP-T** (`synthea-eu-cancer-c0v`) | Terminologie-Validierung: alle Codes aus §4.1, §5.4, §5.5, §6.1 gegen CEIR-OS (SNOMED INT + LOINC 2.83) prüfen; OPS-Codes gegen BfArM; ATC für die 15+ Substanzen (Tamoxifen, AI, Trastuzumab, Pertuzumab, T-DM1, Pembrolizumab, CDK4/6, Anthrazykline, Taxane, Platine, Capecitabin, Olaparib, Zoledronat) dual-kodiert WHO-ATC + ATC-DE | `terminology/breast_data_dictionary.md` | **2 PT** | 4w3 |
| **AP-M1** (`synthea-eu-cancer-5h3`) | Modulbau: Screening-Markov-Kette + Eintrittspfade + Workup | `modules/adult/breast.json` v0.1 | **2 PT** | 51w, AP-T |
| **AP-M2** (`synthea-eu-cancer-qoc`) | Modulbau: Subtyp-Branch + kohärente Biomarker-Emission inkl. Konsistenz-Guard | v0.2 | **2 PT** | 0m8, AP-M1 |
| **AP-M3** (`synthea-eu-cancer-1s7`) | Modulbau: cTNM / pTNM / ypTNM inkl. SLNB-vs-ALND-Logik und DCIS-Sonderregeln | v0.3 | **2 PT** | 98b, AP-M2 |
| **AP-M4** (`synthea-eu-cancer-io5`) | Modulbau: Therapiepfade je Subtyp inkl. Neoadjuvanz + pCR-Branch + post-neoadjuvanter Eskalation | v0.4 | **3 PT** | t3f, AP-M3 |
| **AP-M5** (`synthea-eu-cancer-dba`) | Modulbau: Rezidiv-/Metastasierungs-Pfad mit den **gemessenen TRM-Jahres-Hazards** (§7) + endokrine Persistenz-Abbrüche | v1.0 | **2 PT** | 6r8, AP-M3 |
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
3. **BI-RADS-Stufenverteilung im deutschen Screening** — ✅ **aufgelöst, aber anders als gedacht:** es ist keine
   Publikationslücke, sondern **strukturell nicht erhebbar**, weil das MSP binär befundet (§2). Die Lücke
   verschwindet damit als Lücke und wird zur Designvorgabe.
4. **Neoadjuvanz-Anteil je Subtyp für 2023** 🟡 — die Ära-Reskalierung ist in der Kalibrierungsdatei
   (Teil C §3.3) **hergeleitet** statt geschätzt, inklusive Alters-Multiplikator 1,28 für 50–60. Von
   „wichtigster roter Arrow" auf einen belegten Zwischenschritt herabgestuft.
5. **UICC-Vierwege-Split für screen-detektierte Karzinome** 🔴 — KoopMammo berichtet nur „0+I" vs. „II+".
6. **N1/N2/N3-Split nach Detektionsmodus** 🔴 — Braun 2018 gibt nur N0/N+. *(Die unkonditionierte
   Feinverteilung ist dagegen jetzt belegt, §5.1.)*
7. **Metastasenlokalisation für Deutschland/Europa** 🔴 — es existiert keine Tabelle; nur SEER.
8. **Genexpressionstest-Nutzungsrate** 🔴 — nur eine Kongress-Experteneinschätzung (~20 %), keine Registerzahl;
   der Test ist kein DKG-Qualitätsindikator, also gibt es keinen Nenner. *(Die Erstattungslage ist dagegen
   geklärt und seit 2025 menopausenstatusabhängig, §6.3.)*
9. **monarchE-Anteil und Pertuzumab-/Bisphosphonat-Uptake in Deutschland** 🔴 — nicht publiziert. Ebenso der
   **Pembrolizumab-Uptake**: PubMed-Suche ergab null Treffer, OnkoZert führt keine Immuncheckpoint-Kennzahl
   (belegter Negativbefund) ⇒ freier Parameter.
10. **Erweiterte endokrine Therapie (>5 J.) Uptake** 🔴 — nicht publiziert.
11. **Detektionsmix nach Altersband** 🔴 — auch Buschmann 2024 publiziert den 44/18/38-Split nicht nach Alter,
    obwohl Hintergrundinzidenz und Programmsensitivität im Fenster 50–60 klar gegen den 50–69-Mittelwert
    sprechen (§1.1). (Die Screening-Erweiterung auf 70–75 ist für dieses Kohortenfenster gegenstandslos, für
    spätere Fensterweitungen aber weiterhin ohne Evaluationsdaten.)
12. **Populationsbezogene deutsche PAM50-Verteilung** 🔴 — existiert nicht; alle Subtypzahlen sind Surrogat-IHC.
13. **gBRCA-Prävalenz nach Altersband** 🔴 — keine der vier Großkohorten (CARRIERS, BRIDGES, LIBRO-1, GC-HBOC)
    publiziert eine altersstratifizierte Prävalenztabelle. Belegt ist nur die Richtung; interpolierte Spanne
    für 50–59 unter BC-Patientinnen: 1,5–2,2 %.

**Durch die Evidenzrunde geschlossen** (standen hier noch als 🔴 und sind jetzt belegt): der
N1/N2/N3-Prior (§5.1), die Rezidiv-Hazard-Formen (§7), die cN0→pN+-Matrix und das cT→pT-Upstaging (§5.2),
der endokrine Wirkstoffsplit für 50–60 (§6.3) und die PPV-Kette (§2).

Eine zirkulierende Angabe „Lum B HER2− 55,4 % / Lum A 22,0 %" mit TRM-Zuschreibung ließ sich **nicht** auf eine
Primärquelle zurückführen — **nicht verwenden**. Ebenso „Deutschland 15,9 % HER2-ultralow" (keine Zitatkette).

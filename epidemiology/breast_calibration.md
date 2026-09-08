# Breast module — transition-probability calibration (Frauen 50–60)

Source trace für jeden geplanten Übergangspfeil des Brustkrebs-Moduls (`modules/adult/breast.json`, in Arbeit).
Architektur und Design-Entscheidungen: `docs/breast_module_concept.md`. Stil und Confidence-Legende identisch zu
`prostate_calibration.md`: 🟢 gut belegt · 🟡 belegt mit Übertragbarkeits-/Ära-Vorbehalt · 🔴 Modellierungsprior.

**Entstehung:** Drei parallele Evidenz-Recherchen (2026-08-31, beads-Epic `synthea-eu-cancer-4w3`), hier als
Teile A/B/C mit eigenständiger Abschnittsnummerierung assembliert. Jeder Teil trägt seine eigenen
"Offene Datenlücken" und (A, B) Verifikations-/Korrekturabschnitte; die §0-Korrekturlisten in A und C sind
in `docs/breast_module_concept.md` eingearbeitet.

**Bekannte Überlappung:** pCR-Raten erscheinen in Teil B §6 und Teil C §3 — bei Abweichungen ist **Teil C §3
maßgeblich** (spätere Recherche-Runde, inkl. altersstratifizierter deutscher Brustzentren-Daten 50–59 aus
PMID 36604331 und der Endpunkt-Kritik an NeoSphere).

---


# Teil A — Eintritt & Detektion (beads synthea-eu-cancer-51w)

Draft A zu beads `synthea-eu-cancer-51w`. Quellenspur für jeden Arrow, der eine Frau der Kohorte
**Frauen 50–60, Deutschland** in das Modul hinein und bis zur Diagnosestellung führt. Alles ab Subtyp,
Staging, Therapie und Rezidiv gehört in die Arbeitspakete B ff. und steht hier nicht.

Format und Confidence-Legende identisch zu `epidemiology/prostate_calibration.md`:
🟢 gut belegt (deutsches Register / Vollerhebung / große Primärstudie, genau die gefragte Zahl) ·
🟡 belegt, aber Übertragbarkeits-, Altersband- oder Ära-Vorbehalt · 🔴 Modellierungsprior / Schätzung.

**Kalibrierrahmen.** Struktur aus der S3-Leitlinie Mammakarzinom (AWMF 032-045OL) und den
BMV-Ä-Programmvorgaben; Wahrscheinlichkeiten aus **KoopMammo Jahresbericht Evaluation 2023** (Vollerhebung,
3,12 Mio. Untersuchungen — neueste Ausgabe, ein Bericht für 2024 existiert im August 2026 noch nicht),
**ZfKD/RKI Datenbankabfrage** (Stand 19.11.2025, Fälle bis 2023), **Krebsregister NRW** (Buschmann 2024,
n = 68.230) und **BARMER-Routinedaten** (Heinze 2023, n = 1,99 Mio. Folgescreenings). Wo Deutschland keine
Zahl hat, steht ein klar markierter UK-/US-/NL-Proxy.

Entschieden und hier vorausgesetzt: **DCIS wird mitmodelliert**; der **BRCA-Arm bleibt schlank**.

---

## 0. Korrekturen an `docs/breast_module_concept.md` §1–§2

Die dortigen Zahlen sind überwiegend bestätigt. Sechs Punkte müssen geändert werden, drei davon sind
strukturell (nicht nur Zahlendreher):

| # | Konzept §1–§2 sagt | Befund | Konsequenz |
|---|---|---|---|
| 1 | Detektionsmix **45 / 11 / 44** (Braun 2018, Münster, n = 1.531) | **Buschmann 2024** (Krebsregister NRW, n = 68.230, PMID 38287392) gibt für 2014 **44,2 / 17,7 / 38,1**. Der Intervallanteil im Konzept ist **zu niedrig um Faktor ~1,6** | Auf **0,44 / 0,18 / 0,38** umstellen, Braun 2018 nur noch für die *bedingten* Merkmalsverteilungen (§1.3) nutzen. Begründung in §7 unten |
| 2 | „Programmsensitivität 69,9–71,7 % (**Kaiser** 2023, PMC10496211)" | **Falscher Erstautor.** PMC10496211 = **Heinze F**, Czwikla J, Heinig M, Langner I, Haug U, *BMC Cancer* 2023;23:855, PMID 37697304. Die Werte 69,9–71,7 % sind korrekt | Zitat korrigieren (auch in `docs/calibration_sources.md`, falls dort übernommen) |
| 3 | „gBRCA1/2 in unselektierter BC **1,8 %** (LIBRO-1, PMC6320715)"; Altersgradient „**3,3 %** >50 J. (PMC3240809)" | LIBRO-1 ist **schwedisch**, nicht deutsch (Li 2018, PMID 30175445). Die 3,3 % sind **2 Ereignisse bei 60 Patientinnen** aus Athen (Koumpis 2011), 95 % KI 0,4–11,5 % — als Alters-Evidenz **unbrauchbar** | Auf CARRIERS (**2,15 %**, n = 32.247) + BRIDGES (**2,10 %**, n = 60.466) umstellen. Koumpis streichen |
| 4 | `bc_high_risk` = **0.02 der Kohorte** | 2,1 % gilt **unter Brustkrebs-Patientinnen**. Unter *allen* Frauen 50–60 sind es **0,35 %** (CARRIERS-/BRIDGES-Kontrollen) | **Bezugsgröße explizit machen.** Synthea zieht auf Populationsebene ⇒ 0,02 wäre ~6-fach zu hoch. Siehe §8 |
| 5 | PPV I = **0,16** als ein Wert | 0,157 ist der bundesweite **Mischwert**. Nach Untersuchungsart: **Erst 8,3 %**, reguläre Folge **20,6 %** (JB Eval 2023, Anhang Abb. 25) | Ein pauschaler 0,16 ist in beide Richtungen um Faktor ~2 falsch. Siehe §3.3 |
| 6 | DCIS-Anteil im Screening-Arm „**am oberen Rand**, 22 %" | Bei 6 Runden im Fenster 50–60 stammen **26,8 %** der screen-detektierten Karzinome aus der Erstrunde ⇒ gewichteter DCIS-Anteil **19,1 %** | Nicht 22 %, sondern **~19 %**. Der Erstrunden-Effekt ist real, aber kleiner als im Konzept unterstellt. Siehe §3.4 |

Zwei weitere Zitatkorrekturen aus der Recherche, die §2/§6 des Konzepts betreffen: **Koo 2017** hat
PMID **28549339** (nicht 28347885 — das ist eine Schlafforschungsarbeit); die **1,53 %** IFNP-Detektionsrate
stammt aus dem **DKG/OnkoZert-Jahresbericht FBREK 2025** (226/14.791), nicht aus Bick 2019.

Ein Punkt bleibt offen: das Konzept zitiert die S3 als **v5.1 (Juni 2026)**, der lokale AWMF-Korpus enthält
**v5.0 (Dezember 2025, AWMF-Freigabe 23.01.2026)**. Alle unten genannten Empfehlungsnummern sind gegen
**v5.0** verifiziert — vor Modulbau abgleichen, ob 5.1 die Nummerierung geändert hat.

---

## 1. Kohorten-Yield-Anker — Inzidenz 50–54 und 55–59

**Quelle für alle invasiven Raten:** Zentrum für Krebsregisterdaten im RKI, Datenbankabfrage
(www.krebsdaten.de/abfrage), Statistik Inzidenz, Kennzahl **rohe Rate**, C50, weiblich, 5-Jahres-Klassen,
Datenstand **19.11.2025** (Fälle bis 2023). Das ist dieselbe Quelle, aus der auch die KoopMammo-Fußnote
speist — nur vier Jahrgänge aktueller.

| Altersband | Rate 2023 (je 100.000/Jahr) | Fälle 2023 (DE) | Conf |
|---|---|---|---|
| 45–49 | 196,4 | — | 🟢 |
| **50–54** | **263,1** (2022: 261,6 · 2021: 264,4) | 7.557 | 🟢 |
| **55–59** | **240,6** (2022: 243,9 · 2021: 246,7) | 8.116 | 🟢 |
| 60–64 | 299,2 | 9.501 | 🟢 |
| 65–69 | 354,3 | 9.437 | 🟢 |

> ⚠️ **Der 55–59-Sattel ist echt und muss im Modell erhalten bleiben.** Die Rate *fällt* von 50–54 auf
> 55–59 und steigt danach wieder. Das ist die Signatur des Screening-Programms (Prävalenzgipfel in der
> Erstrunde mit ~50, danach Vorziehen der Diagnosen), reproduziert sich seit 2014 in jedem Jahr und in
> praktisch jedem Landesregister. Ein Modell, das eine monoton steigende Alterskurve unterstellt,
> widerspricht der deutschen Registerrealität — und zwar genau im Kohortenfenster.

**Gegenprobe KoopMammo (Begriffsklärung).** Der Jahresbericht Evaluation 2023 nennt auf S. 34
„259 pro 100.000" (50–54) und „350" (65–69). Fußnote 13 dort lautet **„ohne In-situ-Karzinome"**,
Fußnote 14 verweist auf dieselbe ZfKD-Abfrage mit Datenaufbereitung 03/2023, Fälle bis 2019. Der heutige
ZfKD-Wert für 2019 ist 260,4 — praktisch deckungsgleich. **Konsistent, invasiv-only.**
Achtung: der Terminus **„Hintergrundinzidenz"** meint im KoopMammo-Bericht etwas anderes, nämlich die
eingefrorenen bundeslandspezifischen **Vor-2005-Raten**, gegen die das 1,5-fach-Kriterium der EU-Leitlinien
geprüft wird (S. 20). Die beiden Begriffe nicht vermischen.

**DCIS (D05).** Nationale altersband-genaue Raten existieren nirgends publiziert; KID 2025 Tab. 3.29.1 gibt
nur Gesamtwerte (6.524 Fälle/Jahr, ASR 11,9, medianes Erkrankungsalter 59 J.) 🟢. Ersatz aus den deutschen
Landesregistern über die ECIS-API (Entity 35, 2023, n = 7 liefernde Register):

| Altersband | DCIS-Rate je 100.000 (Registermedian) | Spanne | DCIS : invasiv | Conf |
|---|---|---|---|---|
| **50–54** | **53,5** | 37,2–58,1 | 19,5 % | 🟡 (regional, nicht national) |
| **55–59** | **34,2** | 26,8–56,9 | 13,8 % | 🟡 |
| 65–69 | 44,1 | 32,2–47,6 | 12,4 % | 🟡 |

Unabhängige regionale Bestätigung des Musters (TRM Basisstatistik D05, 2007–2020): 50–54 **39,1** ·
55–59 **35,8** · 65–69 47,4 — niedrigeres Niveau (14-Jahres-Mittel inkl. Vor-Screening-Jahren), gleiche Form.
Der DCIS-Peak bei 50–54 ist dieselbe Erstrunden-Signatur wie bei invasiv, nur ausgeprägter.

### 1.1 Der Durchsatz-Stellknopf (Analogon zu `Symptom_Check` 0,12/Jahr im Prostata-Modul)

Kumulierte Erkrankungswahrscheinlichkeit über das gesamte Fenster 50–60 (11 Altersjahre), aus den Raten oben:

| Entität | kumulativ 50–60 | Conf |
|---|---|---|
| invasiv (C50) | **2,82 %** | 🟢 (Summe der 🟢-Bandraten) |
| DCIS (D05) | **0,48 %** | 🟡 (ECIS-Registermedian) |
| **gesamt** | **3,30 %** | 🟡 |

> 🔴 **`BC_Onset_Check` — Kohorten-Ausbeute, NICHT Epidemiologie.** Rund 33 von 1.000 generierten Frauen
> erreichen im Fenster überhaupt eine Diagnose. Wer eine Demo-Kohorte mit ein paar hundert Patientinnen
> will, muss entweder `-p` in die Zehntausende drehen oder diesen Knopf überhöhen — **wie beim
> Prostata-Modul, und mit derselben Kennzeichnungspflicht.** Der Knopf darf nie mit den kalibrierten
> Arrows dieses Dokuments vermischt werden, und die Validierung (§10 des Konzepts) muss ihn
> herausrechnen, sonst validiert man den Stellknopf gegen sich selbst.

Sekundäranker: medianes Erkrankungsalter Deutschland **65 Jahre**, **15 %** aller Fälle vor dem 50.
Lebensjahr, 29 % nach dem 75. (KID 2025, Tab. 3.17.1 und Fließtext S. 72) 🟢. Das Fenster 50–60 liegt
auf der **ansteigenden Flanke** — das ist der Grund für die niedrige Ausbeute.

### 1.2 Bevölkerungs-Nenner (für jede Raten- und Absolutzahl-Rechnung)

| Größe | Wert | Basis | Conf |
|---|---|---|---|
| **Frauen 50 bis <60 in DE, 31.12.2024** | **5.920.445** | Destatis **12411-0006**, Basis Zensus 2022 | 🟢 |
| dito, 2023 | 6.140,2 Tsd. | ebd. | 🟢 |
| dito, 2022 | 6.349,8 Tsd. | ebd. | 🟢 |

Verifikationsweg: GENESIS 12411-0006 ist nicht anonym abrufbar (API verlangt Registrierung); der Wert
wurde über **zwei unabhängige Wege** bestätigt — Destatis-Bevölkerungspyramide (5.920,4 Tsd.) und
Eurostat `demo_pjan` (Summe der Einzeljahrgänge = exakt 5.920.445). Zitierweise: **Destatis 12411-0006,
verifiziert über Bevölkerungspyramide + Eurostat `demo_pjan`**.

> ⚠️ **Bezugsjahr mitführen.** Das Band schrumpft um ~3,5 % pro Jahr (6.349,8 → 6.140,2 → 5.920,4 Tsd.),
> weil die Babyboomer herauswachsen. Wer eine Rate aus 2023 mit einem Nenner aus 2024 kombiniert, baut
> einen systematischen 3–4-%-Fehler ein. Die Inzidenzraten in §1 stammen aus **2023** — für
> Absolutzahl-Hochrechnungen ist der **2023er** Nenner (6.140,2 Tsd.) zu verwenden, nicht der 2024er.

---

## 2. Screening-Teilnahme als Markov-Kette

**Quelle:** KoopMammo, *Jahresbericht Evaluation 2023*, Kap. 3.2 S. 13 + Anhangstabelle zu Abb. 4 S. 57.
Vollerhebung, 5,90 Mio. Einladungen / 3,08 Mio. Teilnehmerinnen 2023. Der Vorbefund des Konzepts ist
**exakt bestätigt**.

| Arrow (`msp_last_attended`) | Wert | Basis | Conf |
|---|---|---|---|
| `MSP_Invite` (Ersteinladung) → Teilnahme | **0.459** | JB Eval 2023, S. 13 / Anh. Abb. 4 | 🟢 |
| Folgeeinladung **nach Teilnahme** → Teilnahme | **0.863** | ebd. | 🟢 |
| Folgeeinladung **nach Nicht-Teilnahme** → Teilnahme | **0.153** | ebd. | 🟢 |
| (resultierende Gesamtteilnahmerate zur Kontrolle) | 0.521 | ebd. (50,8 % systematisch + 1,3 % Selbsteinladung) | 🟢 |
| Einladungsintervall | **24 Monate**; regulär 22–30 Mon., >30 Mon. = irregulär | ebd. S. 6, 19, Glossar | 🟢 |
| Anspruchsalter (Berichtszeitraum) | 50–69 J.; **seit 01.07.2024 50–75 J.** | G-BA Beschluss 21.09.2023 (6183), iK 01.07.2024 | 🟢 |

Zeitreihe für Sensitivitätsanalysen (Anh. Abb. 4, S. 57): Ersteinladung 43,2 / 44,0 / 46,5 / 44,5 / **45,9 %**
und nach Teilnahme 85,8 / 83,5 / 85,3 / 86,0 / **86,3 %** für 2019–2023 🟢. Die Kette ist über fünf Jahre
inklusive Pandemie bemerkenswert stabil — die Werte dürfen als Konstanten kodiert werden.

**Die Klebrigkeit ist der ganze Punkt.** 86,3 % gegen 15,3 % ist ein Faktor 5,6. Ein i.i.d.-Münzwurf mit
p = 0,52 erzeugt nach 6 Runden eine Binomialverteilung um 3,1 Teilnahmen; die echte Kette erzeugt eine
**bimodale** Population aus Dauerteilnehmerinnen und Dauerverweigerinnen. Das ist genau der Mechanismus,
der den Detektionsmodus-Mix in §7 *erzeugt*, statt ihn zu postulieren.

> ⚠️ **Datenlücke, die eine Modellentscheidung erzwingt.** Der Bericht stratifiziert die Teilnahme
> **ausschließlich** nach Einladungsart und Bundesland — **nicht nach Alter**. Altersaufgelöst gibt es nur
> Untersuchungs*zahlen* (Tab. 2, S. 19), aus denen sich der Altersmix, aber keine altersspezifische
> Teilnahmerate ableiten lässt; Einladungszahlen je Altersband werden nicht publiziert. Die Kette wird
> deshalb **altersunabhängig** kodiert 🟢 — das ist gut vertretbar, weil sie ohnehin rundenbasiert ist,
> muss aber als Annahme dokumentiert werden.

Zur Einordnung der Kohorte in das Programm (Tab. 2, S. 19, Untersuchungen 2023): bei 50–54 sind **76 %**
aller Untersuchungen Erstuntersuchungen (374.892 von 490.963 bundesweiten Erstuntersuchungen liegen in
diesem Band), bei 55–59 nur noch 13 %. Die Erstrunden-Population des Programms *ist* im Wesentlichen die
50–54-Population — die Kohorte trifft also genau den Bereich, in dem Erst- und Folgeuntersuchung
auseinanderlaufen.

---

## 3. Screening-Untersuchung: Recall, Detektionsrate, PPV

Alle Zahlen: KoopMammo JB Eval 2023, **Tab. 4 (S. 33)** für Recall und **Tab. 5 (S. 34)** für die CDR,
jeweils Vollerhebung 2023, altersband-aufgelöst. Diese Arrows sind die einzigen im Modul, die **direkt auf
50–60 kalibrierbar** sind — sie müssen altersbandspezifisch kodiert werden, nicht mit dem Programmmittel.

### 3.1 Wiedereinbestellungsrate (Recall)

| Arrow (`MSP_Exam` → Recall) | 50–54 | 55–59 | Programm | Conf |
|---|---|---|---|---|
| **Erstuntersuchung** | **0.109** | **0.103** | 0.108 | 🟢 |
| **reguläre Folgeuntersuchung** | **0.032** | **0.024** | 0.026 | 🟢 |
| *(irreguläre Folge, >30 Mon.)* | 0.041 | 0.036 | 0.039 | 🟢 |
| Recall → Abklärung wahrgenommen | 0.983 (123.694/125.892) | dito | 0.983 | 🟢 altersunabhängig |

### 3.2 Brustkrebsentdeckungsrate (CDR, ‰ je 1.000 Untersuchungen, **inkl. In-situ**)

| Arrow | 50–54 | 55–59 | Programm | Conf |
|---|---|---|---|---|
| **Erstuntersuchung** | **7,6 ‰** | **10,4 ‰** | 8,7 ‰ | 🟢 |
| **reguläre Folgeuntersuchung** | **3,8 ‰** | **4,4 ‰** | 5,3 ‰ | 🟢 |
| *(irreguläre Folge)* | 5,8 ‰ | 6,3 ‰ | 8,8 ‰ | 🟢 |

> ⚠️ **Label-Falle aus dem Konzept.** Die dort als „Folgeuntersuchung" geführten Werte (5,3 / 3,8 / 7,0 ‰
> und Recall 2,6 / 3,2 / 2,4 %) sind die **regulären** Folgeuntersuchungen. Für *alle* Folgeuntersuchungen
> gilt CDR 5,8 / 4,0 / 7,7 ‰ und Recall 2,8 / 3,2 / 2,6 %. Die Zahlen sind richtig, das Label ist
> unpräzise. Da das Modul mit einem sauberen 24-Monats-Takt arbeitet, ist **regulär** der korrekte Zweig;
> irreguläre Folgeuntersuchungen (11 % aller Folgeuntersuchungen, CDR fast doppelt so hoch) sind in v1
> bewusst nicht abgebildet — als Einschränkung notieren.
>
> Der Wert **55–59 Erstuntersuchung = 10,4 ‰** fehlte im Konzept vollständig und ist der höchste
> CDR-Wert im Kohortenfenster.

### 3.3 PPV I — **abgeleitet, nicht gesetzt**

Das Konzept empfiehlt in §2, den PPV aus Recall und CDR abzuleiten statt ihn zu setzen, weil die drei
Größen sonst eine inkonsistente Kette bilden. Das ist hier durchgerechnet, und die Ableitung
**validiert sich gegen den publizierten Programmwert**:

`PPV I = CDR / Recall`

| Band | Erstuntersuchung | reguläre Folgeuntersuchung | Conf |
|---|---|---|---|
| **50–54** | 7,6 ‰ / 10,9 % = **0.070** | 3,8 ‰ / 3,2 % = **0.119** | 🟢 abgeleitet aus zwei 🟢-Größen |
| **55–59** | 10,4 ‰ / 10,3 % = **0.101** | 4,4 ‰ / 2,4 % = **0.183** | 🟢 |
| 60–64 | 0.129 | 0.238 | 🟢 |
| 65–69 | 0.169 | 0.269 | 🟢 |
| **untersuchungsgewichtetes Mittel** | **8,19 %** | **20,80 %** | — |
| **publizierter Programmwert 2023** | **8,3 %** | **20,6 %** | 🟢 (Anh. Abb. 25, S. 60) |

**Die Kette schließt sich auf 0,1–0,2 Prozentpunkte.** Damit ist bewiesen, dass Recall, CDR und PPV I aus
demselben Bericht arithmetisch kohärent sind und die abgeleiteten Bandwerte belastbar sind. **Das ist der
Konsistenz-Gate für `synthea-eu-cancer-51w`** — jede spätere Änderung an Recall oder CDR muss diese
Rechnung erneut bestehen.

Bemerkenswert: der PPV I ist bei **50–54 in der Erstrunde mit 7,0 % der schlechteste Wert des gesamten
Programms** — hoher Recall trifft auf niedrige Inzidenz. Genau dieser Punkt liegt im Kohortenfenster.
Der pauschale Konzeptwert 0,16 ist für die Erstrunde um Faktor 2,3 zu hoch und für die Folgerunde bei
55–59 um Faktor 0,9 zu niedrig.

### 3.4 Abklärung, Biopsieindikation, PPV II

| Arrow | Wert | Basis | Conf |
|---|---|---|---|
| Alle Untersuchten → **Biopsieindikation** | **0.011** (35.081/3.121.605) | JB Eval 2023, Tab. 1 S. 7 | 🟡 (nicht nach Alter berichtet) |
| Recall → Biopsie (abgeleitet) | **0.279** (35.081/125.892) | ebd., eigene Rechnung | 🟡 |
| **PPV II** (Karzinom je Biopsieindikation) | **0.556** (Tab. 1 gerundet 56 %) | ebd., Kap. 9.2 S. 36 / Anh. Abb. 21 | 🟡 (nicht nach Alter berichtet) |
| Karzinom **präoperativ histologisch gesichert** | **0.952** | ebd., Kap. 9.3 S. 38 | 🟢 |
| Kontrolluntersuchung statt Abklärung (dt. Analogon zu BI-RADS 3) | **0.005** aller Untersuchten (Ref. <1 %) | ebd., Tab. 1 S. 7 | 🟢 |

**Nur ~28 % der Wiedereinbestellten werden überhaupt biopsiert** — rund drei Viertel werden in der
nicht-invasiven Stufe 1 (Palpation, Zusatzaufnahmen, Sonographie, ggf. MRT) entlastet. Das ist der Grund,
warum der deutsche PPV II (55,6 %) fast doppelt so hoch liegt wie der US-PPV3 (~29 %, BCSC/NMD): die
zweistufige Abklärung filtert, bevor die Nadel kommt. **Ein 1:1-Import US-amerikanischer BI-RADS-4-PPVs
würde die Biopsierate im Modell massiv überschätzen** (§4).

Wenn man PPV II als altersunabhängig annimmt (🔴, ungeprüft), folgt eine bandspezifische
Biopsieindikationsrate `= CDR / PPV II`: 50–54 Erst **1,37 %** / reguläre Folge **0,68 %**; 55–59 Erst
1,87 % / reguläre Folge 0,79 %. Als 🔴-Ableitung führen, nicht als belegte Größe.

### 3.5 Rundenmix im Fenster 50–60 — Korrektur zum Konzept §1.2a

Eine Frau, die alle 6 Einladungen (50, 52, 54, 56, 58, 60) wahrnimmt, hat **1 Erst- und 5 reguläre
Folgeuntersuchungen**, also 16,7 % Erstuntersuchungen — praktisch identisch zum Programmmittel von 16 %.
Auf **Untersuchungsebene** ist die Kohorte also *nicht* auffällig erstrundenlastig. Der Effekt sitzt auf
**Karzinomebene**, weil die Erstrunde die doppelte CDR hat:

| Größe | Rechnung | Ergebnis |
|---|---|---|
| Karzinome je 1.000 Frauen über 6 Runden | 7,6 + 5 × 4,16 | **28,4** |
| davon aus der Erstrunde | 7,6 / 28,4 | **26,8 %** (programmweit 22,1 %) |
| ⇒ **DCIS-Anteil im Screening-Arm** | 0,268 × 22 % + 0,732 × 18 % | **19,1 %** 🟡 |

Das Konzept setzt hier „am oberen Rand, 22 %" an — das ist der **reine Erstrunden**-Wert und
überschätzt den Effekt. Korrekt sind **~19 %**. Der Erstrunden-Effekt existiert und rechtfertigt getrennte
Zustände (`msp_round_index`), aber er ist ein 1-Prozentpunkt-Effekt auf den DCIS-Anteil, kein 4-Punkte-Effekt.
(Vorbehalt: die Rechnung unterstellt vollständige Teilnahme; mit der Markov-Kette aus §2 verschiebt sich
der Anteil leicht **nach oben**, weil auch Wiedereinsteigerinnen nach Aussetzern erneut in erstrundennahe
Konstellationen geraten. 🟡)

### 3.6 Tumorcharakteristika der screening-detektierten Karzinome

Vorbefund des Konzepts vollständig bestätigt (JB Eval 2023, **Tab. 3, S. 23**), plus die fehlenden Zeilen:

| Merkmal | Erstuntersuchung | Folgeuntersuchung | Conf |
|---|---|---|---|
| entdeckte Karzinome (n) | 4.294 | 15.145 | 🟢 |
| **In-situ (DCIS)** | 955 = **22 %** | 2.748 = **18 %** | 🟢 |
| invasiv | 3.123 = 73 % | 11.856 = 78 % | 🟢 |
| invasiv ≤10 mm | **29 %** | **36 %** | 🟢 |
| invasiv <15 mm | 49 % | 58 % | 🟢 |
| invasiv ≤20 mm | 72 % | 80 % | 🟢 |
| invasiv nodal-negativ | **76 %** | **82 %** | 🟢 |
| **UICC II+** | **26 %** (Anh. Abb. 27: 26,4 %) | **21 %** (reguläre Folge: 19,6 %) | 🟢 |

DCIS + invasiv summieren nicht auf 100 %: nicht klassifizierbare Fälle liegen im Nenner (Erst 5,0 %,
Folge 3,6 %; Fußnote 6, S. 7) 🟢 — für ein Register-realistisches Modul optional als
`dataAbsentReason`-Variante emittierbar.

> ⚠️ **Nenner-Falle.** Der Anteil nodal-**positiver** Karzinome in Abb. 26 (S. 42) lautet Erst 19,1 % /
> reguläre Folge 13,0 % — das ist **nicht** 100 − 76/82, weil Abb. 26 nur Karzinome *mit bekanntem*
> Lymphknotenstatus im Nenner führt, Tab. 3 dagegen alle invasiven. Beide Zahlen sind korrekt und
> **nicht ineinander umrechenbar**. Im Modul einen der beiden Nenner wählen und dokumentieren.

Historische Baseline zur Einordnung der Screening-Wirkung: DCIS-Anteil in der Zielbevölkerung **vor**
Programmeinführung knapp **7 %** (JB Eval 2023, Kap. 7.1, S. 23) 🟢.

---

## 4. BI-RADS — der PI-RADS-Vergleich trägt nicht, und das ist ein Befund

> 🔴 **Kernbefund dieses Arbeitspakets: Das deutsche MSP erhebt keine BI-RADS-Kategorien.** Die
> Befundung ist **binär** („unauffällig" vs. „Konsensuskonferenz erforderlich"), danach entscheidet die
> Konsensuskonferenz über den Abklärungsbedarf. Die einzige verpflichtende Kategorisierung im Programm
> ist die **B-Klassifikation B1–B5** der Histologie (BMV-Ä Anlage 9.2; BI-RADS kommt im gesamten
> Anlagentext nicht vor). Auch die **S3-Leitlinie v5.0 knüpft in keiner einzigen Empfehlung eine
> Handlungskonsequenz an eine BI-RADS-Kategorie** — der Term erscheint im 497-seitigen Langtext genau
> einmal, als Literaturstelle [262]. Die Leitlinie steuert über **Befundkonstellationen**
> (Herdbefund / Mikrokalk / Dichte / Diskordanz), nicht über eine Suspicion-Skala.

Eine deutsche BI-RADS-Stufenverteilung mit Karzinomraten je Stufe ist damit nicht „zufällig nicht
publiziert", sondern **strukturell nicht erhebbar**. Ebenso wenig existiert eine publizierte deutsche
B1–B5-Verteilung (die Daten werden im MSP erhoben, aber im Jahresbericht nicht als Verteilung berichtet).

**Damit ist Option 1 des Konzepts (§2: BI-RADS als Emissions-Artefakt) nicht nur die pragmatischere,
sondern die einzige fachlich haltbare Wahl** für den Screening-Arm. Die Kaskade wird über die deutschen
Prozess-Kennzahlen gesteuert:

`MSP_Exam → (binär) Recall → Stufe-1-Abklärung → Biopsieindikation → Biopsie → B-Klassifikation → Karzinom`

und der BI-RADS-Wert wird **rückwärts konsistent gesetzt** (BI-RADS 4 bei Biopsieindikation, 5 bei hoher
Malignitätswahrscheinlichkeit). Alle Knoten sind mit Vollerhebungsdaten belegt (§3).

### 4.1 BI-RADS im symptomatischen Arm — dort ist es real im Gebrauch

In der kurativen/symptomatischen Radiologie in Deutschland und Österreich ist ACR BI-RADS 5th ed. per
Fachkonsens etabliert (Müller-Schimpfle et al., RöFo 2016, PMID 27002496; Breast Care 2019, PMID 31798391) 🟢.
Für diesen Arm sind US-Daten der beste verfügbare Ersatz — als **Proxy markiert**:

| Kategorie | ACR-Referenzband | empirischer PPV | Quelle | Conf |
|---|---|---|---|---|
| **BI-RADS 3** | ≤2 % | **1,86 %** kumulativ über 2 J. (810/43.628) | Berg 2020, NMD, PMID 32427557 | 🟡 US-Proxy |
| BI-RADS 3, diagnostisch | | 0,91 % (2.009/220.672) | Elezaby 2022, JACR, PMID 35358482 | 🟡 |
| **BI-RADS 4A** | >2–10 % | **7,6 %** (1.274/16.784) | Elezaby 2018, NMD, PMID 29315061 | 🟡 |
| **BI-RADS 4B** | >10–50 % | **22,0 %** (2.317/10.408) | ebd. | 🟡 |
| **BI-RADS 4C** | >50–95 % | **69,3 %** (2.839/4.099) | ebd. | 🟡 |
| BI-RADS 4 gesamt | | 21,1 % (19.285/91.563) | ebd. | 🟡 |
| **BI-RADS 5** | ≥95 % | **92,9 %** (KI 88–96, n = 156) | Timmers 2012, NL-Screening, PMID 22415412 | 🟡 EU-Proxy |
| BI-RADS 0 (Screening-Recall) | | 14,1 % (KI 12–17, n = 811) | ebd. | 🟡 |

Elezaby 2018 ist mit 125.447 Kategorie-4-Untersuchungen die mit Abstand größte Serie und die belastbarste
Grundlage — Vorbehalt: nur 33,3 % der Kategorie-4-Fälle waren überhaupt subklassifiziert.

**Altersrelevanter Bruchpunkt, der genau im Kohortenfenster liegt** (Lee/Berg/Berg, Radiology 2021,
PMID 33787333, n = 43.628, Median 55 J.) 🟢: die 2-%-Schwelle für BI-RADS 3 wird bei **Baseline**-Befunden
erst ab **59,7 J.** überschritten, bei Befunden **mit Voraufnahme** bereits ab **53,6 J.**
(Baseline-Herdbefund 0,47 % vs. mit Voraufnahme 1,57 %; Baseline-Mikrokalk 0,86 % vs. mit Voraufnahme
**2,80 %**). Das ist der einzige publizierte Wert, der für genau dieses Altersfenster einen Übergang
markiert — falls der symptomatische Arm BI-RADS 3 überhaupt führt.

### 4.2 Biopsie-Pfad (Stanze vs. Vakuum)

Der Methoden-Trigger in Deutschland ist die **Befundart, nicht die Suspicion-Stufe** (S3 v5.0):

| Situation | Verfahren | S3-Empfehlung | Conf |
|---|---|---|---|
| sonographisch sicher darstellbarer Befund (auch primär mammographisch/MRT detektiert) | **sonographisch gesteuerte Stanzbiopsie** | 4.17 (EK) | 🟢 |
| **Mikrokalk ohne Herdbefund** | **röntgengesteuerte Vakuumbiopsie — „soll"** | **4.18 (EG A, LoE 2)** | 🟢 |
| röntgen-/MRT-gesteuert allgemein | Vakuumbiopsie („sollte") | 4.19 (EK) | 🟢 |
| suspekte Lymphknoten | Stanzbiopsie primär | 4.21 (EG A, LoE 2) | 🟢 |
| Mindest-Zylinderzahl | **≥3 Proben bei ≤14 G** | **4.22 (EG B, LoE 2)** | 🟢 |
| histologische Abklärung generell | Stanz-/Vakuumbiopsie; offene Exzisionsbiopsie nur in begründeten Ausnahmefällen | 4.15 (EG A, LoE 2) = Qualitätsindikator QI 2 | 🟢 |

| Arrow | Wert | Basis | Conf |
|---|---|---|---|
| Biopsie → **US-gesteuerte Stanzbiopsie** / stereotaktische **Vakuumbiopsie** | **0.66 / 0.34** | Rückrechnung aus JB Eval 2023 Tab. 1 (unzureichende Biopsien 257 = 1,1 % bzw. 107 = 0,9 %) ⇒ ≈23.400 CNB / ≈11.900 VAB | 🟡 abgeleitet, kein publizierter Direktwert |
| Malignitätsanteil **US-Stanzbiopsie**, reguläre Folge / Erstunters. | **0.812 / 0.473** (B:M = 1:4,3 bzw. 1:0,9) | JB QS 2023, S. 38 | 🟢 |
| Malignitätsanteil **Rö-Vakuumbiopsie**, reguläre Folge / Erstunters. | **0.493 / 0.296** (B:M = 1:1 bzw. 1:0,4) | ebd. | 🟢 |
| Biopsie unzureichend (Wiederholung) | 0.011 (CNB) / 0.009 (VAB) | JB Eval 2023, Tab. 1 | 🟢 |

Die B:M-Verhältnisse beziehen sich auf *durchgeführte Biopsien je Methode*, PPV II dagegen auf *Frauen mit
Biopsieindikation* — **nicht ineinander umrechenbar** (Mehrfachbiopsien, nicht durchgeführte Biopsien,
B3-Befunde). Als zwei getrennte Kalibrieranker behandeln.

### 4.3 B-Klassifikation und Upgrade-Raten

S3 v5.0 Kap. 10.2.4.7, Tab. 31 definiert B1–B5 (B5a in situ, B5b invasiv, B5c unklar, B5d andere
Histogenese). Eine deutsche Verteilung ist nicht publiziert 🔴. Verfügbare Upgrade-Raten:

| Arrow | Wert | Basis | Conf |
|---|---|---|---|
| **B3 → Malignität** (gepoolt) | **0.17** (KI 0,15–0,19; 2.160/11.423, 129 Studien) | Forester 2019, EJSO, PMID 30579653 | 🟢 (international) |
| B3 mit / ohne Atypie | 0.347 / 0.136 | ebd. | 🟢 |
| B3 nach CNB / nach VAB | 0.190 / 0.149 | belgische Nationalkohorte, Clin Breast Cancer 2023 | 🟡 |
| **ADH in Stanzbiopsie → Malignität** | **0.28–0.56** ⇒ offene PE **soll** (S3 4.38) | S3 v5.0 [393]–[397] | 🟢 |
| ADH in Vakuumbiopsie | 0.209 | S3 v5.0 [399] | 🟢 |
| FEA nach VAB / nach Stanze | 0.09 / 0.05; Metaanalyse 0.075 (3 % invasiv) | S3 v5.0 [431],[432],[434] | 🟢 |
| klassische LN (ALH/LCIS), inzidentell + konkordant | ≤0.02 übersehenes Ca in 3–5 J. ⇒ keine weitere Biopsie (S3 4.39) | S3 v5.0 [384],[411] | 🟢 |
| benignes / atypisches Papillom | 0.057 / 0.369 | S3 v5.0 [431],[442] | 🟢 |
| **DCIS in CNB → invasiv im Exzidat** | **0.259** (KI 0,225–0,295; 1.736/7.350, 52 Studien); 14 G 0,303 vs. 11 G VAB 0,189 | Brennan 2011, Radiology, PMID 21493791 | 🟢 (international) |

Der DCIS→invasiv-Upgrade ist für das DCIS-Ast des Moduls direkt relevant: rund ein Viertel der bioptisch
als DCIS klassifizierten Fälle wird am Operationspräparat invasiv. Das rechtfertigt eine
**Reklassifizierungs-Transition** vom DCIS-Ast in den invasiven Ast nach der Operation.

---

## 5. Intervallkarzinome

### 5.1 Programmsensitivität

| Größe | Wert | Basis | Conf |
|---|---|---|---|
| **PS, Folgescreenings, national** | **69,9 % (KI 67,3–72,0) – 71,7 % (KI 69,5–73,9)** | **Heinze** 2023, BMC Cancer 23:855, PMID **37697304** / PMC10496211. BARMER, 1.992.287 Folgescreenings, 50–69 J., 2010–2016 | 🟢 |
| PS, Erstscreenings (zum Vergleich) | 78,2 % | Heidinger 2015, The Breast, PMID 25687106. NRW, 838.579 Erstteilnehmerinnen | 🟢 |
| **PS bei 50–54 J.** | **72,1 %** (65–69: 82,4 %; p-Trend <0,0001) | ebd. | 🟢 |
| PS bei 50–54, nur **invasive** Karzinome | **67,7 %** (invasiv-lobulär 62,8 %; DCIS >90 % in allen Bändern) | ebd. | 🟢 |
| PS nach Brustdichte | ACR 1: 88,8–100 % · ACR 2: 83,2–85,7 % · ACR 3: 72,9–80,7 % · **ACR 4: 50 %** (ACR 4 bei <7 %) | Weigel 2017, Eur Radiol, PMID 27822617 | 🟢 |

> **Für ein 50–60-Modell heißt das: die schlechteste Sensitivität des ganzen Programms.** Rund **72 %**
> gesamt, **68 %** für invasive Karzinome. Die oft zitierten 78–80 % sind **Erstrunden**-Werte und für
> eine Dauerteilnehmerinnen-Kohorte zu optimistisch. Empfohlener Modellwert für 50–60:
> **PS = 0.72** 🟡 (Heidinger-Bandwert 50–54, auf 50–60 extrapoliert; für 55–59 ist der Bandwert im
> Elsevier-Volltext vorhanden, aber nicht frei zugänglich — §9).

### 5.2 Zeitverteilung im 24-Monats-Intervall

Sehr robust über alle deutschen Regionen und Jahrgänge (KoopMammo JB Eval 2018 Tab. 4–5 S. 30–31 und
JB Eval 2022 Tab. 4–6 S. 29–31; Heinze 2023; Heidinger 2012, PMID 23264826):

| Arrow (`Interval_Timing`) | Wert | Basis | Conf |
|---|---|---|---|
| Intervallkarzinom in **Monat 1–12** | **0.32** | Ratenverhältnis 0,6–0,8 vs. 1,3–1,4 je 1.000 (Heinze 2023); regional 27–37 %, Median ~32 % | 🟢 |
| Intervallkarzinom in **Monat 13–24** | **0.68** | ebd. | 🟢 |
| Feinere Monatsverteilung | — | **nicht publiziert, für kein europäisches biennales Programm** | 🔴 |

Regionale Belege für den 32/68-Split (Rate je 10.000 screen-negative Untersuchungen, Jahr 1 / Jahr 2):
NRW 2005–2008 7,4/15,7 · NRW 2012 6,4/13,2 · Niedersachsen 2006–2008 7,6/16,2 · Niedersachsen 2009–2011
7,2/13,3 · HH+HB+NDS 2016–2019 5,7→4,6 / 12,1→10,9 · Bayern 2016–2020 5,1–6,1 / 10,3–11,6 · Hessen
2016–2019 4,3–6,3 / 11,0–12,6. **Anteil Jahr 1 durchgängig 27–37 %.** 🟢

Umsetzungsempfehlung: eine **monoton steigende, stückweise konstante Jahresrate** über die zwei
Delay-Schritte, verankert auf 32/68. Alles Feinere ist Modellannahme, nicht Evidenz 🔴. Der einzige
verfügbare Innerjahres-Hinweis ist ein US-Proxy mit *jährlichem* Screening (PMC12342771, 148 IC:
28 % / 36 % / 36 % über die Drittel eines 12-Monats-Intervalls) — legt einen relativ flachen Anstieg
*innerhalb* eines Jahres mit dem Sprung *zwischen* den Jahren nahe 🔴.

### 5.3 Absolute Rate und Anteil

| Größe | Wert | Basis | Conf |
|---|---|---|---|
| IC-Rate 24 Mon., **50–59 J.** | **21,0 / 10.000** screen-negative | Heidinger 2012, PMID 23264826 | 🟢 |
| IC-Rate 24 Mon., 60–69 J. | 25,8 / 10.000 | ebd. | 🟢 |
| IC-Rate 24 Mon., aktuell (2016–2020, alle Bänder) | 12,6–17,8 / 10.000 | KoopMammo JB Eval 2022 | 🟢 |
| **IC-Anteil an allen Ca unter Teilnehmerinnen (Folgerunden)** | **0.25–0.28** | Heinze 2023: 27,6 % (4.158/14.074); Bokhof 2018 PMID 30421287: Folgescreening 2011 NRW 28,1 % / NDS 25,1 % | 🟢 |
| IC-Anteil, Erstrunde | 0.15–0.22 | Bokhof 2018 (Erstscreening 2011: NRW 19,5 %, NDS 15,3 %); Heidinger 2015: 21,8 % | 🟢 |
| EU-Benchmark (Anteil an Hintergrundinzidenz) | Jahr 1 22–27 % (Ziel <30 %) ✅ · Jahr 2 41–58 % (Ziel <50 %) teils verfehlt | Urbschat/Heidinger 2014, PMID 24357175 | 🟢 |
| IC-Ätiologie-Mix | echt 53,4 % · minimal signs 19,5 % · falsch-negativ 15,6 % · radiologisch okkult 11,4 % | **Byng 2022**, Eur J Radiol, PMID 35512511, n = **2.396** deutsche IC | 🟢 |

> ⚠️ **Eine intuitive Annahme des Konzepts ist falsch.** §1.1 begründet einen höheren Intervallanteil bei
> 50–54 mit „dichterem Drüsengewebe jüngerer Frauen". Die **absolute** IC-Rate ist bei 50–59 aber
> **niedriger** (21,0/10.000) als bei 60–69 (25,8/10.000), weil die Hintergrundinzidenz mit dem Alter
> steigt. Der Dichte-Effekt wirkt auf den **relativen Anteil** (PS 72,1 % vs. 82,4 %), nicht auf die
> Absolutrate. Die Richtung der Verzerrung im Konzept stimmt für den Anteil, die Begründung über die
> Absolutzahl nicht.

Zur Tumorbiologie (nur soweit sie den Detektionsmodus konditioniert; Details in AP B): Braun 2018
(PMID 30149831) ist bestätigt und wird durch **Prange 2019** (Rofo, PMID 30103233, Münster, 53.375
Untersuchungen) ergänzt — TNBC-Anteil an invasiven Karzinomen **5,9 % screen-detektiert vs. 12,7 %
Intervall** (abgeleitet aus den Zählungen) 🟢, und 77,4 % aller „aggressiven" (HER2+ oder TNBC) Karzinome
werden trotzdem im Screening entdeckt.

---

## 6. Symptomatischer Pfad

### 6.1 Erstsymptome

Hier klaffen deutsche und britische Zahlen auseinander, und der Grund ist methodisch:

| Symptom | 🇩🇪 DE, symptomatische BC-Patientinnen | 🇬🇧 UK-Proxy, alle BC-Patientinnen | 🇬🇧 UK-Proxy, Brustsprechstunde (alle Frauen) | Conf |
|---|---|---|---|---|
| **Tastbefund / Knoten** | **66,9 %** | **83 %** | 61,9 % | 🟡 |
| Mamillenauffälligkeit / -sekretion | (in „andere" enthalten) | 7 % | 4,4 % | 🟡 |
| Brustschmerz | (in „andere" enthalten) | 6 % | **18,2 %** | 🟡 |
| andere Brustsymptome (Einziehung, Hautödem, Orangenhaut, Blutung) | **29,6 %** | — | 15,4 % | 🟡 |
| Nicht-Brust-Symptome | <4 % | 1,3 % | — | 🟡 |

Quellen: **Arndt 2002**, Br J Cancer 86:1034-40, PMID 11953844 (VERDI, Saarland, n = 287, Ø 57,3 J.,
1996–98, Face-to-face-Interviews) 🟢 für DE · **Koo 2017**, Cancer Epidemiol 48:140-6, PMID **28549339**
(England, n = 2.316) 🟡 · **Dave 2022**, Br J Gen Pract 72:e234-43, PMID 34990395 (Manchester,
n = 10.830 konsekutive Zuweisungen) 🟡.

> ⚠️ **Die ~80 % des Konzepts sind ein UK-Wert und beziehen sich auf die falsche Grundgesamtheit.**
> Drei verschiedene Nenner werden in der Literatur regelmäßig vermischt: (a) Symptomverteilung **unter
> Karzinompatientinnen** (Koo: 83 % Knoten), (b) Symptomverteilung **in der Sprechstunde** (Dave: 62 %
> Knoten — Schmerz ist dort 3× häufiger, weil Schmerz kaum je Krebs ist), (c) deutsche
> Symptomatiker-Kohorte der Prä-Screening-Ära (Arndt: 66,9 %).
> **Für das Modul ist (b) der richtige Nenner am Eingang des symptomatischen Arms und (a) der richtige
> am Ausgang.** Vorschlag: Eingangsverteilung Knoten **0.62** / Schmerz **0.18** / Mamille **0.04** /
> sonstiges **0.16** 🟡 (UK-Proxy), weil eine deutsche Sprechstunden-Serie nicht existiert (§9).

### 6.2 Karzinomwahrscheinlichkeit bei symptomatischer Vorstellung

**Gathani 2023**, BMJ 381:e073269, PMID 37100445 — England, NCRAS, **alle 576.742** Brust-Zuweisungen
2019–20. Das ist die einzige Quelle mit sauberer Altersstratifizierung 🟡 (UK-Proxy):

| Alter | dringliche Zuweisung (2WW) | Routine-Zuweisung | kombiniert |
|---|---|---|---|
| 40–49 | 3,9 % | 1,4 % | 3,3 % |
| **50–59** | **5,4 %** (4.107/75.403) | **1,8 %** (418/23.405) | **4,6 %** |
| 60–69 | 8,4 % | 2,4 % | 7,0 % |
| ≥80 | 30,9 % | 11,2 % | 26,8 % |

| Arrow | Wert | Basis | Conf |
|---|---|---|---|
| `Symptomatic_Presentation` → Karzinom, 50–60 | **0.046** (dringlich allein 0.054) | Gathani 2023 | 🟡 UK-Proxy |
| Karzinom bei **Tastbefund**, 40–73 J. | **0.068** | Dave 2022, PMID 34990395 | 🟡 |
| Karzinom bei **Brustschmerz allein**, 40–73 J. | **0.004** (OR 0,05 gegen Knoten, adjustiert) | ebd. | 🟡 |
| Karzinom bei Mamillenbeschwerde, 40–73 J. | 0.060 | ebd. | 🟡 |
| Biopsierate bei Tastbefund | 0.18, davon 29 % maligne | ebd. | 🟡 |

**PPV einzelner Symptome, Altersband 50–59** (Walker 2014, Br J Gen Pract 64:e788-93, PMID 25452544;
CPRD-Primärversorgung, 3.994 Fälle / 16.873 Kontrollen, Abb. 2) 🟡 UK-Proxy:

| Symptom | PPV 50–59 | (40–49) | (60–69) |
|---|---|---|---|
| **Brustknoten** | **8,5 %** (KI 6,7–11) | 4,8 % | 25 % |
| Mamilleneinziehung | 2,6 % | n. b. | 3,4 % |
| Mamillensekretion | 2,1 % (KI 0,81–5,1) | 1,2 % | 2,3 % |
| Brustschmerz | 0,80 % (KI 0,52–1,2) | 0,17 % | 1,2 % |

> **Antagonistische Interaktion, die ein naives Modell falsch abbilden würde:** Knoten × Schmerz
> OR **0,13** (p = 0,002), Knoten × Sekretion OR **0,02** (p = 0,001) — **schmerzhafte Knoten sind
> *weniger* prädiktiv als schmerzlose.** Wer die Symptom-PPVs multiplikativ kombiniert, dreht das
> Vorzeichen. Empfehlung für v1: **nur das führende Symptom** ziehen und dessen PPV verwenden 🟡.

### 6.3 Delay

| Größe | Wert | Basis | Conf |
|---|---|---|---|
| Patientenintervall (Symptom → Erstkonsultation), Median | **16 Tage**; >3 Mon. bei 17,4 % | Arndt 2002, PMID 11953844 | 🟡 (Prä-MSP-Ära) |
| … nach Alter | <50 J. 7,1 % >3 Mon. vs. >65 J. 24,7 % (p-Trend 0,01) | ebd. | 🟡 |
| Providerintervall (Erstvorstellung → Therapiebeginn), Median | **15 Tage**; >3 Mon. bei 11 % | Arndt 2003, JCO 21:1440-6, PMID 12697864 | 🟡 |
| Größenordnung heute (Proxy) | medianes Diagnoseintervall Mammakarzinom **13 Tage** | Martins 2025, Br J Gen Pract, PMID 39689922 (England, n = 70.971) | 🟡 |

Beide deutschen Werte stammen aus **1996–98, also vor Einführung des MSP**. Für v1 vertretbar (die
Größenordnung deckt sich mit dem englischen Gegenwartswert), aber als Ära-Vorbehalt zu führen.

---

## 7. Detektionsmodus-Marginale — die tragende Änderung

Das Konzept setzt 45 / 11 / 44 aus **Braun 2018** (Münster, n = 1.531). Es gibt eine 45-fach größere,
methodisch sauberere deutsche Quelle:

**Buschmann L, Wellmann I, Bonberg N, Wellmann J, Hense HW, Karch A, Minnerup H.** *BMC Med* 2024;22:43,
PMID **38287392** / PMC10826012 — **Krebsregister NRW**, alle Frauen 50–69 mit inzidentem C50 2006–2014,
Follow-up bis 31.12.2018, **n = 68.230**.

| Detektionsmodus | 2006–2014 gesamt | **2014 allein** | T1-Anteil | BC-Tod im FU |
|---|---|---|---|---|
| screen-detektiert | 35,8 % | **44,2 %** | 73,8 % | 4,3 % |
| **Intervallkarzinom** | 11,4 % | **17,7 %** | 42,6 % | 11,3 % |
| Nicht-Teilnehmerin | 52,8 % | **38,1 %** | 39,6 % | 19,1 % |

Der Gesamtperiodenwert ist durch die Rollout-Jahre 2006–2009 nach unten verzerrt; für ein
Steady-State-Modell sind die **2014er-Werte** zu nehmen.

| Arrow (`bc_detection_mode`) | **empfohlen** | Konzept | Basis | Conf |
|---|---|---|---|---|
| screen-detektiert (MSP) | **0.44** | 0.45 | Buschmann 2024, NRW 2014 | 🟡 (ein Bundesland, Quelle 50–69) |
| **Intervallkarzinom** | **0.18** | 0.11 | ebd. | 🟡 |
| symptomatisch / Nicht-Teilnehmerin | **0.38** | 0.44 | ebd. | 🟡 |

**Warum das nicht nur „eine größere Studie" ist — die interne Konsistenzprüfung entscheidet.**
Der Intervallanteil *unter Teilnehmerinnen* ist bei diesem Split 17,7 / (44,2 + 17,7) = **28,6 %**,
implizierte Programmsensitivität **71,4 %**. Das deckt sich mit **Heinze 2023 (27,6 % IC-Anteil,
PS 69,9–71,7 %)** aus einer völlig unabhängigen Datenquelle (BARMER-Abrechnungsdaten) 🟢.
Der Konzeptsplit 45/11 ergibt dagegen 11/56 = **19,6 %**, implizierte **PS 80,4 %** — das ist der
Erstrunden-Wert von Heidinger 2015 und für eine Dauerteilnehmerinnen-Kohorte im Fenster 50–60
nachweislich zu optimistisch. **Der 45/11/44-Split ist mit der Programmsensitivität, die dasselbe Modul
in §5 verwendet, nicht vereinbar.**

**Richtung der Verzerrung für 50–60** (unverändert 🔴, keine deutsche Quelle publiziert den Detektionsmix
nach Altersband): Verschiebung **weg vom Screening**, weil die Hintergrundinzidenz im Fenster niedriger
ist (§1) und die Programmsensitivität bei 50–54 am schlechtesten (§5.1). Das spricht dafür, den
Intervallanteil eher am oberen Rand anzusetzen. Der 44/18/38-Split bleibt trotzdem der **Startwert**, nicht
die gesetzte Größe — er ist der Kalibrier-Kandidat für `synthea-eu-cancer-51w`.

**Vorzugsweise gar nicht setzen, sondern erzeugen.** Die sauberste Umsetzung besteht darin, den
Detektionsmodus **aus der Teilnahme-Markov-Kette (§2) plus PS (§5.1) plus CDR (§3.2) emergieren zu lassen**
und den 44/18/38-Split nur als **Validierungsziel** zu verwenden. Damit ist der Modus eine abgeleitete,
keine gezogene Größe — dasselbe Argument, mit dem §3.2 des Konzepts den Subtyp aus den Biomarkern ableitet
statt ihn zu ziehen. Der resultierende Mix ist dann automatisch konsistent mit den Erstrunden-Effekten
des schmalen Fensters.

Braun 2018 bleibt unverzichtbar — aber für die **bedingten** Verteilungen (§1.3 des Konzepts: DCIS-Anteil,
T-Stadium, N-Status, Grading, Subtyp je Detektionsmodus), nicht für die Marginale. Das ist die Tabelle,
die Buschmann so nicht liefert.

---

## 8. Hochrisiko-Arm — schlank, mit korrigierter Bezugsgröße

### 8.1 gBRCA1/2-Prävalenz

| Bezugsgruppe | Wert | Basis | Conf |
|---|---|---|---|
| **unter Brustkrebs-Patientinnen** (unselektiert) | **2,15 %** (BRCA1 0,85 % + BRCA2 1,29 %) | **CARRIERS**, Hu/Hart 2021, NEJM 384:440-451, PMID 33471974, n = **32.247** | 🟢 |
| dito, unabhängige Bestätigung | **2,10 %** (BRCA1 0,85 % + BRCA2 1,25 %) | **BRIDGES/BCAC**, Dorling 2021, NEJM 384:428-439, PMID 33471991, n = **60.466** | 🟢 |
| dito, rein registerbasiert | 1,80 % | LIBRO-1, Li 2018, PMID 30175445, **Schweden**, n = 5.099 | 🟢 |
| **in der Allgemeinbevölkerung** (Frauen ohne BC) | **0,353 %** (BRCA1 0,114 % + BRCA2 0,240 %) | CARRIERS-Kontrollen, n = **32.544** | 🟢 |
| dito, unabhängige Bestätigung | **0,361 %** (BRCA1 0,108 % + BRCA2 0,253 %) | BRIDGES-Kontrollen, n = **53.461** | 🟢 |
| Deutschland, **selektiert** nach Familienanamnese (GC-HBOC) | 24,0 % (KI 23,4–24,6) | Kast 2016, J Med Genet, PMID 26928436, 21.401 Familien | 🟢 |

Zwei Kohorten mit zusammen >90.000 Fällen und >86.000 Kontrollen stimmen auf 0,05 bzw. 0,01
Prozentpunkte überein. Der klassisch zitierte Bereich **1:400–1:800 (0,125–0,25 %) ist zu niedrig** —
er stammt aus Segregationsanalysen der 1990er; die Sequenzierdaten liegen konsistent bei ~0,35 %.
**Die 2:1-Dominanz von BRCA2 über BRCA1 ist stabil** und im Fenster 50–60 sogar noch ausgeprägter, weil
BRCA2-Trägerinnen im Mittel 5–8 Jahre später erkranken (CARRIERS: mittleres Diagnosealter BRCA1 50,3–50,9 J.,
BRCA2 55,4–58,6 J.) 🟢.

> 🔴 **Der `bc_high_risk = 0.02` des Konzepts braucht eine Bezugsgrößen-Entscheidung.** 2,1 % gilt
> **unter Brustkrebs-Patientinnen**. Synthea setzt das Attribut aber im `Initial`-Bereich, also auf
> **Populationsebene** — dort wären es **0,35 %**, ein Faktor 6.
>
> **Empfehlung:** `bc_high_risk` mit **0.0035** auf Populationsebene setzen und den erhöhten
> Erkrankungs-Hazard der Trägerinnen im Modul separat abbilden, sodass sich die 2,1 % unter den
> Erkrankten **ergeben**. Das ist mehr Arbeit, aber es ist die einzige Variante, bei der die Kohorte
> *beide* publizierten Marginalen trifft. Wird stattdessen 0.02 auf Populationsebene gesetzt, muss die
> Einschränkung explizit in `README.md`: **die Kohorte überschätzt den BRCA-Anteil in der
> Nicht-Erkrankten-Population um Faktor 6** — vertretbar für ein Demo-Dataset, tödlich für jede
> Prävalenzauswertung.

Altersband 50–59 direkt: **existiert nicht.** Keine der vier Großkohorten publiziert eine nach Altersband
stratifizierte Prävalenztabelle 🔴. Belegt ist nur die Richtung (CARRIERS wörtlich: *„decreased rapidly
after age 40 years"*; BRIDGES: OR fällt signifikant mit dem Alter, p<0,01) sowie der LIBRO-1-Anker
(**26,0 % der BRCA1-** und **33,3 % der BRCA2-**Trägerinnen sind bei Diagnose ≥60 J., gegen ~50 % der
Nicht-Trägerinnen) 🟢. Interpolierte Spanne für das Band 50–59 unter BC-Patientinnen: **1,5–2,2 %** 🔴.

### 8.2 Intensivierte Früherkennung (IFNP)

| Größe | Wert | Basis | Conf |
|---|---|---|---|
| **Detektionsrate im IFNP** (Kennzahl 1, Quote „Pat. Gesamt") | **1,5 %** | DKG/OnkoZert Jahresberichte FBREK — Zeitreihe unten | 🟢 |
| Programmsensitivität IFNP | **89,6 %** (KI 84,9–93,0) | **Bick 2019**, Breast Cancer Res Treat 175:217-228, PMID 30725383, n = 4.573 / 14.142 Runden | 🟢 |
| Anteil Stadium 0 oder I | **84,5 %** (174/206) | ebd. | 🟢 |
| dito, Registerbestätigung | 82,3 % (2024) / 80,9 % (2023) / 83,3 % (2022) | FBREK Kennzahl 3 | 🟢 |
| DKG-zertifizierte FBREK-Zentren | **24** (Stand 31.12.2025; 2023: 17) | FBREK JB 2026, S. 5 | 🟢 |
| Anteil BC-Patientinnen mit Checklisten-Score ≥3 | **30,4 %** | Rhiem 2019, Breast J 25:455-460, PMID 30953388, n = 5.091 | 🟢 |
| Frauen 50 bis <60 in DE (Nenner) | **5.920.445** (31.12.2024) | Destatis 12411-0006, Basis Zensus 2022 — Details und Bezugsjahr-Warnung in **§1.2** | 🟢 |

**Kennzahl 1 im Zeitverlauf** — Definition: *invasives Karzinom und/oder DCIS binnen 6 Monaten nach auffälliger
Bildgebung*; Nenner = Personen im IFNP mit Bildgebung im Vor-Kennzahlenjahr:

| Kennzahlenjahr | Quote „Pat. Gesamt" | Zähler / Nenner | Zentren | Bericht |
|---|---|---|---|---|
| 2021 | **1,60 %** | 168 / 10.487 | 16 | FBREK 2023 |
| 2022 | **1,33 %** | 151 / 11.358 | 17 | FBREK 2024 |
| 2023 | **1,53 %** | 226 / 14.791 | 23 | FBREK 2025 |
| 2024 | **1,5 %** | 255 / 16.935 | 24 | FBREK 2026 (nur noch 1 Nachkommastelle) |

> ⚠️ **Zwei Fallen in dieser Zeitreihe.** (1) Eine **Sollvorgabe existiert erst ab Bericht 2025**
> (Begründungspflicht bei <1 % / >4 %); die Werte davor sind unregulierte Beobachtungswerte, kein
> erfüllter Qualitätsindikator. (2) **Median und Quote „Pat. Gesamt" laufen 2022→2023 gegenläufig**,
> weil die Zentrenzahl von 17 auf 23 sprang — die beiden Größen dürfen im Zeitvergleich **nie gemischt**
> werden. Das Konzept nennt 1,53 % (KZJ 2023); als Modellwert ist **1,5 %** die ehrlichere Angabe, weil
> die Schwankung 1,33–1,60 % über vier Jahre größer ist als jede Nachkommastelle. Die im Draft zuvor
> geführten „1,51 %" waren eine Eigenrechnung aus 255/16.935 — der Bericht selbst rundet auf 1,5 %,
> und diese Scheingenauigkeit ist gestrichen.
>
> Der FBREK-Bericht 2023 ist nur noch direkt abrufbar unter
> `onkozert.de/wordpress/wp-content/uploads/2023/09/qualitaetsindikatoren_fbrek_2023-A1_230914.pdf`.

> **Rechtsgrundlagen-Korrektur, die das Konzept betrifft:** Es gibt **keinen G-BA-Beschluss und keine
> G-BA-Richtlinie** zur intensivierten Früherkennung bei familiärem Brust-/Eierstockkrebs. Positiv
> verifizierter Negativbefund: die KFE-RL (Fassung 18.12.2025) enthält im normativen Teil keinen Treffer
> für „familiär", „erblich", „BRCA" oder „genetisch". Grundlage sind **Selektivverträge nach § 140a SGB V**
> (vdek seit 2008, Open-House seit 2018, Überarbeitung 2024; 19 der 24 Zentren nehmen teil) — so auch
> wörtlich in der S3-Leitlinie, Kap. 3.3. 🟢

> **Und die für das Kohortenfenster entscheidende Regel:** Die IFNP-Einschlusskriterien (S3 Empf. 3.35)
> lauten (1) nachgewiesene Klasse-4/5-Variante in einem der 13 Kerngene **oder** (2) Frauen **30–50 J.**
> aus nicht-informativ getesteten Familien mit 10-Jahres-Risiko >5 %. **Kriterium 2 endet mit dem 50.
> Lebensjahr.** Im Fenster 50–60 verbleiben im IFNP also praktisch **nur nachgewiesene
> Variantenträgerinnen** — der Hochrisiko-Arm ist dort strukturell schmaler, als das Konzept unterstellt.
> Das ist ein zusätzliches Argument für die Minimalvariante §1.4.1 🟢.

**Anteil der Frauen 50–60 in dokumentierter Hochrisiko-Versorgung: ~0,06–0,09 %** 🔴 — abgeleitet, indem
20–30 % der 16.935 IFNP-Teilnehmerinnen dem Band 50–59 zugerechnet werden (der Altersaufbau des IFNP ist
**nicht publiziert**; die 20–30 % sind eine Annahme, gestützt darauf, dass der Nicht-Trägerinnen-Arm bei
50 J. endet). Zwischen den 0,35 % Trägerinnen und den 0,06–0,09 % Versorgten liegt Faktor 4–6 — das ist
die dokumentierte Unterdiagnostik-Lücke (Versorgungskonzept FBREK 2022: *„erst für rund die Hälfte der
familiär belasteten Frauen ist die genetische Ursache bekannt"*).

**Konsequenz für v1:** Der Arm bleibt schlank wie entschieden. Die drei Größen, die er treffen muss, sind
**PS 89,6 %**, **84,5 % Stadium 0/I** und **Detektionsrate 1,5 %** — alle drei 🟢 und alle drei aus
deutschen Quellen. Der Subtyp-Skew und die Genetik-Observation gehören in AP B.

---

## 9. Offene Datenlücken

Nach Schwere sortiert. Punkte 1–3 blockieren keine Modellierung, aber jede Zahl, die auf ihnen ruht,
bleibt dauerhaft 🔴.

1. **Screening-Teilnahme nach Altersband.** KoopMammo stratifiziert die Teilnahmerate ausschließlich nach
   Einladungsart und Bundesland; Einladungszahlen je Altersband werden nicht publiziert. Die Markov-Kette
   (§2) ist deshalb notwendig altersunabhängig. *Beschaffbar?* Vermutlich nur über eine Datenanfrage bei
   der Kooperationsgemeinschaft Mammographie.
2. **Detektionsmodus-Mix nach Altersband.** Weder Braun 2018 noch Buschmann 2024 schlüsseln nach
   5-Jahres-Bändern auf. Der 44/18/38-Split ist damit eine 50–69-Zahl, die auf 50–60 übertragen wird —
   das ist die größte verbleibende Unsicherheit im Eintrittsteil. Die *Richtung* der Verzerrung ist
   bekannt (weniger Screening, mehr Intervall), die *Größe* nicht.
3. **Deutsche BI-RADS-Stufenverteilung mit Karzinomrate je Stufe.** Existiert nicht und ist strukturell
   nicht erhebbar, weil das MSP binär befundet. Ebenso wenig eine publizierte deutsche
   **B1–B5-Verteilung** (Daten werden erhoben, nicht als Verteilung berichtet). Ersatz: US-NMD-Werte,
   klar als Proxy geführt, und der symptomatische Arm als einziger BI-RADS-Träger.
4. **Deutsche Brustsprechstunden-Serie mit altersstratifizierter Karzinomausbeute.** Existiert nicht.
   Alle Zahlen in §6.2 sind UK-Proxy mit strukturell anderem Zuweisungssystem (GP-Gatekeeping und
   NICE-3-%-Schwelle gegen deutschen Direktzugang zum Gynäkologen). Die Übertragbarkeit ist
   **nicht geprüft** und vermutlich der schwächste Punkt des symptomatischen Arms.
5. **Monatsverteilung der Intervallkarzinome** innerhalb der 24 Monate — für kein europäisches biennales
   Programm publiziert. Nur der Jahr-1/Jahr-2-Split (32/68) ist belegt.
6. **Programmsensitivität für die Bänder 55–59 und 60–64** — in Heidinger 2015 vorhanden, Elsevier-Volltext
   nicht frei zugänglich. Nur 50–54 (72,1 %), 65–69 (82,4 %) und gesamt (78,2 %) sind aus dem Abstract
   verfügbar. *Beschaffbar?* Ja, über Bibliothekszugang — lohnt sich, weil es genau das Kohortenfenster trifft.
7. **BRCA-Prävalenz nach Altersband** bei BC-Patientinnen. Keine der vier Großkohorten publiziert die
   Tabelle. Die Spanne 1,5–2,2 % für 50–59 bleibt Interpolation.
8. **Altersaufbau der IFNP-Population.** Nicht publiziert; die 20–30 %-Annahme in §8.2 ist ungestützt.
9. **Nationale altersband-genaue DCIS-Raten.** KID 2025 Tab. 3.29.1 gibt für D05 bewusst keine
   Alterskurve. Ersatz sind ECIS-Registermediane aus 7 Landesregistern (🟡, drei Register liefern kein D05).
10. **Deutsche Patienten-/Systemintervalle nach 2010.** Die einzigen deutschen Zahlen (Arndt 2002/2003)
    stammen aus 1996–98, also vor dem MSP.
11. **S3-Versionsstand.** Der lokale AWMF-Korpus hat v5.0 (Dez. 2025), das Konzept zitiert v5.1 (Juni 2026).
    Alle Empfehlungsnummern hier sind gegen v5.0 verifiziert.
12. **TOSYMA** (Tomosynthese + synthetische 2D gegen FFDM, ~80.000 Frauen, DE; Protokoll PMID 29764880) —
    der Intervallkarzinom-Endpunkt ist noch nicht publiziert. Er wird §5 ändern, sobald er erscheint.

---

## 10. Quellenverzeichnis (Eintritt & Detektion)

**Register und Programmberichte**
- Zentrum für Krebsregisterdaten im RKI, Datenbankabfrage, www.krebsdaten.de/abfrage, Stand 19.11.2025 (Fälle bis 2023)
- *Krebs in Deutschland für 2021–2023*, 15. Ausgabe, RKI + GEKID, Berlin 2025, ISBN 978-3-89606-334-2, DOI 10.25646/13129 — Kap. 3.17 (Tab. 3.17.1 S. 72, Abb. 3.17.4 S. 74), Kap. 3.29 (Tab. 3.29.1 S. 133)
- Kooperationsgemeinschaft Mammographie, **Jahresbericht Evaluation 2023** — g-ba.de/downloads/17-98-5975/KOOPMAMMO_Jahresbericht_Eval_2023_web.pdf (Tab. 1 S. 7 · Tab. 2 S. 19 · Tab. 3 S. 23 · Tab. 4 S. 33 · Tab. 5 S. 34 · Kap. 9.2 S. 36 · Kap. 9.3 S. 38 · Anh. Abb. 4/20/21/25/27 S. 57–60)
- Kooperationsgemeinschaft Mammographie, **Jahresbericht Qualitätssicherung 2023** — admin.mammo-programm.de/assets/27e3314d-1e99-41a0-b10a-b0c2cf4be549
- Kooperationsgemeinschaft Mammographie, Jahresberichte Evaluation **2018** (Tab. 4–5 S. 30–31) und **2022** (Tab. 4–6 S. 29–31) — Intervallkarzinom-Zeitreihen
- DKG/OnkoZert, **Jahresberichte FBREK 2023/2024/2025/2026**, Kennzahlen 1/3/5/7 — der Bericht 2023 nur noch unter onkozert.de/wordpress/wp-content/uploads/2023/09/qualitaetsindikatoren_fbrek_2023-A1_230914.pdf
- G-BA Beschluss 21.09.2023 (6183), Erweiterung der Altersgrenzen auf 50–75, iK 01.07.2024; G-BA KFE-RL Fassung 18.12.2025 (Negativbeleg zur IFNP)
- ECIS Data Explorer API (ecis.jrc.ec.europa.eu), Entity 34/35, deutsche Landesregister, 2023
- Tumorregister München, Basisstatistiken C50 / D05 Frauen, Stand 20.12.2021
- **Destatis 12411-0006** (Fortschreibung des Bevölkerungsstandes, Basis Zensus 2022), Frauen 50 bis <60, Stichtag 31.12.2024 = 5.920.445 — GENESIS-API nicht anonym abrufbar, verifiziert über Destatis-Bevölkerungspyramide (5.920,4 Tsd.) **und** Eurostat `demo_pjan` (Einzeljahrgangs-Summe, deckungsgleich)

**Leitlinie**
- S3-Leitlinie Mammakarzinom, **AWMF 032-045OL, Version 5.0**, Langversion, Dezember 2025, AWMF-Freigabe 23.01.2026 — Empf. 3.16/3.19/3.23/3.27/3.35, 4.15–4.24, 4.38–4.43, Kap. 3.3, Kap. 10.2.4.7 Tab. 31, QI 2
- BMV-Ä Anlage 9.2 Mammographie-Screening (KBV)

**Primärliteratur**
- Buschmann L et al. *BMC Med* 2024;22:43. **PMID 38287392** — Detektionsmodus, NRW, n = 68.230
- Heinze F, Czwikla J, Heinig M, Langner I, Haug U. *BMC Cancer* 2023;23:855. **PMID 37697304** — Programmsensitivität, BARMER
- Heidinger O et al. *The Breast* 2015;24(3):191-6. **PMID 25687106** — PS nach Alter
- Heidinger O et al. *Dtsch Arztebl Int* 2012;109(46):781-7. **PMID 23264826** — IC-Rate nach Alter
- Bokhof B et al. **PMID 30421287** — IC-Anteil Erst- vs. Folgescreening
- Urbschat I, Heidinger O. *Bundesgesundheitsbl* 2014;57(1):68-76. **PMID 24357175** — EU-Benchmarks
- Weigel S et al. *Eur Radiol* 2017;27(7):2744-51. **PMID 27822617** — PS nach Brustdichte
- Byng D et al. *Eur J Radiol* 2022;152:110321. **PMID 35512511** — IC-Ätiologie, n = 2.396
- Braun B et al. *Dtsch Arztebl Int* 2018;115(31-32):520-7. **PMID 30149831** — bedingte Verteilungen je Detektionsmodus
- Prange A et al. *Rofo* 2019;191(2):130-6. **PMID 30103233** — Subtypen SD vs. IC
- Arndt V et al. *Br J Cancer* 2002;86(7):1034-40. **PMID 11953844** — Erstsymptome und Patientendelay, DE
- Arndt V et al. *J Clin Oncol* 2003;21(8):1440-6. **PMID 12697864** — Providerdelay, DE
- Gathani T et al. *BMJ* 2023;381:e073269. **PMID 37100445** — Karzinomrate nach Alter, UK-Proxy
- Dave RV et al. *Br J Gen Pract* 2022;72(717):e234-43. **PMID 34990395** — Symptom → Karzinom, UK-Proxy
- Walker S, Hyde C, Hamilton W. *Br J Gen Pract* 2014;64(629):e788-93. **PMID 25452544** — Symptom-PPV nach Alter, UK-Proxy
- Koo MM et al. *Cancer Epidemiol* 2017;48:140-6. **PMID 28549339** — Erstsymptome, UK-Proxy
- Elezaby M et al. *Radiology* 2018;287:416-422. **PMID 29315061** — BI-RADS 4A/4B/4C-PPV, NMD
- Berg WA et al. *Radiology* 2020;296:32-41. **PMID 32427557** — BI-RADS 3, NMD
- Lee CS, Berg JM, Berg WA. *Radiology* 2021;299:550-558. **PMID 33787333** — BI-RADS 3 nach Alter
- Timmers JM et al. *Eur Radiol* 2012;22:1717-23. **PMID 22415412** — BI-RADS im NL-Screening
- Lehman CD et al. *Radiology* 2017;283:49-58. **PMID 27918707** — BCSC-Benchmarks
- Forester ND et al. *EJSO* 2019;45:519-527. **PMID 30579653** — B3-Upgrade-Metaanalyse
- Brennan ME et al. *Radiology* 2011;260:119-128. **PMID 21493791** — DCIS→invasiv-Upgrade
- Müller-Schimpfle M et al. *RöFo* 2016;188:346-352. **PMID 27002496**; *Breast Care* 2019;14:308-314. **PMID 31798391** — BI-RADS-Konsens DE/AT
- Hu C, Hart SN et al. *NEJM* 2021;384:440-451. **PMID 33471974** — CARRIERS
- Dorling L et al. (BCAC). *NEJM* 2021;384:428-439. **PMID 33471991** — BRIDGES
- Li J et al. *Int J Cancer* 2018. **PMID 30175445** — LIBRO-1 (Schweden)
- Kast K et al. *J Med Genet* 2016;53(7):465-471. **PMID 26928436** — GC-HBOC, 21.401 Familien
- Bick U et al. *Breast Cancer Res Treat* 2019;175(1):217-228. **PMID 30725383** — IFNP-Programmsensitivität
- Rhiem K et al. *Breast J* 2019;25(3):455-460. **PMID 30953388** — Checklisten-Erfüllung
- Quante AS et al. *Gynäkologe* 2020;53:259-264. DOI 10.1007/s00129-020-04572-9 — IFNP-Kriterienwechsel

**Zitatkorrekturen gegenüber `docs/breast_module_concept.md`:** „Kaiser 2023" → **Heinze 2023, PMID 37697304**;
„Koo 2017, PMID 28347885" → **PMID 28549339**; LIBRO-1 ist **schwedisch**, nicht deutsch;
IFNP-Detektionsrate 1,53 % stammt aus dem **DKG-Jahresbericht FBREK 2025**, nicht aus Bick 2019;
Koumpis 2011 (PMC3240809) als Alters-Evidenz **streichen** (2 Ereignisse, n = 60).


# Teil B — Subtypen, Stadien, pTNM, pCR (beads synthea-eu-cancer-0m8, -98b)

Evidenzrecherche für die Arbeitspakete **`synthea-eu-cancer-0m8`** (Subtypen- & Stadienverteilung) und
**`synthea-eu-cancer-98b`** (pTNM / Sentinel / pCR). Strukturvorbild: `epidemiology/prostate_calibration.md`
(§3 „kohärente Sets je Gruppe", §11.3 Partin-Matrix). Vorlage für die Fachinhalte:
`docs/breast_module_concept.md` §3–§6 — die dortigen Zahlen sind hier **nachgeprüft**, nicht nur übernommen;
Abweichungen sind markiert.

**Kohorte:** Frauen **50–60**, Deutschland-Frame. **DCIS ist im Scope.**

**Confidence-Legende** (identisch zu Prostata): 🟢 gut belegt (deutsches/EU-Register oder große Primärstudie,
genau die gefragte Zahl) · 🟡 belegt, aber Übertragbarkeits-/Ära-Vorbehalt · 🔴 Modellierungsprior / Schätzung.

**Altersband-Konvention** (aus dem Konzeptpapier übernommen): existiert eine 50–59-Zahl, wird sie benutzt;
liegt nur 50–69 vor, wird sie mit **„Quelle 50–69"** markiert und die Confidence um eine Stufe abgesenkt.

> **Was in dieser Runde im Volltext gelesen wurde** (Primärquellen-Verifikation, nicht Suchmaschinen-Referat):
> TRM-DKK-Poster Schrodi 2016 (PDF, alle vier Tabellen extrahiert), von Minckwitz 2012 (PMID 22508812),
> Houssami 2012 (PMID 22766518), KEYNOTE-522 (PMID 32101663), NeoSphere (PMID 22153890), INSEMA
> (PMID 39665649), Lee/Lim 2026 ICES Ontario (PMID 42002711), Alarcon 2019 NCDB (PMID 31350005),
> Nielsen 2023 Dänemark (PMID 37946261), Ortmann 2022 (PMID 35380257), van Steenbergen 2016 NL-DCIS
> (PMID 27160733), Weigel 2014 (PMID 24475843). Verifikationsprotokoll: §8.

---

## 1. Subtypen-Verteilung bei Erstdiagnose (WP 0m8)

### 1.1 Primärquellen-Verifikation: Tumorregister München

Das TRM-Poster (Schrodi/Eckel/Schubert-Fritschle/Engel, DKK Februar 2016, n=**8.228** invasive
Mammakarzinome, Diagnose **2000–2014**, Surrogatdefinition St.-Gallen-Konsensus **2013**, Ki-67-Cutoff 14)
wurde als PDF gezogen und Tabelle 1–4 vollständig extrahiert.

**Wichtiger Lesehinweis zur Quelle:** die Altersblöcke in TRM Tab. 2 sind **Spaltenprozente innerhalb des
Subtyps** (Altersverteilung je Subtyp), nicht die gesuchte Subtypenverteilung je Altersband. Die
50–69-Verteilung entsteht erst durch **Zeilen-Normierung** über die absoluten n. Diese Umrechnung habe ich
nachgerechnet — das Ergebnis stimmt **exakt** mit `docs/breast_module_concept.md` §3.1 überein.

| Surrogat-Subtyp | n (50–69) | **50–69** | n (<50) | <50 | Gesamt (alle Alter) | Conf (50–60) |
|---|---|---|---|---|---|---|
| Luminal A-like | 1.421 | **35,7 %** | 446 | 26,3 % | 31,3 % | 🟡 Quelle 50–69 |
| Luminal B-like HER2− | 1.621 | **40,8 %** | 725 | 42,8 % | 42,8 % | 🟡 |
| Luminal B-like HER2+ | 419 | **10,5 %** | 243 | 14,3 % | 11,4 % | 🟡 |
| HER2+ (non-luminal) | 169 | **4,2 %** | 73 | 4,3 % | 4,4 % | 🟡 |
| Triple-negativ | 348 | **8,7 %** | 207 | 12,2 % | 10,1 % | 🟡 |
| **Summe** | **3.978** | 100 % | **1.694** | 100 % | 8.228 | |

✅ **Verdikt: die Konzept-Tabelle ist korrekt und exakt aus der Primärquelle reproduzierbar.** Keine Korrektur nötig.

Einzelmarker-Marginalen derselben Quelle (TRM Tab. 1, alle Alter, direkt aus dem PDF): **ER+ 85,4 %**
(7.030/8.228), **PR+ 77,7 %** (6.388/8.226), **HER2+ 15,8 %** (1.300/8.228), **Ki-67 <14 in 35,9 %** /
**≥14 in 64,1 %** (n=7.446, 9,5 % k.A.) — alle 🟢. Der HER2+-Wert der Konzeptdoku („15 %", Lacruz 2025) und
der TRM-Wert (15,8 %) sind konsistent.

### 1.2 Startwert für das Fenster 50–60

Es gibt **keine deutsche Quelle mit einer 50–59-Spalte** für den 5-Wege-Split 🔴. Der im Konzept
vorgeschlagene lineare Interpolationsprior (Gewicht 0,25 auf der <50-Spalte) rechnet sich so:

| Subtyp | 50–69 | <50 | **Modellprior 50–60** (0,75·[50–69] + 0,25·[<50]) | Conf |
|---|---|---|---|---|
| Luminal A-like | 35,7 | 26,3 | **33,4 %** | 🔴 |
| Luminal B-like HER2− | 40,8 | 42,8 | **41,3 %** | 🔴 |
| Luminal B-like HER2+ | 10,5 | 14,3 | **11,5 %** | 🔴 |
| HER2+ (non-luminal) | 4,2 | 4,3 | **4,2 %** | 🔴 |
| Triple-negativ | 8,7 | 12,2 | **9,6 %** | 🔴 |

**Begründung des Gewichts 0,25 und seine Schwäche:** das TRM-Band 50–69 hat ein mittleres Alter von ~59–60 J.,
das Fenster 50–60 von ~55 J. Ein Gewicht von 0,25 auf der jüngeren Spalte entspricht grob dieser Verschiebung.
Belegt ist das **nicht** — es ist eine lineare Extrapolation auf einer Kurve, die zwischen 40 und 70 nachweislich
**nicht** linear ist (schwedischer Extremwert: TNBC 26 % bei <40 J., Gkekos 2026, n=89.322 🟢; der Sprung
26 → 12,2 → 8,7 % ist konvex). Der Prior ist damit eher **konservativ**: der wahre TNBC-Anteil bei 50–60 liegt
vermutlich näher an 9,0–9,3 % als an 9,6 %. **Empfehlung: als 🔴-Prior kodieren und den 50–69-Wert als
Validierungs-Fallback dokumentieren** — der Unterschied (8,7 vs. 9,6 %) liegt unter der Register-Rundungsgrenze
und ist für die Kohortengenerierung praktisch irrelevant.

### 1.3 Getrennt nach Detektionsmodus

Braun 2018 (PMID 30149831, Münster MSP 2006–2012, n=1.531, **Quelle 50–69**) ist die einzige deutsche Quelle,
die Subtyp × Detektionsmodus **gemeinsam** publiziert. Aus dem Konzept übernommen, in dieser Runde **nicht**
im Volltext gegengeprüft (Verfügbarkeit) — Confidence deshalb unverändert 🟡:

| Merkmal | screen-detektiert (n=714) | Intervall (n=160) | Nicht-Teilnehmerin (n=657) | Conf (50–60) |
|---|---|---|---|---|
| HR+/HER2− | 78,0 % | 70,1 % | 67,7 % | 🟡 |
| HER2+ (beide luminal-Zustände) | 15,0 % | 17,7 % | 18,9 % | 🟡 |
| Triple-negativ | **6,1 %** | 11,6 % | 12,0 % | 🟡 |

**Das ist die stärkste Konditionierung im ganzen Modul:** TNBC ist unter screen-detektierten Karzinomen um den
**Faktor 2** seltener als unter symptomatischen (6,1 vs. 12,0 %) — direkte Folge des Intervall-Bias (TNBC wächst
schnell und entgeht dem 2-Jahres-Raster). Ein Modul, das den Subtyp unabhängig vom Detektionsmodus zieht,
verfehlt genau den Effekt, der den Screening-Arm interessant macht.

**Aufteilung der Braun-3-Wege-Spalten auf die 5 TRM-Klassen** (Braun publiziert nur HR+/HER2−, HER2+, TNBC).
Vorschlag: die HR+/HER2−-Spalte im TRM-Verhältnis LumA:LumB− = 35,7:40,8 = **0,467:0,533** aufteilen und die
HER2+-Spalte im Verhältnis LumB+:HER2-enriched = 10,5:4,2 = **0,714:0,286**. Ergebnis:

| Subtyp | screen-detektiert | Intervall | symptomatisch | Conf |
|---|---|---|---|---|
| Luminal A-like | **36,4 %** | 32,7 % | 31,6 % | 🔴 (Braun × TRM-Verhältnis) |
| Luminal B-like HER2− | **41,6 %** | 37,4 % | 36,1 % | 🔴 |
| Luminal B-like HER2+ | **10,7 %** | 12,6 % | 13,5 % | 🔴 |
| HER2+ (non-luminal) | **4,3 %** | 5,1 % | 5,4 % | 🔴 |
| Triple-negativ | **6,1 %** | 11,6 % | 12,0 % | 🟡 (direkt Braun) |

⚠️ Diese Aufteilung setzt voraus, dass das LumA/LumB-Verhältnis *innerhalb* HR+/HER2− nicht vom Detektionsmodus
abhängt. Das ist **falsch** — screen-detektierte Tumoren sind deutlich häufiger G1 (34,6 vs. 19,9 %, Braun) und
G1 ist bei Luminal A zu 31,5 % gegen 7,2 % bei Luminal B− (§4.1) vertreten, d. h. der LumA-Anteil im
Screening-Arm ist **höher** als hier berechnet. Größenordnung der Unterschätzung: die G1-Marginale legt eher
LumA:LumB− ≈ 0,55:0,45 im Screening-Arm nahe ⇒ LumA ~43 %, LumB− ~35 %. **Kalibrier-Kandidat**; der Rückweg
über die Grading-Marginale (§4.1) ist die saubere Konsistenzprüfung.

### 1.4 Definitions-Artefakt — zweite Bestätigung aus derselben Registerfamilie

Die Konzeptdoku warnt, der Luminal-A-Anteil schwanke vollständig mit der Definition. Diese Recherche liefert
einen **weiteren TRM-internen Beleg**: eine spätere TRM-Auswertung (n=**32.450**, Diagnosejahre **2004–2015**,
Surrogatdefinition „Ki-67 **oder** Grading") kommt auf **Luminal B-like HER2− 55,4 %, Luminal A-like 22,0 %,
TNBC 9,4 %** 🟢 — dasselbe Register, dieselbe Region, **Luminal A um 9 Prozentpunkte niedriger** als im
St.-Gallen-2013-Poster (31,3 %).

**Konsequenz für das Modul:** die Wahl „St. Gallen 2013 mit Ki-67-Cutoff 14" ist damit nicht nur eine
Konvention, sondern die **einzige** Wahl, für die alle nachgelagerten Kreuztabellen (Grading je Subtyp, M1 je
Subtyp, pT/pN je Subtyp — §4, §5) aus **einer** Quelle mit **einer** Definition stammen. Die 22,0-%-Zahl darf
niemals mit den Kreuztabellen des Posters gemischt werden. Als Modul-Konstante `bc_ki67_cutoff = 14`
dokumentieren, mit dieser Begründung.

---

## 2. DCIS (WP 0m8)

### 2.1 Anteil an allen Detektionen

Aus dem Konzept übernommen (§3.3), in dieser Runde nicht neu verifiziert außer wo vermerkt:

| Population | DCIS-Anteil | Quelle | Conf (50–60) |
|---|---|---|---|
| screen-detektiert, **Erstuntersuchung** | **22 %** | KoopMammo JB Evaluation 2023 | 🟢 |
| screen-detektiert, **reguläre Folgeuntersuchung** | **18 %** | ebd. | 🟢 |
| screen-detektiert (Münster) | 26,3 % | Braun 2018, Quelle 50–69 | 🟡 |
| Intervallkarzinome | 8,1 % | Braun 2018, Quelle 50–69 | 🟡 |
| Nicht-Teilnehmerinnen / symptomatisch | 12,8 % | Braun 2018, Quelle 50–69 | 🟡 |
| alle deutschen Mamma-Neubildungen | ~8 % | RKI KID 2025 (alle Alter) | 🟢 |
| DKG-Zentren, Primärfälle | 9,6 % | OnkoZert JB 2025 (alle Alter) | 🟢 |

**Empfohlener Modulwert für die 50–60-Kohorte** (weil jede Teilnehmerin die Erstrunde mit ~50 J. durchläuft,
Konzept §1.2a): Screening-Arm **0,22** in Runde 1, **0,18** ab Runde 2; Intervall **0,08**; symptomatisch
**0,13**. Das reproduziert bei einem 45/11/44-Detektionsmix einen Gesamt-DCIS-Anteil von ~**0,145** — deutlich
über dem nationalen ~8 %, weil das Modell eine *Screening-Kohorte* erzeugt und nicht die Gesamtinzidenz. Das ist
kein Fehler, gehört aber als Erwartungswert in die Validierung, sonst wird es als einer gemeldet.

### 2.2 Grading-Verteilung des DCIS

DCIS wird nach **Kerngrad (nuclear grade)** klassifiziert, nicht nach Elston-Ellis. Die Konzeptdoku zitiert
TRM Tab. 25 mit niedrig 11,6 / intermediär 26,1 / hoch 33,3 % bei **28,9 % ohne Angabe** — das sind
Roh-Anteile inklusive Unbekannt und **nicht direkt als Branch-Wahrscheinlichkeiten verwendbar**.

**Renormierung auf die 71,1 % mit bekanntem Kerngrad:**

| Kerngrad | TRM roh | **TRM renormiert** | NL-Screening (van Steenbergen 2016) | Conf |
|---|---|---|---|---|
| niedrig (G1) | 11,6 % | **16,3 %** | 17,7 % gesamt / **16,4 %** screen-detektiert | 🟢 |
| intermediär (G2) | 26,1 % | **36,7 %** | 31,4 % / **31,6 %** | 🟢 |
| hoch (G3) | 33,3 % | **46,8 %** | 50,9 % / **52,0 %** | 🟢 |
| k. A. | 28,9 % | — | — | — |

**Unabhängige Bestätigung:** van Steenbergen/Elshof 2016 (PMID 27160733, NL-Screeningprogramm 50–69,
n=**4.232**, 2007–2009) liefert dieselbe Größenordnung und zusätzlich den Split nach Detektionsmodus:
screen-detektiert (n=1.430) 16,4 / 31,6 / 52,0 % gegen Intervall/nicht-screen-detektiert (n=263) 18,8 / 27,2 /
54,0 % — die Autoren berichten **keinen signifikanten Unterschied** der Gradverteilung zwischen screen- und
nicht-screen-detektiertem DCIS.

✅ **Modellierungsempfehlung: DCIS-Kerngrad NICHT auf den Detektionsmodus konditionieren** (im Gegensatz zu
allem anderen im Modul). Ein Satz von Wahrscheinlichkeiten reicht: **niedrig 0,17 / intermediär 0,34 / hoch
0,49** 🟢 — Mittel aus TRM-renormiert und NL, beide Register konvergieren. Das ist eine der wenigen Stellen im
Mamma-Modul, an der zwei unabhängige europäische Register dieselbe Zahl liefern.

Gegen-Evidenz zur Richtung: Weigel 2014 (PMID 24475843, **deutsches** digitales MSP, 17 Screening-Einheiten,
50–69 J., 2005–2008, **n=1.018 DCIS mit Grading**) zeigt, dass Einheiten mit hoher Gesamt-Detektionsrate ihren
Zugewinn **nicht** über niedriggradiges DCIS erzielen (r=0,49, p=0,052), sondern über intermediär- (r=0,89) und
hochgradiges DCIS (r=0,88, beide p<0,001) 🟢. Das stützt die Verschiebung ins Hochgradige. Die Publikation
berichtet **Detektionsraten pro 100 Untersuchte, keine Anteile** — sie taugt als Richtungsbeleg, nicht als
Verteilungsquelle. Das ist der Grund, warum die NL-Zahlen hier den deutschen Anker liefern müssen.

**Emissionsnotiz:** der DCIS-Kerngrad ist *nicht* LOINC 33732-9 (Elston-Ellis-Grading). Getrennter Code nötig —
offener Punkt, siehe §7.

---

## 3. Stadienverteilung bei Diagnose, getrennt nach Detektionsmodus (WP 0m8)

### 3.1 T-Kategorie

Aus dem Konzept (§5.1), abgeleitet aus KoopMammo-Größenklassen × TRM-pT-Feinverteilung — 🟡, weil die
Feinaufteilung (T1a:T1b = 21:79 usw.) eine Rechnung und keine publizierte Zeile ist:

| T (invasiv) | screen-detektiert | Intervall (interpoliert) | symptomatisch | Conf |
|---|---|---|---|---|
| T1a | ~7,6 % | ~5 % | ~3,2 % | 🟡 abgeleitet |
| T1b | ~28,8 % | ~19 % | ~11,9 % | 🟡 |
| T1c | ~45,0 % | ~35 % | ~37,6 % | 🟡 |
| **T1 gesamt** | **~81 %** | **58,5 %** (Braun, direkt) | **~53 %** | 🟡 / 🟢 (Intervall) |
| T2 | ~14,9 % | ~30 % | ~37,7 % | 🟡 |
| T3 | ~2,1 % | ~5 % | ~5,1 % | 🟡 |
| T4 | ~1,8 % | ~5 % | ~4,5 % | 🟡 |

Braun 2018 liefert für die T1-Summe **drei** direkt publizierte Werte: screen 78,3 % / Intervall **58,5 %** /
Nicht-Teilnehmerin 54,8 % 🟡. Die KoopMammo-abgeleiteten 81 % (screen) liegen etwas höher als Brauns 78,3 % —
Erklärung: KoopMammo 2023 ist neuer (bessere Digitalisierung) als die Münsteraner Kohorte 2006–2012.
**Empfehlung: Brauns Werte nehmen**, weil sie aus *derselben* Population wie die Nodal- und Subtypspalten
stammen und das Modul damit intern konsistent bleibt; die KoopMammo-Feinverteilung nur für den Split
innerhalb T1 verwenden.

### 3.2 N-Kategorie

| Detektionsmodus | N0 | N+ | Quelle | Conf |
|---|---|---|---|---|
| screen-detektiert | **75,5 %** | **23,4 %** | Braun 2018, Quelle 50–69 | 🟡 |
| Intervall | 59,9 % | 32,0 % | ebd. | 🟡 |
| symptomatisch / Nicht-Teilnehmerin | 61,3 % | 30,7 % | ebd. | 🟡 |
| Programmweit, Folgeuntersuchungen | nodal-negativ **82 %** | 18 % | KoopMammo 2023 | 🟢 |
| Erstuntersuchung | nodal-negativ **76 %** | 24 % | ebd. | 🟢 |

⚠️ **Wichtige Abgrenzung, die im Konzept fehlt:** diese Zeilen sind **unkonditionierte pN-Anteile** über den
gesamten Arm — sie sind *nicht* die „cN0 → pN+"-Rate. Ein Teil dieser Patientinnen ist beim Workup bereits
**cN+** (sonographisch auffälliger, punktierter Lymphknoten) und geht nie in die Sentinel-Logik ein. Die
Aufspaltung ist in §5.5 hergeleitet — sie ist die Brücke zwischen diesem Kapitel und dem Partin-Analogon.

Aufteilung der N+-Fälle auf N1/N2/N3: die Konzeptdoku nutzt die TRM-Marginale **70:19:11** als 🔴-Prior.
**Diese Recherche liefert einen 🟢-Ersatz** — siehe §5.4.

### 3.3 UICC-Gesamtstadium und M1

| Größe | Wert | Quelle | Conf |
|---|---|---|---|
| UICC I / II / III / IV, Frauen **50–69** | **51 / 35 / 7 / 7 %** | RKI KID 2025, gültige Werte | 🟡 Quelle 50–69 |
| UICC II+ Screening-**Erstuntersuchung** | **26 %** | KoopMammo 2023 | 🟢 |
| UICC II+ Screening-**Folgeuntersuchung** | **21 %** | ebd. | 🟢 |
| UICC II+ Prä-Screening-Zielpopulation 2000–2005 | **56 %** | ebd. | 🟢 |
| unbekanntes UICC-Stadium in deutschen C50-Registerdaten | **26 %** | RKI KID 2025 | 🟢 |
| **pM1 bei Erstdiagnose, 50–59 J.** | **6,2 %** | TRM, n=60.479 | 🟢 (echte 50–59-Zahl) |
| pM1 bei Erstdiagnose, gesamt (Subtypkohorte) | **6,2 %** (510/8.228) | TRM-Poster Tab. 2, **verifiziert** | 🟢 |

**Neue Verifikation:** der M1-Anteil von 6,2 % erscheint im TRM-Poster als Gesamt-Marginale (510/8.228)
**und** in der TRM-Survival-Auswertung als 50–59-Wert. Dass beide Wege auf 6,2 % führen, ist Zufall der
Alterszusammensetzung, aber ein nützlicher Konsistenzanker 🟢.

**M1 je Subtyp** (TRM Tab. 2, direkt aus dem PDF, 🟢): Luminal A **2,6 %** · Luminal B HER2− **7,2 %** ·
Luminal B HER2+ **10,1 %** · HER2+ non-luminal **13,2 %** · TNBC **6,0 %**.
✅ Deckungsgleich mit dem Konzept §4.2. Die Verdopplung zwischen Luminal A und Luminal B HER2− ist der
größte biologische Effekt in dieser Tabelle.

**M1 je T- und N-Kategorie** (TRM Tab. 3, 🟢) — für die Konsistenz von M-Ziehung und T/N-Ziehung wichtig:

| Kategorie | M1-Anteil | Kategorie | M1-Anteil |
|---|---|---|---|
| pT1 | **0,4 %** | pN0 | **0,6 %** |
| pT2 | **3,3 %** | pN+ | **5,7 %** |
| pT3 | **8,5 %** | pNX | 13,1 % |
| pT4 | **27,3 %** | | |

Multivariat (TRM Tab. 4): pT4 vs. pT1 **OR 32,6** (18,3–58,3), pN+ vs. pN0 **OR 4,24** (2,77–6,50), Subtyp nur
**OR 1,15–1,72**. **Modellierungskonsequenz: M1 muss auf T und N konditioniert werden, nicht (nur) auf den
Subtyp** — genau umgekehrt zu dem, was die Subtyp-M1-Tabelle nahelegt. Wer M1 allein aus dem Subtyp zieht,
erzeugt metastasierte pT1N0-Fälle in einer Häufigkeit, die das Register um Faktor 10 verfehlt.
Die Alters-OR derselben Regression ist ebenfalls relevant: **50–69 J. vs. <50 J. OR 2,26** (1,57–3,23) 🟢.

⚠️ **Interne Inkonsistenz der Quelle, die dokumentiert gehören muss:** die Grading-Zeile von TRM Tab. 3
(G1 0,7 % / G2 2,9 % / G3 7,8 %) ergibt hochgerechnet nur ~316 M1-Fälle gegen 510 in der Gesamtsumme, und der
abgedruckte n-Wert „742" für G2-M1 widerspricht dem Prozentwert 2,9 % (2,9 % von 4.944 ≈ 143). Die pT- und
pN-Zeilen sind dagegen intern konsistent (M1 ohne Resektat hat kein pT/pN). **Die Grading-M1-Zeile daher
nicht als Arrow verwenden** 🔴; pT-/pN-M1-Zeilen 🟢.

---

## 4. Kohärente Sets je Subtyp (WP 0m8 — Analogon zu Prostata §3 „Per-group encoded staging/grade")

### 4.1 Grading (Elston-Ellis) je Subtyp — Primärquelle nachgerechnet

TRM Tab. 2, **auf die jeweils gegradeten Fälle renormiert** (das Poster druckt für Luminal B HER2+ den
offensichtlichen Setzfehler „6,0" statt 52,8 — die Konzeptdoku hat ihn bereits korrigiert, hier bestätigt):

| Subtyp | n (gegradet) | G1 | G2 | G3 | Conf |
|---|---|---|---|---|---|
| Luminal A-like | 2.560 | **31,4 %** | **65,9 %** | **2,7 %** | 🟢 |
| Luminal B-like HER2− | 3.502 | **7,4 %** | **69,6 %** | **22,9 %** | 🟢 |
| Luminal B-like HER2+ | 922 | **2,9 %** | **52,8 %** | **44,3 %** | 🟢 (Setzfehler korrigiert) |
| HER2+ (non-luminal) | 356 | **0,8 %** | **34,0 %** | **65,2 %** | 🟢 |
| Triple-negativ | 831 | **1,4 %** | **25,4 %** | **73,2 %** | 🟢 |
| **Gesamt-Marginale** | 8.171 | **13,6 %** | **60,5 %** | **26,0 %** | 🟢 |

✅ Konzept §4.2 stimmt bis auf Rundungsstellen (dort 31,5/7,2 auf ungegradeter Basis). **Empfehlung: die hier
renormierten Werte verwenden**, weil ein Branch summieren muss.

**Die Gesamt-Marginale 13,6 / 60,5 / 26,0 ist der Validierungsanker**: zieht das Modul Subtyp und dann Grading
aus diesen fünf Sätzen, muss die Kohorten-Marginale diese drei Zahlen reproduzieren. Gegenprobe mit dem
50–69-Subtypmix: 0,357·31,4 + 0,408·7,4 + 0,105·2,9 + 0,042·0,8 + 0,087·1,4 = **14,7 % G1** — leicht über der
Alle-Alter-Marginale von 13,6 %, was zur Altersrichtung passt (Luminal A ist im Band 50–69 überrepräsentiert).
Konsistent 🟢.

Gegenprobe Detektionsmodus (Braun 2018): screen G1/G2/G3 = 34,6/48,7/**16,5** gegen symptomatisch
19,9/52,4/**27,2** 🟡. Der Screening-Arm muss also deutlich G1-lastiger herauskommen — was er über den
Subtyp-Skew (§1.3) automatisch tut, wenn LumA dort auf ~43 % korrigiert wird: 0,43·31,4 + 0,35·7,4 + ... ≈ 16,5 %
G1 — das trifft die Braun-Zahl **nicht** (34,6 %). **Offene Inkonsistenz: der Subtyp-Skew allein erklärt Brauns
G1-Anteil im Screening-Arm nicht.** Entweder muss Grading zusätzlich direkt auf den Detektionsmodus
konditioniert werden (Bruch der „Subtyp determiniert Grading"-Logik), oder Brauns 34,6 % sind mit dem
TRM-Grading nicht kompatibel (unterschiedliche Grading-Praxis/Ära). **Das ist die wichtigste offene
Kalibrierfrage aus WP 0m8** — siehe §7.

### 4.2 ER / PR je Subtyp — Definition plus Empirie

Deutsche S3-Konvention (Empf. 4.72, mod. 2025): **negativ <1 % · gering positiv 1–10 % · positiv >10 %**,
Prozentsatz **und** Färbeintensität angeben 🟢.

| Subtyp | ER | PR | Basis | Conf |
|---|---|---|---|---|
| Luminal A-like | positiv (per Definition) | **positiv** (per Definition: PR+ *erforderlich*) | St. Gallen 2013 | 🟢 |
| Luminal B-like HER2− | positiv | **PR− in einem Teil** (PR− ist eines der beiden B-Kriterien) | ebd. | 🟢 |
| Luminal B-like HER2+ | positiv | beliebig | ebd. | 🟢 |
| HER2+ (non-luminal) | **negativ** | **negativ** | ebd. | 🟢 |
| Triple-negativ | **negativ** | **negativ** | ebd. | 🟢 |

Zu reproduzierende deutsche Marginalen (TRM Tab. 1, 🟢): **ER+ 85,4 %**, **PR+ 77,7 %**.
Gegenprobe der Definition: ER+ muss = LumA + LumB− + LumB+ = 31,3+42,8+11,4 = **85,5 %** sein — TRM misst
85,4 %. ✅ Die Definition ist in sich geschlossen; ER ist **keine frei zu ziehende Größe**, sondern durch den
Subtyp determiniert. Nur die 1–10-%-„gering positiv"-Randzone ist ein echter Freiheitsgrad 🔴.

PR ist der einzige Marker mit echtem Ziehbedarf: PR+ gesamt 77,7 %, und PR+ ist bei LumA per Definition 100 %.
Daraus folgt rechnerisch der PR+-Anteil in den übrigen Ästen:
0,313·1,0 + 0,428·p + 0,114·q + 0,044·0 + 0,101·0 = 0,777 ⇒ 0,428p + 0,114q = 0,464.
Mit q ≈ 0,75 (LumB HER2+ ist PR-freier als LumB−, da HER2+ das B-Kriterium schon erfüllt) folgt
**p ≈ 0,884** für Luminal B HER2−. Das widerspricht dem Konzept-Prior „PR− in 30–40 %" deutlich —
**dort sind es nur ~12 %** 🟡. Grund: bei LumB HER2− ist Ki-67 ≥14 das *dominante* B-Kriterium
(64,1 % aller Tumoren sind Ki-67-hoch), PR− trägt nur einen kleinen Rest bei.
✅ **Korrektur gegenüber `docs/breast_module_concept.md` §4.2: PR− bei Luminal B HER2− auf ~10–15 % senken**,
sonst wird die deutsche PR+-Marginale von 77,7 % um ~10 Punkte verfehlt.

### 4.3 Ki-67 je Subtyp

**Es gibt keine deutsche Ki-67-Verteilung pro Subtyp** 🔴 — bestätigt in dieser Runde; auch international keine
große Registerquelle mit Median + IQR über alle fünf Klassen. Zu reproduzierende deutsche Marginalen:

| Marginale | Wert | Quelle | Conf |
|---|---|---|---|
| Ki-67 **<14 / ≥14** | **35,9 % / 64,1 %** | TRM Tab. 1 (n=7.446), **verifiziert** | 🟢 |
| Mittelwert ± SD | **20,3 ± 18,1 %** | Inwald 2013, Krebsregister Regensburg, n=3.658, PMID 23674192 | 🟢 |
| Median | **15 %** | ebd. | 🟢 |
| Bins <10 / 10–14 / 15–24 / ≥25 % | **22,0 / 23,2 / 26,1 / 28,4 %** | ebd. | 🟢 |
| Mittelwert je Grading G1/G2/G3 | **9,7 / 16,2 / 37,4 %** | ebd. | 🟢 |

Beste verfügbare Subtyp-Priors (beide klein, beide nicht-deutsch, beide 🔴):

| Subtyp | Mittelwert ± SD (n=363, PMC6797656) | Median (n=200, Cancer Biol Med 2016) | **Modellprior Median (IQR)** | Conf |
|---|---|---|---|---|
| Luminal A-like | **5,8 ± 3,6 %** | 17 % | **9 (6–12)** | 🔴 |
| Luminal B-like HER2− | **24,3 ± 9,8 %** | 29 % | **25 (18–35)** | 🔴 |
| Luminal B-like HER2+ | **31,0 ± 15,8 %** | — | **30 (20–45)** | 🔴 |
| HER2+ (non-luminal) | **43,0 ± 19,6 %** | 40 % | **40 (25–55)** | 🔴 |
| Triple-negativ | **46,4 ± 23,1 %** (basal) | 50 % | **55 (38–75)** | 🔴 |

**Hartrandbedingung, die jeder Prior einhalten muss** (sonst ist der Subtyp nicht rückrechenbar, Konzept §3.2):
Luminal A **muss** Ki-67 <14 haben; Luminal B HER2− **muss** Ki-67 ≥14 haben *oder* PR− sein. Der
Luminal-A-Prior muss also bei 14 hart abgeschnitten werden — Median 9 mit IQR 6–12 tut das; ein Median von 17
(die zweite Quelle) wäre mit der Definition **unvereinbar**. Das ist der Grund, warum die Priors hier näher an
der ersten Quelle liegen.

Gegenprobe der Marginale mit dem Alle-Alter-Subtypmix: Ki-67 ≥14 ergibt sich als
LumA 0 % + LumB− ~88 % + LumB+ ~85 % + HER2-enriched ~90 % + TNBC ~95 % gewichtet =
0,428·0,88 + 0,114·0,85 + 0,044·0,90 + 0,101·0,95 = 0,376+0,097+0,040+0,096 = **60,9 %** gegen gemessene
**64,1 %** 🟡. Die 3-Punkte-Lücke stammt daher, dass ein Teil der Luminal-B-HER2−-Fälle über PR− und nicht über
Ki-67 klassifiziert wird — konsistent mit §4.2. **Beide Größen (PR−-Anteil und Ki-67-Prior) müssen gemeinsam
kalibriert werden**; sie sind über die St.-Gallen-Regel gekoppelt und dürfen nicht unabhängig gesetzt werden.

### 4.4 HER2-IHC-Score-Verteilung

Beste Quelle bleibt das dänische Nationalregister — in dieser Runde **im Volltext verifiziert**:
Nielsen 2023, **PMID 37946261** (Konzeptdoku nennt nur PMC10636935), Dänemark **2007–2019**, Gesamtkohorte
n=**50.714**, HER2-IHC-Verteilung auf n=**48.382**:

| IHC-Score | Dänemark (verifiziert) | **auf DE reskaliert (HER2+ 15,8 %)** | Conf |
|---|---|---|---|
| 0 | **26,8 %** | **26 %** | 🟢 / 🔴 (Reskalierung) |
| 1+ | **45,5 %** | **44 %** | 🟢 / 🔴 |
| 2+ | **16,4 %** | **17 %** | 🟢 / 🔴 |
| 3+ | **11,6 %** | **13 %** | 🟢 / 🔴 |

⚠️ **Präzisierung gegenüber dem Konzept:** dort steht „P(ISH+ | IHC 2+) = 0,144". Die Primärquelle berichtet
auf n=8.029 IHC-2+-Fällen: **Amplifikation 13,2 %**, normal 78,6 %, **unbekannter Genstatus 8,2 %**. Beide
Zahlen sind richtig, aber mit **verschiedenen Nennern**: 13,2 % auf allen 2+, **14,4 %** auf den 2+ mit
bekanntem ISH-Ergebnis (13,2/91,8). Für das Modul ist **0,144** der korrekte Wert (jedes 2+ bekommt per
S3-Empfehlung 4.73 eine Reflex-ISH, es gibt also keine „unbekannt"-Klasse) 🟢. Die Konzeptdoku ist damit
richtig; die Herkunft der Zahl sollte aber notiert werden, sonst wirkt sie beim nächsten Quellenabgleich falsch.

**Robustheitswarnung (verifiziert):** der HER2-low-Anteil schwankte zwischen dänischen Pathologien von
**46,3 % bis 71,8 %** und über die Jahre von 49,3 % bis 65,6 %, bei einem Gesamtwert von **59,2 %** (n=28.633)
🟢. Interlabor- und Ära-Varianz ist hier größer als jeder Modellierungsfehler; der deutsche Nationalwert von
42 % (Lacruz 2025) liegt sogar **unterhalb** der dänischen Spannweite. **HER2-low deshalb als abgeleitetes
Attribut aus dem IHC-Score führen (0/1+ ⇒ low bei ER-Kontext), nicht als eigenständig gezogene Größe** —
so erbt es automatisch die Kalibrierung des IHC-Scores.

### 4.5 pT und pN je Subtyp — neu erschlossen aus der Primärquelle

Diese beiden Blöcke aus TRM Tab. 2 **fehlen in `docs/breast_module_concept.md` vollständig** und sind der
direkteste Konsistenz-Check für die kohärenten Sets (alle 🟢, deutsches Register, n=8.228, alle Alter):

| Subtyp | pT1 | pT2 | pT3 | pT4 |
|---|---|---|---|---|
| Luminal A-like | **72,3 %** | 23,7 % | 2,9 % | 1,1 % |
| Luminal B-like HER2− | **54,6 %** | 36,8 % | 4,5 % | 4,1 % |
| Luminal B-like HER2+ | **54,0 %** | 37,4 % | 4,0 % | 4,6 % |
| HER2+ (non-luminal) | **46,8 %** | 41,5 % | 8,0 % | 3,7 % |
| Triple-negativ | **48,5 %** | 42,0 % | 5,5 % | 4,0 % |
| **Gesamt** | **59,4 %** | 33,3 % | 4,1 % | 3,1 % |

| Subtyp | pN0 | pN+ | pNX | **pN+ (ohne pNX)** |
|---|---|---|---|---|
| Luminal A-like | 73,8 % | 23,9 % | 2,4 % | **24,4 %** |
| Luminal B-like HER2− | 61,6 % | 36,1 % | 2,3 % | **36,9 %** |
| Luminal B-like HER2+ | 58,1 % | 39,0 % | 2,9 % | **40,2 %** |
| HER2+ (non-luminal) | 51,2 % | 45,5 % | 3,3 % | **47,1 %** |
| Triple-negativ | 56,2 % | 31,6 % | 3,3 % | **32,6 %** |
| **Gesamt** | 65,1 % | 32,4 % | 2,5 % | **33,2 %** |

**Das ist der Baustein, aus dem das Partin-Analogon in §5 gebaut wird.** Beachte die klinisch wichtige
Nicht-Monotonie: TNBC hat den **zweithöchsten** G3-Anteil (73,2 %) und den **zweitgrößten** pT2+-Anteil, aber
einen **unterdurchschnittlichen** pN+-Anteil (32,6 % gegen HER2+ non-luminal 47,1 %). TNBC metastasiert
bevorzugt hämatogen statt lymphogen — das Modul darf Aggressivität und Nodalstatus daher **nicht** über eine
gemeinsame latente „Aggressivitäts"-Variable koppeln.

---

## 5. Das Partin-Analogon: cN0 → pN+ nach Sentinel-Node-Biopsie (WP 98b)

Ziel: das Mamma-Gegenstück zur Prostata-Partin-Matrix (§11.3 dort) — die **Übergangsmatrix vom klinischen zum
pathologischen Nodalstatus**, stratifiziert nach cT und Subtyp.

**Staging-Guardrails** (Analogon zu „Prostata hat kein pT1"): pN erfordert eine Lymphknoten-Entnahme; das
Suffix `(sn)` nur nach Sentinel-Biopsie; DCIS ist **pTis(DCIS)**, nie pN-relevant (axilläre Diagnostik bei DCIS
ist ein Qualitätsmangel, OnkoZert KZ 18 Soll ≤ 2,5 %); nach Neoadjuvanz sind **alle** Kategorien mit `y` zu
präfigieren.

### 5.1 Die unkonditionierte Marginale — cN0 → pN+ gesamt

Zwei große, unabhängige Quellen, beide in dieser Runde im Volltext/Abstract verifiziert:

| Quelle | Population | n | **cN0 → pN+** | Conf |
|---|---|---|---|---|
| **NCDB** (Alarcon 2019, PMID 31350005) | USA, klin. Stadium I–III, 2004–2014 | **433.514** | **17,9 %** | 🟢 |
| **INSEMA** (Reimer 2024, PMID 39665649) | **Deutschland/Österreich**, cT1–2 cN0, BET | **751** SLNB-Pathologien | **17,0 %** | 🟢 |

**Diese Konvergenz ist das belastbarste Einzelergebnis dieser Recherche.** Ein US-Registerdatensatz mit
433.514 Fällen und die deutsche INSEMA-Studie (151 Zentren, DKH-finanziert) landen unabhängig bei
17–18 % — das ist der Anker, den die Modulmatrix reproduzieren muss.

**Vorbehalt zu INSEMA:** die Studienpopulation ist selektiert — **98,5 % HR-positiv, nur 3,6 % HER2-positiv,
nur 3,6 % G3, 90 % cT1 / 79 % pT1**, alle BET-geeignet. Der 17,0-%-Wert ist damit im Wesentlichen die
**luminale** cN0 → pN+-Rate, nicht die aller Subtypen. Genau das macht ihn als Kalibrierungsanker für den
größten Ast (§5.4) aber besonders brauchbar 🟢.

### 5.2 Feinverteilung des pN-Status bei cN0 — ersetzt einen 🔴-Prior

NCDB (Alarcon 2019, n=433.514) publiziert die vollständige Zeile 🟢:

| pN nach cN0 | Anteil aller cN0 | **Anteil der pN+** | Conf |
|---|---|---|---|
| pN0 | **82,1 %** | — | 🟢 |
| pN1mi | **3,6 %** | **20,1 %** | 🟢 |
| pN1 (Makro) | **11,4 %** | **63,7 %** | 🟢 |
| pN2 | **2,1 %** | **11,7 %** | 🟢 |
| pN3 | **0,8 %** | **4,5 %** | 🟢 |

Deutsche Gegenprobe INSEMA (n=751): pN0 **83,0 %**, pN1mi **2,8 %**, 1–2 Makrometastasen **12,9 %**,
≥3 Makrometastasen **1,3 %** 🟢. Auf pN+ normiert: pN1mi 16,4 %, 1–2 Makro 75,8 %, ≥3 Makro 7,8 %.

✅ **Ersetzt den 🔴-Prior „N1:N2:N3 = 70:19:11" aus `docs/breast_module_concept.md` §5.1 durch einen
🟢-Wert.** Empfohlene Kodierung für den cN0-Ast: **pN1mi 0,20 / pN1a 0,64 / pN2a 0,12 / pN3a 0,04**.
Der alte Prior überschätzte pN2/pN3 um mehr als das Doppelte — er stammte aus einer Marginale, die auch die
cN+-Patientinnen enthielt, und die sind genau die mit N2/N3.

**Klinische Relevanz der pN1mi-Zeile:** 20 % aller cN0-pN+-Fälle sind Mikrometastasen, und für die gilt der
OnkoZert-Qualitätsindikator KZ 23 („axilläre Therapie bei pN1mi soll vermieden werden", Ist **7,3 %**) 🟢. Das
Modul erzeugt damit automatisch die richtige Menge an „pN1mi ohne Axilladissektion"-Journeys — ein
Datenpunkt, den kein anderes synthetisches Mamma-Dataset abbildet.

### 5.3 Publizierte Nodalpositivität nach Tumorgröße und Subtyp

Beste Quelle: **Lee/Lim 2026, ICES Ontario** (PMID 42002711, Ann Surg Oncol 33:6444–6454, populationsbezogen
**2000–2019**, n=**11.007** T1a–T2-Fälle: 1.923 HR−HER2+, 4.542 HR+HER2+, 4.542 triple-negativ) 🟢:

| Größe | HR−/HER2+ | HR+/HER2+ | Triple-negativ | HR+/HER2− |
|---|---|---|---|---|
| T1a/b | **11–22 %** | **11–14 %** | **7–11 %** | *nicht berichtet* |
| T1c | **32 %** | **26 %** | **19 %** | *nicht berichtet* |
| T2 | **38 %** | **42 %** | **30 %** | *nicht berichtet* |

⚠️ Zwei Einschränkungen, die beim Übernehmen zählen: (1) **die HR+/HER2−-Spalte fehlt** — genau der Ast, der
in einer 50–60-Screening-Kohorte ~76 % ausmacht; (2) die Raten sind **nicht auf cN0 konditioniert**, sondern
gelten für alle T1–T2-Fälle. Die Multiplikatoren über die Größenklassen sind aber sehr stabil und über die
drei Subtypen fast identisch: **T1a/b : T1c : T2 ≈ 1 : 2,0 : 3,0** (Einzelwerte 1:2,0:2,4 / 1:2,0:3,2 /
1:2,1:3,3). Diese Ratio ist der brauchbare Teil der Quelle.

Weitere Größenanker (kleinere Serien, 🟡): T1mic 0 % · T1a 3,4 % · T1b 8,5 % · T1c 15,3 % (institutionelle
Serie n=986); alternative Serie T1a 4,3 % · T1b 19,5 % · T1c 23,8 % · T2 48,9 % · T3 66,7 %. Die Spannweite
zwischen diesen beiden Serien ist groß — sie taugen nur als Plausibilitätsschranke, nicht als Kalibrierung.

⚠️ **Nicht verwendbar:** eine chinesische T1-Serie (PMID 35836596, n=1.619) berichtet „SLN-Positivität nach
Subtyp" mit Luminal A 24,1 %, Luminal B HER2− 39,0 %, **Luminal B HER2+ 12,3 %, HER2-enriched 6,7 %,
TNBC 10,5 %**. Die HER2+-Werte liegen unter Luminal A, was biologisch und gegen alle anderen Quellen
unplausibel ist — das sind mit hoher Wahrscheinlichkeit **Spaltenanteile der SLN+-Gruppe**, keine Raten.
**Diese Zahlen dürfen nicht ins Modul.**

### 5.4 Die kodierte Übergangsmatrix cN0 → pN+ (Mamma-Partin)

Weil keine Quelle die vollständige 5×4-Matrix publiziert, wird sie **konstruiert** — mit der ausdrücklichen
Nebenbedingung, dass sie die 🟢-Anker aus §5.1 reproduziert. Konstruktionsregel:

> `P(pN+ | cN0, Subtyp s, Kategorie t) = b × r_s × m_t`
> mit **b = 9,7 %** (Kalibrierkonstante), **r_s** = subtypspezifischer Faktor aus der TRM-pN+-Spalte (§4.5,
> normiert auf die Gesamtmarginale 33,2 %), **m_t** = Größenmultiplikator aus ICES Ontario (§5.3).

Faktoren: r = LumA **0,735** · LumB HER2− **1,111** · LumB HER2+ **1,211** · HER2+ non-lum **1,418** ·
TNBC **0,982**. m = cT1a/b **1,0** · cT1c **2,0** · cT2 **3,0** · cT3/4 **4,0**.

**Kalibrierung von b:** auf die INSEMA-Zusammensetzung angewandt (98,5 % HR+, cT-Mix 22,5/67,5/10,0 ⇒
mittleres r 0,935, mittleres m 1,875) muss `b × 0,935 × 1,875 = 17,0 %` gelten ⇒ **b = 9,7 %**. Die Matrix
reproduziert den deutschen 🟢-Anker damit **per Konstruktion**.

| Subtyp | cT1a/b | cT1c | cT2 | cT3/cT4 | Conf |
|---|---|---|---|---|---|
| Luminal A-like | **0,07** | **0,14** | **0,21** | **0,29** | 🟡 (Anker 🟢, Spreizung abgeleitet) |
| Luminal B-like HER2− | **0,11** | **0,22** | **0,32** | **0,43** | 🟡 |
| Luminal B-like HER2+ | **0,12** | **0,24** | **0,35** | **0,47** | 🟡 |
| HER2+ (non-luminal) | **0,14** | **0,28** | **0,41** | **0,55** | 🟡 |
| Triple-negativ | **0,10** | **0,19** | **0,29** | **0,38** | 🟡 |

**Externe Gegenprobe gegen ICES Ontario (Quelle war an der Konstruktion nur über die Ratio beteiligt, nicht
über die Niveaus):** TNBC cT1c Modell **19 %** gegen ICES 19 % · HR+HER2+ cT1c Modell 24 % gegen ICES 26 % ·
HR−HER2+ cT1c Modell 28 % gegen ICES 32 % · TNBC cT2 Modell 29 % gegen ICES 30 %. Die Modellwerte liegen
durchweg **leicht unter** ICES — genau die erwartete Richtung, weil das Modell auf **cN0** konditioniert und
ICES nicht. ✅ **Die Matrix ist gegen zwei unabhängige Quellen konsistent.**

### 5.5 Die fehlende Brücke: wie viele cN0 gibt es überhaupt?

Die Braun-2018-Nodalanteile (§3.2) sind **unkonditioniert**. Damit die Matrix aus §5.4 anschlussfähig wird,
braucht das Modul den **cN+-Anteil beim Workup** — die Patientinnen, die per sonographisch/zytologisch
gesichertem Lymphknotenbefall gar nicht erst in die Sentinel-Logik laufen. Dieser Wert ist in keiner deutschen
Quelle publiziert 🔴; er lässt sich aber aus der Konsistenzbedingung **ableiten**:

> `P(pN+) = P(cN+) + [1 − P(cN+)] × P(pN+ | cN0)`

| Arm | Braun pN+ (unkond.) | Matrix-Ergebnis P(pN+\|cN0) | **⇒ abgeleiteter cN+-Anteil** | Conf |
|---|---|---|---|---|
| screen-detektiert | 23,4 % | 17,7 % | **~0,07** | 🔴 abgeleitet |
| Intervall | 32,0 % | ~22 % | **~0,13** | 🔴 |
| symptomatisch | 30,7 % | ~23,5 % | **~0,09** | 🔴 |

Die Größenordnung (7–13 %) ist klinisch plausibel: die axilläre Sonographie im Rahmen der Abklärung findet
einen kleinen, aber relevanten Anteil eindeutig befallener Lymphknoten. Dass der symptomatische Arm hier
*niedriger* liegt als der Intervall-Arm, ist wahrscheinlich ein Artefakt der Braun-Zahlen und **der Punkt, an
dem WP 51w nachkalibrieren muss**. Erste Empfehlung: einheitlich **cN+ = 0,08 im Screening-Arm** und
**0,12 in den beiden anderen Armen** 🔴.

### 5.6 SLNB vs. primäre Axilladissektion — heutige deutsche Praxis

| Arrow | Wert | Quelle | Conf |
|---|---|---|---|
| pN0-Patientinnen mit **SLNB allein** (ohne präop. Systemtherapie) | **0,931** (26.156/28.098; Soll ≥80 %) | OnkoZert KZ 20a, JB 2023/2025 | 🟢 |
| ⇒ ALND oder SLNB+ALND bei pN0 | 0,069 | abgeleitet | 🟢 |
| Nodalstatus überhaupt bestimmt (invasiv) | 0,966 | OnkoZert KZ 19 | 🟢 |
| Axilläre LK-Entfernung bei **DCIS** (Soll: vermeiden) | 0,025 | OnkoZert KZ 18 | 🟢 |
| Axilläre Therapie bei **pN1mi** (Soll: vermeiden) | 0,073 | OnkoZert KZ 23 | 🟢 |
| **Komplett-Verzicht auf axilläre Chirurgie** (cT1–2 cN0, BET + Ganzbrust-RT) | **v1: 0,00**, ab 2026 klinisch verbreitet | INSEMA (PMID 39665649) + SOUND | 🟡 |

⚠️ **Ära-Entscheid, der explizit getroffen werden muss.** INSEMA hat die Nichtunterlegenheit des
**Verzichts auf jede axilläre Chirurgie** bei cT1–2 cN0 mit BET + Ganzbrustbestrahlung gezeigt
(5-J-iDFS 91,9 % ohne gegen 91,7 % mit SLNB, HR 0,91 [0,73–1,14], medianes Follow-up 73,6 Monate, n=4.858
per protocol) 🟢. Die AGO-Empfehlungen 2025 und die S3 v5.1 haben das aufgenommen. Für eine Kohorte mit
Diagnosedatum **2023** (dem Bezugsjahr der OnkoZert-Kennzahlen) ist der Verzicht noch **nicht** Praxis —
für eine Kohorte mit Bezugsjahr 2026 wäre er es. **Empfehlung: v1 auf 2023 kalibrieren (kein Verzichtspfad,
SLNB-Rate 93,1 %) und den Verzichtspfad als dokumentierten v2-Punkt führen**, weil sonst der OnkoZert-Block
(§6 des Konzepts) und der Axilla-Block aus verschiedenen Jahren stammen und die Kohorte intern inkonsistent
wird. Das ist die Mamma-Entsprechung zur PSA-3-vs-4-Schwellenwertnotiz beim Prostata-Modul.

### 5.7 cT → pT-Upstaging

NCDB (Alarcon 2019, PMID 31350005, n=433.514) 🟢 — das direkte Gegenstück zur Partin-„organbegrenzt"-Spalte:

| Klinische Kategorie | konkordant | **upstaged** | downstaged | Conf |
|---|---|---|---|---|
| **Gesamt** | **86,9 %** | **8,5 %** | **4,6 %** | 🟢 |
| cT1 | **86,4 %** | **7,7 %** | **5,9 %** | 🟢 (Zeile summiert exakt auf 100) |
| cT2 | **66,4 %** | **10,9 %** | **22,7 %** | 🟢 (summiert exakt auf 100) |
| cT3 / cT4 | — | — | — | 🔴 **nicht sauber extrahierbar** |

**Nodal, dieselbe Quelle:** N-Stadium gesamt **80,3 % konkordant / 18,5 % upstaged / 1,2 % downstaged** 🟢;
für cN0 speziell die Zeile aus §5.2 (82,1 % bleiben pN0).

Ergänzender Größenanker: die radiologisch-pathologische Größenkonkordanz ist bei ≤2 cm mit **51,1 %** deutlich
besser als bei >2 cm mit **19,7 %**; die Bildgebung **überschätzt** in 14,5 % und **unterschätzt** in 25,6 %
der Fälle (PMID 30774698) 🟡. Sonographie- und MRT-Konkordanz liegen bei **71,1 % bzw. 72,6 %** 🟡.

**Empfohlene Kodierung:**

| Arrow | Wert | Conf |
|---|---|---|
| cT1 → pT1 (konkordant) | **0,864** | 🟢 |
| cT1 → **pT2** (upstaged) | **0,077** | 🟢 |
| cT1 → pT1mi/pTis (downstaged) | **0,059** | 🟢 |
| cT2 → pT2 (konkordant) | **0,664** | 🟢 |
| cT2 → **pT3** (upstaged) | **0,109** | 🟢 |
| cT2 → pT1 (downstaged) | **0,227** | 🟢 |

⚠️ **Vorzeichen-Unterschied zum Prostata-Modul, der leicht übersehen wird:** beim Prostatakarzinom ist das
Upstaging **einseitig** (Nadelbiopsie kann Extraprostatik nicht ausschließen; Downstaging existiert praktisch
nicht). Beim Mammakarzinom ist **Downstaging bei cT2 mit 22,7 % die häufigste Diskordanz überhaupt** — die
präoperative Bildgebung überschätzt große Tumoren systematisch. Wer die Prostata-Matrix mechanisch überträgt,
erzeugt eine Kohorte mit zu vielen pT2/pT3-Fällen. Der Effekt ist im Screening-Arm (T1-lastig) klein, im
symptomatischen Arm groß.

⚠️ **Extraktionsvorbehalt cT3/cT4:** die Diskussion der Publikation nennt „70,4 % für cT3 (niedrigste
Konkordanz)", die Tabellenwerte im Volltext (65,4 / 15,4 / 19,2 und 45,8 / 2,0 / 52,3) ließen sich den Spalten
nicht eindeutig zuordnen. cT1 und cT2 sind dagegen eindeutig (Zeilensumme 100,0). Da cT3/cT4 im 50–60-Fenster
zusammen nur ~4 % ausmachen, ist ein 🔴-Prior (cT3/4 konkordant 0,70, up 0,10, down 0,20) hier vertretbar.

---

## 6. Neoadjuvanz und pCR (WP 98b)

### 6.1 Wer bekommt Neoadjuvanz

| Größe | Wert | Quelle | Conf |
|---|---|---|---|
| alle Primärfälle 2023 | **21,4 %** | OnkoZert JB 2025 | 🟢 |
| cT1N0M0 / cT2N0M0 / N+M0 | **18,9 / 32,7 / 29,5 %** | ebd. | 🟢 |
| HR+/HER2− (2007–2018) | **5,8 %** | Ortmann 2022, PMID 35380257, n=94.638, 55 DKG-Zentren, **verifiziert** | 🟢 |
| HR+/HER2+ | **26,5 %** | ebd. | 🟢 |
| HR−/HER2+ | **31,9 %** | ebd. | 🟢 |
| Triple-negativ | **31,8 %** | ebd. | 🟢 |
| Gesamtrate im Ortmann-Zeitraum | 5 % (2007) → **17,3 %** (2016) | ebd. | 🟢 |

✅ Alle Ortmann-Zahlen im Volltext bestätigt; Konzeptdoku §6.2 korrekt.

⚠️ **Ära-Vorbehalt bleibt bestehen und ist der wichtigste rote Arrow des Therapieteils.** Ortmanns
Subtyp-Anteile beziehen sich auf eine Gesamtrate von 17,3 % (2016); 2023 sind es 21,4 %. Zwischen 2016 und 2023
liegen **KEYNOTE-522** (Neoadjuvanz wird bei TNBC ab Stadium II zum Standard, weil Pembrolizumab nur
neoadjuvant zugelassen ist) und **KATHERINE** (Resttumor bei HER2+ eröffnet die T-DM1-Eskalation, was ein
starkes Argument für den neoadjuvanten Weg ist). Beide verschieben Neoadjuvanz **strukturell**, nicht graduell.

Reskalierungsvorschlag, so gewählt, dass er gewichtet mit den deutschen Subtyp-Prävalenzen 21,4 % ergibt 🔴:
**TNBC 0,65 · HR−/HER2+ 0,60 · HR+/HER2+ 0,47 · HR+/HER2− 0,10**.
Rechenprobe mit dem 50–69-Subtypmix: 0,087·0,65 + 0,042·0,60 + 0,105·0,47 + 0,765·0,10 = 0,057+0,025+0,049+0,077
= **20,8 %** — trifft die 21,4 % innerhalb einer Rundungsstelle ✅. Der Vorschlag ist damit intern konsistent,
bleibt aber 🔴, weil keine der vier Einzelzahlen publiziert ist.

### 6.2 pCR-Raten je Subtyp

Drei Evidenzebenen, alle in dieser Runde primärverifiziert:

| Quelle | Definition | HR+/HER2− | HR+/HER2+ | HR−/HER2+ | TNBC | Conf |
|---|---|---|---|---|---|---|
| **Ortmann 2022** (DE-Realwelt, n=94.638, 2007–2018) | Registerdefinition | **12 %** | **36 %** | **53 %** | **38 %** | 🟢 |
| **Houssami 2012** Metaanalyse (PMID 22766518, 20 Studien, n=8.095) | studienabhängig | **8,3 %** (6,7–10,2) | **18,7 %** (15,0–23,1) | **38,9 %** (33,2–44,9) | **31,1 %** (26,5–36,1) | 🟢 (Ära-Vorbehalt) |
| **von Minckwitz 2012** (GBG-Pool, PMID 22508812, n=6.377) | **ypT0 ypN0 (streng)** | — | — | — | — | 🟢 |

**von Minckwitz 2012 — was der Volltext tatsächlich hergibt.** Das Abstract nennt **keine** pCR-Raten je
Subtyp; es nennt die **Definitionsfrage** und die **prognostische Wirksamkeit**. Beides ist für das Modul
wichtiger als eine weitere Ratenschätzung:

- **Definitionsvergleich (HR für DFS, pCR vs. keine pCR):** „keine invasiven **und keine In-situ**-Residuen in
  Brust und Lymphknoten" (n=955) → **HR 0,446**; mit In-situ-Residuen (n=309) → **0,523**; keine invasiven
  Brustresiduen aber befallene Lymphknoten (n=186) → **0,623**; nur fokal-invasive Erkrankung (n=478) →
  **0,727** 🟢. ⇒ **Das Modul muss die strenge Definition ypT0 ypN0 verwenden** — bestätigt Konzept §5.3.
- **Streng definierte Gesamt-pCR-Rate: 955/6.377 = 15,0 %** 🟢 (anthrazyklin-taxanbasiert, **ohne** moderne
  HER2-Doppelblockade und ohne Immuntherapie).
- **Prognostische Wirksamkeit je Subtyp:** pCR verbessert DFS bei **Luminal B/HER2−** (p=0,005),
  **HER2+/nicht-luminal** (p<0,001) und **triple-negativ** (p<0,001) — **nicht** bei **Luminal A** (p=0,39) und
  **nicht** bei **Luminal B/HER2+** (p=0,45) 🟢. ⇒ Der `pCR`-Zustand darf nur in den ersten drei Ästen auf den
  Rezidiv-Hazard wirken. ✅ Konzept §6.2 korrekt.

**Moderne Regime-Anker (primärverifiziert):**

| Studie | Regime / Population | pCR | Conf |
|---|---|---|---|
| **KEYNOTE-522** (PMID 32101663) | TNBC Stadium II/III, Pembrolizumab + Paclitaxel/Carboplatin → Anthrazyklin | **64,8 %** (95 % KI 59,9–69,5) | 🟢 |
| KEYNOTE-522 Kontrollarm | dieselbe Chemo + Placebo | **51,2 %** (44,1–58,3) | 🟢 |
| **NeoSphere** Arm B (PMID 22153890) | HER2+, Docetaxel + Trastuzumab + **Pertuzumab** | **45,8 %** (36,1–55,7) | 🟢 |
| NeoSphere Arm A | HER2+, Docetaxel + Trastuzumab (einfach) | **29,0 %** (20,6–38,5) | 🟢 |

⚠️ **Definitionsfalle bei NeoSphere:** der primäre Endpunkt ist **pCR *in der Brust*** (`ypT0/is`), **nicht**
`ypT0 ypN0`. Die 45,8 % sind daher **nicht** direkt mit der strengen Moduldefinition vergleichbar und liegen
etwa 5–8 Punkte darüber. **KEYNOTE-522 dagegen definiert pCR als „kein invasives Karzinom in der Brust *und*
negative Lymphknoten"** — die 64,8 % sind mit der Moduldefinition kompatibel (bis auf verbliebenes DCIS) 🟢.
Diese Unterscheidung fehlt in `docs/breast_module_concept.md` und ist der häufigste Fehler beim Übernehmen
publizierter pCR-Raten.

**Empfohlener Modellprior (Diagnosejahr 2023, leitliniengerechte Regime, strenge Definition ypT0 ypN0):**

| Subtyp | Regime | **pCR-Prior** | Herleitung | Conf |
|---|---|---|---|---|
| Triple-negativ, Stadium II/III | Carboplatin/Taxan + Anthrazyklin **+ Pembrolizumab** | **0,60** | KEYNOTE-522 64,8 % minus ~5 Punkte für die strengere Definition und Realwelt-Adhärenz | 🟡 |
| Triple-negativ, Stadium I (kein Pembro) | Chemo allein | **0,38** | Ortmann-Realwelt 38 % | 🟢 |
| HER2+ / HR− (HER2-enriched) | Chemo + Trastuzumab **+ Pertuzumab** | **0,55** | Ortmann 53 % (schon Doppelblockade-nah), NeoSphere-Arm-B-Definition korrigiert | 🟡 |
| HER2+ / HR+ (Luminal B HER2+) | Chemo + Doppelblockade + endokrin | **0,38** | Ortmann 36 %, Houssami 18,7 % (Prä-Pertuzumab-Ära) — Ortmann ist die neuere und deutsche Quelle | 🟡 |
| Luminal B HER2− | Chemo | **0,12** | Ortmann 12 %, Houssami 8,3 % | 🟢 |
| Luminal A | Chemo (Ausnahmeindikation) | **0,05** | Ortmanns 12 % ist der HR+/HER2−-**Mischwert**; Luminal A liegt darunter, weil pCR dort nicht einmal prognostisch ist (von Minckwitz p=0,39) | 🔴 |

**Konsistenz-Nebenbedingung:** die Aufspaltung des Ortmann-Werts von 12 % auf Luminal A 5 % und
Luminal B HER2− 12 % ist **rechnerisch inkonsistent** (der Mischwert müsste zwischen beiden liegen). Korrekt
ist: mit LumA:LumB− = 0,467:0,533 und einem Mischwert von 12 % folgt aus LumA = 5 % ⇒
LumB− = (12 − 0,467·5)/0,533 = **18,2 %**. **Empfehlung: Luminal A 0,05 / Luminal B HER2− 0,18** —
das reproduziert Ortmanns 12 % exakt 🟡. Die im Konzept vorgeschlagenen 6 %/12 % tun das nicht.

### 6.3 Post-neoadjuvante Eskalation und ypTNM

| Arrow | Wert | Quelle | Conf |
|---|---|---|---|
| HER2+ mit Resttumor → **T-DM1** | 1 − pCR ≈ **0,45–0,62** je nach HER2-Ast | KATHERINE: 3-J-iDFS 88,3 vs. 77,0 %, HR 0,50 | 🟢 (Studie) / 🔴 (Anteil) |
| TNBC mit Resttumor → Capecitabin bzw. **Olaparib** bei gBRCA | — | S3 v5.1 / AGO 2026.1D | 🟢 |
| pCR-Emission | **ypT0 (SCT 1352650002) + ypN0 (SCT 1352797005)** | Konzept §5.4, SNOMED INT 20260501 | 🟢 |
| Resttumor-Emission | ypT1a–ypT4 / ypN0–ypN3a nach Konzept §5.4 | ebd. | 🟢 |

**Verteilung des Resttumors (nicht-pCR-Fälle)** — im Konzept nicht adressiert, hier als Prior 🔴:
Vorschlag, das Residuum aus der cT-Kategorie um **eine Stufe herabzustufen** und ypN aus §5.4 mit halbiertem
`b` zu ziehen (Neoadjuvanz sterilisiert einen Teil der Axilla). Zahlenanker aus der Recherche: bei
cN0-Patientinnen nach neoadjuvanter Systemtherapie liegt die ypN+-Rate bei **HR−/HER2+ 5,6 %** und
**TNBC 6,5 %**, aber bei **HR+/HER2− 29 %** (multizentrische BJS-Kohorte, PMC10763529) 🟡 — die Spreizung ist
also **größer** als vor Therapie und **umgekehrt** zur prätherapeutischen Reihenfolge. Patientinnen mit
Brust-pCR haben nur noch ~2 % Wahrscheinlichkeit für positive Sentinel-Lymphknoten 🟡.
✅ **Modellierungsregel: ypN muss vom Brust-Ansprechen abhängen, nicht nur vom Subtyp.**

---

## 7. Offene Datenlücken

1. **Grading × Detektionsmodus vs. Grading × Subtyp — die zentrale Inkonsistenz (§4.1).** Brauns G1-Anteil im
   Screening-Arm (34,6 %) lässt sich mit dem TRM-Grading-je-Subtyp **nicht** über den Subtyp-Skew allein
   erzeugen; die Rechnung landet bei ~16,5 %. Entweder muss Grading zusätzlich direkt auf den Detektionsmodus
   konditioniert werden (womit die „Subtyp determiniert Grading"-Logik aus Konzept §3.2 bricht), oder Brauns
   Werte sind mit TRM nicht kompatibel. **Blockierend für WP 0m8** — muss vor dem Modulbau entschieden werden.
2. **HR+/HER2− Nodalpositivität nach Tumorgröße.** ICES Ontario publiziert die Spalte nicht, obwohl sie den
   größten Ast betrifft. Die Matrix in §5.4 leitet sie aus dem TRM-Subtypfaktor ab (🟡). Eine direkte Quelle
   (SEER- oder NCDB-Sonderauswertung, oder die ICES-Autoren anschreiben) würde §5.4 von 🟡 auf 🟢 heben.
3. **cN+-Anteil beim Workup in Deutschland (§5.5).** Vollständig unpubliziert; derzeit aus der
   Konsistenzbedingung rückgerechnet (🔴). KoopMammo berichtet Wiedereinbestellung und PPV, aber keinen
   axillären Sonographiebefund. Kandidat für eine gezielte OnkoZert-/KoopMammo-Anfrage.
4. **Ki-67-Verteilung je Subtyp (§4.3).** Keine deutsche, keine große internationale Quelle mit Median + IQR
   über alle fünf Klassen. Die aktuellen Priors stammen aus einer Serie mit n=363. Da Ki-67 der einzige
   *stetige* Marker im kohärenten Set ist und den Luminal-A/B-Schnitt definiert, ist das die datenärmste
   Stelle mit der größten Hebelwirkung.
5. **Deutsche cT3/cT4 → pT-Diskordanz (§5.7).** Aus der NCDB-Publikation nicht eindeutig extrahierbar; im
   50–60-Fenster nur ~4 % der Fälle, deshalb niedrige Priorität.
6. **DCIS-Kerngrad-Emissionscode.** LOINC 33732-9 ist Elston-Ellis-Grading und für DCIS-Kerngrad **falsch**.
   Ein passender LOINC/SNOMED-Code muss gegen den CEIR-OS-Terminologieserver gesucht werden — offener Punkt
   für den Terminologie-Block, blockierend für den DCIS-Ast.
7. **Ära-Entscheid Axilla-Verzicht (§5.6).** INSEMA/SOUND haben den Standard 2024/2025 verschoben; die
   OnkoZert-Kennzahlen sind von 2023. Das Modul braucht **ein** Bezugsjahr — Empfehlung 2023, Verzichtspfad als
   v2. Das ist ein Entscheid, keine Datenlücke, muss aber dokumentiert werden.
8. **50–59-Subtypenspalte für Deutschland (§1.2).** Bleibt unpubliziert; der Interpolationsprior ist 🔴. Eine
   TRM-Sonderauswertung wäre die naheliegende Quelle, da das Register die Rohdaten offensichtlich hat.
9. **Braun 2018 im Volltext.** Die gesamte Detektionsmodus-Konditionierung (§1.3, §3.1, §3.2) hängt an einer
   Publikation, die in dieser Runde nur sekundär vorlag. Der Volltext sollte vor dem Modulbau gelesen werden,
   insbesondere wegen der Grading-Frage aus Punkt 1.

---

## 8. Verifikationsprotokoll dieser Runde

| Behauptung | Konzeptwert | Primärquelle sagt | Verdikt |
|---|---|---|---|
| TRM-Subtypen 50–69 | 35,7 / 40,8 / 10,5 / 4,2 / 8,7 | Zeilennormierung von TRM Tab. 2 auf n=3.978 | ✅ **EXAKT** |
| TRM-Subtypen <50 | 26,3 / 42,8 / 14,3 / 4,3 / 12,2 | Zeilennormierung auf n=1.694 | ✅ **EXAKT** |
| Grading je Subtyp | 31,5/65,9/2,7 … 1,4/25,4/73,2 | TRM Tab. 2; Setzfehler „6,0" bei LumB HER2+ korrekt als 52,8 erkannt | ✅ **EXAKT** (renormierte Fassung in §4.1) |
| M1 je Subtyp | 2,6 / 7,2 / 10,1 / 13,2 / 6,0 | TRM Tab. 2 | ✅ **EXAKT** |
| ER+ 85,4 / PR+ 77,7 / Ki-67 ≥14 in 64,1 % | ebenso | TRM Tab. 1 | ✅ **EXAKT** |
| Luminal-A-Definitionsartefakt | „31,3 % St. Gallen 2013" | TRM Tab. 2 Gesamtspalte 31,3 %; zweite TRM-Auswertung (n=32.450, Ki-67 *oder* Grading) 22,0 % | ✅ bestätigt, **zusätzlicher Beleg gefunden** |
| Nielsen HER2-IHC 26,8/45,5/16,4/11,6 | ebenso | PMID 37946261, n=48.382 | ✅ **EXAKT**; PMID ergänzt |
| P(ISH+ \| IHC 2+) = 0,144 | 0,144 | 13,2 % aller 2+ / **14,4 %** der 2+ mit bekanntem ISH | ✅ korrekt, **Nenner präzisiert** |
| Ortmann NACT-Anteile 5,8/26,5/31,9/31,8 | ebenso | PMID 35380257 | ✅ **EXAKT** |
| Ortmann pCR 12/36/53/38 | ebenso | ebd. | ✅ **EXAKT** |
| KEYNOTE-522 pCR 64,8 % | 64,8 % | PMID 32101663, KI 59,9–69,5 | ✅ **EXAKT** |
| NeoSphere pCR 45,8 % | 45,8 % | PMID 22153890, KI 36,1–55,7 | ✅ **EXAKT**, aber ⚠️ **pCR *in der Brust***, nicht ypT0 ypN0 |
| von Minckwitz pCR-Definitions-HR 0,446 vs. 0,523 | ebenso | PMID 22508812 | ✅ **EXAKT** |
| pCR prognostisch nicht bei LumA (p=0,39) / LumB HER2+ (p=0,45) | ebenso | ebd. | ✅ **EXAKT** |
| N1:N2:N3 = 70:19:11 (🔴-Prior) | 70:19:11 | NCDB cN0 → pN1mi/pN1/pN2/pN3 = 20,1/63,7/11,7/4,5 | ❌ **ERSETZT** durch 🟢-Wert (§5.2) |
| PR− bei Luminal B HER2− in 30–40 % | 30–40 % | rechnerisch aus PR+ 77,7 % Marginale: **~10–15 %** | ❌ **KORREKTUR** (§4.2) |
| DCIS-Kerngrad 11,6/26,1/33,3 (28,9 % k.A.) | Rohwerte | renormiert 16,3/36,7/46,8; NL-Register 17,7/31,4/50,9 | ⚠️ **RENORMIERUNG NÖTIG**, dann 🟢 durch zweites Register bestätigt |
| pCR-Prior LumA 6 % / LumB HER2− 12 % | 6 / 12 | reproduziert Ortmanns Mischwert 12 % nicht | ⚠️ **KORREKTUR: 5 % / 18 %** (§6.2) |
| pT/pN je Subtyp | **fehlt im Konzept** | TRM Tab. 2 vollständig extrahiert | ➕ **NEU** (§4.5) |
| cN0 → pN+ Übergangsmatrix | **fehlt im Konzept** | NCDB 17,9 % + INSEMA 17,0 % + ICES-Ratios | ➕ **NEU** (§5.4) |
| cT → pT-Upstaging | **fehlt im Konzept** | NCDB, PMID 31350005 | ➕ **NEU** (§5.7) |

**Bilanz:** von 14 nachgeprüften Konzeptwerten sind **11 exakt bestätigt**, **2 zu korrigieren**
(PR− bei Luminal B HER2−; pCR-Split Luminal A/B), **1 zu ersetzen** (N1:N2:N3-Prior) und **1 zu renormieren**
(DCIS-Kerngrad). Drei Tabellenblöcke sind neu erschlossen (pT/pN je Subtyp, cN0→pN+-Matrix, cT→pT-Upstaging).


# Teil C — Therapie-Allokation, Verlauf & Outcomes (beads synthea-eu-cancer-t3f, -6r8)

Evidenz-Entwurf für die Arbeitspakete **`synthea-eu-cancer-t3f`** (Therapie-Allokation, deckt Konzept §6) und
**`synthea-eu-cancer-6r8`** (Verlauf & Outcomes, deckt Konzept §7). Format nach dem Muster von
`epidemiology/prostate_calibration.md`.

**Kohorte:** Frauen **50–60 Jahre**, Deutschland-Frame.
**Klinischer Frame:** **S3-Leitlinie Mammakarzinom, AWMF 032-045OL** (Versionen v5.0 12/2025 und v5.1 06/2026 —
beide im Text unterschieden, weil einige Empfehlungen 2025 *modifiziert* bzw. *neu* sind) gibt die Pfad-*Struktur*;
**OnkoZert/DKG-Jahresbericht Brustkrebszentren 2025** (Auditjahr 2024, **Kennzahlenjahr 2023**, 312 Standorte,
73.505 Primärfälle), **Tumorregister München (TRM)**, **RKI/ZfKD „Krebs in Deutschland" 15. Ausgabe (2025)** und
deutsche Verordnungsdaten (IQVIA LRx) kalibrieren die *Wahrscheinlichkeiten*. Wo eine deutsche Zahl fehlt, wird
die beste internationale Quelle genommen **und die Lücke explizit benannt**.

**Confidence:** 🟢 gut belegt (Primärquelle im Volltext geprüft) · 🟡 belegt, aber Transferierbarkeits-/Ära-/
Altersband-Vorbehalt · 🔴 Modellprior / eigene Ableitung.

**Altersband-Konvention** (Querschnittsauflage aus Konzept §10.1): jede Zahl trägt einen Vermerk, ob sie für
**50–60** gilt (**[50–60]**), aus einer 50–69-Quelle stammt (**[Quelle 50–69]**) oder eine Alle-Alter-Zahl ist
(**[alle Alter]**). Alle-Alter- und 50–69-Werte sind gegenüber der Primärquelle **um eine Confidence-Stufe
abgesenkt**, sofern der Alterseffekt nicht separat belegt ist.

> ⚠️ **Die zentrale strukturelle Einschränkung bleibt Konzept §1.2d:** in einem 50–60-Fenster entfaltet sich nur
> der *frühe* Teil der Rezidiv-Hazardkurven. Die Hazard-*Funktionen* in §6 sind trotzdem vollständig anzugeben —
> Synthea zieht daraus nur das im Fenster liegende Stück.

---

## 0. Korrekturen am Konzeptpapier (`docs/breast_module_concept.md` §6–§7)

Diese Recherche hat alle dort genannten Zahlen gegen die Primärquellen geprüft. Die große Mehrheit ist **exakt
bestätigt**. Acht Punkte sind zu korrigieren oder zu präzisieren — sie stehen hier gesammelt, weil sie das
Konzept an entscheidenden Stellen ändern.

| # | Konzept §6/§7 sagt | Primärquelle sagt | Konsequenz |
|---|---|---|---|
| **K1** | Endokrin 50–60: „AI ~55–65 % / TAM ~35–45 %" 🔴 | Kostev 2023 altersstratifiziert (rekonstruiert): **51–60 J. = AI 46,4 % / TAM 53,6 %** | **Der Split kippt: Tamoxifen ist in 50–60 die Mehrheit.** Der Konzeptvorschlag ist ~10–19 Pp. zu AI-lastig. Neuer Wert 🟢 statt 🔴 |
| **K2** | Persistenz-Abbruch: implizit „jüngere brechen häufiger ab" | Kostev 2023 Tab. 2: ≤50 J. HR **1,08**, **51–60 J. HR 0,92**, 61–70 J. HR 0,89 (Ref. >70 J.) | U-förmig. **Die Zielgruppe 50–60 hat unterdurchschnittliches Abbruchrisiko.** Stärkster Prädiktor ist nicht das Alter, sondern der Verordner (Hausarzt HR 1,24) |
| **K3** | Genexpressionstest: „seit 20.06.2019 Oncotype DX für HR+/HER2−, N0 GKV-erstattet" | Stimmt nur für 2019–2020. Seit **15.10.2020** vier Tests (Oncotype, EndoPredict, MammaPrint, Prosigna); seit **17.07.2025** Oncotype auch bei **N1** — dafür **alle vier eingeschränkt auf postmenopausal** (oder prämenopausal mit Ovarialsuppression) | Modell-Schalter: Testzugang ist ab 2025 **menopausenstatusabhängig** — in einer 50–60-Kohorte mit gemischtem Status ein echter Verzweigungspunkt |
| **K4** | „Radiatio nach BET, invasiv 0.978 (OnkoZert KZ 4)" als Durchführungsrate | KZ 4 misst **„denen eine Radiatio *empfohlen* wurde"** — Indikations-, nicht Durchführungsrate | Für die *Durchführung* ist die beste deutsche Zahl **91 %** (Heinig 2022, Dx-Jahr 2008) bzw. die DCIS-Kennzahl KZ 5, die tatsächlich „begonnen" misst |
| **K5** | Neoadjuvanz „alle Primärfälle 2023: 21,4 %" | **Richtig** — 15.699/73.505 = 21,36 %. Der parallel kursierende Wert 25,45 % ist derselbe Zähler auf dem Nenner *operierte* Primärfälle (61.675). **Beide korrekt, zwei Nenner.** Aber: die Kategorie heißt „neoadjuvant **oder präoperativ systemisch**" — breiter als reine NACT | Nenner und Kategoriename im Modul explizit festlegen (§3.1). Für **50–60** kommt ein belegter Alters-Multiplikator **1,28** hinzu ⇒ **0,25–0,28** |
| **K9** | pCR-Anker „NeoSphere 45,8 %" gleichrangig neben KEYNOTE-522 | NeoSphere misst **pCR in der Brust allein** (ohne Nodalstatus), KEYNOTE-522 ypT0/Tis ypN0 — **nicht vergleichbar**, 45,8 % ist nach oben verzerrt | Als HER2+-Anker **TRYPHAENA (45–52 %)** oder TRAIN-2 verwenden (§3.5) |
| **K10** | „TNBC … Pembrolizumab (bei CPS≥10 bzw. Stadium II/III)" | S3 Empf. 4.154 nennt **ausschließlich > 2 cm oder N+** — **kein PD-L1/CPS-Cutoff**. CPS-Abhängigkeit gilt nur metastasiert (KEYNOTE-355) | Verzweigungsbedingung im Modul korrigieren (§3.4) |
| **K11** | pCR-Definition „ypT0 ypN0 streng" (Konzept §5.3) | S3 ist inkonsistent; die maßgebliche Definition (Pathologiekapitel + RT-Tabelle 8) ist **ypT0/is ypN0** — wie in KEYNOTE-522/TRYPHAENA/KATHERINE | Modellkonvention auf **ypT0/is ypN0** umstellen (§3.5) |
| **K12** | pCR wirkt auf den Rezidiv-Hazard in drei Ästen (von Minckwitz) | S3 wörtlich: *„Nur bei triple-negativen und HER2-positiven Mammakarzinomen wird die pCR derzeit als Surrogatmarker … anerkannt"* | pCR-Effekt nur im **TNBC- und HER2+-Ast** — leitlinienkonform und einfacher |
| **K13** | „Ortmann 2022" | **Ortmann O et al., J Cancer Res Clin Oncol 2023;149(3):1195–1209, PMID 35380257 / PMC9984341** (online first 04/2022) | Zitation korrigieren |
| **K6** | §7: „Lokalrezidiv … TRM Survival Tab. 5b" mit Fernmetastasierung 11,0 @5J / 16,6 @10J | TRM-Spezialauswertung `RisikoM0` (n=46.418, Dx 2002–2020) ergibt gewichtet **≈8,4 @5J / ≈13,1 @10J** | **Zwei TRM-Tabellen, zwei Werte.** Nicht mischen — Auflösung siehe §6.2 |
| **K7** | „Kontralaterales Mamma-Ca … Nicht-Trägerinnen 4,6 % @10J (Engel 2020)" | Engel 2020 Abstract wörtlich: Nicht-Trägerinnen **3,6 % (2,2–5,7)** | Zahlendreher im Konzept. BRCA1 25,1 % und BRCA2 6,6 % sind korrekt |
| **K8** | §7 Hazardformen implizit aus Colleoni/Dent/Pan synthetisiert 🔴 | Das **TRM publiziert eine gemessene Hazard-Rate-Spalte pro Jahresintervall** (Spezialauswertung `RisikoM0`, Tab. 21–24, DE, Dx 2002–2020) | **Die Hazardformen müssen nicht mehr aus KM-Kurven abgeleitet werden.** Deutsche, konkurrenzrisikokorrigierte Primärzahlen — der wichtigste Fund dieser Recherche (§6.2) |

Zusätzlich **bestätigt** (keine Änderung nötig): alle zehn OnkoZert-BET/OP-Werte exakt; Radiatio-DCIS 78,4 %;
Revisionsrate 2,39 %; Chemo bei HR+/N+ 60,78 %; endokrine Therapie bei HR+ 96,82 %; Trastuzumab 95,03 %;
KATHERINE 88,3/77,0 % und HR 0,50; Kostev-Persistenz 5 J. AI 35,1 % / TAM 32,5 %; Kostev-Altersmittel AI 69,0 /
TAM 59,1 J.; RKI 5-J-RS nach UICC 101/95/76/31 %; RKI 5-J-RS 50–59 J. 92 %; TRM 15-J-RS 50–59 J. 80,7 %;
alle zehn TRM-pTNM-Überlebenswerte; TRM Überleben ab Metastasierung 69,3/52,2/23,8/10,7 %;
CLEOPATRA 57,1 Monate; Narod 2015 DCIS-20-J-Mortalität 3,3 %; die drei stadienweisen Neoadjuvanz-Anteile
18,9 / 32,7 / 29,5 %; alle vier Ortmann-Neoadjuvanz-Anteile (5,8 / 26,5 / 31,9 / 31,8 %) und alle vier
Ortmann-pCR-Raten (12 / 36 / 53 / 38 %); KEYNOTE-522 pCR 64,8 %; NeoSphere 45,8 % (mit Definitionsvorbehalt, K9).

---

## 1. Lokale Therapie — Operation

### 1.1 BET vs. Mastektomie nach Stadium

**Quelle für alle Zeilen:** OnkoZert/DKG *Jahresbericht der zertifizierten Brustkrebszentren, Kennzahlenauswertung
2025* (Auditjahr 2024, **Kennzahlenjahr 2023**), Abschnitt „Basisdaten — Verteilung operierte Primärfälle
Mammakarzinom", S. 9 — **im Volltext geprüft**, alle Werte exakt. **[alle Alter]**, 312 Standorte, 96,9 % weiblich.

| Arrow (Stadium) | Wert | Zähler / Nenner | Conf. |
|---|---|---|---|
| BET bei **T1 N0 M0** | **0,8615** | 22.187 / 25.753 | 🟢 |
| BET bei **T2 N0 M0** | **0,7053** | 8.362 / 11.856 | 🟢 |
| BET bei T3 N0 M0 | **0,3110** | 306 / 984 | 🟢 |
| BET bei T4 N0 M0 | **0,2720** | 102 / 375 | 🟢 |
| BET bei **N+ (jedes T) M0** | **0,5753** | 8.312 / 14.448 | 🟢 |
| BET bei **DCIS (Tis N0 M0)** | **0,7934** | 5.414 / 6.824 | 🟢 |
| BET bei M1 | **0,3613** | 280 / 775 | 🟢 |
| BET gesamt (operierte Primärfälle) | 0,7370 | 45.455 / 61.675 | 🟢 |
| Mastektomie gesamt (KZ 17) | 0,2630 | 16.220 / 61.675 | 🟢 |

**Repräsentativität der OnkoZert-Basis** (wichtig, weil praktisch der gesamte Therapieteil auf dieser Quelle
steht): RKI-Inzidenz 2022 = **81.206**, in deutschen DKG-zertifizierten Zentren behandelte Primärfälle =
**69.205** ⇒ **Abdeckungsgrad 85,2 %** (KZ 14a, Anmerkung S. 27) 🟢. Die im Bericht ausgewiesenen 73.505
Primärfälle enthalten zusätzlich die 22 NRW-Standorte mit 5.849 Fällen. Der Selektionsvorbehalt „nur zertifizierte
Zentren" ist damit **klein, aber nicht null** — rund ein Siebtel der deutschen Fälle wird außerhalb behandelt.
Quergröße für die Verlaufsmodellierung: **KZ 14b** — 12.976 Patientinnen mit neu aufgetretenem (Lokal-)Rezidiv
und/oder Fernmetastasen (ohne primär M1) = **15,0 %** aller Zentrumsfälle (86.481) 🟢.

> ⚠️ **c/p-Präfix:** Der Bericht beschriftet die Gruppen nur „T1, N0, M0" — **ohne c- oder p-Präfix**. Die im
> Konzept verwendete Lesart „cT1N0M0" ist eine Interpretation. Da neoadjuvante Fälle separat ausgewiesen sind,
> ist eine gemischte Klassifikation wahrscheinlich. **Modellentscheidung explizit dokumentieren.**

**Nicht operierte Primärfälle** — im Konzept als flacher Wert 0,161 geführt, ist aber **stark stadienabhängig**:

| Stadium | Anteil nicht operiert | Conf. |
|---|---|---|
| gesamt | **0,1609** (11.830 / 73.505) | 🟢 |
| **M1** | **0,8463** | 🟢 |
| T4 N0 M0 | 0,458 | 🟢 |
| T1 N0 M0 | **0,0724** | 🟢 |
| DCIS | 0,0304 | 🟢 |

**Nicht als flacher Prior verwenden** — sonst erzeugt das Modul nicht operierte Frühkarzinome in unplausibler Zahl.

Weitere OP-Kennzahlen (alle OnkoZert 2025, 🟢, **[alle Alter]**):

| Kennzahl | Wert |
|---|---|
| KZ 16: BET bei pT1 (inkl. (y)pT0/(y)pT1) | **0,8240** (28.831 / 34.987) |
| KZ 15: R0 mit **nur einem** Eingriff bei BET | **0,8852** ⇒ **Nachresektionsrate ≈ 0,115** |
| KZ 22: Revisionsoperation | **0,0239** (1.474 / 61.675) |
| KZ 13: prätherapeutische histologische Sicherung | 0,9830 |

### 1.2 Alters- und Detektionsmodus-Effekt auf die BET-Quote

Die OnkoZert-Kennzahlen sind **nicht altersstratifiziert**. Die einzige deutsche Quelle mit Altersband *und*
Detektionsmodus ist **Heinig et al., BMC Cancer 2022;22:130 (PMID 35109813 / PMC8812022)**, GePaRD-Claims,
**Diagnosejahr 2008**, n=10.802 — starker Ära-Vorbehalt.

| Stratum | BET | Mastektomie | Conf. |
|---|---|---|---|
| < 50 J. | 70,5 % | 29,5 % | 🟡 Ära 2008 |
| **50–69 J.** | **75,8 %** | 24,2 % | 🟡 **[Quelle 50–69]** |
| 70–79 J. | 66,1 % | 33,9 % | 🟡 |
| ≥ 80 J. | 37,8 % | 62,2 % | 🟡 |
| **50–69 J., screen-detektiert** | **85,7 %** | 14,3 % | 🟡 — für den Screening-Arm des Moduls direkt relevant |
| 50–69 J., Intervallkarzinom | 70,7 % | 29,3 % | 🟡 |
| 50–69 J., screening-berechtigt, ungescreent | 73,1 % | 26,9 % | 🟡 |

**Design-Entscheidung bestätigt** (Konzept §6.1): *auf das Stadium konditionieren, nicht aufs Alter.* Der
Stadieneffekt (86 % → 27 %) ist deutlich größer als der Alterseffekt (75,8 % vs. 69,6 % über alle Alter). Der
Detektionsmodus-Effekt (85,7 % screen-detektiert vs. 73,1 % ungescreent) läuft ohnehin über den Stadienmix und
trägt sich damit implizit durch — **eine zusätzliche Konditionierung auf `bc_detection_mode` bei der
BET-Entscheidung wäre Doppelzählung.**

### 1.3 Axilla — der Teil, der sich gerade ändert

| Arrow | Wert | Basis | Conf. |
|---|---|---|---|
| **alleinige SLNB bei pN0** (Frauen, invasiv, ohne präop. Therapie) | **0,9309** (26.156 / 28.098) | OnkoZert 2025 KZ 20a, S. 34 **[alle Alter]** | 🟢 |
| ⇒ ALND bei pN0 (Übertherapie) | **0,0691** | eigene Rechnung aus KZ 20a | 🟢 |
| Nodalstatus überhaupt bestimmt (KZ 19) | 0,9664 ⇒ **3,4 % ohne axilläres Staging** | ebd., S. 33 | 🟢 |
| **weitere Axillatherapie bei pN1mi** (ALND o. Radiatio) | **0,0733** (84 / 1.146) ⇒ 92,7 % ohne | ebd. KZ 23, Sollvorgabe ≤5 % | 🟢 |
| axilläre LK-Entnahme bei **DCIS + BET** | **0,0248** (132 / 5.314); 214/310 Standorte bei 0 % | ebd. KZ 18 | 🟢 |
| axilläre Rezidivrate nach SLNE | < 0,01 | S3 v5.1 Kap. 4.4.5 | 🟢 |
| **ALND-Rate bei pN+ (Makrometastasen)** | — | **keine Kennzahl im Bericht** | 🔴 Lücke |
| SLNB-Detektionsrate | > 0,99 (indirekt: „SLN nicht identifizierbar" 9 Nennungen bei 53.800 operierten invasiven Fällen) | OnkoZert-Begründungstexte | 🟡 abgeleitet |
| mediane Zahl entfernter LK | SLNB 2–3, ALND 12–16 | **keine deutsche Quelle**; Literaturkonvention | 🔴 Prior |

**Leitlinienstand S3 v5.1 — für eine 50–60-Kohorte hochrelevant:**

| Empf. | Inhalt | Grad |
|---|---|---|
| 4.60 (*mod. 2025*) | pT1–pT3 / cN0, **BET + Ganzbrustbestrahlung**, 1–2 positive SLN → auf ALND verzichten (vorher „kann", jetzt **„sollte"**) — Z0011 | B, EL 2 |
| 4.61 (*neu 2025*) | pT1–pT3 / cN0, **Mastektomie + Bestrahlung**, 1–2 positive SLN → auf ALND verzichten (Basis **SENOMAC**) | B, EL 2 |
| **4.57** (*neu 2025*) | **≥ 50 J. postmenopausal, cT1 cN0, HR+ HER2− G1–2, BET + WBI + adäquate Systemtherapie → Verzicht auf das gesamte operative axilläre Staging möglich** (SOUND, INSEMA) | **0 („kann"), EL 2** |

> ⚠️ **Empfehlung 4.57 trifft genau die Modellkohorte.** In INSEMA hatten > 80 % der Patientinnen dieses
> Low-Risk-Profil. Für Behandlungsjahre ≥ 2025 braucht das Modul einen wachsenden Ast **„keine Axillachirurgie"**.
> Reale Umsetzungsraten liegen **noch nicht vor** 🔴 — im Kennzahlenjahr 2023 tauchte das nur als
> Studienbegründung (EUBREAST/SOUND/INSEMA) bei 14 Zentren auf. **Modellprior für 2025+: 5–15 % der
> Low-Risk-Konstellation ohne axilläres Staging** 🔴, als bewusster Stellknopf zu kennzeichnen.

### 1.4 Rekonstruktion nach Mastektomie — **klare Datenlücke**

> 🔴 **Es existiert keine publizierte deutsche Rekonstruktionsrate.** Der DKG-Kennzahlenbogen Brust enthält
> **keine** Rekonstruktions-Kennzahl (alle 23 KZ geprüft). Das Implantatregister **IRegG** ist erst seit
> **01.07.2024** im Regelbetrieb mit Meldepflicht — Auswertungen sind noch nicht publiziert.

| Aspekt | Beste verfügbare Angabe | Quelle | Conf. |
|---|---|---|---|
| Zeitpunkt-Empfehlung | Sofortrekonstruktion **AGO ++** (LoE 3b/B); Spätrekonstruktion **++**; „delayed-immediate" **+** | AGO 2026.1D Kap. 09 | 🟢 (Empfehlung, keine Rate) |
| Verfahrenswahl bei geplanter RT | Präferenz **autolog** nach/bei geplanter RT; Implantat *vor* RT `+`, *nach* RT `+/-` | ebd. | 🟢 |
| Implantatbasiert an allen Rekonstruktionen | 70–80 % | PMC10415025 (2023) | 🟡 **international**, keine DE-Zahl |
| Mikrochirurgische Lappen DE | 5.671 Lappen / 4.909 Pat., 22 Zentren, 2011–2018 (≈710/Jahr); DIEP dominant; Lappenverlust 2,6–4,2 % | DGPRÄC-QS-Datenbank, PMID 42486463 | 🟢 Absolutzahl, **kein Nenner** |
| Altersabhängigkeit | jüngere Frauen rekonstruieren häufiger — plausibel, **für DE nicht quantifiziert** | — | 🔴 |

**Modellprior 50–60 J. (explizit als Prior kennzeichnen):** Rekonstruktion bei **0,40–0,55** der Mastektomien,
davon **~0,70** implantatbasiert, **~0,65** sofort 🔴. Alle drei Zahlen sind aus internationalen Registern
abgeleitet und **nicht** deutschlandvalidiert. Alternative: Rekonstruktion für v1 ganz auslassen (Konzept §10.2
listet sie bereits unter den bewussten Ausschlüssen) — dann entfällt der 🔴-Block vollständig.

---

## 2. Strahlentherapie

### 2.1 Bestrahlung nach BET

| Arrow | Wert | Basis | Conf. |
|---|---|---|---|
| **RT *empfohlen* nach BET, invasiv** (ohne primär M1) | **0,9780** (38.714 / 39.583); von **allen 312** Standorten erfüllt | OnkoZert 2025 **KZ 4**, S. 15 **[alle Alter]** | 🟢 |
| **RT *begonnen* nach BET, DCIS** | **0,7841** (4.238 / 5.405) | ebd. **KZ 5**, S. 16 | 🟢 |
| **RT tatsächlich durchgeführt, invasiv** | **0,91** (BET + adjuvante Systemtherapie, Start innerhalb 10 Monaten) | Heinig 2022, Dx 2008 | 🟡 Ära |
| RT-Rate gesamt (jede OP-Art), 50–69 J. | 0,802 | ebd. | 🟡 **[Quelle 50–69]** |

> ⚠️ **KZ 4 ist eine Empfehlungs-, keine Durchführungsrate** (Korrektur K4). Der Zähler lautet „denen eine
> Radiatio *empfohlen* wurde". Nur KZ 5 (DCIS) misst „begonnen". Für das Modul: **Indikation 0,978 ·
> Durchführung | Indikation ≈ 0,93** ⇒ effektive RT-Rate nach BET ≈ **0,91** 🟡.

**RT-Verzicht (Omission) — in 50–60 praktisch irrelevant, aber sauber zu begründen:**

| Studie | Einschlussalter | für 50–60 anwendbar? | 5-J-LR ohne RT |
|---|---|---|---|
| PRIME II | ≥ 65 J. | ❌ nein | 4,3 % (10-J **9,8 % vs. 0,9 %**) |
| CALGB 9343 | ≥ 70 J. | ❌ nein | 4 % (10-J 8 % vs. 2 %) |
| LUMINA | ≥ 55 J., pT1 pN0 R0, ER≥1 %, Ki67≤13,25 % | ⚠️ formal ab 55 J., aber einarmig, kurzes FU | 2,3 % (1,2–4,1) |
| **IDEA** | **50–69 J.**, pT1 pN0 R0, HR+, HER2−, Oncotype RS ≤18 | ✅ **direkt** | **50–59 J.: 3,3 %**; 60–69 J.: 3,6 % |
| PROSPECT | ≥ 50 J., cT1cN0, prä-OP MRT | ⚠️ ja, n=201 | 1,0 % |

**S3/AGO-Position:** RT-Verzicht nach BET nur bei **Lebenserwartung < 10 Jahre UND** pT1 pN0 R0 HR+ HER2− unter
endokriner Therapie (**alle** Faktoren, LoE 1a, GR B, AGO `+`). Für 50–60 ist die Lebenserwartungs-Bedingung
praktisch nie erfüllt.
⇒ **Modellwert: RT-Omission in 50–60 = 0,00–0,03**, faktisch nur Ablehnung/Komorbidität 🟢 (leitlinienbasiert).

### 2.2 Fraktionierung und Boost — Hypofraktionierung ist heute Standard

| Regime | Leitlinienstatus | Conf. |
|---|---|---|
| **Moderat hypofraktioniert, ~40 Gy / 15–16 Fx (2,67 Gy ED)** | **S3 v5.1 Empf. 4.95, Empfehlungsgrad A („soll"), EL 1** — *mod. 2025*, starker Konsens; AGO **++** | 🟢 |
| Konventionell 50 Gy / 25–28 Fx | in v5.1 **nicht mehr Standard**; AGO `+` | 🟢 |
| **Ultra-hypo 26 Gy / 5 Fx (FAST-Forward)** | S3 v5.1 Empf. 4.96, Grad **0 („kann")**, *neu 2025*; AGO `+/-` | 🟢 |
| Thoraxwand (PMRT) | moderat hypofraktioniert **„sollte"**; auch nach Rekonstruktion keine Kontraindikation (FABREC, RT-CHARM) | 🟢 |
| Lymphabflusswege (RNI) | **DEGRO 2026** (PMID 42289007 / PMC13290887): moderate Hypofraktionierung 40–43,5 Gy / 15–16 Fx **soll Standard** sein (HypoG-01, DBCG Skagen 1). AGO 2024 noch konservativer — **Divergenz, DEGRO ist aktueller** | 🟢 / ⚠️ |
| **DCIS** | S3 v5.1 Empf. 4.33, Grad **A**: 40 Gy / 15–16 Fx | 🟢 |
| Herzschonung links | S3 v5.1 Empf. 4.97, Grad B: DIBH oder Gating | 🟢 |

**Reale Umsetzung in Deutschland** — nur zwei DEGRO-Befragungen, keine Registerzahl:

| Erhebung | Ergebnis | Conf. |
|---|---|---|
| DEGRO-Mitgliederbefragung 07–08/2017 (n=180), PMID 32904392 | **83,9 %** der Chefärzt:innen nannten **Normofraktionierung** als Standard; Hypofraktionierung nur bei 16 % dominierend | 🟡 **historisch, überholt** |
| DEGRO-AG-Umfrage 2026 (n=69), PMID 42329259 | **moderate Hypofraktionierung ist Standard in 77 %** der Abteilungen; >95 % setzen überhaupt (ultra-)hypofraktionierte Regime ein | 🟡 kleine n, Selbstauskunft |

**Modellwerte (Behandlungsjahr ≥ 2024):**

| Arrow | Wert | Conf. |
|---|---|---|
| moderat hypofraktioniert (40,05 Gy / 15 Fx à 2,67 Gy) | **0,80** (Korridor 0,75–0,85) | 🟡 |
| konventionell (50 Gy / 25 Fx) | **0,17** | 🟡 |
| ultra-hypofraktioniert (26 Gy / 5 Fx) | **0,03** | 🔴 |

**Boost:**

| Aspekt | Wert | Basis | Conf. |
|---|---|---|---|
| S3 v5.1 Empf. 4.98 | **≤ 50 J.: „soll"**; **> 50 J.: „sollte" nur bei erhöhtem Risiko** (G3, HER2+, TNBC, > T1) | S3 v5.1, GR A/B | 🟢 |
| Boostdosis | **16 Gy / 8 Fx** sequentiell (EORTC 22881-10882) **oder** SIB (48 Gy / 15 Fx auf das Tumorbett bei 40 Gy / 15 Fx Brust; IMPORT-HIGH, RTOG 1005) | S3 Empf. 4.99, GR B | 🟢 |
| **Boost-Nutzen exakt im Zielalter** | 51–60 J., 20-J-IBTR **10,3 % (Boost) vs. 13,2 %**, Δ 2,96 Pp., HR 0,69 | Bartelink, Lancet Oncol 2015, via AGO 2024.1D | 🟢 **[50–60!]** |
| **Reale Boost-Rate DE** | **~0,40** (1.366 / 3.411, hypofraktioniert bestrahlte Pat.); Prädiktoren: jüngeres Alter, T2, HER2+ | Horry et al., Oncol Lett 2026;32(4), PMID 42643741 (Halle + Magdeburg) | 🟡 **2 Zentren**, nicht national |

⇒ **Modellwert Boost bei 50–60:** wegen der Altersgrenze „≤50 soll / >50 sollte bei Risiko" **risikoabhängig**:
G3 oder HER2+ oder TNBC oder >T1 ⇒ **0,80**; sonst **0,25** 🔴 (kalibriert auf die beobachteten ~40 % Gesamtrate).

### 2.3 Bestrahlung nach Mastektomie (PMRT) und regionale Lymphabflusswege

**Indikationen — S3 v5.1 Empf. 4.110, Empfehlungsgrad A, EL 1 („soll angeboten werden"):** pT4 · pT3 pN0 R0 mit
Risikofaktoren (L1, G3, prämenopausal, Alter < 50 J.) · R1/R2 ohne Nachresektionsmöglichkeit · **≥ 4 befallene
axilläre LK** („regelhaft") · **1–3 befallene LK mit erhöhtem Risiko** (HER2+, TNBC, G3, L1, Ki-67 > 30 %,
> 25 % der entfernten LK befallen, ≤ 45 J. + Zusatzfaktor, ER−). **Verzicht** bei 1–3 LK mit geringem Risiko
(pT1, G1, ER+, HER2− — ≥ 3 Merkmale). Risikodefinition: hoch = LRR > 20 %, intermediär = 10–20 %. Nutzen
(EBCTCG): ca. **8 %** Verbesserung des mammakarzinomspezifischen Überlebens. Alle 🟢.

**Indikationsanteil unter den Mastektomie-Patientinnen** (eigene Ableitung aus der OnkoZert-Stadienverteilung,
n=16.220 Mastektomien) 🔴:

| Stadiengruppe der Mastektomierten | Anteil | PMRT-Indikation |
|---|---|---|
| N+ (jedes T) M0 | 37,8 % | ja bzw. risikoadaptiert |
| T3 N0 M0 | 4,2 % | nur mit Risikofaktoren |
| T4 N0 M0 | 1,7 % | ja (Grad A) |
| T1/T2 N0 M0 | 43,5 % | nein |
| DCIS | 8,7 % | nein (AGO: `--`) |
| M1 | 3,1 % | individuell |
| **⇒ PMRT-Indikationskorridor** | **0,33–0,44** | 🔴 eigene Ableitung |

**Trianguliert** mit der einzigen realen deutschen Zahl: **0,39** (Mastektomie + adjuvante Systemtherapie,
RT-Start innerhalb 10 Monaten; Heinig 2022, Dx 2008) 🟡. ⇒ **Modellwert PMRT = 0,38** 🟡.

**RNI (regionale Lymphabflusswege):** Indikationslogik AGO 2024.1D — ≥4 befallene LK (1a/A/`++`); 1–3 LK mit
zentralem/medialem Sitz **oder** HR-negativ (1a/A/`+`); pN0 + prämenopausal + zentral/medial + G3 + HR− (1a/B/`+`).
EBCTCG 2023 (n=12.167, med. FU 13,7 J.): Rezidiv −2,6 Pp., **BC-Mortalität −3,0 Pp.** nach 15 J.; nach pN:
pN0 −1,6 · pN1-3 −2,7 · pN4+ −4,5 Pp. 🟢.
⚠️ **Kein deutscher realer RNI-Anteil publiziert** 🔴 — zusätzlich fehlt im OnkoZert-Bericht der **N1/N2/N3-Split**
(nur „N+ gesamt"), was das Konzept in §11 Lücke 6 bereits als offen führt.

---

## 3. Neoadjuvanz und pCR

Der im Konzept als „wichtigster roter Arrow" bezeichnete Block. Er lässt sich jetzt **deutlich verbessern**:
die stadienweisen Anteile sind für 2023 gemessen 🟢, es gibt eine **altersstratifizierte deutsche Kohorte mit
einer direkten 50–59-Zeile** 🟢, und die Subtyp-Reskalierung bekommt eine dokumentierte Herleitung statt einer
freien Setzung.

### 3.1 Anteil neoadjuvant behandelter Patientinnen nach Stadium (2023, gemessen)

**Nennerkonflikt aufgelöst — beide im Umlauf befindlichen Zahlen sind richtig** (OnkoZert 2025, S. 8, Zeile
„Primärfälle operiert mit neoadj. Th."):

| Nenner | Zähler | Wert |
|---|---|---|
| **alle Primärfälle** (73.505) | 15.699 | **21,36 %** ⇒ der Konzeptwert „21,4 %" ✅ |
| **operierte Primärfälle** (61.675) | 15.699 | **25,45 %** |

Die stadienweisen Werte des Berichts benutzen den Nenner **„Primärfälle gesamt der jeweiligen Stadiengruppe"**
(inkl. der nicht operierten); Probe: „nicht operiert" + „operiert mit neoadj." + „operiert ohne neoadj." = 100,00 %
je Spalte 🟢.

| Stadiengruppe | neoadj. operiert | Primärfälle gesamt | **Anteil** | Conf. |
|---|---|---|---|---|
| **Tis (DCIS) N0 M0** | 90 | 7.038 | **0,0128** | 🟢 |
| **T1 N0 M0** | 5.247 | 27.762 | **0,1890** ✅ | 🟢 |
| **T2 N0 M0** | 4.553 | 13.947 | **0,3265** ✅ | 🟢 |
| **T3 N0 M0** | 329 | 1.161 | **0,2834** | 🟢 |
| **T4 N0 M0** | 171 | 692 | **0,2471** | 🟢 |
| **N+ (jedes T) M0** | 5.048 | 17.092 | **0,2953** ✅ | 🟢 |
| M1 | 212 | 5.042 | **0,0420** | 🟢 |
| nicht zuzuordnen | 49 | 771 | 0,0636 | 🟢 |
| **Gesamt** | 15.699 | 73.505 | **0,2136** | 🟢 **[alle Alter]** |

Die drei im Konzept genannten Stadienwerte (18,9 / 32,7 / 29,5 %) sind exakt bestätigt; **T3, T4, Tis und M1 sind
neu** und schließen die Tabelle.

> ⚠️ **Zwei Definitionsvorbehalte.** (1) Wieder **kein c/p-Präfix** im Bericht. (2) Die Kategorie lautet
> **„neoadjuvant *oder präoperativ systemisch*"** — also **breiter als reine NACT**; präoperative endokrine
> Therapie ist mit erfasst. Das erklärt vermutlich einen Teil der 18,9 % bei T1 N0 M0, die für reine Chemotherapie
> hoch erscheinen. Das Modul sollte die Kategorie entsprechend breit benennen (`bc_preop_systemic`), nicht
> `bc_nact`.
> ❌ **pCR-Rate, Subtypaufschlüsselung und Zeittrend 2019–2023 stehen im OnkoZert-Bericht nicht** — Volltext-Grep
> auf `pCR`, `ypT0`, `Komplettremission`: null Treffer; Rezeptor-/HER2-Status erscheint ausschließlich als
> *Nennerfilter* in KZ 6/7/8/9, nie als Verteilungsgröße; die Basisdatentabellen haben keine Jahresachse 🟢
> (Negativbefunde).

### 3.2 Altersstratifizierung — die 50–59-Zeile, die im Konzept fehlte

**Neuer Fund, größer als Ortmann und mit direkter Altersaufschlüsselung:**
*Impact of age on indication for chemotherapy in early breast cancer patients: results from 104 German
institutions from 2008 to 2017*, Arch Gynecol Obstet 2023;308(1):219–229, **PMID 36604331 / PMC10191903**,
n=**124.084**, 104 deutsche Brustzentren, Dx **2008–2017**.

| Altersgruppe | n | Chemo gesamt | davon **neoadjuvant** | davon adjuvant |
|---|---|---|---|---|
| 40–49 J. | 17.266 | 59,4 % | 40,1 % | 59,9 % |
| **50–59 J.** | **28.394** | **47,1 %** | **33,4 %** | **66,6 %** |
| 60–69 J. | 31.620 | 37,5 % | 25,5 % | 74,5 % |
| ≥ 70 J. | 42.066 | 17,6 % | 22,8 % | 77,2 % |

Alle 🟢 **[50–60 direkt]**. Gesamtkohorte: Chemo 37,3 %, davon NACT 33,0 % ⇒ **NACT-Anteil an allen Patientinnen
gesamt 12,3 %**, für **50–59 J. 0,471 × 0,334 = 15,7 %**.
⇒ **Alters-Multiplikator 50–59 vs. alle Alter = 15,7 / 12,3 = 1,28** 🟢.

**Auf das Kennzahlenjahr 2023 hochgerechnet:** 0,2136 × 1,28 = **≈ 0,27**.
⇒ **Modellwert Neoadjuvanz-/Präoperativ-systemisch-Anteil für die Kohorte 50–60: 0,25–0,28** 🟡 (gemessene
2023-Marginale × belegter Alters-Multiplikator). Das liegt spürbar über den 21,4 % des Konzepts, weil die
50–60-Kohorte chemotherapie-affiner ist als der Alle-Alter-Durchschnitt.

### 3.3 Subtyp-Anteile — die Ära-Reskalierung, jetzt hergeleitet

**Basisquelle (exakte Zitation korrigiert):** Ortmann O, Blohmer JU, Sibert NT, Brucker S, Janni W, Wöckel A,
Scharl A, Dieng S, Ferencz J, Inwald EC, Wesselmann S, Kowalski C. *Current clinical practice and outcome of
neoadjuvant chemotherapy for early breast cancer: analysis of individual data from 94,638 patients treated in
55 breast cancer centers.* **J Cancer Res Clin Oncol 2023;149(3):1195–1209**, doi 10.1007/s00432-022-03938-x,
**PMID 35380257 / PMC9984341**. Online first **April 2022** (daher die kursierende Jahresangabe 2022);
Datenbasis **OncoBox Research**, Dx **2007–2018**. **Alle Werte exakt bestätigt** 🟢:

| Subtyp | NACT-Anteil 2007–2018 | n / Nenner | rel. zum Gesamt (11,0 %) |
|---|---|---|---|
| HR+/HER2− | **0,058** ✅ | 4.061 / 69.522 | 0,53 |
| HR+/HER2+ | **0,265** ✅ | 2.193 / 8.281 | 2,41 |
| HR−/HER2+ | **0,319** ✅ | 1.253 / 3.927 | 2,90 |
| TNBC | **0,318** ✅ | 3.098 / 9.731 | 2,89 |
| **Gesamt** | **0,110** (10.372 / 94.638) | | 1,00 |

Trend in Ortmann: 5 % (2007) → **17,3 % (2016)**, danach stabil ~17–18 % bis 2018 🟢.

**Konsistenzprobe der Subtyp-Marginale.** Mit der deutschen Subtypverteilung aus Konzept §3.1 (TRM 50–69,
zusammengefasst: HR+/HER2− 76,5 % · HR+/HER2+ 10,5 % · HR−/HER2+ 4,2 % · TNBC 8,7 %) ergibt die Ortmann-Tabelle
gewichtet **11,3 %** gegen die publizierten **11,0 %** ✓ — die Subtypraten und die Marginale sind intern
konsistent 🟢. Das rechtfertigt die folgende proportionale Reskalierung.

**Reskalierung auf das Kennzahlenjahr 2023** (Methode: relative Subtyp-Multiplikatoren aus Ortmann konstant
halten, auf die gemessene 2023-Marginale 0,2136 skalieren, anschließend so normieren, dass die gewichtete
Marginale wieder 0,2136 trifft):

| Subtyp | Ortmann 2007–18 | **Vorschlag 2023 (alle Alter)** | Konzept-Vorschlag | Conf. |
|---|---|---|---|---|
| HR+/HER2− | 0,058 | **0,11** | ~0,10 | 🔴 |
| HR+/HER2+ | 0,265 | **0,50** | 0,45–0,50 | 🔴 |
| HR−/HER2+ | 0,319 | **0,60** | ~0,60 | 🔴 |
| TNBC | 0,318 | **0,60** | 0,60–0,70 | 🔴 |
| *gewichtete Marginale (Probe)* | *0,113* | ***0,214*** ✓ | — | |

> ✅ **Der Konzeptvorschlag ist damit bestätigt** — er war eine gute Setzung und bekommt hier nur eine
> nachvollziehbare Herleitung und eine Konsistenzprobe. Einzige Änderung: **TNBC 0,60 statt 0,60–0,70**, weil
> 0,65+ die Marginale übersteuert.
> Für die **50–60-Kohorte** alle vier Werte zusätzlich mit dem Alters-Multiplikator **1,28** aus §3.2 versehen
> (⇒ HR+/HER2− 0,14 · HR+/HER2+ 0,64 · HR−/HER2+ 0,77 · TNBC 0,77) 🔴 — oder, sauberer, **die Neoadjuvanz auf
> das Stadium konditionieren (§3.1, gemessen 🟢) und den Subtyp nur als Multiplikator anhängen**. Letzteres ist
> die empfohlene Modellstruktur, weil dann nur ein einziger Faktor 🔴 ist statt der ganzen Tabelle.

**Bestätigte Lücke:** Es existiert **keine deutsche Auswertung mit Diagnosezeitraum nach 2018** und
subtypspezifischem Neoadjuvanz-Anteil (systematische PubMed-Suche 2021–2026: 16 Treffer, keiner passend) 🔴.
Beide besten Quellen enden 2017/2018, also **vor** der Pembrolizumab-Ära (EU-Zulassung TNBC neoadjuvant 2021)
und vor der Ausweitung der dualen HER2-Blockade. Die realen Anteile bei TNBC und HER2+ liegen heute
**mit Sicherheit über** 31,8 / 31,9 % — die Höhe bleibt unbelegt.

### 3.4 Wann neoadjuvant? — die S3-Logik, die das Modul verzweigen lässt

Die S3 (v5.0, Dez. 2025) kennt **keine subtypspezifische „soll-neoadjuvant"-Empfehlung**. Neoadjuvanz ist formal
**Grad 0 („kann")**; die faktische Subtypsteuerung entsteht **indirekt** über die Pembrolizumab- und
Pertuzumab-Empfehlungen, die *nur neoadjuvant* definiert sind.

| Empf. | Inhalt (gekürzt zitiert) | Grad |
|---|---|---|
| **4.138** (*mod. 2025*) | lokal fortgeschritten, primär inoperabel oder inflammatorisch → neoadjuvante Systemtherapie **soll** | EK, „soll" — **die einzige Soll-Indikation** |
| **4.139** (*geprüft 2025*) | *„Ist eine Chemotherapie indiziert, **kann** diese vor der Operation … oder danach … Beide Verfahren sind hinsichtlich des Gesamtüberlebens gleichwertig."* | **0**, EL 2 |
| Fließtext S. 143 | *„Triple-negative und HER2 positive Karzinome werden **in der Regel** neoadjuvant behandelt."* | — |
| **4.152** (*neu 2025*) | TNBC **> 10 mm und N0** → Chemotherapie **sollte** | EK |
| **4.151** (*mod. 2025*) | TNBC **Stadium II–III** → **Platinsalze** zusätzlich, **unabhängig vom BRCA-Status** (Cochrane, 20 Studien: neoadj. DFS HR 0,63 [0,53–0,75], OS HR 0,69 [0,55–0,86]) | EK |
| **4.154** (*neu 2025*) | TNBC **> 2 cm oder N+** → **Pembrolizumab** + neoadjuvante Chemo mit **Anthrazyklin/Taxan/Carboplatin**, postoperativ **9 Zyklen adjuvant** fortsetzen | **B** |
| **4.161** (*neu 2025*) | HER2+ **> 2 cm und/oder N+** → neoadjuvante Chemo + **Trastuzumab und Pertuzumab** | **B**, EL 2 |
| **4.160** (*mod. 2025*) | HER2+ **≤ 2 cm und cN0** → **primäre Operation** möglich, um auf **Paclitaxel + Trastuzumab über 12 Wochen** zu deeskalieren (APT, n=410, 10-J-iDFS 91,3 %, OS 94,3 %) | A / 0 |
| **4.144** (*geprüft 2025*) | neoadjuvante **endokrine** Therapie ist **keine Standardtherapie**; nur bei fehlender Chemo-Indikation oder inoperablen Tumoren multimorbider Patientinnen | EK |

> ✅ **Antwort auf die offene CPS-Frage: Pembrolizumab neoadjuvant ist NICHT CPS-abhängig.** Die S3 nennt
> ausschließlich **> 2 cm oder N+** — kein PD-L1-Cutoff. Das entspricht KEYNOTE-522, wo der pCR-Vorteil
> unabhängig von der PD-L1-Expression war. Die CPS-Abhängigkeit gilt **nur im metastasierten Setting**
> (KEYNOTE-355) 🟢. Der Konzepttext („Pembrolizumab bei CPS≥10 bzw. Stadium II/III") ist an dieser Stelle zu
> korrigieren.

⇒ **Empfohlene Modell-Verzweigung** (ersetzt einen flachen Subtyp-Prior):

| Subtyp | Bedingung | Pfad |
|---|---|---|
| **TNBC** | > 2 cm oder N+ | neoadjuvant, Anthrazyklin/Taxan/**Carboplatin + Pembrolizumab**, danach 9 Zyklen Pembrolizumab adjuvant |
| **TNBC** | 10–20 mm, N0 | neoadjuvant oder adjuvant Chemo (ohne Pembro-Pflicht) |
| **TNBC** | ≤ 10 mm, N0 | Chemo nicht generell empfohlen |
| **HER2+** | > 2 cm und/oder N+ | neoadjuvant Chemo + **Trastuzumab + Pertuzumab** → pCR-Weiche |
| **HER2+** | ≤ 2 cm und cN0 | **primäre OP** + De-Eskalation (Paclitaxel + Trastuzumab 12 Wochen, Trastuzumab gesamt 1 J.) |
| **HR+/HER2−** | — | überwiegend primäre OP; neoadjuvante endokrine Therapie ist Ausnahme |

**Anteil der TNBC, die das Pembrolizumab-Kriterium erfüllen (> 2 cm oder N+): ~0,60–0,70** 🔴 grobe Schätzung,
nicht belegt. **Uptake von Pembrolizumab neoadjuvant in Deutschland: keine publizierte Zahl** (PubMed-Suche
`pembrolizumab AND German AND triple-negative AND (real-world OR uptake OR registry)`: **count = 0**);
OnkoZert führt keine Immuncheckpoint-Kennzahl 🟢 (Negativbefund). ⇒ **Uptake als freier Parameter** 🔴.

### 3.5 pCR — Definition, Raten, Surrogatstatus

**Definition:** Die S3 ist **in sich nicht konsistent** — Pathologiekapitel S. 143: *„die pCR, definiert als das
**Fehlen invasiver Tumorresiduen in Mamma und Lymphknoten**"* (= **ypT0/is ypN0**, DCIS zulässig); Empf. 4.111
(Radiotherapie) schreibt dagegen *„bei pCR (**ypT0 und ypN0**)"*; Tabelle 8 (RT-Algorithmus) wieder
**ypT0/is ypN0** 🟢.
⇒ **Modellkonvention: durchgängig `ypT0/is ypN0`**, weil das der Definition der Zulassungsstudien (KEYNOTE-522,
TRYPHAENA, KATHERINE) entspricht. **Das ist eine Änderung gegenüber Konzept §5.3, das „ypT0 ypN0 streng"
vorsieht** — die strenge Variante ist die Minderheitsschreibweise innerhalb derselben Leitlinie.

**Surrogatstatus — S3 wörtlich (S. 143):**
> *„Allerdings gilt der enge Zusammenhang zwischen pCR und Verlauf offensichtlich **nicht für alle Subtypen in
> gleicher Weise**. **Nur bei triple-negativen und HER2-positiven Mammakarzinomen wird die pCR derzeit als
> Surrogatmarker** für den Benefit einer Chemotherapie bzw. Anti-HER2-Therapie anerkannt."* 🟢

Das ist **enger** als die im Konzept zitierte von-Minckwitz-Nuance (pCR prognostisch bei Luminal B/HER2−,
HER2+ nicht-luminal und TNBC, *nicht* bei Luminal A und *nicht* bei Luminal B/HER2+). ⇒ **Modellregel: der
pCR-Zustand wirkt nur im TNBC- und im HER2+-Ast auf den Rezidiv-Hazard** — das ist die leitlinienkonforme,
konservativere Variante und zugleich einfacher zu implementieren.

**pCR-Raten — deutsche Realwelt, altersstratifiziert (PMID 36604331, Dx 2008–2017):**

| Altersgruppe | HR+/HER2− | HR+/HER2+ | HR−/HER2+ | TNBC | alle |
|---|---|---|---|---|---|
| 40–49 J. | 10,9 % | 27,2 % | 37,2 % | 31,3 % | 22,5 % |
| **50–59 J.** | **9,0 %** | **26,2 %** | **43,2 %** | **28,4 %** | **22,6 %** |
| 60–69 J. | 8,1 % | 29,4 % | 37,9 % | 27,7 % | 21,3 % |

Alle 🟢 **[50–60 direkt]** — das ist die einzige altersaufgelöste deutsche pCR-Tabelle.

**Gegen Ortmann (Dx 2007–2018, alle Alter):** HR+/HER2− **12 %** · HR+/HER2+ **36 %** · HR−/HER2+ **53 %** ·
TNBC **38 %** — alle vier exakt bestätigt 🟢, aber **systematisch höher** als die altersstratifizierte Kohorte
(TNBC 38 vs. 28,4 % @50–59). Ursachen: andere Zentrenauswahl, anderer Zeitraum, **in beiden Papieren nicht
ausformulierte pCR-Definition**.
⇒ **Für die 50–60-Kohorte die altersstratifizierten Werte verwenden, Ortmann als Obergrenze führen.**

**Studienanker (per E-utilities am Abstract verifiziert):**

| Studie | Arm | pCR | Definition | PMID |
|---|---|---|---|---|
| **KEYNOTE-522** | Pembro + Chemo | **64,8 %** (59,9–69,5) ✅ | ypT0/Tis ypN0 | **32101663** |
| | Placebo + Chemo | **51,2 %** (44,1–58,3) | Δ **13,6 Pp.** (5,4–21,8), p<0,001 | |
| **NeoSphere** Gr. B | Pertuzumab+Trastuzumab+Docetaxel | **45,8 %** (36,1–55,7) ✅ | ⚠️ **nur pCR in der Brust** | **22153890** |
| Gr. A | Trastuzumab+Docetaxel | 29,0 % (20,6–38,5), p=0,0141 | | |
| **TRYPHAENA** | Arm A / B / C | **50,7 / 45,3 / 51,9 %** | ypT0 ypN0 | via S3 S. 196 |
| **TRAIN-2** | anthrazyklinhaltig / -frei | **67 / 68 %** (p=0,95) | | via S3 S. 196 |

> ⚠️ **Korrektur zum Konzept:** die NeoSphere-45,8 % sind **nicht** mit ypT0/ypN0-Definitionen vergleichbar —
> primärer Endpunkt war **pCR in der Brust allein** (ohne Nodalstatus) und damit nach oben verzerrt.
> **Als HER2+-Anker besser TRYPHAENA (45–52 %) oder TRAIN-2 (67–68 %) verwenden.**
> KEYNOTE-522 Langzeit: 36-Mon.-EFS **84,5 % vs. 76,8 %** (PMID 35139274); **60-Mon.-OS 86,6 % vs. 81,7 %,
> p=0,002**, medianes FU 75,1 Mon. (PMID 39282906) 🟢.
> **GeparOcto ist im S3-Korpus nicht zitiert** (FTS-Treffer 0 für GeparOcto/GeparX/GeparSepto) — der im Konzept
> genannte Anker „GeparOcto TNBC 48,5/51,7 %" sollte entweder direkt belegt oder gestrichen werden 🔴.

**Empfohlene pCR-Modellwerte für eine 50–60-Kohorte, Behandlungsjahr ≥ 2023** — deutsche Altersbasis, um den
Ära-Effekt der neuen Substanzen angehoben:

| Subtyp | deutsche Basis @50–59 (2008–17) | **Modellwert 2023+** | Herleitung | Conf. |
|---|---|---|---|---|
| **HR+/HER2−** | 9,0 % 🟢 | **0,09** | keine neue Substanz in diesem Ast | 🟢 |
| **HR+/HER2+** | 26,2 % 🟢 | **0,35** | duale Blockade (TRYPHAENA 45–52 % Trial-Niveau) | 🔴 |
| **HR−/HER2+** | 43,2 % 🟢 | **0,52** | dito | 🔴 |
| **TNBC ohne Pembrolizumab** | 28,4 % 🟢 | **0,28** | unverändert | 🟢 |
| **TNBC mit Pembrolizumab** | — | **0,36** | deutsche Basis × KEYNOTE-522-Effektverhältnis (64,8/51,2 = **1,27**) | 🔴 |

> Die Konzeptvorschläge (TNBC 60 %, HER2+/HR− 60 %, HER2+/HR+ 40 %, Luminal B 12 %, Luminal A 6 %) sind
> **Trial-Niveau** und liegen deutlich über der deutschen Versorgungsrealität. Für ein Modell, das gegen deutsche
> Register validiert wird, sind die Werte oben die besseren Anker; die Trial-Werte gehören als Obergrenze
> dokumentiert.

**Post-neoadjuvante Eskalation — die Weiche hinter dem pCR-Zustand:**

| Ast | Bedingung | Therapie | Anteil |
|---|---|---|---|
| HER2+ | **non-pCR** | **14 Zyklen T-DM1** (S3 4.165, Grad A) | 1 − pCR ⇒ **0,48–0,65** je nach Regime 🟡 |
| HER2+ | pCR | Trastuzumab auf 1 Jahr komplettieren; Pertuzumab-Fortführung nur „kann" bei initialem axillärem LK-Befall (S3 4.162) | pCR-Anteil |
| TNBC | **non-pCR** | **Capecitabin 6–8 Zyklen** (S3 4.155, Grad B) | 1 − pCR ⇒ **0,64–0,72** 🟡 |
| TNBC | non-pCR **oder** > pT2 und/oder > pN1, **+ gBRCA1/2** | **Olaparib 1 Jahr** (S3 4.156, Grad B) | klein 🔴 |

⚠️ **Reihenfolge-Falle:** die S3 schreibt zu 4.155 selbst *„Die Datenlage lässt keine eindeutige Empfehlung für
Patientinnen zu, die zuvor Platin möglicherweise dann auch in Kombination mit Pembrolizumab erhalten haben."* 🟢
Ein Modul, das erst Pembrolizumab und dann automatisch Capecitabin vergibt, überzeichnet die Realität.

---

## 4. Adjuvante Systemtherapie

### 4.1 Endokrine Therapie — Wirkstoffwahl in 50–60 (Korrektur K1)

**Der Menopausenstatus ist die primäre latente Variable dieses Blocks**, nicht das Alter. Im Fenster 50–60 liegt
genau der Übergang.

| Alter | Anteil postmenopausal | Basis | Conf. |
|---|---|---|---|
| 50 | ~0,50 | Median Menopausenalter DE **50 J. (IQR 47–53)**, Bonn-Kohorte, DOI 10.2478/s11536-007-0017-3; DEGS1 Mittel **49,7 J.**; EPIC-Potsdam Median 50 J. | 🟡 abgeleitet |
| 52 | ~0,68 | Interpolation aus IQR | 🔴 |
| 55 | ~0,86 | ebd. | 🔴 |
| 58 | ~0,95 | ebd. | 🔴 |
| 60 | ~0,97 | ebd. | 🔴 |

> Zusätzlich: **chemotherapie-induzierte Amenorrhoe** macht den Status in dieser Altersgruppe meist permanent.
> S3 Empf. 4.142 verlangt bei Hochrisiko-Patientinnen mit CIA **Hormonstatus-Monitoring**, damit bei biochemisch
> prämenopausalen Werten die Ovarialsuppression noch bis 2 Jahre nach ET-Beginn indiziert werden kann 🟢. Das
> Modul braucht also einen **Statuswechsel-Arm nach Chemotherapie**, keinen fixen Baseline-Status.

**Wirkstoffsplit — die wichtigste Korrektur dieses Kapitels:**

| Altersgruppe | n AI | n TAM | **AI-Anteil** | **TAM-Anteil** | Conf. |
|---|---|---|---|---|---|
| ≤ 50 J. | 8.607 | 39.023 | 0,181 | **0,819** | 🟢 abgeleitet |
| **51–60 J.** | **30.583** | **35.395** | **0,464** | **0,536** | 🟢 **[50–60]** |
| 61–70 J. | 44.023 | 24.274 | 0,645 | 0,355 | 🟢 |
| > 70 J. | 72.793 | 29.685 | 0,710 | 0,290 | 🟢 |
| *Gesamt (Kontrollwert)* | 156.006 | 128.377 | *0,548* | *0,452* | 🟢 |

Quelle: **Jacob L, Kalder M, Kostev K.** *Persistence with tamoxifen and aromatase inhibitors in Germany*,
J Cancer Res Clin Oncol 2023;149(6):2417–2424, **PMID 36149512 / PMC10349696**, IQVIA **LRx**, Indexzeitraum
2016–2020, **n=284.383 Neueinsteller**. Der altersstratifizierte Split ist aus der publizierten Altersverteilung
je Wirkstoffkohorte exakt rekonstruiert (Summenprobe: 47.630 + 65.978 + 68.297 + 102.478 = 284.383 ✓).
Altersmittelwerte AI **69,0 J.** / TAM **59,1 J.** ✅ wie im Konzept.

⇒ **Modellwert 50–60: AI 0,46 / Tamoxifen 0,54** 🟢 — statt der im Konzept vorgeschlagenen 0,55–0,65 AI 🔴.
Innerhalb des Fensters ist ein Gradient plausibel (bei 50 J. eher 0,30 AI, bei 60 J. eher 0,60) 🔴 — nicht
publiziert, aber konsistent mit dem Menopausenprofil oben.
*Caveat:* LRx erfasst Verordnungen, nicht Indikationen; ein kleiner metastasierter Anteil ist enthalten 🟡.

**Leitlinien-Logik (S3 v5.0, Kap. 4.8.2, S. 180–186) — bestimmt, welche Äste das Modul überhaupt braucht:**

| Empf. | Inhalt | Grad |
|---|---|---|
| 4.140 | alle HR+ invasiven Tumoren **sollen** endokrine Therapie erhalten | A |
| 4.141 | ET erst **nach** Chemo beginnen; parallel zur Radiatio erlaubt | A |
| 4.143 | postmenopausal **sollte** die ET einen Aromatasehemmer enthalten | B |
| **4.146** (*neu 2025*) | prämenopausal mit **erhöhtem Rezidivrisiko sollte** OFS enthalten: **2–5 J. OFS + Tamoxifen** *oder* **5 J. OFS + AI** | B |
| 4.147 (*neu 2025*) | AI+OFS vs. TAM+OFS: geringeres Rezidivrisiko, **noch kein OS-Effekt** | EK |
| **4.148** (*neu 2025*) | postmenopausal: AI-haltig **≥ 5 J.**, bei erhöhtem Risiko **bis 7–8 J.** | ST |

**OFS-Indikationskriterien** (S3 S. 182, SOFT/TEXT-Logik): prämenopausaler Status trotz Chemo · Lymphknotenbefall ·
Tumor > 2 cm · G3 · sonstiges erhöhtes tumorbiologisches Risiko · Alter < 35 J. 🟢. Prämenopausal mit niedrigem
Risiko: **Tamoxifen 5 J. bleibt Standard** 🟢.

⇒ **Modellstruktur endokrin:**

| Ast | Bedingung | Regime |
|---|---|---|
| A | postmenopausal (Alter-abhängige Wahrscheinlichkeit oben) | **AI 5 J.**, bei erhöhtem Risiko 7–8 J. |
| B | prämenopausal, niedriges Risiko | **Tamoxifen 5 J.** |
| C | prämenopausal, erhöhtes Risiko | **OFS + Tamoxifen (2–5 J.)** *oder* **OFS + AI (5 J.)** |

Der beobachtete Verordnungssplit (AI 0,46 / TAM 0,54) ist die **Marginale, gegen die diese drei Äste kalibriert
werden müssen** — nicht ein eigener unabhängiger Arrow.

### 4.2 Dauer und Switch

| Größe | Wert | Basis | Conf. |
|---|---|---|---|
| Zieldauer Standard | **5 Jahre** | S3 Empf. 4.148 | 🟢 |
| Zieldauer bei erhöhtem Risiko | **7–8 Jahre** (nicht 10) | ebd.; 10 J. AI vs. 7–8 J. **ohne** Überlebensvorteil | 🟢 |
| Tamoxifen 10 J. vs. 5 J. | Rezidiv/Mortalität −~20 %, Effekte **v. a. nach Jahr 10**; aktuell v. a. **prämenopausal** mit Risikoprofil | ATLAS/aTTom via S3 | 🟡 |
| Erweiterte AI nach 5 J. AI | Rezidivrisiko −10–30 %, **kein signifikanter OS-Effekt** | S3-Referat | 🟢 |
| Sequenz TAM → AI | leitliniengerecht („AI 5 J. **oder in der Sequenz mit Tamoxifen**"), der alleinigen TAM-Therapie überlegen | S3 | 🟢 |
| **Anteil Switch-Strategien in DE** | — | **keine Daten**; Kostev/LRx schließt Switcher aus | 🔴 Lücke |
| **Uptake erweiterte ET > 5 J. in DE** | — | **keine Daten** | 🔴 Lücke (= Konzept §11 Lücke 10, bestätigt) |

> ⚠️ Ein **binäres „5 vs. 10 Jahre"** bildet die deutsche Leitlinie **nicht** korrekt ab. Richtig ist ein
> Dreizustand: **5 J. (Standard) / 7–8 J. (erhöhtes Risiko) / > 8 J. (Ausnahme)**. Switch-Anteil als freier
> Parameter, plausible Größenordnung 0,15–0,25 der TAM-Starterinnen 🔴 (reine Annahme).

### 4.3 Persistenz und Abbruch — der modellierbare Zeitprozess

Das ist der Teil, den kein anderes synthetisches Mammadataset abbildet, und er ist direkt aus deutschen
Verordnungsdaten belegt.

| Abbruchdefinition | Persistenz @5 J. AI | Persistenz @5 J. TAM | Conf. |
|---|---|---|---|
| **≥ 90 Tage Lücke** | **0,351** | **0,325** | 🟢 Kostev 2023 ✅ Konzeptwert exakt bestätigt |
| ≥ 180 Tage Lücke | 0,519 | 0,504 | 🟢 |

**Jahresverlauf:** Kostev 2023 publiziert **nur den 5-Jahres-Endpunkt**; Jahreswerte existieren nur als
KM-Kurve 🔴. Qualitativ im Text belegt: *„a sharp drop in persistence within the first month of ET initiation"* 🟢.
Ersatzanker aus einer älteren deutschen Kostev-Kohorte (Disease Analyzer, 2.067 Allgemein- + 397 gynäkologische
Praxen), **Abbruch innerhalb 3 Jahren**: Tamoxifen 52,2 % (n=12.412) · Anastrozol 47,0 % · Letrozol 44,3 % ·
Exemestan 55,1 % ⇒ Persistenz @3 J. ≈ 0,45–0,56 🟡 (andere Datenbank, andere Abbruchdefinition — **nicht** mit
den 35,1/32,5 % verrechnen).

**Vorgeschlagener Jahresverlauf für das Modul** (auf die zwei belegten Anker kalibriert):

| Jahr | Persistenz AI | Persistenz TAM | ⇒ jährlicher Abbruch-Arrow AI / TAM | Conf. |
|---|---|---|---|---|
| 1 | 0,72 | 0,70 | 0,28 / 0,30 | 🔴 |
| 2 | 0,60 | 0,57 | 0,17 / 0,19 | 🔴 |
| 3 | 0,52 | 0,48 | 0,13 / 0,16 | 🟡 (ältere DE-Kohorte) |
| 4 | 0,43 | 0,40 | 0,17 / 0,17 | 🔴 |
| **5** | **0,351** | **0,325** | 0,18 / 0,19 | 🟢 (Endpunkt belegt) |

**Altersabhängigkeit — Korrektur K2** (Cox-Regression, Kostev 2023 Tab. 2, Referenz > 70 J.):

| Prädiktor | HR Non-Persistenz (95 % CI) | Lesart |
|---|---|---|
| ≤ 50 J. | **1,08 (1,06–1,10)** | jüngste Gruppe bricht **häufiger** ab |
| **51–60 J.** | **0,92 (0,91–0,94)** | **bricht seltener ab** als > 70 J. |
| 61–70 J. | 0,89 (0,88–0,91) | Minimum |
| TAM vs. AI | 1,06 (1,04–1,07) | TAM minimal schlechter |
| **Hausarzt vs. Gynäkologe** | **1,24 (1,21–1,27)** | **stärkster Einzelprädiktor** |

Alle 🟢. Die Kurve ist **U-förmig** mit Minimum bei 61–70 J.; die Modellkohorte 50–60 liegt im günstigen Teil.
Ein Alters-Multiplikator im Modul ist damit **nicht** nötig — die Kostev-Kurven gelten näherungsweise direkt.

**Adhärenz (MPR < 80 %):** kein spezifischer deutscher Wert gefunden 🔴. S3 (S. 182) nur qualitativ: *„bis zu
**40 %** der Patientinnen [brechen] die Behandlung aufgrund der Toxizität früher ab"* und *„Diese Non-Adhärenz
ist mit einer erhöhten Mortalität assoziiert"* 🟡.

### 4.4 Chemotherapie bei Luminal und der Genexpressionstest

**Recurrence-Score-Verteilung — es gibt eine deutsche Zahl** (besser als TAILORx):

| RS-Kategorie | **Deutschland** (Hein 2020, PMID 32565552, n=4.695, HR+/HER2−, pT1-3 pN0-1, 11/2015–07/2018) | TAILORx (PMID 29860917, n=9.719, N0) | Conf. |
|---|---|---|---|
| RS 0–10 | **0,21** | 0,17 | 🟢 **[DE]** |
| RS 11–25 | **0,63** | 0,69 | 🟢 |
| RS 26–100 | **0,15** | 0,14 | 🟢 |

**Direkt für die Modellkohorte:** In der Subgruppe **> 50 Jahre, nodalnegativ** (n=2.175) lagen **1.772 (81 %)**
bei RS ≤ 25 🟢. Weitere DE-Subgruppen mit RS ≤ 25: Ki-67 ≥ 20 % → 79 % · G2 → 86 % · G3 → 70 % · Tumor > 5 cm →
88 % · N0 mit hohem klinischem Risiko → 82 % 🟢.

⇒ **Chemo-Quote bei getesteten HR+/HER2−/N0 in 50–60 ≈ 0,15–0,19** 🟡 (abgeleitet, TAILORx-Schwelle RS ≥ 26).

**Der prä-/postmenopausale Bruch — RxPONDER (Kalinsky 2021, NEJM 385:2336, PMID 34914339), N1, RS 0–25:**

| Subgruppe | 5-J-iDFS Chemo+ET | ET allein | HR (95 % CI) | Δ absolut | Conf. |
|---|---|---|---|---|---|
| **prämenopausal** | 93,9 % | 89,0 % | **0,60 (0,43–0,83)**, p=0,002 | **+4,9 Pp.** | 🟢 |
| **postmenopausal** | 91,3 % | 91,9 % | 1,02 (0,82–1,26), p=0,89 | **−0,6 Pp.** | 🟢 |

> **Das ist der stärkste Chemo-Prädiktor bei N1/RS ≤ 25 und liegt genau im Modellfenster.** S3 mahnt zur
> Interpretation: in RxPONDER, TAILORx und MINDACT lässt sich der **zytotoxische nicht vom ovarsuppressiven
> Effekt** der Chemotherapie trennen — nur eine Minderheit erhielt OFS 🟢.
> TAILORx-Altersanalyse (explorativ): höchster Chemo-Effekt bei **45–50-Jährigen**; bei ≤ 50 J. mit RS 21–25
> Δ Fernrezidiv nach 9 J. **6,5 Pp.**, bei RS 16–20 nur 1,6 Pp.; **OS-Raten vergleichbar** 🟢.

**GKV-Erstattung — Korrektur K3:**

| Datum | Regelung | Conf. |
|---|---|---|
| 20.06.2019 | Aufnahme MVV-RL Anlage I Nr. 30 — **nur Oncotype DX**, HR+/HER2−/**N0**/M0 | 🟢 |
| 15.10.2020 | **zusätzlich EndoPredict, MammaPrint, Prosigna** (ebenfalls N0) | 🟢 |
| **17.07.2025** | (a) **Oncotype DX zusätzlich für N1 (1–3 LK)**; (b) **alle vier eingeschränkt auf postmenopausale Patientinnen** bzw. prämenopausale **mit geplanter/erfolgter Ovarialsuppression** | 🟢 |

Quelle: G-BA, Tragende Gründe zum Beschluss vom 17.07.2025, MVV-RL Anlage I Nr. 30, Abschnitte 2.2 und 9.
Nutzungsanteile der vier Tests in DE: **keine publizierte Zahl** 🔴; die deutsche RS-Studie mit n=4.695 allein für
Oncotype in ~2,5 Jahren legt Marktdominanz nahe 🔴 Interpretation. Die im Konzept genannte Nutzungsrate „~20 % der
Berechtigten" bleibt eine Kongress-Experteneinschätzung 🟡 — der Test ist **kein DKG-Qualitätsindikator**, es gibt
also keinen Nenner 🟢.

S3 Empf. 4.86/4.87: Multigentest **nur wenn** konventionelle Parameter inkl. Ki-67 keine eindeutige Entscheidung
erlauben, bei N0 **oder** 1–3 befallenen LK; *„Es soll nicht mehr als ein Test zur Entscheidungsfindung
herangezogen werden"* 🟢. Ki-67-Schwellen (Empf. 4.85, *mod. 2025*): **> 25 % erhöhtes**, **< 10 % niedriges**
Rezidivrisiko 🟢.

**Reale Chemo-Quote Deutschland:**

| Arrow | Wert | Basis | Conf. |
|---|---|---|---|
| **Chemo bei HR+ und N+** | **0,6078** (8.374 / 13.777); Median über Standorte 0,6134 | OnkoZert 2025 **KZ 6** **[alle Alter]** | 🟢 ✅ Konzeptwert bestätigt |
| Zeittrend (Median über Standorte) | 2019 **64,0 %** → 2020 65,5 → 2021 63,2 → 2022 62,0 → 2023 **61,3 %** | ebd. | 🟢 |
| **Chemo bei HR+/HER2−/N0** | **keine Kennzahl** — KZ 6 ist definitorisch auf N+ beschränkt | Näherung 0,15–0,19 über RS-Verteilung | 🟡 abgeleitet |
| **endokrine Therapie bei HR+** | **0,9682** (49.671 / 51.302) | ebd. **KZ 7** | 🟢 ✅ (Konzept: 96,8 %) |

Die vom Bericht selbst genannten Begründungen für die ausbleibende Chemo-Empfehlung sind wörtlich:
*„die Ergebnisse von **Genexpressionsanalysen**, keine Chemotherapieempfehlung aufgrund des hohen Alters u./o.
Komorbiditäten oder die **Therapie mit CDK4/6-Inhibitoren**"* 🟢. Der Rückgang 2019→2023 belegt eine reale
**Substitution von Chemotherapie durch Genexpressionstestung und CDK4/6-Inhibitoren** — ein Effekt, den das
Modul über das Behandlungsjahr abbilden kann.

### 4.5 CDK4/6-Inhibitoren adjuvant

**S3 Empf. 4.149 (*neu 2025*), Empfehlungsgrad B** — wörtlich:
> *„Bei Patientinnen mit HR+/HER2-Mammakarzinom und hohem Rückfallrisiko (bei **N2-3 oder N1 mit G3 oder
> Tumorgröße ≥ 5 cm**) sollte **Abemaciclib für 2 Jahre** in Kombination mit der endokrinen Standard-Therapie
> **oder Ribociclib** (bei **N+, oder N0 T3/T4, oder N0 T2 G3, oder N0 T2 G2 und (Ki-67 ≥ 20 % oder high-risk
> Genexpression)**) **für 3 Jahre** in Kombination mit einem **Aromatasehemmer (+ OFS bei prämenopausalen
> Patientinnen)** durchgeführt werden."* 🟢

| Größe | monarchE (Abemaciclib) | NATALEE (Ribociclib) | Conf. |
|---|---|---|---|
| Therapiedauer | **2 Jahre** | **3 Jahre** | 🟢 |
| 5-J-iDFS | **83,6 % vs. 76,0 %** (Δ **+7,6 Pp.**), HR **0,680 (0,599–0,772)** | 5-J-Zahlen in dieser Recherche nicht verifiziert | 🟢 / 🔴 |
| EMA-Indikation | HR+/HER2−, **node positive**, hohes Rezidivrisiko | HR+/HER2−, hohes Rezidivrisiko — **schließt N0 ein** | 🟢 |
| **Eligibility-Anteil DE** | **0,194** (217/1.121, Tübingen 2018–2020, PMC8951288); 0,155 nach FDA-Label (+ Ki-67 ≥ 20 %) | **0,430** (747/1.738, Ulm + Tübingen, PMC10671738), davon 27,6 % N0 | 🟢 **[DE]** |
| Vergleich international | DK (DBCG) 0,130; SE 0,196 (n=52.602, PMC12513154) | SE 0,368; FR 0,344 | 🟢 |
| Überlappung (SE) | beide 18,2 % · nur NATALEE 18,6 % · **nur monarchE 1,4 %** · gesamt CDK4/6i-eligible **38,2 %** | | 🟢 |

⇒ **Modellstruktur:** monarchE ist fast vollständig eine **Teilmenge** von NATALEE. Eine Hierarchie genügt:
**NATALEE-eligible ≈ 0,43 der HR+/HER2−-Frühfälle ⊃ monarchE-eligible ≈ 0,19** 🟢 (beide DE-Zahlen).
Der im Konzept genannte dänische Wert 13 % ist damit durch **zwei deutsche Kohorten (19,4 % / 18,1 %)** ersetzbar
— die Konzept-Lücke „kein deutscher Wert 🔴" ist **geschlossen**.

> ⚠️ **Eligibility ≠ Behandlung.** In Tübingen hatten **48,85 % (106/217)** der monarchE-eligiblen Patientinnen
> **weder adjuvante noch neoadjuvante Chemotherapie** erhalten 🟢. **Realer Verordnungs-Uptake adjuvanter
> CDK4/6-Inhibitoren in DE: keine Daten** 🔴 (= Konzept §11 Lücke 9, bestätigt). Einziger indirekter Beleg ist
> die OnkoZert-Begründungsliste zu KZ 6.
> Für 50–60 zusätzlich relevant: Ribociclib erfordert laut S3 **AI + OFS bei prämenopausalen** Patientinnen —
> bei einer 50-Jährigen mit ~50 % Prämenopause entsteht eine Dreifachkombination (AI + GnRHa + Ribociclib, 3 J.).

### 4.6 Anti-HER2-Therapie

| Arrow | Wert | Basis | Conf. |
|---|---|---|---|
| **Trastuzumab 1 Jahr bei HER2+ ≥ pT1c** | **0,9503** (5.834 / 6.139) | OnkoZert 2025 **KZ 8** **[alle Alter]** | 🟢 ✅ Konzeptwert bestätigt |
| Begründungen für Abweichung | Ko-/Multimorbidität, **insb. kardial (89×)**, hohes Alter (45×), Patientinnenwunsch (13×) | ebd. | 🟢 |
| Kurzdauer 6 Monate | **keine DE-Daten**; abgeleitet **< 0,05**. S3 Empf. 4.164 (*neu 2025*): 12 Monate „sollte", 6 Monate „kann" bei **niedrigem Risiko oder kardialer Komorbidität**. Metaanalyse 3 RCTs: DFS HR **1,18 (0,97–1,44)** — Nichtunterlegenheit **nicht** gezeigt | 🟡 / 🟢 |
| **Pertuzumab adjuvant** | S3 Empf. 4.162 (*neu 2025*): nur **„kann"**, und nur bei initial nachgewiesenem **ipsilateralem axillärem LK-Befall**. APHINITY 8-J-iDFS nodal-positiv **86,1 % vs. 81,2 % (+4,9 Pp.)**, HR 0,72; **nodal-negativ kein Benefit**; OS gesamt 92,7 % vs. 92,0 %, p=0,078 **n.s.** | 🟢 |
| Pertuzumab **neoadjuvant** | S3 Empf. 4.161 (*neu 2025*, Grad B): HER2+ mit **> 2 cm und/oder N+** → Chemo + Trastuzumab + Pertuzumab | 🟢 |
| **Uptake Pertuzumab adjuvant DE** | — | **keine Daten** | 🔴 Lücke (= Konzept §11 Lücke 9) |
| **T-DM1 bei non-pCR (KATHERINE)** | 3-J-iDFS **88,3 % vs. 77,0 %**, HR **0,50 (0,39–0,64)** ✅ Konzeptwert exakt; **neu: 7-J-OS 89,1 % vs. 84,4 %, HR 0,66 (0,51–0,87), p=0,0027** (5-J-OS 91,4 % vs. 87,7 %) | von Minckwitz 2019 PMID 30516102 + Langzeitanalyse med. FU 8,4 J. | 🟢 |
| S3 zu T-DM1 | Empf. 4.165 (*neu 2025*), **Grad A**: bei non-pCR **sollen** 14 Zyklen T-DM1 gegeben werden | 🟢 |
| **Anteil non-pCR unter neoadjuvant behandelten HER2+** | **0,35–0,45** für ein modernes duales Regime | TRYPHAENA pCR 45,3–51,9 % ⇒ non-pCR 48–55 %; TRAIN-2 pCR 67–68 % ⇒ non-pCR 32–33 % | 🟡 abgeleitet |
| Neratinib (ExteNET) | 5-J-iDFS 90,2 % vs. 87,7 % (+2,5 Pp.); **OS bei 8,1 J. 90,1 % vs. 90,2 % — kein Unterschied**; hohe Diarrhoe-Toxizität. S3 Empf. 4.166 Grad **0**, nur HR+/HER2+ Stadium II–III **nach Trastuzumab allein**; Tumoren < 2 cm ausdrücklich nicht | 🟢 |
| ⇒ Neratinib-Anteil DE | **0,00–0,02** — Nischenindikation, moderne Regime erfüllen die Voraussetzung „Trastuzumab allein" kaum noch | 🔴 |

Trastuzumab-Effektgrößen (Metaanalyse 7 RCTs, n=13.864, med. FU 10,7 J., via S3): Rezidiv **RR 0,66 (0,62–0,71)**;
brustkrebsspezifische Mortalität RR 0,67; **absolute Risikoreduktion nach 10 J.: Rezidiv 9,0 %, BC-Sterblichkeit
6,4 %, Gesamtmortalität 6,5 %**; absolute RR nach 5 J. nach Nodalstatus **N0 5,7 % · N1–3 6,8 % · N ≥ 4 10,7 %**
— alle 🟢.

### 4.7 Weitere adjuvante Bausteine

| Baustein | Regel / Wert | Basis | Conf. |
|---|---|---|---|
| **Bisphosphonate** | S3 Empf. 4.175 (*mod. 2025*), Grad B: bei **postmenopausalen** Patientinnen **unter AI** sowie bei **prämenopausalen unter OFS** *sollte* adjuvant behandelt werden — **off-label**. Denosumab: Wirkung „bisher nicht eindeutig gezeigt" | S3 v5.x | 🟢 |
| | Wirkstoffe mit Nutzennachweis: Alendronat 70 mg/Wo · Clodronat · Ibandronat · Risedronat · **Zoledronat 4 mg i.v. alle 6 Monate** | ebd. | 🟢 |
| | Effekt (gepoolt, unter ET): Rezidiv **RR 0,78 (0,67–0,90)**, lokoregionär RR 0,69 | Wang 2013 | 🟡 |
| | **Uptake DE** | **keine Daten** (off-label erschwert die Erfassung) | 🔴 |
| **Olaparib bei gBRCA** | S3 Empf. 4.150 (*neu 2025*), Grad B: HR+/HER2− mit **hohem Rückfallrisiko (N2-3 oder CPS-EG ≥ 3 nach Neoadjuvanz)** und **gBRCA1/2** → 1 Jahr Olaparib. OlympiA: **OS HR 0,68 (0,47–0,97), p=0,009** | S3 / OlympiA | 🟢 |
| | Anteil aller HR+/HER2−: **0,01–0,02** (gBRCA-Prävalenz unselektiert ~5 %, davon nur die Hochrisiko-Teilmenge) | eigene Ableitung | 🔴 |
| **Capecitabin post-neoadjuvant (TNBC)** | S3 Empf. 4.155 (*neu 2025*), Grad B: TNBC mit **non-pCR** nach Anthrazyklin/Taxan → **6–8 Zyklen Capecitabin**. CREATE-X TNBC-Subgruppe: 5-J-DFS **69,8 % vs. 56,1 %** (HR 0,58), 5-J-OS **78,8 % vs. 70,3 %** (HR 0,52) | S3 / CREATE-X | 🟢 |
| | ⚠️ **Interferenz mit KEYNOTE-522:** Pembrolizumab erhöht die pCR-Rate und **verkleinert damit die non-pCR-Population**, die für Capecitabin infrage kommt. Das Modul muss die Reihenfolge respektieren | — | 🟢 |

### 4.8 Erstlinie im metastasierten Setting — die einzige DE-Kennzahl dazu

| Arrow | Wert | Basis | Conf. |
|---|---|---|---|
| **endokrin-basierte Erstlinientherapie bei HR+/HER2− mit erster Fernmetastasierung** | **0,8943** (4.914 / 5.495); Median über Standorte 0,9286; **Sollvorgabe ≥ 95 % — nicht erreicht** | OnkoZert 2025 **KZ 9**, S. 20 **[alle Alter]** | 🟢 |

Das ist die einzige deutsche Versorgungskennzahl für den metastasierten Ast und der passende Eingangsarrow zum
CDK4/6-Block (§4.5) bzw. zu den Überlebenswerten in §7.4: rund **11 % der HR+/HER2−-Patientinnen starten
metastasiert *nicht* endokrin-basiert** (Chemotherapie bei viszeraler Krise o. Ä.). Eine Aufschlüsselung, welcher
Anteil davon einen CDK4/6-Inhibitor erhält, enthält der Bericht **nicht** 🔴.

---

## 5. DCIS-Pfad

DCIS ist im Konzept (§3.3) verbindlich für v1. Der Pfad ist vollständig belegbar — **außer** der endokrinen
Therapie.

### 5.1 Therapieverteilung (Deutschland)

| Arrow | Wert | Basis | Conf. |
|---|---|---|---|
| DCIS-Anteil an allen Primärfällen | **0,0958** (7.038 / 73.505) | OnkoZert 2025, S. 8 **[alle Alter]** | 🟢 |
| DCIS **nicht operiert** | **0,0304** | ebd. | 🟢 |
| **BET bei DCIS** | **0,7934** (5.414 / 6.824) | ebd., S. 9 | 🟢 |
| **Mastektomie bei DCIS** | **0,2066** | ebd. | 🟢 |
| **RT nach BET, DCIS (begonnen)** | **0,7841** (4.238 / 5.405); Median Zentrum 0,818; nur 58,7 % der Standorte ≥ 0,80 | ebd. **KZ 5** | 🟢 |
| Gründe für RT-Verzicht | **Patientinnenwunsch 85×**, geringe Größe 44×, noch nicht begonnen 28×, lost to FU 26×, Alter/Komorbidität 23×, Low Grade 21×, M. Paget 13× | ebd. | 🟢 |
| axilläre LK-Entnahme bei DCIS + BET | **0,0248** | ebd. **KZ 18** | 🟢 |
| SLN-Positivität bei DCIS | 0,049 (16 prospektive Studien, n=4.388) | S3 v5.1 Kap. 4.2 | 🟢 international |
| Upstaging DCIS → invasiv im OP-Präparat | **0,05–0,26** | AGO 2026.1D | 🟢 (breite Spanne) |
| **endokrine Therapie bei ER+ DCIS** | **keine deutsche Rate** — nicht im DKG-Kennzahlenbogen (KZ 7 umfasst ausdrücklich **nur invasive** Karzinome) | Prior **0,15–0,30** | 🔴 Lücke |

> ⚠️ **Diskrepanz beachten:** S3 v5.1 Kap. 4.2 schreibt *„In ca. **30 %** der Patienten mit einem reinen DCIS wird
> eine Mastektomie durchgeführt"* 🟡 — die aktuellen deutschen Zentrumsdaten (**20,7 %**) sind präziser und
> jünger. **OnkoZert verwenden.**
> Leitlinienstatus endokrin: S3 Empf. 4.36 Grad **0 („kann")**, EL 2; AGO 2026 **`+/-`** (nur ER+), aufgewertet
> auf `+` falls trotz Risikofaktoren **keine** RT erfolgte 🟢. Bei diesem schwachen Empfehlungsgrad ist eine
> **niedrige** deutsche Rate zu erwarten — der Prior 0,15–0,30 ist entsprechend gewählt 🔴.

### 5.2 Rezidiv nach DCIS — inklusive in-situ/invasiv-Split

| Größe | ohne RT | mit RT | Basis | Conf. |
|---|---|---|---|---|
| 10-J ipsilaterale Brustereignisse, gesamt | **0,281** | **0,129** (ARR 15,2 Pp., SE 1,6, p<0,00001) | EBCTCG/Correa 2010, JNCI Monogr, **PMID 20956824**, 4 RCTs | 🟢 |
| dito, **Alter ≥ 50 J.** ✅ Zielgruppe | **0,278** | **0,108** | ebd. | 🟢 **[≥50 J.]** |
| dito, Alter < 50 J. | 0,291 | 0,185 | ebd. | 🟢 |
| dito, negative Ränder + kleines Low-Grade-DCIS | 0,301 | 0,121 (ARR 18,0 Pp.) | ebd. — **auch Niedrigrisiko profitiert** | 🟢 |
| 10-J In-Brust-Rezidiv nach Randstatus, R0 | 0,260 | 0,120 | S3 v5.1 (zit. EBCTCG) | 🟢 |
| dito, R1 | 0,438 | 0,242 | ebd. | 🟢 |
| **10-J intramammäres Rezidiv, moderne Schätzung** | **0,19** | **0,11** | **S3 v5.1** — für heutige Kohorten die realistischere Zahl | 🟢 |
| ipsilaterale Ereignisse @10 J / @20 J | 0,246 / 0,306 | 0,096 / 0,182 | AGO 2026.1D (kumulative Inzidenz) | 🟢 |
| **Anteil invasiver Ereignisse an allen ipsilateralen** | **~0,50** | | ebd. — **direkt der in-situ/invasiv-Split fürs Modul** | 🟢 |
| kontralaterale Ereignisse @10 J / @15 J | 0,048–0,064 / 0,064–0,11 | | ebd. | 🟢 |
| RTOG 9804 (Niedrigrisiko), 7-J | 0,067 | 0,009 (p=0,0003) | | 🟢 |
| RTOG 9804-Verlängerung (G1/G2 ≤ 2,5 cm), 12-J | 0,125 (≈ **1 %/Jahr**) | — | | 🟢 |
| 20-J aktuarisch ipsilateral **invasiv** | **0,139** | | Giannakeas/Narod, JAMA Netw Open 2020;3(9):e2017124 (SEER, n=144.524) | 🟢 |
| 20-J aktuarisch kontralateral invasiv | 0,113 | | ebd. | 🟢 |
| Boost beim DCIS | 10-J Freedom from LR **93,2 % (Boost) vs. 86,6 %**, p<0,001; **Fraktionierung 42,5 Gy/16 vs. 50 Gy/25 n.s.** (90,7 vs. 89,1 %, p=0,409) | BIG 3-07/TROG 07.01, SABCS 2025, n=1.608, med. FU 10,2 J. | 🟢 |

**Effektgrößen für die Arrow-Konstruktion:**
RT **halbiert** das ipsilaterale Rezidivrisiko (invasiv *und* nicht-invasiv), LoE 1a, **NNT 9** (alle Risikogruppen)
bzw. **NNT 17** im Niedrigrisikokollektiv (< 2 cm, G1/2, > 50 J.); **kein Einfluss auf das Gesamtüberleben**
(LoE 1a) 🟢. Endokrine Therapie: **NNT 15**, ipsilateral invasiv **HR 0,79 (0,62–1,01)**, ipsilateral DCIS
HR 0,75 (0,61–0,92), kontralateral invasiv **RR 0,57 (0,39–0,83)**, kontralateral in situ RR 0,50 (0,28–0,87);
**ohne RT** ist der endokrine Effekt stärker: ipsilateral invasiv **HR 0,49 (0,28–0,84)** 🟢.

### 5.3 Mortalität nach DCIS — „quasi keine", aber nicht null

| Größe | Wert | Basis | Conf. |
|---|---|---|---|
| **20-J brustkrebsspezifische Mortalität** | **0,033 (0,030–0,036)** | **Narod 2015, JAMA Oncol, PMID 26291673** ✅ Konzeptwert bestätigt; n=108.196, SEER 1988–2011, **mittleres Alter 53,8 J.** | 🟢 **[nahe 50–60]** |
| 10-J BC-Mortalität nach Therapieart | BET **0,009** · BET+RT **0,008** · unilaterale Mastektomie **0,013** | AGO 2026.1D | 🟢 |
| **RT-Effekt auf die BC-Mortalität @10 J** | 0,009 → 0,008, HR 0,86 (0,67–1,10), **p=0,22 n.s.** | Narod 2015 | 🟢 |
| RT-Effekt auf ipsilaterale **invasive** Rezidive @10 J | **0,049 → 0,025**, adj. HR **0,47 (0,42–0,53)**, p<0,001 | ebd. | 🟢 |
| **Mortalitätsrisiko nach ipsilateralem invasivem Rezidiv** | **HR 18,1 (14,0–23,6)** | ebd.; auch in S3 v5.1 zitiert | 🟢 |
| Tod **ohne** vorheriges invasives In-Brust-Rezidiv | 517 Patientinnen (von 108.196) | ebd. | 🟢 |
| SMR ggü. Normalbevölkerung | **3,36 (3,20–3,53)** | Giannakeas/Sopik/Narod 2020 | 🟢 |
| < 35 J. bei Diagnose | 7,8 % vs. 3,2 % (HR 2,58) | Narod 2015 | 🟢 (außerhalb des Fensters) |

> **Der zentrale Befund für die Modellstruktur:** RT verhindert **Rezidive, nicht Tod**. Der DCIS-Ast braucht
> deshalb *keinen* eigenen Sterbe-Arrow, sondern nur einen **Übergang zu invasivem Rezidiv**, an den dann der
> normale invasive Pfad mit seiner Mortalität angehängt wird. Das ist strukturell sauberer und reproduziert die
> 3,3 % @20 J automatisch.

---

## 6. Rezidiv, Hazard-Zeitverlauf, Metastasierung

### 6.1 Lokoregionäres Rezidiv

**EBCTCG Darby 2011 (PMID 22019144 / PMC3254252)** — 10.801 Frauen, 17 RCTs, Randomisierung **vor 2000**.
⚠️ **Prämissenkorrektur:** die vielzitierten **19,3 % vs. 35,0 %** sind *jedes Erstrezidiv* (lokoregionär **oder**
fern) in der **Gesamtkohorte** — **nicht** die Lokalrezidivrate und nicht pN0. Die pN0-Werte sind 15,6 % vs. 31,0 %.

| Stratum (pN0, 10-J *jedes* Rezidiv) | BET+RT | BET allein | Δ absolut | Conf. |
|---|---|---|---|---|
| Alter < 40 | 36,1 % | 60,7 % | 24,6 | 🟢 |
| Alter 40–49 | 20,8 % | 41,4 % | 20,6 | 🟢 |
| **Alter 50–59** | **15,0 %** | **29,7 %** | **14,7 (10,8–18,6)** | 🟢 **[50–60 direkt!]** |
| Alter 60–69 | 14,2 % | 28,3 % | 14,1 | 🟢 |
| ER+ **mit** Tamoxifen | **8,7 %** | 22,0 % | 13,3 | 🟢 |
| pT1 / pT2 | 12,4 / 30,7 % | 27,5 / 50,0 % | 15,1 / 19,3 | 🟢 |

15-J-BC-Mortalität pN0: 17,2 % (RT) vs. 20,5 % (Δ 3,3); pN+ 42,8 % vs. 51,3 % (Δ 8,5) 🟢.
Aufteilung LR vs. fern beim Erstereignis: BET allein LR 25 % / fern 10 % (~71 % lokoregionär); BET+RT LR 8 % /
fern 12 % (< 50 % lokoregionär) 🟢. **Ära-Vorbehalt der Autoren selbst:** kein Trastuzumab, kein AI, kein
HER2-Status, keine Margin-Standardisierung.

**Moderne deutsche kumulative Lokalrezidiv-Inzidenz** — TRM, Spezialauswertung `RisikoM0` Tab. 11/12, n=46.418,
Dx **2002–2020**, gemischte Lokaltherapie, konkurrierendes Risiko Tod, **[alle Alter]** 🟢:

| Jahr | pN0 | pN+ | G3 | TNBC | nicht-TNBC |
|---|---|---|---|---|---|
| 1 | 0,4 | 1,1 | 1,4 | 2,3 | 0,5 |
| 2 | 1,3 | 3,2 | 4,0 | 6,2 | 1,6 |
| 3 | 2,4 | 4,5 | 5,8 | 8,3 | 2,6 |
| **5** | **3,9** | **6,3** | **7,7** | **10,6** | **4,2** |
| **10** | **6,9** | **9,4** | **10,6** | **14,0** | **7,2** |
| **15** | **9,8** | **11,6** | **12,5** | **15,7** | **9,9** |

**Regionäres LK-Rezidiv** (TRM Tab. 17): pN0 5-J **1,4 %** / 10-J **2,2 %** / 15-J 2,8 %; pN+ 5-J **3,1 %** /
10-J **4,4 %** / 15-J 5,0 % 🟢. Das reproduziert die Konzeptwerte (2,2 / 3,2 %) für pN0 gut.
**TRM-Textanker:** BET-Kohorte n=40.842 (91,4 % bestrahlt, Dx 1998–2020) → *„Lokalrezidivrate ca. 10 % in
10 Jahren"* 🟢 — konsistent mit den Konzeptwerten 5,2 / 8,2 %.

**Moderne Einzelkohorten zur Kalibrierung des Niveaus:**

| Quelle | Kohorte | Endpunkt | Wert | Conf. |
|---|---|---|---|---|
| Arvold 2011 JCO, PMID 21900114 | 1.434 BET, 1997–2006 | 5-J LR gesamt | **2,1 % (1,4–3,0)** | 🟢 |
| ebd. | **Alter 47–54** | 5-J LR | **2,2 % (1,0–4,6)** | 🟢 **[50–60]** |
| ebd. | **Alter 55–63** | 5-J LR | **0,9 % (0,3–2,6)** | 🟢 **[50–60]** |
| DBCG HYPO, Offersen 2020, PMID 32910709 | 1.854 BET pN0, Dx 2009–2014 | 9-J LRR (50 Gy / 40 Gy) | 3,3 % / 3,0 % | 🟢 |
| van Maaren 2019, PMID 30368776 (NL, Dx 2005) | 8.062 | 10-J LR Luminal A / HER2+ | 3,7 % / 7,5 % | 🟢 |
| S3 v5.1 Kap. 5.1.1 | Konsens DE | LR nach BET+RT @10 J | **5–10 %** | 🟡 |

⇒ **Modellwert Lokalrezidiv nach BET+RT, pN0, HR+, 50–60:** **5-J 0,015–0,025 · 10-J 0,04–0,06** 🔴
(Formanker TRM, Niveauanker Arvold).
**Mastektomie ohne PMRT, pN0:** 5-J LRR **0,02–0,03** 🟢/🔴 (Jwa 2015 PMID 26691445: 5-J LRR 3,0 %; McGale pN0:
1,4 % LRR vor Fernmetastase @10 J; S3: Thoraxwandrezidiv 4 % [2–20 %], Axilla 1 % [0,1–8 %]).

**Subtypabhängigkeit** — Voduc 2010 JCO (PMID 20194857), BC Cancer Agency, **Dx 1986–1992**, n=2.985,
Medianalter 59 J., nur 57 % Systemtherapie, **kein Trastuzumab**:

| Subtyp | 10-J LR nach BET+RT | 10-J RR | 10-J LR nach Mastektomie | Conf. |
|---|---|---|---|---|
| Luminal A | 8 % | 3 % | 8 % | 🟢 Ära ⚠️ |
| Luminal B | 10 % | 8 % | 14 % | 🟢 ⚠️ |
| Luminal-HER2 | 9 % | 5 % | 20 % | 🟢 ⚠️ |
| **HER2-enriched** | **21 %** | 16 % | 17 % | 🟢 ⚠️ **unter Trastuzumab ungültig** |
| Basal-like | 14 % | 14 % | 19 % | 🟢 ⚠️ |
| TN non-basal | 8 % | 7 % | 13 % | 🟢 ⚠️ |

Multivariat (BET+RT): HER2-enriched vs. Luminal A — LR **HR 2,7 (1,4–4,9)**, RR **HR 4,7 (2,2–10,2)**; Basal RR
HR 2,7; Alter 40–55 vs. > 55 LR HR 1,6 (p=0,050) 🟢. **Autoren wörtlich:** *„the differences in locoregional
relapse between the molecular subtypes will likely be diminished in a population receiving modern systemic
therapy."*

**Moderne Ersatzwerte (Arvold 2011, 5-J LR nach BET, kein Trastuzumab)** 🟢: Luminal A **0,8 %** · Luminal B (G3)
2,3 % · Luminal-HER2 1,1 % · HER2 (ER−PR−HER2+) **10,8 %** · TNBC **6,7 %**.
**Lowery 2012 Metaanalyse (PMID 22147079)** 🟢: LRR Luminal vs. TNBC nach BET **RR 0,38 (0,23–0,61)**; Luminal vs.
HER2+ **RR 0,34 (0,26–0,45)**.
**TNBC-Multiplikator aus deutschen, modernen Daten (TRM)** 🟢: Lokalrezidiv **×2,5 @5 J**, **×1,9 @10 J** gegenüber
nicht-TNBC — das ist der belastbarste Subtyp-Multiplikator für das Modul.

### 6.2 ⭐ Gemessene jährliche Fernmetastasierungs-Hazards (Deutschland) — Korrektur K8

**Der wichtigste Fund dieser Recherche.** Das Tumorregister München publiziert in der Spezialauswertung
`spec_C50f__09_20210923_RisikoM0.pdf` (Tab. 21–24) eine **explizite Hazard-Rate-Spalte pro Jahresintervall**,
konkurrenzrisikokorrigiert, n=**46.418** invasive M0-Ersttumoren, Dx **2002–2020**, Einzugsgebiet 4,94 Mio.
Einwohner, **[alle Alter]**. Die Hazardformen müssen damit **nicht mehr aus KM-Kurven abgeleitet** werden.

Werte in **%/Jahr**; die letzten drei Spalten sind die publizierten kumulativen Inzidenzen.

| Stratum | J1 | J2 | J3 | J4 | J5 | J6–10 Ø | J11–15 Ø | CI 5J | CI 10J | CI 15J |
|---|---|---|---|---|---|---|---|---|---|---|
| **pN0** (n=31.119) | 0,4 | 1,1 | 1,1 | 1,0 | 0,9 | **0,66** | **0,46** | 4,5 | **7,6** | 9,5 |
| **pN+** (n=15.299) | 2,4 | 4,2 | 4,2 | 3,4 | 3,3 | **2,24** | **1,20** | 15,9 | **23,7** | 27,2 |
| T1 (n=25.556) | 0,3 | 0,8 | 0,8 | 0,8 | 0,8 | 0,72 | 0,48 | 3,6 | 6,9 | 9,1 |
| T2 (n=16.662) | 1,3 | 3,1 | 3,3 | 2,6 | 2,4 | 1,64 | 0,94 | 12,0 | 18,4 | 21,5 |
| T3/4 (n=4.200) | 4,95 | 6,7 | 6,3 | 5,1 | 4,6 | 2,64 | 1,42 | 22,8 | 29,8 | 32,5 |
| G1 (n=6.197) | 0,15 | 0,2 | 0,3 | 0,3 | 0,4 | 0,36 | 0,30 | 1,3 | 3,0 | 4,5 |
| G2 (n=27.855) | 0,65 | 1,4 | 1,7 | 1,6 | 1,6 | 1,24 | 0,82 | 6,7 | 12,0 | 15,1 |
| G3 (n=12.366) | 2,5 | 4,9 | 4,1 | 2,8 | 2,4 | 1,38 | 0,54 | 15,4 | 20,5 | 22,3 |
| **TNBC** (n=3.977) | 3,4 | **7,5** | 4,8 | 3,0 | 1,8 | **0,76** | **0,24** | 18,8 | **21,5** | 22,3 |
| **nicht-TNBC** (n=42.441) | 0,85 | 1,6 | 1,9 | 1,6 | 1,6 | **1,14** | **0,72** | 7,4 | **12,3** | 15,0 |
| Risikokohorte¹ (n=24.094) | — | — | — | — | — | — | — | 13,6 | 20,1 | 23,0 |
| **nicht** Risikokohorte¹ (n=22.324) | — | — | — | — | — | — | — | 2,5 | 5,2 | 7,3 |

¹ Risikokohorte = T3/4 **oder** N+ **oder** G3 **oder** TNBC. Alle Zeilen 🟢.
**Additivitätsprobe:** Σ Hazards J1–J5 (nicht-TNBC) = 7,55 % gegen publizierte CI 7,4 % ⇒ die Spalte ist in
%/Jahr und additiv verwendbar 🟢.

> **Das Kernmuster, das das Modul reproduzieren muss:** der TNBC-Hazard bricht nach Jahr 3 zusammen und liegt ab
> Jahr 6 **unter** dem der Nicht-TNBC; der luminale Hazard läuft nahezu linear bis Jahr 15 weiter. Genau das ist
> die Struktur, für die eine `Delay` + `complex_transition`-Schleife mit stückweise konstanten Jahresraten
> gebaut wird (Konzept §7).

**Auflösung der Diskrepanz K6.** Konzept §7 zitiert aus dem TRM-*Survival*-Faktenblatt (Tab. 5b, n=58.903,
Dx 1998–2020) Fernmetastasierung **11,0 @5J / 16,6 @10J / 19,4 @15J**; die Spezialauswertung `RisikoM0`
(n=46.418, Dx 2002–2020) ergibt gewichtet **≈ 8,4 / 13,1 / 15,6 %**. Beides sind TRM-Zahlen, aber **verschiedene
Kollektive und Zeiträume** (die Survival-Tabelle beginnt 1998 und hat einen anderen Ausschluss). Empfehlung:
**für die Hazard-*Form* und die stratifizierten Werte die `RisikoM0`-Auswertung verwenden** (sie ist jünger,
konkurrenzrisikokorrigiert und publiziert die Hazardspalte); die 11,0/16,6 % nur als **oberen Plausibilitätsrand**
führen. Nicht mischen.

**Ergänzende Hazardformen aus der Literatur** (für die Jahre, die TRM nicht auflöst):

| Quelle | Aussage | Conf. |
|---|---|---|
| **Colleoni 2016** IBCSG (PMID 26786933), n=4.105, Rand. **1978–1985**, FU 24,2 J. | BCFI-Hazard **J1–2 Peak 15,2 %/J**; J0–5 gesamt 10,4 (ER+ **9,9** / ER− **11,5**, p=0,01); J5–10 4,5 (5,4 / 3,3); J10–15 2,2 (**2,9** / 1,3); J15–20 1,5 (2,8 / 1,2); J20–25 0,7 (1,3 / 1,4). **Hazard-Kreuzung ER+/ER− zwischen Jahr 2 und 3** | 🟢 Form; ⚠️ Ära |
| ebd., ER+ nach Nodalstatus | N0: J10–15 **2,0 %/J**, J15–20 2,1, J20–25 1,1 · 1–3 pos. LK: **3,0 / 3,5 / 1,5 %/J** | 🟢 |
| **Dent 2007** (PMID 17671126), n=1.601, Dx 1987–1997 | Fernrezidiv-HR TNBC vs. andere **2,6 (2,0–3,5) nur innerhalb 5 J.**; *„risk of distant recurrence peaked at approximately 3 years and declined rapidly thereafter"* | 🟢 |
| **Pan 2017** NEJM (PMID 29117498), 88 Studien, 62.923 ER+ | Fernrezidiv **Jahre 5–20**: T1N0 **13 %** (G niedrig 10 / mittel 13 / hoch 17) · T1N1-3 **20 %** · T1N4-9 **34 %** · T2N0 **19 %** · T2N1-3 **26 %** · **T2N4-9 41 %**. *„Recurrences occurred at a steady rate throughout the study period from 5 to 20 years"* ⇒ **konstanter Hazard für J5–20 empirisch gerechtfertigt** | 🟢 |
| **Cossetti 2015** JCO (PMID 25422485), matched C1 Dx 1986–92 vs. C2 Dx 2004–08, je n=3.589 | Rezidiv-Hazardrate in C2 **in allen Jahresintervallen bis Jahr 9 etwa halbiert**; größte Differenz in den ersten fünf Intervallen, bei HER2+ und TNBC. Muster bleibt gleich, der frühe Peak ist gedämpft | 🟢 |

⇒ **Ära-Korrekturfaktor 0,5** auf alle Prä-2000-Hazards (Colleoni, Voduc, Kennecke, Darby) für die Jahre 1–9 🟢.
Die TNBC-Peak-Lage weicht ab: Dent sieht ihn in **Jahr 3**, das TRM (DE, modern) in **Jahr 2** (7,5 %/J).
**Für die deutsche Kalibrierung TRM verwenden.**

### 6.3 Konsolidierte jährliche Fernrezidiv-Hazards je Subtyp (%/Jahr)

Zielgröße: kumulative Fernmetastasierungsinzidenz, N0/N+-Mix wie in einer deutschen 50–60-Kohorte, moderne
Therapie. **Nur die TNBC-Zeile ist direkt gemessen** (TRM); die übrigen sind abgeleitet — Formanker die
TRM-Hazardspalten (G1/G2/G3, nicht-TNBC), Niveauanker van Maaren 2019 (10-J DM Luminal A **9,5 %**, HER2+
**25,6 %** ohne Trastuzumab), Metzger-Filho 2013 (Subtyp-Relativitäten), Pan 2017 (J5–20 konstant), HERA
(Trastuzumab HR 0,76), Cossetti (Ära-Faktor 0,5).

| Subtyp | J1 | J2 | J3 | J4 | J5 | J6–10 Ø | J11–15 Ø | Σ 5J | Σ 10J | Σ 15J | Conf. |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Luminal A** | 0,4 | 0,9 | 1,1 | 1,1 | 1,0 | **0,9** | **0,7** | 4,5 | 9,0 | 12,5 | 🔴 |
| **Luminal B HER2−** | 1,2 | 2,4 | 2,6 | 2,2 | 2,0 | **1,5** | **1,0** | 10,4 | 17,9 | 22,9 | 🔴 |
| **HER2+ (mit Trastuzumab)** | 1,8 | 3,0 | 2,5 | 2,0 | 1,6 | **1,0** | **0,7** | 10,9 | 15,9 | 19,4 | 🔴 |
| *HER2+ (ohne Trastuzumab, Referenz)* | 2,6 | 4,4 | 3,7 | 2,9 | 2,3 | 1,5 | 1,0 | 15,9 | 23,4 | 28,4 | 🔴 |
| **TNBC** | **3,4** | **7,5** | **4,8** | **3,0** | **1,8** | **0,76** | **0,24** | **18,8** | **21,5** | **22,3** | 🟢 **TRM** |

**Plausibilitätsprüfungen gegen unabhängige Quellen:**

| Prüfgröße | Modelltabelle | Referenz | Quelle |
|---|---|---|---|
| Luminal A 10-J DM | 9,0 % | 9,5 % (NL, Dx 2005) / 7,3 % (T1-2N0-1) | van Maaren 2019 / 2018 🟢 |
| Luminal A Hazard J5–20 | 0,7–0,9 %/J | T1N0 13 % / 15 J = 0,87 %/J | Pan 2017 🟢 |
| TNBC 10-J DM | 21,5 % | 16,7 % (NL, T1-2N0-1) | van Maaren 2018 🟢 |
| HER2+ 10-J DM ohne Trastuzumab | 23,4 % | 25,6 % | van Maaren 2019 🟢 |
| Gewichteter Mix (≈56/26/6/12 %) 10-J | ≈ 12,6 % | TRM nicht-TNBC 12,3 % + TNBC 21,5 % ⇒ 13,1 % | TRM 🟢 |

**Konditionierung auf den Nodalstatus** (falls das Modul das zusätzlich braucht): Subtypzeile ×
**pN0 0,62 / pN+ 1,93** 🔴 (aus TRM CI 10 J: 7,6 / 23,7 gegen Gesamt 12,3).

**Weitere Stadien-Anker, moderne Kohorten:**

| Quelle | Stratum | Peak-Hazard | ab J5/J7 | kumulativ |
|---|---|---|---|---|
| Nickson 2022 MJA (PMID 35987521), NSW-Register, n=6.338, Medianalter 59 J. | **localised** | J2 **2,8 %/J** (2,3–3,3) | ~1 %/J ab J5 | 14-J **14,3 %** |
| ebd. | **regional** | J2 **9,1 %/J** (7,8–10,3) | ~2 %/J ab J7 | 14-J **34,7 %** |
| van Maaren 2018 EJC (PMID 30144661), NL, T1-2N0-1, Dx 2005 | 10-J DM | | | T1N0 **7,8 %**, T2N1 **19,6 %**, Luminal A 7,3 %, TNBC 16,7 % |
| Metzger-Filho 2013 JCO (PMID 23897954), IBCSG, **node-negativ**, n=1.951 | 10-J Ereignisrate | | | Luminal A 14 % · Luminal B 24 % · HER2+ 27 % · TNBC 29 % |
| HERA, Cameron 2017 (PMID 28215665), n=5.102, FU 11 J. | 10-J DFS | | | Beobachtung **63 %** vs. **1 J. Trastuzumab 69 %**; DFS HR **0,76 (0,68–0,86)**; 2 J. ohne Zusatznutzen |
| Pedersen 2022 JNCI (PMID 34747484), DBCG | Spätrezidiv J10–32 nach 10 J. rezidivfrei | | | **16,6 %** (IR 15,53/1.000 PJ); Treiber > 20 mm, N+, **ER+** |

Alle 🟢 (mit Ära-Vorbehalt bei DBCG 1987–2004).

### 6.4 De-novo-M1 und Metastasierungsmuster

**M1 bei Erstdiagnose — Prämissenkorrektur.** Die im Konzept genannten **6,2 %** sind die **Gesamtrate über alle
Alter** im TRM-Subtypenkollektiv (Schrodi et al., DKK 2016, n=8.228, Dx 2000–2014, mittleres Alter 62,4 J.),
nicht die 50–59-Rate.

| Subtyp | n (%) | **M1 bei Erstdiagnose** | multivariate OR vs. Luminal A | Conf. |
|---|---|---|---|---|
| Luminal A-like | 2.571 (31,3) | **2,6 %** | Referenz | 🟢 |
| Luminal B-like HER2− | 3.524 (42,8) | **7,2 %** | 1,72 (1,23–2,42) | 🟢 |
| Luminal B-like HER2+ | 935 (11,4) | **10,1 %** | 1,71 (1,12–2,60) | 🟢 |
| HER2+ (non-luminal) | 365 (4,4) | **13,2 %** | 1,69 (1,01–2,81) | 🟢 |
| Triple-negativ | 833 (10,1) | **6,0 %** | 1,15 (0,70–1,87) n.s. | 🟢 |
| **Gesamt** | 8.228 | **6,2 %** (510) | p = 0,0085 | 🟢 **[alle Alter]** |

Weitere Prädiktoren (gleiche Quelle): pT1 **0,4 %** · pT2 3,3 · pT3 8,5 · **pT4 27,3 %** (OR 32,63); pN0 **0,6 %** ·
pN+ **5,7 %** (OR 4,24) · pNX 13,1 %; G1 0,7 % · G3 7,8 % 🟢. **Altersanker:** OR für M1 bei **50–69 J. vs. < 50 J.
= 2,26 (1,57–3,23)**, ≥ 70 J. 1,63 🟢.

**Gegenprobe RKI/ZfKD** „Krebs in Deutschland 2021–2023", 15. Ausgabe, **Abb. 3.17.4** (nur gültige Werte):
Frauen gesamt I 41 / II 40 / III 10 / **IV 9 %**; **Frauen 50–69 J. I 51 / II 35 / III 7 / IV 7 %** 🟢.
TRM-Datenbankstand 12/2021: M1-Anteil gesamt **6,9 %** (5.819/84.151), Medianalter M1 **68,3 J.** vs. M0 62,6 J. 🟢.

⇒ **Modellwert de-novo M1 für invasive Tumoren, Frauen 50–60: 0,060–0,065**, mit den Subtyp-Multiplikatoren oben
🟡. DCIS separat modellieren, sonst systematisch zu niedrig. **Nicht die SEER-Zahl (4,4 %) verwenden** — der
deutsche Wert liegt belegbar höher.

**Metastasierungsmuster — Konzept §11 Lücke 7 bestätigt und teilweise geschlossen.**

> ⚠️ **Es existiert keine bevölkerungsbezogene deutsche Registertabelle „Erstmetastasenort × Subtyp".** Das TRM
> publiziert diese Kreuztabelle nicht (Hölzel/Engel PMID 36538148 liefert nur Zeittrends). Die beste **deutsche**
> Quelle ist eine regionale Kohorte:

**Ignatov et al. 2018, J Cancer Res Clin Oncol 144:1347 (PMID 29675790)** — Sachsen-Anhalt/Magdeburg, n=12.053,
Dx **2000–2016**, med. FU 80,8 Mon., Medianalter 60–64 J. Werte = % **aller** Patientinnen des Subtyps 🟢:

| Lokalisation | Luminal A | Luminal B | Luminal/HER2 | HER2-enr. | TNBC |
|---|---|---|---|---|---|
| Knochen | 2,1 | 5,7 | **7,9** | 6,0 | 5,5 |
| Leber | 1,0 | 2,8 | 5,2 | **5,4** | 3,4 |
| Lunge | 1,1 | 2,9 | 4,7 | 4,9* | **7,0** |
| Hirn | 0,3 | 1,5 | 3,4 | **5,9** | 4,9 |
| distant nodal | 0,4 | 1,3 | 2,6 | 2,6 | 3,8 |
| **Rezidiv gesamt** | 4,8 | 10,7 | 16,1 | **20,2** | 19,2 |

\* im Extrakt als 2,5 % ausgewiesen, rechnerisch 30/614 = 4,9 % → 🟡, vor Verwendung im Volltext prüfen.

**Anteilsverteilung unter den Metastasierten** (für die Zuweisung der Lokalisation im Modul) — Kennecke 2010
(PMID 20498394), BC Cancer Agency, Dx 1986–1992, ⚠️ Ära:

| Subtyp | Gehirn | Leber | Lunge | Knochen | distant nodal | Pleura/Perit. |
|---|---|---|---|---|---|---|
| Luminal A (n=458) | 7,6 | 28,6 | 23,8 | **66,6** | 15,9 | 28,2 |
| Luminal B (378) | 10,8 | 32,0 | 30,4 | **71,4** | 23,3 | 35,2 |
| Luminal/HER2 (117) | 15,4 | 44,4 | 36,8 | 65,0 | 22,2 | 34,2 |
| HER2-enriched (136) | **28,7** | 45,6 | 47,1 | 59,6 | 25,0 | 31,6 |
| Basal-like (159) | **25,2** | 21,4 | 42,8 | 39,0 | **39,6** | 29,6 |

Mehrfachnennung, Summe > 100 % 🟢. Multivariat vs. Luminal A: HER2-enriched Gehirn **OR 5,3 (3,0–9,2)**, Lunge
3,2; Basal Gehirn 3,6, Knochen **0,4 (0,2–0,6)**, nodal 2,9 🟢. **Einziger Altersanker:** Alter > 50 J. → Gehirn
**OR 0,5 (0,4–0,7)**, Knochen **OR 0,6 (0,5–0,8)** 🟢 — in 50–60 also **weniger** Hirn- und Knochenmetastasen als
bei Jüngeren.

**Für de-novo-M1 gilt eine andere Verteilung** (Single-Site-M1, Gong 2017 PMID 28345619, SEER, n=4.295) 🟢:

| Subtyp | Knochen | Leber | Lunge | Hirn |
|---|---|---|---|---|
| HR+/HER2− | **79,7 %** | 8,1 | 11,0 | 1,2 |
| HR+/HER2+ | 61,0 | 20,3 | 17,1 | 1,6 |
| HR−/HER2+ | 35,8 | 32,7 | 28,1 | 3,4 |
| TNBC | 43,0 | 18,9 | **33,1** | 5,1 |

> ⚠️ **Methodenwarnung für die Implementierung:** die Nenner wechseln zwischen den Quellen — Kennecke Tab. 2 =
> % aller Patientinnen des Subtyps (15-J kum. Inzidenz), Tab. 3 = % **unter Metastasierten** (Mehrfachnennung),
> SEER/Gong = % unter Single-Site-**de-novo**-M1, TRM = konkurrenzrisikokorrigierte kumulative Inzidenz.
> **Nicht mischen.** Und: SEER-Verteilungen betreffen de-novo-M1 (Knochen überrepräsentiert, weil
> Skelettszintigraphie Staging-Standard ist), Kennecke/Ignatov die **metachrone** Metastasierung ⇒ das Modul
> braucht **zwei getrennte Lokalisations-Generatoren**.

**ZNS-Metastasierung:**

| Setting | Wert | Quelle | Conf. |
|---|---|---|---|
| MBC, kumulative Inzidenz Hirnmetastasen | gesamt **15 %** (11–20) · **HER2+ 31 %** (22–38) · **TNBC 32 %** (19–49) · HR+/HER2− 15 % (7,8–27) | Kuksis 2021 Neuro Oncol, PMID 33367836, Metaanalyse 25 Studien | 🟢 |
| ZNS **bei MBC-Erstdiagnose** | HR+/HER2− 4,3 % · HR+/HER2+ 9,2 % · **HR−/HER2+ 17,0 %** · TNBC 13,1 % | Darlix 2019 ESME, PMID 31719684, n=16.701 | 🟢 |
| kum. Inzidenz ab MBC-Dx, 12 / 24 Mon. | HR+/HER2− 8,3 / 14,4 · HR+/HER2+ 16,8 / 29,2 · **HR−/HER2+ 32,4 / 49,0** · TNBC 29,8 / 44,8 % | ebd. | 🟢 |
| Median bis ZNS-Metastase | HR+/HER2− 15,1 · HR+/HER2+ 12,8 · HR−/HER2+ 8,5 · **TNBC 5,8** Mon. | ebd. | 🟢 |
| **frühes Mammakarzinom** (Stadium I–III), kum. Inzidenz behandelter Hirnmetastasen | gesamt **2,8 % @12 J**; Stadium III 5-J/12-J: HR+/HER2− 3,3/5,9 · HER2+/HR+ 7,5/11,8 · HER2+/HR− 11,2/14,3 · **TNBC 13,1/13,4 %** (Plateau) | Ontario, PMID 41722138, n=92.973 | 🟡 |
| Trastuzumab und ZNS | ZNS als erstes DFS-Ereignis **2 % vs. 2 %** (HERA); Metaanalyse 4 RCTs: 2,56 % vs. 1,94 %, **RR 1,35 (1,02–1,78)** — relative Verschiebung, weil extrakranielle Rezidive stärker gesenkt werden | Pestalozzi 2013 / Olson 2013 | 🟢 |

### 6.5 Kontralaterales Mammakarzinom (Korrektur K7)

| Kollektiv | 5-J | **10-J** | ⇒ Ø %/Jahr | Quelle | Conf. |
|---|---|---|---|---|---|
| NL-Register, Erst-BC 2003–2010, n=83.144 | — | **3,8 % (3,7–4,0)** | **0,38** | Kramer 2019 JNCI, PMID 30698719 | 🟢 |
| PredictCBC-2.0, 23 Studien, n=207.510 | 2,2 % | **4,1 %** | **0,41** | Giardiello 2022, PMID 36271417 | 🟢 |
| **duktal, MIT Systemtherapie** | — | **2,8 %** | **0,28** | Akdeniz 2023 Cancer Med, PMID 36127572 | 🟢 |
| **duktal, OHNE Systemtherapie** | — | **5,6 %** | **0,56** | ebd. | 🟢 |
| lobulär mit / ohne | — | 3,2 / 6,6 % | — | ebd. | 🟢 |
| EBCTCG-Kontrollarm ER+ ohne Tamoxifen | — | 15-J **9,8 %** | ≈0,65 | Davies 2011, PMID 21802721 | 🟢 (15-J) |

> **Verdikt zu „0,4–0,5 %/Jahr":** nur für eine **gemischte moderne Registerkohorte** korrekt (0,38–0,41). Zu hoch
> für ER+ **mit** endokriner Therapie (0,28), zu niedrig ohne Systemtherapie (0,56). **Eine einzige konstante
> CBC-Rate ist nicht kalibrierbar — die endokrine Therapie ist der dominierende Modifikator (Faktor ~2).**

**Therapieeffekt auf das CBC-Risiko:**

| Intervention | Effektmaß | Wert | Quelle | Conf. |
|---|---|---|---|---|
| **Tamoxifen 5 J. vs. keine, ER+** | RR | **0,62** (SE 0,07), 2p<0,00001; 15-J **6,5 % vs. 9,8 %** | EBCTCG Davies 2011, Tab. 1 | 🟢 |
| Tamoxifen, ER-arm/negativ | RR | 0,94 (0,73–1,20) **n.s.** | ebd. | 🟢 |
| Tamoxifen 10 J. vs. 5 J. | RR | 0,88 (0,77–1,00), 2p=0,05 | ATLAS, PMID 23219286 | 🟢 |
| **endokrine Therapie gesamt** | HR | **0,46 (0,41–0,52)**; nur ER+ CBC 0,41; ER− CBC 1,32 n.s. | Kramer 2019 / Akdeniz 2023 | 🟢 |
| **Aromatasehemmer** vs. keine ET | HR | **0,32 (0,23–0,44)** — stärkster Effekt | Kramer 2019 | 🟢 |
| Chemotherapie | HR | 0,70 (0,62–0,80); taxanhaltig 0,48 | ebd. | 🟢 |
| Trastuzumab + Chemo | HR | 0,57 (0,45–0,73) | ebd. | 🟢 |

**BRCA — Korrektur K7.** Engel C et al., Int J Cancer 2020;146(4):999–1009, **PMID 31081934** (GC-HBOC,
12 Zentren, n=2.993, 10.090 Personenjahre, Median-Baseline-Alter **42 J.**), 10-J CBC:
**BRCA1 25,1 % (19,6–31,9)** ✅ · **BRCA2 6,6 % (3,4–12,5)** ✅ · **Nicht-Trägerinnen 3,6 % (2,2–5,7)** —
**nicht 4,6 %** wie im Konzept. Autorenfazit: CBC-Risiko der Nicht-Trägerinnen *„similar to women with unilateral
BC from the general population"* 🟢.
⚠️ Engel/Rhiem sind **klinisch selektierte Hochrisikofamilien unter MRT-Intensivüberwachung**. Populationsbasiert
(BRIDGES + CARRIERS 2026, PMID 42236538) liegt das 10-J-CBC bei **BRCA1 10,1 % (7,5–13,6)** und BRCA2 10,2 % —
die Diskrepanz zu 25,1 % ist Selektionsbias 🟢. **Für den schlanken Hochrisiko-Arm (Konzept §1.4.1) die
populationsbasierten Werte verwenden, nicht Engel.**
**Altersabhängigkeit in 50–60:** PredictCBC modelliert Alter als Spline mit Knoten bei **50** bzw. **60 J.**; das
Modellfenster liegt damit im **flachen** Teil der Alterskurve. EBCTCG: *„the absolute (and proportional) decrease
in CBC was independent of age"* (RR Tamoxifen: < 45 J. 0,52 · 45–54 J. 0,64 · 55–69 J. 0,64) 🟢.
⇒ **altersflache CBC-Rate für 50–60 ist vertretbar**; der Therapiestatus dominiert 🔴.

### 6.6 Lokoregionäres Rezidiv → Ausgang

**S3 v5.1 Kap. 5.1.2:** *„Beim lokalen und beim lokoregionären Rezidiv **ohne Fernmetastasierung** besteht in der
Regel ein **kuratives Therapieziel**"*; Prognosefaktoren: Alter < 70 J., kleiner Befund, **DFI > 2–3 J.**,
**R0-Entfernung**. Höchste lokale Kontrolle beim intramammären Rezidiv: sekundäre **Mastektomie** — die Radikalität
beeinflusst das **Überleben nicht** (Statement 5.8). 5-J-Überleben nach Rezidiv: **21–65 %** 🟡.
Ein expliziter Anteil „R0-resektabel" ist **in keiner Primärquelle publiziert** 🔴.

**Der wichtigste Modellierungsbefund — IBTR und regionäres Rezidiv sind prognostisch fundamental verschieden:**

| Rezidivtyp | kum. Inzidenz | **Anteil < 5 J.** | **5-J-OS danach** | 5-J-DDFS | HR Mortalität | Quelle |
|---|---|---|---|---|---|---|
| **IBTR nach BET, pN0** | 6,6 % @12 J | 37,1 % | **76,6 %** | — | — | Anderson 2009, PMID 19349544 |
| **regionäres/anderes LRR, pN0** | 1,8 % @12 J | **72,7 %** | **34,9 %** | — | — | ebd. |
| **IBTR nach BET, pN+** | 8,7 % @10 J | 62,2 % | **59,9 %** | 51,4 % | 2,58 (2,11–3,15) | Wapnir 2006, PMID 16648502 |
| **regionäres LRR, pN+** | 6,0 % @10 J | **80,6 %** | **24,1 %** | 18,8 % | **5,85 (4,80–7,13)** | ebd. |
| Thoraxwandrezidiv nach Mastektomie | — | Median PFS 17,4 Mon. | **52,1 %** | 35,6 % | — | Zhao 2021, PMID 34794225 |

Alle 🟢. Zusätzlich Lee 2019 (PMID 31642987, n=495): DMFS nach isoliertem LRR nach Risikogruppe — low **79,4 %** ·
intermediate 68,1 % · high 47,6 % · sehr hoch **36,0 %** 🟢.

⇒ **Das Modul braucht getrennte Zustände `IBTR` und `regionäres LRR`** — nicht einen gemeinsamen
„Lokalrezidiv"-Zustand. Übergang LRR → Fernmetastase innerhalb 5 J.: **IBTR ≈ 0,40–0,50 · regionär ≈ 0,80** 🔴
(aus Wapnir 2006 DDFS 51,4 % vs. 18,8 %).

**Chemotherapie nach isoliertem lokoregionärem Rezidiv — CALOR** (Aebi 2014 Lancet Oncol PMID 24439313; final
Wapnir 2018 JCO **PMID 29443653**), n=162, nur **R0-resezierte** ILRR:

| Endpunkt | ER− Chemo | ER− keine | ER+ Chemo | ER+ keine | p-Interaktion |
|---|---|---|---|---|---|
| **10-J-DFS** | **70 %** | **34 %** (HR 0,29; 0,13–0,67) | 50 % | 59 % (HR 1,07) | **0,013** |
| 10-J-BCFI | 70 % | 34 % | 58 % | 62 % | 0,034 |
| 10-J-OS | 73 % | 53 % (HR 0,48; 0,19–1,20) | 76 % | 66 % (HR 0,70) | 0,53 |

🟢, aber kleine Fallzahlen (58 ER− / 104 ER+). ⚠️ CALOR ist per Design auf **R0-resezierte, fernmetastasenfreie**
ILRR beschränkt und liegt deshalb deutlich über Register-Baselines — **CALOR nur als Effektschätzer für den
Chemo-Nutzen bei ER− verwenden, nicht als Populations-Baseline** 🔴.

---

## 7. Überleben und Mortalität — Validierungsanker

Diese Werte werden **nicht als Arrows kodiert**, sondern sind die Zielgrößen, gegen die die generierte Kohorte in
AP-V validiert wird.

### 7.1 Relatives Überleben nach UICC-Stadium

**RKI/GEKID „Krebs in Deutschland für 2021–2023", 15. Ausgabe (2025), Kap. 3.17, S. 74, Abbildung 3.17.6** —
⚠️ **es ist eine Abbildung, keine Tabelle**; die Werte sind gerundete Balkenbeschriftungen ohne Konfidenzintervalle.

| UICC (TNM 8. Aufl.) | 5-J-RS | Conf. |
|---|---|---|
| I | **101 %** | 🟢 ✅ |
| II | **95 %** | 🟢 ✅ |
| III | **76 %** | 🟢 ✅ |
| IV | **31 %** | 🟢 ✅ |
| unbekannt | 80 % | 🟢 |

**10-Jahres-RS nach UICC-Stadium existiert nicht** — Volltextprüfung des Berichts: stadienspezifisches Überleben
wird durchgängig **nur als 5-Jahres-RS** ausgewiesen 🟢 (Negativbefund). Ersatzanker für 10 Jahre ist die
TRM-pTNM-Tabelle (§7.3).

Gesamt C50 Frauen (RKI Tab. 3.17.1, S. 72): **absolut 5-J 79 % / 10-J 66 %; relativ 5-J 88 % / 10-J 83 %** 🟢.

> ⚠️ **UICC I = 101 % darf nicht als Überlebenswahrscheinlichkeit implementiert werden.** Relatives Überleben
> > 100 % heißt, dass Stadium-I-Patientinnen die Allgemeinbevölkerung übertreffen (Screening-Selektion). Korrekt
> ist: **Hintergrundmortalität als eigenständigen Arm** (§7.5) modellieren und für UICC I eine **Exzessmortalität
> ≈ 0** ansetzen; das absolute Überleben ergibt sich dann aus der Sterbetafel.

### 7.2 Altersstratifizierte Anker — die Zielwerte für die Kohorten-Validierung

**RKI, Abb. 3.17.5, S. 74** (5-J-RS nach Diagnosealter): 20–39 J. 91 % · 40–49 J. 93 % · **50–59 J. 92 %** ✅ ·
**60–69 J. 90 %** ✅ · 70–79 J. 85 % · ≥ 80 J. 75 % — alle 🟢.

**TRM Survival-Faktenblatt C50 Frauen, Tab. 3c, S. 8** (Dx 1998–2020, N=58.994), Altersgruppe **50–59 J.**
(n=13.526) — liefert als einzige Quelle absolutes **und** relatives Überleben bis 15 Jahre:

| Jahr | beobachtet (absolut) | relativ | Conf. |
|---|---|---|---|
| 1 | 98,1 % | 98,4 % | 🟢 |
| 3 | 93,2 % | 94,3 % | 🟢 |
| **5** | **89,0 %** | **90,8 %** | 🟢 |
| **10** | **80,6 %** | **84,9 %** | 🟢 |
| **15** | **73,1 %** | **80,7 %** ✅ | 🟢 |

**Konsolidierte Validierungsziele für die generierte Kohorte (Frauen 50–60):**

| Endpunkt | Zielwert | Quelle |
|---|---|---|
| 5-J relatives Überleben | **91 ± 1 %** (RKI 92 / TRM 90,8) | 🟢 |
| 5-J absolutes Überleben | **89,0 %** | TRM 🟢 |
| 10-J relatives Überleben | **84,9 %** | TRM 🟢 |
| 10-J absolutes Überleben | **80,6 %** | TRM 🟢 |
| 15-J relatives Überleben | **80,7 %** | TRM 🟢 |
| medianes Gesamtüberleben | **19,8 Jahre** (Wert der 60–69-Gruppe; für 50–59 nicht erreicht) | TRM 🟢 |

⚠️ **Kohorten-Caveat:** TRM = Dx 1998–2020, München; RKI = 2021–2023 bundesweit. Für eine moderne Kohorte ist der
RKI-Wert (92 %) der bessere Anker, für die Langzeitpunkte (10/15 J.) gibt es nur TRM.
**Nicht gegen die 88 % des nationalen Alle-Alter-Werts validieren** (Konzept-Hinweis bestätigt).

### 7.3 Überleben nach pTNM

**TRM Survival-Faktenblatt, Tab. 4b, S. 9–10** (Dx 1998–2020, N=56.209) — alle zehn Konzeptwerte exakt bestätigt,
**[alle Alter]**:

| pTNM | n (Anteil) | 5-J rel. | 10-J rel. | 5-J beob. | 10-J beob. | 15-J rel. | Median OS |
|---|---|---|---|---|---|---|---|
| **pT1N0M0** | 23.217 (41,3 %) | **100,8** ✅ | **98,7** ✅ | 95,5 | 87,0 | 94,6 | n. err. |
| **pT2N0M0** | 8.606 (15,3 %) | **95,4** ✅ | **88,2** ✅ | 87,4 | 73,3 | 80,1 | 20,4 J. |
| **pT1N+M0** | 6.691 (11,9 %) | **94,8** ✅ | **86,6** ✅ | 90,0 | 76,9 | 80,0 | n. err. |
| **pT2N+M0** | 7.790 (13,9 %) | **85,3** ✅ | **71,3** ✅ | 78,9 | 60,6 | 61,5 | 13,9 J. |
| **M1** | 4.230 (7,5 %) | **28,3** ✅ | **13,7** ✅ | 25,6 | 11,2 | 9,3 | **2,3 J.** |

Ergänzend (im Konzept nicht enthalten) 🟢: pT3N0M0 86,1 / 76,2 · pT4N0M0 72,9 / 55,5 · pT3N+M0 73,6 / 54,7 ·
pT4N+M0 54,6 / 35,2 · pT1NXM0 99,2 / 84,8 · pT2NXM0 74,0 / 47,1 %.
Die pTNM-Tabelle ist **nicht** nach Subtyp aufgeschlüsselt 🔴 — Subtypdaten gibt es nur für das metastasierte
Setting (§7.4).

### 7.4 Metastasiertes Setting

**Deutsche Realwelt-Baseline** — TRM Survival Tab. 5f, S. 15, beobachtetes Überleben **ab erster Fernmetastase**,
Progressionszeitraum **ab 2007**, n=8.811 (alle vier Konzeptwerte exakt bestätigt) 🟢:

| Jahr ab Metastase | 1 | 2 | 3 | 4 | **5** | 7 | **10** |
|---|---|---|---|---|---|---|---|
| Überleben | **69,3 %** ✅ | **52,2 %** ✅ | 38,8 % | 29,6 % | **23,8 %** ✅ | 16,4 % | **10,7 %** ✅ |

⚠️ **Zwei Präzisierungen:** (1) Es ist **beobachtetes (all-cause) Überleben**, **nicht** relatives — für einen
Synthea-Sterbe-Arm genau richtig, aber nicht mit den RS-Werten aus §7.1–7.3 mischen. (2) Die Metrik ist
Post-Progression-Survival ab erster Fernmetastase; „ab 2007" bezeichnet den **Progressions**-, nicht den
Diagnosezeitraum.

**De-novo-M1 vs. metachron — ein Befund, der die Modellstruktur ändert** (TRM Spezialauswertung `abmet`,
Tab. 4–7) 🟢:

| Kollektiv | Zeitraum | n | **Median PPS** | 1-J | 2-J | 5-J |
|---|---|---|---|---|---|---|
| **de novo M1** | 2012–2020 | 1.972 | **2,6 Jahre** | 73,5 % | 58,5 % | 28,7 % |
| **metachron (M0→Met)** | 2012–2020 | 1.672 | **1,5 Jahre** | 61,6 % | 40,9 % | 18,1 % |
| de novo M1, **> 50 J.** | — | 3.273 | **2,3 Jahre** | | | |
| metachron, **> 50 J.** | — | 4.019 | **1,5 Jahre** | | | |

> **De-novo-M1 überlebt ab Metastasierung deutlich länger als metachrone Metastasierung** (2,6 vs. 1,5 Jahre,
> +73 %) — unabhängig bestätigt durch SystHERs (HER2+: de novo OS nicht erreicht vs. 44,5 Mon. bei rezidiviert,
> HR 0,55; PMID 32043771) 🟢. Ursachen: keine Vortherapie/Resistenz, günstigere Metastasenmuster, chemonaiv.
> ⇒ **Das Modul darf keinen einheitlichen M1-Hazard verwenden. Zwei getrennte Zustände mit unterschiedlichen
> Sterberaten sind nötig.**

**Medianes Überleben ab Metastasierung je Subtyp — deutsche Realwelt** (TRM `abmet` Tab. 12/13). **Das ersetzt
den im Konzept verwendeten Kennecke-2010-Block** (kanadische Kohorte 1986–92):

| Subtyp | **de novo M1** | **metachron** | Conf. |
|---|---|---|---|
| **HR+/HER2−** | n=2.368 · **2,8 J.** (1-J 78,1 · 2-J 61,9 · 5-J 28,5 · 10-J 11,0 %) | n=3.446 · **2,1 J.** | 🟢 |
| **HR+/HER2+** | n=478 · **2,8 J.** (1-J 75,0 · 5-J 31,3 · 10-J 15,4 %) | n=593 · **1,9 J.** | 🟢 |
| **HR−/HER2+** | n=234 · **2,3 J.** (1-J 71,5 · 5-J 27,7 · 10-J 13,8 %) | n=282 · **1,3 J.** | 🟢 |
| **TNBC** | n=293 · **1,1 J.** (1-J 53,0 · 2-J 30,5 · 5-J 13,5 %) | n=771 · **0,8 J.** | 🟢 |

⚠️ Kohorte 2002–2020, DB-Stand 09/2021 ⇒ **prä-CDK4/6i, prä-T-DXd, prä-Immuntherapie**. Valide deutsche
*historische* Baseline, **nicht** das Ziel für eine 2025er-Kohorte. Die Subtyp-*Relationen* (TNBC ≈ 40 % des
HR+-Überlebens) sind dagegen stabil.

**Moderne Studienanker** (für eine Kohorte mit Behandlungsjahr ≥ 2020):

| Subtyp / Setting | Studie | Median OS | PMID | Conf. |
|---|---|---|---|---|
| HR+/HER2−, **1L CDK4/6i** | MONALEESA-2 (Ribociclib+Letrozol) | **63,9 Mon.** (52,4–71,0), HR 0,76 | 35263519 | 🟢 |
| dito | MONARCH-3 (Abemaciclib+AI) | **66,8 Mon.**, HR 0,804 **n.s.** | 38729566 | 🟢 |
| dito | MONALEESA-3 ITT / 1L-Subgruppe | 53,7 / **67,6 Mon.** | 34102253 / 37653397 | 🟢 / 🟡 |
| dito | PALOMA-2 (Palbociclib) | **53,9 Mon.**, HR 0,96 **n.s.** | 38252901 | 🟢 |
| dito, **Realwelt** | Flatiron-EHR, 1L CDK4/6i | **54,3 Mon.** (ohne Dosisreduktion) | 39516687 | 🟡 US |
| HR+/HER2−, ≥ 2L | MONARCH-2 / PALOMA-3 | 46,7 / 34,8 Mon. | 31563959 / 35552673 | 🟢 |
| **HER2+, 1L** | **CLEOPATRA** (End-of-Study, FU 99,9 Mon.) | **57,1 Mon.** (50–72) vs. 40,8 ✅ Konzeptwert | **32171426** | 🟢 |
| HER2+, 2L | DESTINY-Breast03 (T-DXd) | **52,6 Mon.** vs. 42,7, HR 0,73; PFS 29,0 vs. 7,2 Mon. | 38825627 | 🟢 |
| HER2-low, ≥ 2L | DESTINY-Breast04 | 23,4 Mon. vs. 16,8, HR 0,64 | 35665782 | 🟢 |
| **TNBC, 1L, CPS ≥ 10** | KEYNOTE-355 | **23,0 Mon.** vs. 16,1, HR 0,73, p=0,0185 | 35857659 | 🟢 |
| TNBC, ITT | ebd. | 17,2 vs. 15,5 Mon. **n.s.** | 35857659 | 🟢 |
| TNBC, ≥ 2L | ASCENT (Sacituzumab Govitecan) | **12,1 Mon.** vs. 6,7, HR 0,48 | 33882206 | 🟢 |

**Empfehlung für die Modellwerte medianes Überleben ab Metastasierung** (Kompromiss zwischen deutscher
Registerrealität und modernem Therapiestandard) 🔴:

| Subtyp | Konzept-Vorschlag (Kennecke 2010) | **Empfehlung Draft C** | Begründung |
|---|---|---|---|
| Luminal A / B (HR+/HER2−) | 2,2 / 1,6 J. | **4,0–4,5 J.** (48–54 Mon.) | TRM 2,8 J. (prä-CDK4/6i) ↔ 1L-Studien 54–67 Mon. ↔ Realwelt 54,3 Mon.; Populationsmittel liegt unter dem Studienwert |
| HER2+ (HR+ oder HR−) | 1,3 / 0,7 J. | **3,5–4,0 J.** | TRM 2,3–2,8 J. (prä-Pertuzumab) ↔ CLEOPATRA 57,1 Mon. |
| TNBC | 0,5 J. (basal) | **1,3–1,7 J.** (16–20 Mon.) | TRM 1,1 J. (prä-Immuntherapie) ↔ KEYNOTE-355 17,2–23,0 Mon. |

Die im Konzept genannten Kennecke-Werte sind **nicht mehr verwendbar** — sie stammen aus einer Kohorte ohne
Trastuzumab, ohne AI, ohne CDK4/6-Inhibitoren und unterschätzen das moderne Überleben um Faktor 2–3.
Die größte Kluft zwischen Studie und deutscher Registerrealität besteht beim **TNBC**.

### 7.5 Hintergrundmortalität — der Arm, der nicht mit Krebsmortalität verwechselt werden darf

**DESTATIS, Statistischer Bericht Sterbetafeln 2023/2025, EVAS 12621, Tab. 12613-b02** (Deutschland, weiblich):

| Alter x | qₓ | qₓ in % | lₓ |
|---|---|---|---|
| **50** | 0,0017610 | **0,176 %** | 97.814,2 |
| 52 | 0,0021046 | 0,210 % | 97.452,3 |
| **55** | 0,0028265 | **0,283 %** | 96.769,2 |
| 58 | 0,0042526 | 0,425 % | 95.482,8 |
| **60** | 0,0047979 | **0,480 %** | 95.076,8 |
| 65 | 0,0080769 | 0,808 % | 92.246,7 |

Alle 🟢. Kumuliert (aus lₓ berechnet) 🟢:

| Zeitraum | Sterbewahrscheinlichkeit | Überleben |
|---|---|---|
| 5 J. ab Alter 50 | 1,07 % | 98,93 % |
| **10 J. ab Alter 50** | **2,80 %** | 97,20 % |
| 15 J. ab Alter 50 | 5,69 % | 94,31 % |
| **10 J. ab Alter 55** | **4,67 %** | 95,33 % |
| 10 J. ab Alter 60 | 7,67 % | 92,33 % |

⇒ **Direkt implementierbar:** jährliche Hintergrund-Sterberate **0,18 %** mit Alter 50, steigend auf **0,48 %** mit
Alter 60.

**Anteil brustkrebsbedingter vs. anderer Todesfälle, 50–59 J.** — aus TRM Tab. 3c über die Ederer-II-Identität
*erwartetes Überleben = beobachtet / relativ* hergeleitet 🟡:

| Nach | Gesamttote | davon Hintergrund | **nicht tumorbedingt** | **tumorbedingt** |
|---|---|---|---|---|
| **5 J.** | 11,0 Pp. | 1,98 Pp. | **18 %** | **82 %** |
| **10 J.** | 19,4 Pp. | 5,06 Pp. | **26 %** | **74 %** |
| **15 J.** | 26,9 Pp. | 9,42 Pp. | **35 %** | **65 %** |

Die impliziten Hintergrundwerte (10 J.: 94,9 % Überleben) stimmen gut mit der DESTATIS-Sterbetafel überein
(10 J. ab 55: 95,3 %) — **gegenseitige Validierung zweier unabhängiger Quellen** 🟢 für die Konsistenz.

⇒ **Zwei getrennte Sterbe-Arme sind zwingend.** Ohne Hintergrundarm überschätzt das Modul die Brustkrebsmortalität
in der Langzeitnachbeobachtung um bis zu einem Drittel. Im Fenster 50–60 (max. ~10 Jahre Follow-up) ist der
Hintergrundarm klein (2,8 % kumuliert), aber nicht vernachlässigbar.

### 7.6 Screening-Kontext (keine Arrows, nur Plausibilität)

| Befund | Wert | Quelle | Conf. |
|---|---|---|---|
| Rückgang der Brustkrebsmortalität 2003/04 → 2015/16, **50–59 J.** | **−25,8 %** | Katalinic et al., Int J Cancer 2020;147(3):709–718, **PMID 31675126** | 🟢 **[50–59]** |
| dito, 60–69 J. | −21,2 % | ebd. | 🟢 |
| Rückgang Inzidenz Stadium III / IV, 50–59 J. | −24,2 % / −23,0 % | ebd. | 🟢 |
| Reduktion fortgeschrittener Karzinome (UICC ≥ II) nach 1./2. Folgescreening | −16,5 % / **−21,3 %** | Simbrich/Hense, BMC Cancer 2020;20:174, PMID 32131766, n=498.029 | 🟢 |
| Preis | „moderate Überdiagnose, v. a. starker Anstieg von In-situ-Karzinomen" | Katalinic 2020 | 🟢 |

⚠️ Katalinic 2020 ist eine **ökologische Vorher-Nachher-Analyse** ohne individuelle Expositionszuordnung; die
formale Mortalitätsevaluation des deutschen MSP war zum Protokollzeitpunkt (PMID 36353307) **noch nicht
abgeschlossen** 🟢 (Negativbefund).
⇒ **Nicht als kausalen Effektparameter implementieren.** Der mechanistisch korrekte Hebel ist der
**Stadienshift** (50–69 J.: 51 % Stadium I gegen 41 % in der Gesamtpopulation, §6.4), nicht ein aufgeprägter
Mortalitäts-Multiplikator.

---

## 8. Offene Datenlücken

Nummeriert und getrennt nach „bereits im Konzept §11 geführt" (K) und „neu aus dieser Recherche" (N).
Priorität = Einfluss auf die Modellausgabe.

| # | Lücke | Ersatz / Prior | Prio |
|---|---|---|---|
| **N1** | **Neoadjuvanz-Anteil je Subtyp für Diagnosejahre nach 2018** — Ortmann endet 2018, PMID 36604331 endet 2017, beide **vor** der Pembrolizumab-Zulassung (2021) und vor der Ausweitung der dualen HER2-Blockade. Systematische PubMed-Suche 2021–2026: kein passender Treffer. OnkoZert schlüsselt **nicht** nach Subtyp auf | **Teilweise geschlossen:** die Marginale ist für 2023 gemessen 🟢, der Alters-Multiplikator 1,28 belegt 🟢, die Subtyp-Reskalierung jetzt hergeleitet und mit Konsistenzprobe versehen (§3.3) — bleibt aber 🔴 | **hoch** (= K4 des Konzepts) |
| **N1b** | **Uptake Pembrolizumab neoadjuvant beim TNBC in DE** — PubMed count = 0; keine OnkoZert-Kennzahl zu Immuncheckpoint-Inhibitoren | eligible Fraktion (TNBC > 2 cm oder N+) ≈ 0,60–0,70 🔴, Uptake als freier Parameter | **hoch** |
| **N1c** | **pCR-Rate als deutsche Versorgungskennzahl** — im OnkoZert-Bericht kein einziger Treffer auf `pCR`/`ypT0`/`Komplettremission` | zwei Registerkohorten (PMID 36604331 altersstratifiziert 🟢, Ortmann als Obergrenze 🟢); pCR-Definition in beiden Papieren **nicht ausformuliert** | mittel |
| **N1d** | **Zeittrend des Neoadjuvanz-Anteils 2019–2023** — die OnkoZert-Basisdatentabellen haben keine Jahresachse; die 5-Jahres-Perzentilreihen existieren nur für die 23 Kennzahlen, von denen keine die Neoadjuvanz abbildet | rekonstruierbar nur durch Auslesen der Vorjahresberichte 2021–2024 (S. 8 je einzeln) | niedrig |
| **N1e** | Konzept-Anker **„GeparOcto TNBC 48,5/51,7 %"** ist im S3-Korpus nicht zitiert (FTS-Treffer 0 für GeparOcto/GeparX/GeparSepto) | direkt belegen oder streichen | niedrig |
| **N2** | **Rekonstruktionsrate nach Mastektomie** (gesamt, sofort/verzögert, implantat/autolog, altersabhängig) — keine DKG-Kennzahl, IRegG-Daten erst ab 07/2024 erhoben und unpubliziert | 🔴 Prior 0,40–0,55; **Alternative: für v1 auslassen** | mittel |
| **N3** | **Realer Uptake adjuvanter CDK4/6-Inhibitoren in DE** — nur Eligibility-Studien (Tübingen 19,4 %, Ulm+Tü 43 % NATALEE), kein Verordnungsanteil | Eligibility × Prior-Uptake 🔴 | **hoch** (Therapiepfad-Verzweigung) |
| **N4** | **Uptake Pertuzumab adjuvant** und **Anteil 6-Monats-Trastuzumab** in DE | Pertuzumab: keine; Trastuzumab-6-Mon. < 0,05 abgeleitet 🟡 | mittel |
| **N5** | **Chemo-Quote bei HR+/HER2−/N0** — OnkoZert KZ 6 ist definitorisch auf N+ beschränkt | Näherung 0,15–0,19 über die deutsche RS-Verteilung 🟡 | mittel |
| **N6** | **Jahresverlauf der endokrinen Persistenz** (Jahre 1, 2, 4) — Kostev publiziert nur den 5-J-Endpunkt | interpolierte Kurve auf zwei Anker kalibriert 🔴 (§4.3) | mittel |
| **N7** | **Anteil Switch-Strategien (TAM → AI)** und **Uptake erweiterter ET > 5 J.** in DE | keine Daten 🔴; freie Parameter | niedrig |
| **N8** | **Endokrine Therapie bei ER+ DCIS in DE** — KZ 7 umfasst ausdrücklich nur invasive Karzinome | Prior 0,15–0,30 aus dem schwachen Empfehlungsgrad 🔴 | niedrig |
| **N9** | **Realer RNI-Anteil** und **ALND-Rate bei pN+** — beide nicht als Kennzahl erhoben; zusätzlich fehlt der N1/N2/N3-Split | Indikationslogik aus AGO/S3/DEGRO 🔴 | mittel |
| **N10** | **Reale Umsetzung des Axilla-Verzichts (S3 Empf. 4.57, INSEMA/SOUND)** — 2023 nur als Studienbegründung sichtbar | Prior 0,05–0,15 für 2025+ 🔴, als Stellknopf kennzeichnen | mittel |
| **N11** | **Hypofraktionierungsanteil national, registerbasiert** — nur zwei DEGRO-Umfragen (2017: 16 %, 2026: 77 %) | Korridor 0,75–0,85 🟡 | niedrig |
| **N12** | **Mediane Zahl entfernter LK (SLNB/ALND)** und **SLNB-Detektionsrate als Kennzahl** | Literaturkonvention 2–3 / 12–16 🔴; Detektion > 99 % indirekt 🟡 | niedrig |
| **N13** | **Subtypspezifische jährliche Fernrezidiv-Hazards, gemessen** — TRM liefert nur TNBC vs. nicht-TNBC; Luminal A/B und HER2+ bleiben abgeleitet | §6.3, gegen vier unabhängige Quellen plausibilisiert 🔴 | **hoch** |
| **N14** | **Deutsche Registertabelle „Erstmetastasenort × Subtyp"** — existiert nicht; TRM publiziert sie nicht | Ignatov 2018 (Magdeburg, regional) als deutsche Näherung 🟢, SEER/Kennecke international | mittel (= K7 des Konzepts, jetzt teilweise geschlossen) |
| **N15** | **ZNS-Metastasen, 2-Jahres-kumulative Inzidenz im frühen Mammakarzinom** — in keiner Quelle separat berichtet | Interpolation Ontario (5/12 J.) ↔ Kennecke (15 J.) 🔴 | niedrig |
| **N16** | **Expliziter Anteil R0-resektabler isolierter LRR** | keine Primärquelle 🔴 | niedrig |
| **N17** | **10-Jahres-RS nach UICC-Stadium für DE** — RKI publiziert stadienspezifisch nur 5 Jahre | TRM-pTNM-Tabelle als Ersatz 🟢 | niedrig |
| **N18** | **Diskrepanz zweier TRM-Tabellen zur kumulativen Fernmetastasierung** (11,0/16,6 % vs. ≈8,4/13,1 %) | `RisikoM0` verwenden, Survival-Tab. 5b als oberen Rand führen (§6.2) | mittel |
| **K0** | **Das Altersband 50–60 selbst** bleibt die größte strukturelle Lücke — sämtliche OnkoZert-Therapiekennzahlen sind **[alle Alter]**, Heinig 2022 ist **[Quelle 50–69]** und aus dem Diagnosejahr 2008 | Konditionierung über das Stadium (§1.2) trägt den Alterseffekt implizit | **hoch** |

**Neu geschlossene oder verkleinerte Konzept-Lücken:**

| Konzept §11 | Status nach Draft C |
|---|---|
| Lücke 9 „monarchE-Anteil … kein deutscher Wert" 🔴 | **geschlossen** — Tübingen **19,4 %**, Ulm+Tübingen **18,1 % monarchE / 43,0 % NATALEE** 🟢 (§4.5). Offen bleibt nur der *Verordnungs*-Uptake |
| Lücke 7 „Metastasenlokalisation für DE/Europa — nur SEER" 🔴 | **teilweise geschlossen** — Ignatov 2018 (n=12.053, DE) 🟢 und Sihto 2011 (FIN, national) 🟢 (§6.4); eine bevölkerungsbezogene deutsche Kreuztabelle „Ort × Subtyp" existiert weiterhin nicht |
| Lücke 4 „Neoadjuvanz-Anteil je Subtyp für 2023" 🔴 | **verkleinert** — Marginale 2023 gemessen 🟢, stadienweise Anteile gemessen 🟢, Alters-Multiplikator 1,28 belegt 🟢; nur die Subtyp-Reskalierung bleibt 🔴, jetzt aber mit Herleitung und Konsistenzprobe (§3.3) |
| Lücke 0 „Altersband 50–60 ist die größte strukturelle Lücke" 🔴 | **verkleinert** — neu hinzugekommen sind altersaufgelöste deutsche Werte für **Chemo-/Neoadjuvanz-Anteil (50–59)**, **pCR je Subtyp (50–59)**, **AI/TAM-Split (51–60)**, **Persistenz-Abbruch-HR (51–60)**, **Lokalrezidiv nach BET±RT (50–59, EBCTCG)**, **Boost-Nutzen (51–60, EORTC)**, **Screening-Mortalitätsrückgang (50–59)** und die Überlebensanker (50–59) 🟢 |

**Draft C liefert damit erstmals einen zusammenhängenden 50–60-Kern** statt nur abgesenkter 50–69-Werte:
Therapieanteile über den Alters-Multiplikator 1,28 bzw. den Verordnungssplit, pCR direkt altersstratifiziert,
Rezidiv- und Überlebensanker direkt altersstratifiziert.

**Für Draft C nicht recherchiert** (liegt in anderen Arbeitspaketen): Screening-Markov-Kette und Detektionsmodus
(`51w`), Subtyp- und Stadienverteilung bei Diagnose (`0m8`), pTNM/Sentinel/pCR-Staging-Mechanik (`98b`),
Terminologie-Validierung (AP-T).

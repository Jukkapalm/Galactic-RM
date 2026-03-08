# ◈ Galactic Resource Management System

Reaaliaikainen galaktinen resurssienhallintasimulaatio. Rakennettu Python · NumPy · Pandas · Streamlit · Plotly.

> **⚠️ Kehitysvaiheessa** - Ohjelma on toimiva mutta resurssitasapainoon ja pelimekaniikkoihin tulossa vielä päivityksiä. Käyttöliittymä vielä vähän kömpelö, mutta tähän tulossa myös päivityksiä.

---

## Ominaisuudet

- **Reaaliaikainen simulaatio** — päivittyy automaattisesti 10 sekunnin välein
- **6 planeettaa** erikoistumisilla: Forest, Volcanic, Ocean, Gas Giant, Trade, Balanced
- **Resurssiriippuvuudet** — energiapula leikkaa tuotantoa, ruoka- ja vesipula vähentävät väestöä
- **Alusjärjestelmä** — Scout, Freighter, Heavy Hauler — lastaus, matka, purku
- **Kaupankäynti** — Mineraalien myynti Mercantisille Crediteiksi
- **Satunnaiset tapahtumat** — planeettatapahtumat, galaktiset tapahtumat, alusrikot
- **Galaktinen kartta** — Plotly-pohjainen interaktiivinen kartta
- **Resurssihistoria** — Plotly-kaavio viimeisistä 60 tickistä
- **Tapahtumaloki** — värikoodattu loki kaikista tapahtumista
- **HUD-tyylinen käyttöliittymä** — avaruusteemalla

---

## Tech Stack

| Kirjasto | Käyttötarkoitus |
|---|---|
| Streamlit | UI ja reaaliaikainen päivitys |
| NumPy | Simulaatiolaskenta vektoreina |
| Pandas | Resurssihistoria |
| Plotly | Kaaviot ja galaktinen kartta |
| streamlit-autorefresh | Automaattinen tick-päivitys |

---

## Roadmap

### Valmis ✅
- Reaaliaikainen simulaatio
- Resurssiriippuvuudet
- HUD-käyttöliittymä
- 6 planeettaa erikoistumisilla
- Galaktinen kartta
- Alusjärjestelmä (Scout, Freighter, Heavy Hauler)
- Mineraalien myynti Mercantisille
- Satunnaiset tapahtumat (planeettatapahtumat, galaktiset tapahtumat, alusrikot)

### Suunnitteilla 🔧
- Käyttöliittymään parannuksia
- Resurssitasapainon hiominen
- Save/Load — pelin tallennus JSON-tiedostoon
- Lisää kauppamekaniikkoja
- Lisää satunnaisia tapahtumia
# ◈ Galactic Resource Management System

Reaaliaikainen galaktinen resurssienhallintasimulaatio. Hallinnoi 6 planeettaa, lähetä aluksia, käy kauppaa ja selviä satunnaisista galaktisista tapahtumista.

> **⚠️ Kehitysvaiheessa** - Ohjelma on toimiva mutta resurssitasapainoon ja pelimekaniikkoihin tulossa vielä päivityksiä. Käyttöliittymä vielä vähän kömpelö, mutta tähän tulossa myös päivityksiä.

**Live demo:** [https://galactic-rm.streamlit.app/]

---

## Ominaisuudet

- **Reaaliaikainen simulaatio** — päivittyy automaattisesti 10 sekunnin välein
- **6 planeettaa** erikoistumisilla: Forest, Volcanic, Ocean, Gas Giant, Trade, Balanced
- **Resurssiriippuvuudet** — energiapula leikkaa tuotantoa, ruoka- ja vesipula vähentävät väestöä
- **Alusjärjestelmä** — Scout, Freighter, Heavy Hauler — lastaus, matka, purku
- **Kaupankäynti** — mineraalien myynti Mercantisille Crediiteiksi
- **Satunnaiset tapahtumat** — planeettatapahtumat, galaktiset tapahtumat, alusrikot
- **Galaktinen kartta** — Plotly-pohjainen interaktiivinen kartta
- **Resurssihistoria** — Plotly-kaavio viimeisistä 60 tickistä
- **Tapahtumaloki** — värikoodattu loki kaikista tapahtumista
- **HUD-tyylinen käyttöliittymä** — avaruusteemalla

---

## Teknologiat

| Kirjasto | Käyttötarkoitus |
|---|---|
| Streamlit | UI ja reaaliaikainen päivitys |
| NumPy | Simulaatiolaskenta vektoreina |
| Pandas | Resurssihistoria |
| Plotly | Kaaviot ja galaktinen kartta |
| streamlit-autorefresh | Automaattinen tick-päivitys |

---

## Rakenne

```
galactic-rms/
├── core/
│   ├── __init__.py
│   ├── game_state.py   # Pelin tilan hallinta (session_state)
│   ├── simulation.py   # Tick-laskenta ja resurssiriippuvuudet (NumPy)
│   ├── ships.py        # Aluslogiikka: rakennus, lastaus, matka, purku
│   └── events.py       # Satunnaiset tapahtumat
├── app.py              # Streamlit UI
├── config.py           # Kaikki vakiot: resurssit, planeetat, alukset, värit
└── requirements.txt
```

---

## Ajaminen paikallisesti

```bash
# Kloonaa repo
git clone https://github.com/Jukkapalm/galactic-rms.git
cd galactic-rms

# Asenna riippuvuudet
pip install -r requirements.txt

# Käynnistä
streamlit run app.py
```

Avaa selaimessa: `http://localhost:8501`

---

## Pelimekaniikka

**Resurssit:** Energy, Minerals, Food, Credits, Water, Population

**Resurssiriippuvuudet:**
- Energiapula → Minerals ja Food tuotanto -50%
- Ruoka- tai vesipula → väestö vähenee 20 per tick
- Väestö vaikuttaa kaikkeen tuotantoon (puolet väestöstä = puolet tuotannosta)

**Alukset:**
| Alus | Nopeus | Kapasiteetti | Hinta |
|---|---|---|---|
| Scout | 15 AU/tick | 100 | 150 Credits + 50 Minerals |
| Freighter | 8 AU/tick | 500 | 300 Credits + 150 Minerals |
| Heavy Hauler | 4 AU/tick | 1500 | 600 Credits + 300 Minerals |

**Kauppa:** Mineraaleja voi myydä Mercantisille kursilla 2x Credits

---

## Roadmap

### Valmis ✅
- Reaaliaikainen simulaatio
- Resurssiriippuvuudet
- HUD-käyttöliittymä
- 6 planeettaa erikoistumisilla
- Galaktinen kartta
- Alusjärjestelmä
- Mineraalien myynti Mercantisille
- Satunnaiset tapahtumat

### Suunnitteilla 🔧
- Käyttöliittymän parannuksia
- Resurssitasapainon hiominen
- Save/Load — pelin tallennus JSON-tiedostoon
- Lisää kauppamekaniikkoja
- Lisää satunnaisia tapahtumia
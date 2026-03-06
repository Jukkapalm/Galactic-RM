# ◈ Galactic Resource Management System

Reaaliaikainen galaktinen resurssienhallintasimulaatio. Rakennettu Python · NumPy · Pandas · Streamlit · Plotly.

---

## Ominaisuudet

- Reaaliaikainen simulaatio - päivittyy automaattisesti 10 sekunnin välein

- 6 resurssia: Energia, Mineraalit, Ruoka, Krediitit, Tutkimus, Populaatio

- Resurssiriippuvuudet: energiapula leikkaa tuotantoa, ruokapula vähentää väestöä

- Resurssihistoria Plotly-kaaviossa

- Tapahtumaloki sidebarissa

- HUD-tyylinen terminaalikäyttöliittymä

---

## Tech Stack

| | Käyttötarkoitus |
|---|---|
| Streamlit | UI ja reaaliaikaine päivitys |
| NumPy | Simulaatiolaskenta vektoreina |
| Pandas | Resurssihistoria |
| Plotly | Kaaviot |
| Streamlit-autorefresh | Automaattinen päivitys |

---

## Roadmap

- [x] Reaaliaikainen simulaatio
- [x] Resurssiriippuvuudet
- [x] HUD-UI
- [ ] Resurssisiirrot planeettojen välillä
- [ ] Alustenhallinta
- [ ] Useampia planeettoja
- [ ] Satunnaiset tapahtumat
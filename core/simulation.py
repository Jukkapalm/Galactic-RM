# Tämä tiedosto sisältää kaiken laskentalogiikan
# Sisältää milloin tick etenee
# Miten resurssit muuttuvat per tick
# Resurssiriippuvuudet
# NumPy hoitaa resurssien laskemisen tehokkaasti vektoreina
# sen sijaan että laskettaisiin yksi resurssi kerrallaan

import time
import numpy as np
import streamlit as st

from config import (
    RESOURCE_NAMES, TICK_INTERVAL_SECONDS,
    CRITICAL_THRESHOLDS,
)
from core.game_state import (
    get_last_tick_time, advance_tick, add_event,
)

# Pääfunktio - kutsutaan app.py:stä joka renderissä
def maybe_advance_tick() -> bool:
    # Tarkistaa onko TICK_INTERVAL_SECONDS kulunut edellisestä tickistä
    # Jos on, suorittaa yhden tick-päivityksen ja palauttaa True
    # Jos ei ole, ei tee mitään ja palauttaa False
    elapsed = time.time() - get_last_tick_time()
    if elapsed >= TICK_INTERVAL_SECONDS:
        _run_tick()
        return True
    return False

def _run_tick() -> None:
    # Päivitetään kaikki planeetat joka tickillä
    for planet in st.session_state.planets.values():
        _update_planet(planet)
    advance_tick()

def _update_planet(planet: dict) -> None:
    
    res = planet["resources"]
    prod = planet["production"]
    cons = planet["consumption"]
    stor = planet["storage"]

    # Väestokerroin: puolet väestöstä = puolet tuotannosta
    base_pop = 1200.0
    pop_modifier = max(0.1, min(2.0, res["Population"] / base_pop))

    # Energiakerroin: energiapula puolittaa mineraali- ja ruokatuotannon
    energy_ok = res["Energy"] >= CRITICAL_THRESHOLDS["Energy"]
    energy_mod = 1.0 if energy_ok else 0.5

    # NumPy-vektorit laskentaan
    prod_arr = np.array([prod[r] for r in RESOURCE_NAMES], dtype=float)
    cons_arr = np.array([cons[r] for r in RESOURCE_NAMES], dtype=float)
    res_arr  = np.array([res[r]  for r in RESOURCE_NAMES], dtype=float)
    stor_arr = np.array([stor[r] for r in RESOURCE_NAMES], dtype=float)

    # Väestökerroin kaikkeen tuotantoon
    prod_arr *= pop_modifier

    # Energiakerroin vain Mineraalit ja Ruoka
    prod_arr[RESOURCE_NAMES.index("Minerals")] *= energy_mod
    prod_arr[RESOURCE_NAMES.index("Food")]     *= energy_mod

    # Nettolaskenta ja varastoon rajaus
    new_arr = np.clip(res_arr + (prod_arr - cons_arr), 0.0, stor_arr)

    # Ruokapula: väestö vähenee
    food_idx = RESOURCE_NAMES.index("Food")
    water_idx = RESOURCE_NAMES.index("Water")
    pop_idx = RESOURCE_NAMES.index("Population")
    food_critical = new_arr[food_idx] < CRITICAL_THRESHOLDS["Food"]
    water_critical = new_arr[water_idx] < CRITICAL_THRESHOLDS["Water"]

    # Ruokapula: väestö vähenee 20 per tick
    if food_critical:
        new_arr[pop_idx] = max(0.0, new_arr[pop_idx] - 20)
        add_event(f"Nälänhätä {planet['name']} — väestö vähenee!", "danger")

    # Vesipula: väestö vähenee 20 per tick (kumulatiivinen ruokapulan kanssa)
    if water_critical:
        new_arr[pop_idx] = max(0.0, new_arr[pop_idx] - 20)
        add_event(f"Vesipula {planet['name']} - väestö vähenee!", "danger")

    # Energiapula: varoitus lokiin
    if not energy_ok:
        add_event(f"Energiapula {planet['name']} — Minerals & Food tuotanto -50%", "warning")

    # Kirjoitetaan uudet arvot takaisin sanakirjaan
    for i, r in enumerate(RESOURCE_NAMES):
        res[r] = round(float(new_arr[i]), 1)
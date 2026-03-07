# Pelin tilan hallinta
# Kaikki pelin data tallennetaan Streamlitin session_stateen

import time
import copy
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime

from config import (
    STARTING_YEAR, RESOURCE_NAMES, STARTING_RESOURCES,
    BASE_PRODUCTION, BASE_CONSUMPTION, STORAGE_MAX,
    HISTORY_MAX_TICKS, CRITICAL_THRESHOLDS,
    TICK_INTERVAL_SECONDS, PLANET_TYPES,
)

# Sisäinen apufunktio - luo yhden planeetan sanakirjarakenteena
def _create_planet(name:str, ptype: str, is_capital: bool, coords: dict) -> dict:
    # Soveltaa planeettatyypin bonukset perustuotantoon
    bonuses = PLANET_TYPES[ptype]["bonuses"]
    rng = np.random.default_rng()

    # Pienet satunnaisvaihtelut alkuresursseissa (+-10%)
    resources = {
        res: int(STARTING_RESOURCES[res] * rng.uniform(0.90, 1.10))
        for res in RESOURCE_NAMES
    }
    # Tuotanto = perus x tyyppibonus
    production = {
        res: round(BASE_PRODUCTION[res] * bonuses.get(res, 1.0), 1)
        for res in RESOURCE_NAMES
    }
    return {
       "name": name,
       "type": ptype,
       "color": PLANET_TYPES[ptype]["color"],
       "is_capital":  is_capital,
       "coords":      coords,
       "resources":   resources,
       "production":  production,
       "consumption": copy.deepcopy(BASE_CONSUMPTION),
       "storage":     copy.deepcopy(STORAGE_MAX),
    }

# Pelin alustus
def init_game() -> None:
    # Alustaa pelin session_stateen
    # Tarkistetaan onko peli jo alustettu - jos on, poistutaan heti
    if st.session_state.get("initialized"):
        return
    
    # Merkitään alustetuksi niin ettei ajeta uudelleen
    st.session_state.initialized = True
    st.session_state.tick = 0
    st.session_state.year = STARTING_YEAR
    st.session_state.last_tick_time = time.time()

    # Luodaan planeetat sanakirjaan
    # Avain on planeetan nimi, arvo on planeetan data
    st.session_state.planets = {
        "Terra Nova": _create_planet("Terra Nova", "Forest", True,  {"x": 0.0,  "y": 0.0}),
        "Pyros":      _create_planet("Pyros",      "Volcanic", False, {"x": 38.0, "y": -22.0}),
        "Aquatica":   _create_planet("Aquatica",   "Ocean",     False, {"x": -25.0, "y":  30.0}),
        "Helios":     _create_planet("Helios",     "Gas Giant", False, {"x":  55.0, "y":  40.0}),
        "Mercantis":  _create_planet("Mercantis",  "Trade",     False, {"x": -45.0, "y": -15.0}),
        "Nexus":      _create_planet("Nexus",      "Balanced",  False, {"x":  10.0,  "y": -50.0}),
    }

    # Valittu planeetta - oletuksena pääkaupunki
    st.session_state.selected_planet = "Terra Nova"

    # Aluslista - jokainen alus on sanakirja
    st.session_state.ships = []

    # Resurssihistoria (Pandas DataFrame)
    # Tallennetaan jokaisen tick resurssiarvot kaaviota varten
    st.session_state.history = pd.DataFrame(columns=[
        "tick", "year", "planet", "resource", "value"
    ])

    # Tapahtumaloki
    # Lista sanakirjoja - uusin tapahtuma ensin (insert kohtaan 0)
    st.session_state.event_log = []

    _save_to_history()
    add_event("Siirtokunta perustettu. Kaikki järjestelmät toiminnassa.", "success")


# Historia - sisäinen apufunktio
def _save_to_history() -> None:
    # Ottaa tilannekuvan nykyisistä resursseista ja lisää DataFrameen
    # Kutsutaan jokaisen tickin lopussa automaattisesti
    tick = st.session_state.tick
    year = st.session_state.year
    rows = []

    # Käydään kaikki planeetat läpi
    for planet in st.session_state.planets.values():
        for resource, value in planet["resources"].items():
            rows.append({
                "tick": tick,
                "year": year,
                "planet": planet["name"],
                "resource": resource,
                "value": float(value),
            })

    # Lisätään uudet rivit olemassaolevaan DataFrameen
    new_df = pd.DataFrame(rows)
    st.session_state.history = pd.concat(
        [st.session_state.history, new_df], ignore_index=True
    )

    # Rajoitetaan historian koko - poistetaan vanhimmat rivit tarvittaessa
    max_rows = HISTORY_MAX_TICKS * len(RESOURCE_NAMES) * len(st.session_state.planets)
    if len(st.session_state.history) > max_rows:
        st.session_state.history = st.session_state.history.iloc[-max_rows:]

# Julkiset lukufunktiot - muut tiedosto käyttävät näitä
def get_planet(name: str = None) -> dict:
    # Jos nimi annetaan, palauttaa sen planeetan
    # Muutoin palauttaa valitun planeetan
    if name:
        return st.session_state.planets[name]
    return st.session_state.planets[st.session_state.selected_planet]

def get_all_planets() -> dict:
    return st.session_state.planets

def get_selected_planet() -> str:
    return st.session_state.selected_planet

def set_selected_planet(name: str) -> None:
    st.session_state.selected_planet = name

def get_ships() -> list:
    return st.session_state.ships

def get_tick() -> int:
    # Palauttaa nykyisen tick-numeron
    return st.session_state.tick

def get_year() -> int:
    # Palauttaa nykyisen galaktisen vuoden
    return st.session_state.year

def get_event_log() -> list:
    # Palauttaa tapahtumalistan - uusin ensin
    return st.session_state.event_log

def get_history(resource: str) -> pd.DataFrame:
    # Palauttaa resurssin historian valitulle planeetalle
    planet_name = st.session_state.selected_planet
    df = st.session_state.history
    mask = (df["resource"] == resource) & (df["planet"] == planet_name)
    return df[mask][["tick", "value"]].copy()

def time_until_next_tick() -> float:
    # Palauttaa sekunnit seuraavaan automaattiseen tickiin
    elapsed = time.time() - st.session_state.last_tick_time
    return max(0.0, TICK_INTERVAL_SECONDS - elapsed)

def get_last_tick_time() -> float:
    return st.session_state.last_tick_time

# Julkiset kirjoitusfunktiot
def add_event(message: str, severity: str = "info") -> None:
    # Lisää tapahtumalokiin
    # Severity-arvot: "info" | "warning" | "danger" | "success"
    st.session_state.event_log.insert(0, {
        "tick":      st.session_state.tick,
        "year":      st.session_state.year,
        "time":      datetime.now().strftime("%H:%M:%S"),
        "message":   message,
        "severity":  severity,
    })
    # Pidetään loki enintään 50 tapahtumassa
    st.session_state.event_log = st.session_state.event_log[:50]

def advance_tick() -> None:
    # Kasvattaa tick- ja vuosilaskuria yhdellä.
    # Tallentaa nykyisen tilanteen historiaan
    # Kutsutaan simulaation.py:stä tick-laskennan jälkeen
    st.session_state.tick += 1
    st.session_state.year += 1
    st.session_state.last_tick_time = time.time()
    _save_to_history()
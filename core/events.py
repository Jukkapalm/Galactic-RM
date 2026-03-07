# Satunnaiset tapahtumat
# Joka tick on 15% mahdollisuus tapahtumalle
# Tapahtumat jaetaan kolmeen kategoriaan:
# - Planeettatapahtumat (vaikuttaa yhteen planeettaan)
# - Alusrikot (vaikuttaa matkalla olevaan alukseen)
# - Galaktiset tapahtumat (vaikuttaa kaikkiin)

import random
import streamlit as st

from core.game_state import add_event

# Todennäköisyys tapahtumalle per tick (0.0 - 1.0)
EVENT_CHANCE = 0.15

# Tapahtumien painot - suurempiluku = todennäköisempi
# Positive 40%, negative 60%
PLANET_EVENTS = [
    # (paino, kuvaus, resurssi, muutos)
    (10, "Aurinkomyrsky", "Energy", +500),
    (8,  "Mineraalisuoni", "Minerals", +300),
    (6,  "Poikkeuksellinen sato","Food", +400),
    (6,  "Vesisade", "Water", +300),
    (12, "Sato epäonnistui", "Food", -200),
    (10, "Kuivuus", "Water", -200),
    (8,  "Epidemia", "Population", -100),
    (8,  "Energiaverkon häiriö", "Energy", -300),
    (6,  "Kaivosromahdus", "Minerals", -200),
]

GALACTIC_EVENTS = [
    # (paino, kuvaus, resurssi, muutos per planeetta)
    (8,  "Galaktinen kauppasopimus", "Credits", +200),
    (6,  "Kosminen säteily",         "Energy",  -150),
]

def maybe_trigger_event() -> None:
    # Arvotaan joka tick tapahtuuko event
    if random.random() > EVENT_CHANCE:
        return
    
    # Valitaan kategoria painotetusti
    # Alustapahtumat vain jos aluksia matkalla
    travelling = [s for s in st.session_state.ships if s["status"] == "travelling"]

    # Kategorian painot
    cat_weights = [5, 3] # Planeetta, galaktinen
    categories = ["planet", "galactic"]

    if travelling:
        cat_weights.append(2)
        categories.append("ship")

    category = random.choices(categories, weights=cat_weights, k=1)[0]

    if category == "planet":
        _trigger_planet_event()
    elif category == "galactic":
        _trigger_galactic_event()
    elif category == "ship":
        _trigger_ship_event(travelling)

def _trigger_planet_event() -> None:
    # Valitaan satunnainen planeetta ja taphtuma
    planet_name = random.choice(list(st.session_state.planets.keys()))
    planet = st.session_state.planets[planet_name]

    weights = [e[0] for e in PLANET_EVENTS]
    event = random.choices(PLANET_EVENTS, weights=weights, k=1)[0]
    _, desc, resource, delta = event

    # Sovelletaan muutos - ei mennä alle 0 tai yli varaston
    current = planet["resources"].get(resource, 0)
    maximum = planet["storage"].get(resource, 999999)
    planet["resources"][resource] = max(0.0, min(current + delta, maximum))

    sign = "+" if delta > 0 else ""
    severity = "success" if delta > 0 else "warning"
    add_event(
        f"{desc} — {planet_name}: {resource} {sign}{delta}",
        severity
    )

def _trigger_galactic_event() -> None:
    # Vaikuttaa kaikkiin planeettoihin
    weights = [e[0] for e in GALACTIC_EVENTS]
    event = random.choices(GALACTIC_EVENTS, weights=weights, k=1)[0]
    _, desc, resource, delta = event

    for planet in st.session_state.planets.values():
        current = planet["resources"].get(resource, 0)
        maximum = planet["storage"].get(resource, 999999)
        planet["resources"][resource] = max(0.0, min(current + delta, maximum))

    sign     = "+" if delta > 0 else ""
    severity = "success" if delta > 0 else "warning"
    add_event(
        f"GALAKTINEN: {desc} — kaikki planeetat: {resource} {sign}{delta}",
        severity
    )

def _trigger_ship_event(travelling: list) -> None:
    # Valitaan satunnainen matkalla oleva alus
    ship = random.choice(travelling)

    # Kolme mahdollista alustapahtumaa
    roll = random.random()

    if roll < 0.40:
        # Moottorihäiriö - matka-aika +3 tickiä
        ship["ticks_left"] += 3
        add_event(
            f"Moottorihäiriö — {ship['id']} viivästyy 3 tickiä",
            "warning"
        )

    elif roll < 0.70:
        # Asteroidi osuma - alus tuhoutuu
        st.session_state.ships.remove(ship)
        cargo_str = ", ".join(
            f"{v} {r}" for r, v in ship["cargo"].items()
        ) if ship["cargo"] else "ei kuormaa"
        add_event(
            f"ASTEROIDIOSUMA — {ship['id']} tuhoutunut! ({cargo_str} menetetty)",
            "danger"
        )

    else:
        # Väijytys - alus palaa tyhjänä lähtöplaneetalle
        origin = ship["location"]
        ship["cargo"] = {}
        ship["destination"] = origin
        ship["ticks_left"] = max(1, ship["ticks_left"])
        add_event(
            f"VÄIJYTYS — {ship['id']} ryöstetty, palaa {origin}:lle tyhjänä",
            "danger"
        )
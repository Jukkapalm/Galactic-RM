# Aluslogiikka
# Rakentaminen, lastaus, matka, purku
# Jokainen alus on sanakirja session_state.ships listassa

import math
import streamlit as st

from config import SHIP_TYPES, RESOURCE_NAMES
from core.game_state import add_event

# Apufunktio - laskee etäisyyden kahden planeetan välillä (AU)
def calc_distance(planet_a: dict, planet_b: dict) -> float:
    dx = planet_a["coords"]["x"] - planet_b["coords"]["x"]
    dy = planet_a["coords"]["y"] - planet_b["coords"]["y"]
    return math.sqrt(dx * dx + dy * dy)

# Apufunktio - laskee matka-ajan tickeinä
def calc_travel_ticks(planet_a: dict, planet_b: dict, ship_type: str) -> int:
    dist = calc_distance(planet_a, planet_b)
    speed = SHIP_TYPES[ship_type]["speed_au_per_tick"]
    return max(1, math.ceil(dist/ speed))

# Rakenna uusi alus - vähennetään resurssit ja lisätään listaan
def build_ship(ship_type: str, home_planet: str) -> bool:
    # Tarkistaa onko Credits ja Minerals riittävästi
    # Jos riittää, niin rakentaa aluksen ja palauttaa True
    cost_c = SHIP_TYPES[ship_type]["cost_credits"]
    cost_m = SHIP_TYPES[ship_type]["cost_minerals"]
    planet = st.session_state.planets[home_planet]

    if planet["resources"]["Credits"] < cost_c:
        add_event(f"Ei tarpeeksi Crediittejä - {ship_type} vaatii {cost_c}", "warning")
        return False
    if planet["resources"]["Minerals"] < cost_m:
        add_event(f"Ei tarpeeksi mineraaleja - {ship_type} vaatii {cost_m}", "warning")
        return False
    
    # Vähennetään resurssikustannukset
    planet["resources"]["Credits"] -= cost_c
    planet["resources"]["Minerals"] -= cost_m

    # Luodaan uusi alus
    ship_id = f"{ship_type[:2].upper()}-{len(st.session_state.ships) + 1:03d}"
    st.session_state.ships.append({
        "id": ship_id,
        "type": ship_type,
        "status": "idle",
        "location": home_planet,
        "destination": None,
        "cargo": {},
        "ticks_left": 0,
    })

    add_event(f"Alus {ship_id} rakennettu {home_planet}:lla", "success")
    return True

# Aloita lastaus - asettaa aluksen loading-tilaan
def start_loading(ship_id: str, resource: str, amount: int) -> bool:
    ship = _get_ship(ship_id)
    planet = st.session_state.planets[ship["location"]]

    if planet["resources"].get(resource, 0) < amount:
        add_event(f"{ship_id}: Ei tarpeeksi {resource} lastaukseen", "warning")
        return False
    
    cap = SHIP_TYPES[ship["type"]]["cargo_capacity"]
    if amount > cap:
        add_event(f"{ship_id}: Kuorma ylittää kapasiteetin {cap}", "warning")
        return False
    
    # Vähennetään resurssi planeetalta ja lastataan alukseen
    planet["resources"][resource] -= amount
    ship["cargo"] = {resource: amount}
    ship["status"] = "loading"
    ship["ticks_left"] = SHIP_TYPES[ship["type"]]["load_ticks"]

    add_event(f"{ship_id} lastaa {amount} {resource} ({ship['ticks_left']} tickiä)", "info")
    return True

# Lähetä alus matkaan - kutsutaan kun lastaus valmis
def dispatch_ship(ship_id: str, destination: str) -> bool:
    ship = _get_ship(ship_id)

    if ship["status"] not in ("idle", "loading"):
        add_event(f"{ship_id}: Ei voi lähettää, status={ship['status']}", "warning")
        return False
    
    origin = st.session_state.planets[ship["location"]]
    dest = st.session_state.planets[destination]
    ticks = calc_travel_ticks(origin, dest, ship["type"])
    dist = round(calc_distance(origin, dest), 1)

    ship["destination"] = destination
    ship["status"] = "travelling"
    ship["ticks_left"] = ticks
    
    add_event(
        f"{ship_id} lähtee {ship['location']} → {destination} "
        f"({dist} AU, {ticks} tickiä)", "info"
    )
    return True

# Tick-päivitys kaikille aluksille - kutsutaan simulation.py:stä
def update_ships() -> None:
    for ship in st.session_state.ships:
        if ship["ticks_left"] > 0:
            ship["ticks_left"] -= 1

        # Lastaus valmis - odottaa lähetyskäskyä
        if ship["status"] == "loading" and ship["ticks_left"] == 0:
            ship["status"] = "idle"
            add_event(f"{ship['id']} lastaus valmis - valmis lähtöön", "info")

        # Matka valmis - akoitetaan purku automaattisesti
        elif ship["status"] == "travelling" and ship["ticks_left"] == 0:
            ship["location"] = ship["destination"]
            ship["destination"] = None
            ship["status"] = "unloading"
            ship["ticks_left"] = SHIP_TYPES[ship["type"]]["unload_ticks"]
            add_event(f"{ship['id']} saapui {ship['location']}", "success")

        # Purku valmis
        elif ship["status"] == "unloading" and ship["ticks_left"] == 0:
            planet = st.session_state.planets[ship["location"]]
            for resource, amount in ship["cargo"].items():
                current = planet["resources"].get(resource, 0)
                maximum = planet["storage"].get(resource, 999999)
                planet["resources"][resource] = min(current + amount, maximum)
            add_event(
                f"{ship['id']} purki kuorman {ship['location']}:lle", "success"
            )
            ship["cargo"] = {}
            ship["status"] = "idle"

# Sisäinen apufunktio - hakee aluksen id:llä
def _get_ship(ship_id: str) -> dict:
    for ship in st.session_state.ships:
        if ship["id"] == ship_id:
            return ship
    raise ValueError(f"Alusta ei löydy: {ship_id}")
# Kaikki vakiot ja asetukset
# Täällä voi muuttaa värejä, resursseja tai peliarvoja

# Pelin perustiedot
GAME_VERSION = "2.0.0"
STARTING_YEAR = 2450

# Simulaation nopeus
# Kuinka monen sekunnin välein simulaatio päivittyy automaattisesti
TICK_INTERVAL_SECONDS = 10

# Resurssit
# Resurssien nimet järjestyksessä - sama järjestys kaikkiallla koodissa
RESOURCE_NAMES = ["Energy", "Minerals", "Food", "Credits", "Water", "Population"]

# Väri jokaiselle resurssille - käytetään korteissa ja kaavioissa
RESOURCE_COLORS = {
    "Energy":     "#FFD700", # keltainen
    "Minerals":   "#A8B8C8", # hopea
    "Food":       "#4CAF50", # vihreä
    "Credits":    "#FFA500", # kulta
    "Water":   "#4Fc3F7", # vaaleansininen
    "Population": "#B0BEC5", # valkoinen/harmaa
}

# Kriittinen raja - jos resurssi putoaa alle tämän, tulee varoitus ja seurauksia
CRITICAL_THRESHOLDS = {
    "Energy":     100, # alle tämän, minerals & ruoka tuotanto puolittuu
    "Minerals":   50,  # alle tämän, aluksia ei voi rakentaa
    "Food":       100, # alle tämän, väestö alkaa vähentyä
    "Credits":    0,
    "Water":      100,
    "Population": 50,  # alle tämän, kaikki tuotanto romahtaa
}

# Planeettatyyppien tuotantobonukset
# Kerroin joka vaikuttaa perustuotantoon (1.0 = ei muutosta)
PLANET_TYPES = {
    "Forest": {
        "color": "#208040",
        "bonuses": {"Food": 2.0, "Water": 1.2, "Energy": 0.8, "Minerals": 0.5, "Credits": 0.0},
    },
    "Volcanic": {
        "color": "#FF6030",
        "bonuses": {"Minerals": 2.5, "Energy": 1.5, "Food": 0.1, "Water": 0.1, "Credits": 0.0},
    },
    "Ocean": {
        "color":   "#1A8FD1",
        "bonuses": {"Water": 2.0, "Food": 1.2, "Energy": 0.7, "Minerals": 0.3, "Credits": 0.0},
    },
    "Gas Giant": {
        "color":   "#C87030",
        "bonuses": {"Energy": 3.0, "Minerals": 1.2, "Food": 0.1, "Water": 0.1, "Credits": 0.0},
    },
    "Trade": {
        "color":   "#D4AF37",
        "bonuses": {"Credits": 3.0, "Food": 0.5, "Water": 0.5, "Minerals": 0.4, "Energy": 0.8},
    },
    "Balanced": {
        "color":   "#7A9AAA",
        "bonuses": {"Energy": 0.8, "Minerals": 0.8, "Food": 0.8, "Water": 0.8, "Credits": 0.0},
    },
}

# Planeetan alkuarvot
# Resurssimäärät kun peli alkaa
STARTING_RESOURCES = {
    "Energy":     600,
    "Minerals":   400,
    "Food":       500,
    "Credits":    1200,
    "Water":   150,
    "Population": 1200,
}

# Perustuotanto per tick - ennen minkäänlaista bonuksia tai miinuksia
BASE_PRODUCTION = {
    "Energy":     50,
    "Minerals":   30,
    "Food":       40,
    "Credits":    20,
    "Water":   10,
    "Population": 5,
}

# Peruskulutus per tick
BASE_CONSUMPTION = {
    "Energy":     30,
    "Minerals":   15,
    "Food":       35,
    "Credits":    10,
    "Water":   0,
    "Population": 0,
}

# Maksimimäärä resursseja varastossa
STORAGE_MAX = {
    "Energy":     8000,
    "Minerals":   8000,
    "Food":       8000,
    "Credits":    999999,
    "Water":   999999,
    "Population": 999999,
}



# UI-värit
COLOR_BG           = "#05070F"   # sivun tausta — lähes musta avaruus
COLOR_PANEL        = "#0B1527"   # kortit ja paneelit — syvänsininen
COLOR_SIDEBAR      = "#0D1A30"   # sivupalkki
COLOR_BORDER       = "#2A3A4A"   # reunaviivat — teräksen harmaa
COLOR_TEXT_DIM     = "#4A6A8A"   # toissijainen teksti
COLOR_TEXT         = "#8AAAC8"   # normaali teksti
COLOR_TEXT_BRIGHT  = "#C8E8FF"   # korostettu teksti
COLOR_ALERT        = "#FF3333"   # hälytys / resurssipula
COLOR_SUCCESS      = "#00FF88"   # positiivinen tapahtuma
COLOR_WARNING      = "#FFB300"   # varoitus

# Resurssihistoria
# Miten monta tickiä historiasta säilytetään kaaviota varten
HISTORY_MAX_TICKS = 60
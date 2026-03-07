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
RESOURCE_NAMES = ["Energy", "Minerals", "Food", "Credits", "Research", "Population"]

# Väri jokaiselle resurssille - käytetään korteissa ja kaavioissa
RESOURCE_COLORS = {
    "Energy":     "#FFD700", # keltainen
    "Minerals":   "#A8B8C8", # hopea
    "Food":       "#4CAF50", # vihreä
    "Credits":    "#FFA500", # kulta
    "Research":   "#00BCD4", # cyan
    "Population": "#B0BEC5", # valkoinen/harmaa
}

# Kriittinen raja - jos resurssi putoaa alle tämän, tulee varoitus ja seurauksia
CRITICAL_THRESHOLDS = {
    "Energy":     100, # alle tämän, minerals & ruoka tuotanto puolittuu
    "Minerals":   50,  # alle tämän, aluksia ei voi rakentaa
    "Food":       100, # alle tämän, väestö alkaa vähentyä
    "Credits":    0,
    "Research":   0,
    "Population": 50,  # alle tämän, kaikki tuotanto romahtaa
}

# Planeettatyyppien tuotantobonukset
# Kerroin joka vaikuttaa perustuotantoon (1.0 = ei muutosta)
PLANET_TYPES = {
    "Forest": {
        "color": "#208040",
        "bonuses": {"Food": 1.4, "Research": 1.3, "Energy": 0.9},
    },
    "Volcanic": {
        "color": "#FF6030",
        "bonuses": {"Minerals": 1.6, "Energy": 1.3, "Food": 0.4},
    },
    "Ocean": {
        "color":   "#1A8FD1",
        "bonuses": {"Food": 1.5, "Credits": 1.4, "Minerals": 0.4, "Energy": 0.8},
    },
    "Gas Giant": {
        "color":   "#C87030",
        "bonuses": {"Energy": 2.5, "Minerals": 1.2, "Food": 0.1, "Population": 0.3},
    },
    "Trade": {
        "color":   "#D4AF37",
        "bonuses": {"Credits": 2.5, "Research": 1.3, "Minerals": 0.5, "Food": 0.6},
    },
    "Balanced": {
        "color":   "#7A9AAA",   # harmaan sininen
        "bonuses": {"Energy": 1.0, "Minerals": 1.0, "Food": 1.0,
                    "Credits": 1.0, "Research": 1.0, "Population": 1.0},
    },
}

# Planeetan alkuarvot
# Resurssimäärät kun peli alkaa
STARTING_RESOURCES = {
    "Energy":     600,
    "Minerals":   400,
    "Food":       500,
    "Credits":    1200,
    "Research":   150,
    "Population": 1200,
}

# Perustuotanto per tick - ennen minkäänlaista bonuksia tai miinuksia
BASE_PRODUCTION = {
    "Energy":     50,
    "Minerals":   30,
    "Food":       40,
    "Credits":    20,
    "Research":   10,
    "Population": 5,
}

# Peruskulutus per tick
BASE_CONSUMPTION = {
    "Energy":     30,
    "Minerals":   15,
    "Food":       35,
    "Credits":    10,
    "Research":   0,
    "Population": 0,
}

# Maksimimäärä resursseja varastossa
STORAGE_MAX = {
    "Energy":     8000,
    "Minerals":   8000,
    "Food":       8000,
    "Credits":    999999,
    "Research":   999999,
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
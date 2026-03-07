# Pääsovellus. Käynnistä komennolla: streamlit run app.py
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from config import (
    GAME_VERSION, TICK_INTERVAL_SECONDS,
    RESOURCE_NAMES, RESOURCE_COLORS, CRITICAL_THRESHOLDS,
    COLOR_BG, COLOR_PANEL, COLOR_SIDEBAR, COLOR_BORDER,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_TEXT_BRIGHT,
    COLOR_ALERT, COLOR_SUCCESS, COLOR_WARNING,
)
from core.game_state import (
    init_game, get_planet, get_all_planets,
    get_selected_planet, set_selected_planet,
    get_tick, get_year, get_event_log, 
    get_history, time_until_next_tick,
)
from core.simulation import maybe_advance_tick

# Sivun perusasetukset - oltava sivun ensimmäinen Streamlit-kutsu
st.set_page_config(
    page_title = "GALACTIC RM",
    page_icon = "◈",
    layout = "wide",
    initial_sidebar_state = "expanded",
)

# CSS - HUD
# Määritykset koko sovelluksen visuaaliselle ilmeelle
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600&display=swap');

/* Sivun tausta ja perusfontti */
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {COLOR_BG};
    color: {COLOR_TEXT};
    font-family: 'Rajdhani', sans-serif;
}}

/* Pääsisältöalue */
[data-testid="stMain"] {{
    background-color: {COLOR_BG};
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {COLOR_SIDEBAR};
    border-right: 1px solid {COLOR_BORDER};
}}

/* Otsikot */
h1, h2, h3 {{
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 3px;
    color: {COLOR_TEXT_BRIGHT};
}}

/* Napit */
.stButton > button {{
    background-color: {COLOR_PANEL};
    color: {COLOR_TEXT_BRIGHT};
    border: 1px solid {COLOR_BORDER};
    border-radius: 0;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
    font-size: 12px;
    transition: border-color 0.15s;
}}
.stButton > button:hover {{
    border-color: {COLOR_TEXT_BRIGHT};
    color: #FFFFFF;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background-color: {COLOR_PANEL} !important;
    color: {COLOR_TEXT_BRIGHT} !important;
    border: 1px solid {COLOR_BORDER} !important;
    border-radius: 0 !important;
    font-family: 'Rajdhani', sans-serif !important;
}}

/* Divider */
hr {{ border-color: {COLOR_BORDER} !important; }}

/* Kaavioiden kehys */
.js-plotly-plot {{ border: 1px solid {COLOR_BORDER}; }}

/* Piilotetaan sidebarin piilotusnappi kokonaan */
[data-testid="collapsedControl"] {{
    display: none !important;
}}

</style>
""", unsafe_allow_html=True)

# Alustus ja automaattinen päivitys
# Alustetaan peli
init_game()

# Automaattinen uudelleenlataus millisekunteina
st_autorefresh(interval=TICK_INTERVAL_SECONDS * 1000, key="autorefresh")

# Tarkistetaan onko aika edetä tickissä - jos on, ajetaan yksi simulaatiolaskelma
maybe_advance_tick()

# Sidebar
with st.sidebar:
    #Otsikko
    st.markdown(
        f"<div style='font-family:Rajdhani; letter-spacing:4px; font-size:18px; "
        f"color:{COLOR_TEXT_BRIGHT}; padding:8px 0'>◈ GALACTIC RM</div>"
        f"<div style='color:{COLOR_TEXT_DIM}; font-size:10px; "
        f"letter-spacing:2px; margin-bottom:12px'>v{GAME_VERSION}</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Simulaation tila
    st.markdown(
        f"<div style='font-size:11px; color:{COLOR_TEXT_DIM}; "
        f"letter-spacing:2px; margin-bottom:6px'>SIMULAATIO</div>"
        f"<div style='font-size:13px; color:{COLOR_TEXT}; margin-bottom:2px'>"
        f"TICK: <span style='color:{COLOR_TEXT_BRIGHT}'>{get_tick()}</span><br>"
        f"VUOSI: <span style='color:{COLOR_TEXT_BRIGHT}'>{get_year()} GE</span><br>"
        f"<span style='color:{COLOR_TEXT_DIM}; font-size:11px'>"
        f"Seuraava päivitys: {time_until_next_tick():.0f}s</span></div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Planeettavalinta - nappi per planeetta
    st.markdown(
        f"<div style='font-size:11px; color:{COLOR_TEXT_DIM}; "
        f"letter-spacing:2px; margin-bottom:6px'>PLANEETTA</div>",
        unsafe_allow_html=True,
    )
    for pname, pdata in get_all_planets().items():
        is_sel = pname == get_selected_planet()
        hq_mark = " [HQ]" if pdata["is_capital"] else ""

        # Valitun planeetan reunaviiva on planeetan oma väri
        border = pdata["color"] if is_sel else COLOR_BORDER
        st.markdown(
            f"<div style='border-left:2px solid {border}; "
            f"padding-left:6px; margin-bottom:2px'>",
            unsafe_allow_html=True,
        )
        if st.button(f"{pname}{hq_mark}", key=f"btn_{pname}"):
            set_selected_planet(pname)
            st.rerun()
        # Planeetan tyyppi planeetan omalla värillä
        st.markdown(
            f"<div style='color:{pdata['color']}; font-size:11px; "
            f"margin-left:4px; margin-bottom:4px'>{pdata['type']}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.divider()

    # Tapahtumaloki
    st.markdown(
        f"<div style='font-size:11px; color:{COLOR_TEXT_DIM}; "
        f"letter-spacing:2px; margin-bottom:8px'>TAPAHTUMALOKI</div>",
        unsafe_allow_html=True,
    )

    # Väri kullekkin vakavuusasteelle
    severity_colors = {
        "info": COLOR_TEXT_DIM,
        "warning": COLOR_WARNING,
        "danger": COLOR_ALERT,
        "success": COLOR_SUCCESS,
    }

    event_log = get_event_log()
    if not event_log:
        st.markdown(
            f"<span style='color:{COLOR_TEXT_DIM}; font-size:11px'>Ei tapahtumia.</span>",
            unsafe_allow_html=True,
        )
    else:
        for ev in event_log[:6]:
            sc = severity_colors.get(ev["severity"], COLOR_TEXT_DIM)
            st.markdown(
                f"<div style='font-size:10px; border-left:2px solid {sc}; "
                f"padding:3px 8px; margin-bottom:5px; color:{COLOR_TEXT_DIM}'>"
                f"<span style='color:{COLOR_TEXT_DIM}'>{ev['time']}</span><br>"
                f"<span style='color:{COLOR_TEXT}'>{ev['message']}</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

# Pääsisältö
planet = get_planet()
res = planet["resources"]
prod = planet["production"]
cons = planet["consumption"]

# Sivun otsikko
hq_mark = " [HQ]" if planet["is_capital"] else ""
st.markdown(
    f"<h2 style='margin-bottom:2px; color:{planet['color']}'>"
    f"{planet['name']}{hq_mark}</h2>"
    f"<div style='color:{COLOR_TEXT_DIM}; font-size:12px; margin-bottom:20px'>"
    f"GALAKTINEN VUOSI {get_year()} GE &nbsp;·&nbsp; TICK {get_tick()}</div>",
    unsafe_allow_html=True,
)

# Resurssikortit
# Näytetään kaikki 6 resurssia vierekkäin omissa korteissaan
st.markdown(
    f"<div style='font-size:11px; color:{COLOR_TEXT_DIM}; "
    f"letter-spacing:2px; margin-bottom:8px'>RESURSSIT</div>",
    unsafe_allow_html=True,
)

cols = st.columns(6)
for col, resource in zip(cols, RESOURCE_NAMES):
    value = res[resource]
    net = round(prod[resource] - cons[resource], 1)
    critical = value < CRITICAL_THRESHOLDS.get(resource, 0)

    # Värit tilanteen mukaan
    r_color = RESOURCE_COLORS[resource]
    bg = "#1A0505" if critical else COLOR_PANEL
    border = COLOR_ALERT if critical else COLOR_BORDER
    net_color = COLOR_ALERT if net < 0 else "#00CC66"
    net_str = f"+{net:.1f}" if net >= 0 else f"{net:.1f}"
    alert_text = "<br><span style='color:#FF3333; font-size:10px'>⚠ KRIITTINEN</span>" if critical else ""

    with col:
        st.markdown(
            f"<div style='background:{bg}; border:1px solid {border}; "
            f"padding:12px 14px; font-family:Rajdhani'>"
            f"<div style='color:{COLOR_TEXT_DIM}; font-size:10px; "
            f"letter-spacing:2px'>{resource.upper()}</div>"
            f"<div style='color:{r_color}; font-size:24px; "
            f"font-weight:bold; margin:4px 0'>{int(value):,}</div>"
            f"<div style='color:{net_color}; font-size:11px'>{net_str} / tick</div>"
            f"{alert_text}"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

# Resurssihistoriakaavio
st.markdown(
    f"<div style='font-size:11px; color:{COLOR_TEXT_DIM}; "
    f"letter-spacing:2px; margin-bottom:8px'>RESURSSIHISTORIA</div>",
    unsafe_allow_html=True,
)

# Käyttäjä valitsee mikä resurssi näytetään kaaviossa
selected_resource = st.selectbox(
    "", RESOURCE_NAMES, key="chart_resource", label_visibility="collapsed"
)

df = get_history(selected_resource)
color = RESOURCE_COLORS[selected_resource]

fig = go.Figure()
if len(df) >= 2:
    fig.add_trace(go.Scatter(
        x = df["tick"],
        y = df["value"],
        mode = "lines",
        line = dict(color=color, width=2),
        fill = "tozeroy",
        fillcolor = f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
        name = selected_resource,
    ))

fig.update_layout(
    plot_bgcolor = COLOR_BG,
    paper_bgcolor =COLOR_PANEL,
    font = dict(family="Rajdhani", color=COLOR_TEXT, size=11),
    margin = dict(l=10, r=10, t=10, b=10),
    height = 240,
    xaxis = dict(title="TICK", gridcolor=COLOR_BORDER, showgrid=True, zeroline=False),
    yaxis = dict(gridcolor=COLOR_BORDER, showgrid=True, zeroline=False),
    showlegend = False,
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("<div style='margin:8px 0'></div>", unsafe_allow_html=True)

# Tuotanto & kulutus taulukko
st.markdown(
    f"<div style='font-size:11px; color:{COLOR_TEXT_DIM}; "
    f"letter-spacing:2px; margin-bottom:8px'>TUOTANTO & KULUTUS</div>",
    unsafe_allow_html=True,
)

prod_rows = []
for r in RESOURCE_NAMES:
    p = prod[r]
    c = cons[r]
    net = round(p - c, 1)
    prod_rows.append({
        "Resurssi": r,
        "TUOTANTO": f"+{p}",
        "KULUTUS":  f"-{c}",
        "NETTO":    f"+{net}" if net >= 0 else str(net),
    })

st.dataframe(
    pd.DataFrame(prod_rows).set_index("Resurssi"),
    use_container_width=True,
    height = 260,
)
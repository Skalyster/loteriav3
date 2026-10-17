import streamlit as st
import random

# ==========================================
# ESTADÍSTICAS CONGELADAS (Extraídas de tu BD)
# ==========================================
DATOS = {
    "Bonoloto": {
        "calientes": [3, 10, 22, 33, 41, 46, 2, 34, 39, 45, 32, 47, 49, 5, 18, 26, 37, 11, 25, 8, 38, 15, 44, 1, 21],
        "frios": [29, 4, 16, 20, 36, 12, 48, 6, 13, 40, 31, 23, 30, 43, 14, 42, 9, 28, 7, 35, 17, 24, 19, 27, 45]
    },
    "Eurodreams": {
        "calientes": [21, 22, 24, 23, 3, 8, 37, 19, 30, 4, 15, 25, 29, 11, 17, 20, 38, 26, 27, 9, 16, 5, 33, 39, 36],
        "frios": [13, 31, 2, 10, 1, 6, 40, 14, 34, 18, 35, 28, 7, 32, 12, 21, 15, 20, 19, 26, 25, 37, 38, 9, 11]
    },
    "Lotería Nacional": {
        # Terminaciones de 2 cifras más premiadas extraídas de tu histórico
        "terminaciones_calientes": ["84", "22", "20", "97", "44", "08", "33", "70", "47", "80", "05", "11", "14", "10", "19"]
    }
}

# ==========================================
# CONFIGURACIÓN MÓVIL
# ==========================================
st.set_page_config(page_title="Generador Lotto", page_icon="📱", layout="centered")

st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>📱 Generador Lotto</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-top: 0px;'>Tus apuestas inteligentes al instante</p>", unsafe_allow_html=True)

st.markdown("""
<style>
    /* Los 3 botones de juego siempre en una sola fila, también en móvil */
    .st-key-topnav [data-testid="stHorizontalBlock"] { flex-wrap: nowrap !important; gap: 0.4rem !important; }
    .st-key-topnav [data-testid="stColumn"] { min-width: 0 !important; flex: 1 1 0 !important; width: auto !important; }
    .st-key-topnav button { padding: 0.35rem 0.2rem !important; }
    .st-key-topnav button p { font-size: clamp(12px, 3.4vw, 15px) !important; line-height: 1.15 !important; }
</style>
""", unsafe_allow_html=True)

if "juego" not in st.session_state:
    st.session_state.juego = "Bonoloto"

with st.container(key="topnav"):
    for col, nombre in zip(st.columns(3), ["Bonoloto", "Eurodreams", "Lotería Nacional"]):
        with col:
            if st.button(nombre, key=f"nav_{nombre}", use_container_width=True,
                         type="primary" if st.session_state.juego == nombre else "secondary"):
                st.session_state.juego = nombre
                st.rerun()

juego = st.session_state.juego

# Solo mostramos la estrategia si no es Lotería Nacional
if juego != "Lotería Nacional":
    estrategia = st.selectbox("Estrategia:", ["🔥 Caliente", "❄️ Mixta (3 Calientes / 3 Fríos)"])
else:
    estrategia = "N/A" # En Lotería Nacional siempre usamos terminaciones calientes

# ==========================================
# MOTOR DE GENERACIÓN
# ==========================================
def generar(juego, estrategia):
    apuestas = []
    
    if juego == "Lotería Nacional":
        terminaciones = DATOS[juego]["terminaciones_calientes"]
        for _ in range(5):
            # Elegimos una terminación caliente de 2 cifras
            term = random.choice(terminaciones)
            # Generamos las 3 primeras cifras al azar (000 al 999)
            inicio = random.randint(0, 999)
            numero = f"{inicio:03d}{term}"
            apuestas.append(numero)
        return apuestas
        
    # Lógica para Bonoloto y Eurodreams
    datos = DATOS[juego]
    max_num = 49 if juego == "Bonoloto" else 40
    
    for _ in range(5):
        if estrategia == "🔥 Caliente":
            nums = random.choices(range(1, max_num + 1), 
                                 weights=[3 if n in datos["calientes"] else 1 for n in range(1, max_num + 1)], 
                                 k=6)
            comb = list(set(nums))
            while len(comb) < 6:
                nuevo = random.randint(1, max_num)
                if nuevo not in comb: comb.append(nuevo)
        else:
            comb = random.sample(datos["calientes"], 3) + random.sample(datos["frios"], 3)
            
        comb.sort()
        extra = random.randint(0, 9) if juego == "Bonoloto" else random.randint(1, 5)
        apuestas.append((comb, extra))
        
    return apuestas

# ==========================================
# INTERFAZ DE RESULTADOS (MÓVIL)
# ==========================================
if st.button("🎰 GENERAR 5 APUESTAS", use_container_width=True):
    res = generar(juego, estrategia)
    
    st.write("---")
    
    if juego == "Lotería Nacional":
        # Diseño de tarjetas planas para Lotería Nacional
        html = "<div style='display: flex; flex-direction: column; gap: 12px; align-items: center;'>"
        for i, num in enumerate(res):
            html += f"<div style='background: #f9f9f9; border-left: 5px solid #ff7f0e; padding: 12px 20px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 80%; text-align: center;'>"
            html += f"<b style='color: #555; font-size: 12px;'>Apuesta {i+1}</b><br>"
            html += f"<span style='font-size: 28px; font-weight: bold; color: #333; letter-spacing: 3px;'>{num}</span>"
            html += f"</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
    else:
        # Diseño de bolas para Bonoloto y Eurodreams
        cp = "#1f77b4" if juego == "Bonoloto" else "#2ca02c"
        ce = "#d62728" if juego == "Bonoloto" else "#ff7f0e"
        txt = "R" if juego == "Bonoloto" else "E"
        
        html = "<div style='display: flex; flex-direction: column; gap: 14px;'>"
        for i, (nums, extra) in enumerate(res):
            html += "<div style='display: flex; flex-direction: column; gap: 4px;'>"
            html += f"<b style='opacity: 0.7; font-size: 13px;'>Apuesta {i+1}</b>"
            html += "<div style='--ball: clamp(30px, 9.4vw, 40px); --gap: clamp(4px, 1.3vw, 7px); display: flex; align-items: center; justify-content: flex-start; flex-wrap: nowrap; gap: var(--gap);'>"
            base = "flex: 0 0 var(--ball); width: var(--ball); height: var(--ball); box-sizing: border-box; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: white; font-weight: bold; line-height: 1; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);"
            for n in nums:
                html += f"<span style='{base} font-size: calc(var(--ball) * 0.42); background-color: {cp};'>{n}</span>"
            html += f"<span style='{base} font-size: calc(var(--ball) * 0.36); background-color: {ce}; margin-left: var(--gap);'>{txt}{extra}</span>"
            html += "</div></div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
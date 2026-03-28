import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import random

# Configurações da Página
st.set_page_config(page_title="Alicia School Homework", layout="wide")

# --- ESTILO ---
st.markdown("""
    <style>
    .stApp { background-color: #fdf6e3; }
    div.stButton > button {
        width: 100%; height: 60px; font-size: 20px !important;
        font-weight: bold; border-radius: 15px;
        border: 2px solid #d97706; background-color: #fef3c7; color: #92400e;
    }
    </style>
    """, unsafe_allow_html=True)

# Dados das Capitais e Nomes
dados_estados = {
    "AM": {"nome": "Amazonas", "capital": "Manaus", "x": 300, "y": 380},
    "PA": {"nome": "Pará", "capital": "Belém", "x": 500, "y": 380},
    "BA": {"nome": "Bahia", "capital": "Salvador", "x": 650, "y": 550},
    "MT": {"nome": "Mato Grosso", "capital": "Cuiabá", "x": 480, "y": 580},
    "MG": {"nome": "Minas Gerais", "capital": "Belo Horizonte", "x": 620, "y": 680},
    "SP": {"nome": "São Paulo", "capital": "São Paulo", "x": 580, "y": 750},
    "RJ": {"nome": "Rio de Janeiro", "capital": "Rio de Janeiro", "x": 640, "y": 760},
    "RS": {"nome": "Rio Grande do Sul", "capital": "Porto Alegre", "x": 500, "y": 880},
    # Adicionaremos todos os outros conforme a Alicia for testando!
}

# --- INTERFACE ---
if 'modo' not in st.session_state: st.session_state.modo = "Aprender"

col_menu, col_mapa = st.columns([1, 4])

with col_menu:
    st.markdown("### 🧜‍♀️ MENU")
    if st.button("📖 APRENDER"): st.session_state.modo = "Aprender"
    if st.button("🎮 JOGAR QUIZ"): 
        st.session_state.modo = "Jogar"
        st.session_state.reset = True
    
    st.write("---")
    if st.session_state.modo == "Aprender":
        st.info("Alicia, toque em uma sigla no mapa!")
    else:
        st.warning("Adivinhe onde está o estado!")

with col_mapa:
    try:
        img = Image.open("mapa_alicia.png")
        # Captura o clique na imagem
        value = streamlit_image_coordinates(img, key="alicia_map")
        
        if value:
            # Lógica para encontrar qual estado foi clicado baseado na proximidade
            click_x, click_y = value["x"], value["y"]
            estado_clicado = None
            menor_distancia = 50 # Raio de clique em pixels
            
            for sigla, pos in dados_estados.items():
                dist = ((click_x - pos["x"])**2 + (click_y - pos["y"])**2)**0.5
                if dist < menor_distancia:
                    estado_clicado = sigla
                    break
            
            if estado_clicado:
                info = dados_estados[estado_clicado]
                if st.session_state.modo == "Aprender":
                    st.success(f"✨ **{info['nome']}** | Capital: **{info['capital']}**")
                else:
                    # Lógica de Quiz aqui
                    st.session_state.resposta_alicia = estado_clicado
            else:
                st.write("🧜‍♀️ Quase! Tente tocar bem em cima da sigla!")
                
    except Exception as e:
        st.error("Suba a imagem 'mapa_alicia.png' para o GitHub!")

# --- LÓGICA DO QUIZ (Simplificada para teste inicial) ---
if st.session_state.modo == "Jogar":
    if 'alvo' not in st.session_state or st.session_state.get('reset'):
        st.session_state.alvo = random.choice(list(dados_estados.keys()))
        st.session_state.reset = False
    
    alvo = st.session_state.alvo
    st.markdown(f"### 🎯 Alicia, onde fica o estado: **{dados_estados[alvo]['nome']}**?")
    
    if 'resposta_alicia' in st.session_state:
        if st.session_state.resposta_alicia == alvo:
            st.balloons()
            st.success("VOCÊ ACERTOU! VOCÊ É DEMAIS! 🧜‍♀️✨")
            if st.button("PRÓXIMO ➡️"):
                st.session_state.reset = True
                del st.session_state.resposta_alicia
                st.rerun()
        else:
            st.error("Ainda não... procure a sigla certa no mapa! 💡")

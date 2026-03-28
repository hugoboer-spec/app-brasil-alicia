import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
import random

# Configurações da Página
st.set_page_config(page_title="Alicia School Homework", layout="wide")

# --- ESTILO LIMPO E MÁGICO ---
st.markdown("""
    <style>
    .stApp { background-color: #fdf6e3; }
    /* Botões grandes na lateral */
    div.stButton > button {
        width: 100%; height: 70px; font-size: 22px !important;
        font-weight: bold; border-radius: 15px;
        border: 3px solid #0077be; background-color: #e0f2fe; color: #0369a1;
    }
    .sereia-msg {
        background-color: #ffffff; border-radius: 20px; padding: 15px;
        border: 2px solid #0077be; font-size: 22px; color: #0369a1;
        text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. TABELA MÁGICA DE COORDENADAS (Recalibrada com seus dados!)
# Baseado em AM(473,306), SP(782,566), CE(949,311)
dados_estados = {
    "AM": {"nome": "Amazonas", "capital": "Manaus", "x": 473, "y": 306},
    "PA": {"nome": "Pará", "capital": "Belém", "x": 670, "y": 315},
    "RR": {"nome": "Roraima", "capital": "Boa Vista", "x": 490, "y": 215},
    "AP": {"nome": "Amapá", "capital": "Macapá", "x": 665, "y": 230},
    "AC": {"nome": "Acre", "capital": "Rio Branco", "x": 335, "y": 420},
    "RO": {"nome": "Rondônia", "capital": "Porto Velho", "x": 455, "y": 445},
    "MT": {"nome": "Mato Grosso", "capital": "Cuiabá", "x": 615, "y": 465},
    "MS": {"nome": "Mato Grosso do Sul", "capital": "Campo Grande", "x": 615, "y": 615},
    "GO": {"nome": "Goiás", "capital": "Goiânia", "x": 710, "y": 510},
    "DF": {"nome": "Distrito Federal", "capital": "Brasília", "x": 745, "y": 490},
    "TO": {"nome": "Tocantins", "capital": "Palmas", "x": 735, "y": 415},
    "MA": {"nome": "Maranhão", "capital": "São Luís", "regiao": "Nordeste", "x": 795, "y": 320},
    "PI": {"nome": "Piauí", "capital": "Teresina", "x": 845, "y": 375},
    "CE": {"nome": "Ceará", "capital": "Fortaleza", "x": 949, "y": 311},
    "RN": {"nome": "Rio Grande do Norte", "capital": "Natal", "x": 1005, "y": 355},
    "PB": {"nome": "Paraíba", "capital": "João Pessoa", "x": 1005, "y": 400},
    "PE": {"nome": "Pernambuco", "capital": "Recife", "x": 1005, "y": 445},
    "AL": {"nome": "Alagoas", "capital": "Maceió", "x": 995, "y": 480},
    "SE": {"nome": "Sergipe", "capital": "Aracaju", "x": 985, "y": 515},
    "BA": {"nome": "Bahia", "capital": "Salvador", "x": 860, "y": 485},
    "MG": {"nome": "Minas Gerais", "capital": "Belo Horizonte", "x": 815, "y": 585},
    "ES": {"nome": "Espírito Santo", "capital": "Vitória", "x": 890, "y": 635},
    "RJ": {"nome": "Rio de Janeiro", "capital": "Rio de Janeiro", "x": 845, "y": 680},
    "SP": {"nome": "São Paulo", "capital": "São Paulo", "x": 782, "y": 566},
    "PR": {"nome": "Paraná", "capital": "Curitiba", "x": 715, "y": 685},
    "SC": {"nome": "Santa Catarina", "capital": "Florianópolis", "x": 740, "y": 745},
    "RS": {"nome": "Rio Grande do Sul", "capital": "Porto Alegre", "x": 665, "y": 795},
}

# --- INTERFACE ---
if 'modo' not in st.session_state: st.session_state.modo = "Aprender"

col_menu, col_mapa = st.columns([1, 4])

with col_menu:
    st.markdown("### 🧜‍♀️ ALICIA THE BEST")
    if st.button("📖 APRENDER"): 
        st.session_state.modo = "Aprender"
        st.rerun()
    if st.button("🎮 JOGAR QUIZ"): 
        st.session_state.modo = "Jogar"
        st.session_state.reset = True
        st.rerun()
    
    st.write("---")
    if st.session_state.modo == "Aprender":
        st.markdown('<div class="sereia-msg">🧜‍♀️ "Alicia, toque nas siglas do mapa!"</div>', unsafe_allow_html=True)
    else:
        if 'alvo' in st.session_state:
            st.markdown(f'<div class="sereia-msg">🧜‍♀️ "Onde fica: <b>{dados_estados[st.session_state.alvo]["nome"]}</b>?"</div>', unsafe_allow_html=True)

with col_mapa:
    try:
        img = Image.open("mapa_alicia.png")
        # Captura o toque
        value = streamlit_image_coordinates(img, key="mapa_final")
        
        if value:
            click_x, click_y = value["x"], value["y"]
            estado_clicado = None
            raio = 50 # Raio de clique ajustado
            
            for sigla, pos in dados_estados.items():
                dist = ((click_x - pos["x"])**2 + (click_y - pos["y"])**2)**0.5
                if dist < raio:
                    estado_clicado = sigla
                    break
            
            if estado_clicado:
                info = dados_estados[estado_clicado]
                if st.session_state.modo == "Aprender":
                    st.balloons()
                    st.success(f"🧜‍♀️ **{info['nome']}** | Capital: **{info['capital']}**")
                else:
                    if estado_clicado == st.session_state.alvo:
                        st.snow()
                        st.success(f"🧜‍♀️ ISSO AÍ! Você achou o {info['nome']}! 🎉")
                        if st.button("PRÓXIMO ESTADO ➡️"):
                            st.session_state.reset = True
                            st.rerun()
                    else:
                        st.error("🧜‍♀️ Quase! Procure a sigla certa no mapa!")
            else:
                st.info("🧜‍♀️ Tente tocar bem em cima das letras (ex: AM, SP, CE)!")
                
        st.image(img, use_container_width=True)

    except Exception as e:
        st.error("Certifique-se de que o arquivo 'mapa_alicia.png' está no seu GitHub!")

# Lógica de sorteio do Quiz
if st.session_state.modo == "Jogar":
    if 'alvo' not in st.session_state or st.session_state.get('reset'):
        st.session_state.alvo = random.choice(list(dados_estados.keys()))
        st.session_state.reset = False
        st.rerun()


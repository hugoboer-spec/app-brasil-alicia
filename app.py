import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import random

# Configurações para o iPad
st.set_page_config(page_title="Alicia Homework", layout="wide")

# --- ESTILO CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Faz a imagem ocupar a tela toda na Home */
    .home-image-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
    }
    .home-image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* Botão Circular Flutuante SOBRE a imagem */
    .btn-iniciar-container {
        position: fixed;
        bottom: 40px;
        right: 40px;
        z-index: 9999; /* Garante que fique por cima de tudo */
    }
    
    /* Estilo do Botão Iniciar */
    div.stButton > button.btn-iniciar {
        width: 140px !important;
        height: 140px !important;
        border-radius: 50% !important;
        background-color: #ff4b4b !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border: 4px solid #ffffff !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.4) !important;
        cursor: pointer !important;
    }
    div.stButton > button.btn-iniciar:hover {
        background-color: #0077be !important;
        transform: scale(1.05);
    }

    /* Estilo para a página do Mapa */
    .map-header {
        display: flex;
        justify-content: center;
        padding: 10px;
    }
    .sereia-msg {
        background-color: #f0f9ff;
        border-radius: 20px;
        padding: 15px;
        border: 2px solid #0077be;
        font-size: 22px;
        color: #0369a1;
        text-align: center;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 1. Dados dos Estados e Regiões
estados_brasil = {
    "AC": {"nome": "Acre", "capital": "Rio Branco", "regiao": "Norte", "cor": "#4ade80"},
    "AL": {"nome": "Alagoas", "capital": "Maceió", "regiao": "Nordeste", "cor": "#f87171"},
    "AP": {"nome": "Amapá", "capital": "Macapá", "regiao": "Norte", "cor": "#4ade80"},
    "AM": {"nome": "Amazonas", "capital": "Manaus", "regiao": "Norte", "cor": "#4ade80"},
    "BA": {"nome": "Bahia", "capital": "Salvador", "regiao": "Nordeste", "cor": "#f87171"},
    "CE": {"nome": "Ceará", "capital": "Fortaleza", "regiao": "Nordeste", "cor": "#f87171"},
    "DF": {"nome": "Distrito Federal", "capital": "Brasília", "regiao": "Centro-Oeste", "cor": "#fbbf24"},
    "ES": {"nome": "Espírito Santo", "capital": "Vitória", "regiao": "Sudeste", "cor": "#60a5fa"},
    "GO": {"nome": "Goiás", "capital": "Goiânia", "regiao": "Centro-Oeste", "cor": "#fbbf24"},
    "MA": {"nome": "Maranhão", "capital": "São Luís", "regiao": "Nordeste", "cor": "#f87171"},
    "MT": {"nome": "Mato Grosso", "capital": "Cuiabá", "regiao": "Centro-Oeste", "cor": "#fbbf24"},
    "MS": {"nome": "Mato Grosso do Sul", "capital": "Campo Grande", "regiao": "Centro-Oeste", "cor": "#fbbf24"},
    "MG": {"nome": "Minas Gerais", "capital": "Belo Horizonte", "regiao": "Sudeste", "cor": "#60a5fa"},
    "PA": {"nome": "Pará", "capital": "Belém", "regiao": "Norte", "cor": "#4ade80"},
    "PB": {"nome": "Paraíba", "capital": "João Pessoa", "regiao": "Nordeste", "cor": "#f87171"},
    "PR": {"nome": "Paraná", "capital": "Curitiba", "regiao": "Sul", "cor": "#a78bfa"},
    "PE": {"nome": "Pernambuco", "capital": "Recife", "regiao": "Nordeste", "cor": "#f87171"},
    "PI": {"nome": "Piauí", "capital": "Teresina", "regiao": "Nordeste", "cor": "#f87171"},
    "RJ": {"nome": "Rio de Janeiro", "capital": "Rio de Janeiro", "regiao": "Sudeste", "cor": "#60a5fa"},
    "RN": {"nome": "Rio Grande do Norte", "capital": "Natal", "regiao": "Nordeste", "cor": "#f87171"},
    "RS": {"nome": "Rio Grande do Sul", "capital": "Porto Alegre", "regiao": "Sul", "cor": "#a78bfa"},
    "RO": {"nome": "Rondônia", "capital": "Porto Velho", "regiao": "Norte", "cor": "#4ade80"},
    "RR": {"nome": "Roraima", "capital": "Boa Vista", "regiao": "Norte", "cor": "#4ade80"},
    "SC": {"nome": "Santa Catarina", "capital": "Florianópolis", "regiao": "Sul", "cor": "#a78bfa"},
    "SP": {"nome": "São Paulo", "capital": "São Paulo", "regiao": "Sudeste", "cor": "#60a5fa"},
    "SE": {"nome": "Sergipe", "capital": "Aracaju", "regiao": "Nordeste", "cor": "#f87171"},
    "TO": {"nome": "Tocantins", "capital": "Palmas", "regiao": "Norte", "cor": "#4ade80"}
}
regioes_lista = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

@st.cache_data
def carregar_mapa():
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    return requests.get(url ).json()

geojson_brasil = carregar_mapa()

# --- NAVEGAÇÃO ---
if 'pagina' not in st.session_state: st.session_state.pagina = "Inicial"

# --- PÁGINA INICIAL ---
if st.session_state.pagina == "Inicial":
    # Imagem de fundo que cobre a tela
    try:
        st.markdown(f'<div class="home-image-container"><img src="https://raw.githubusercontent.com/{st.query_params.get("user", "seu_usuario_github" )}/{st.query_params.get("repo", "app-brasil-alicia")}/main/meninas.png"></div>', unsafe_allow_html=True)
        # Como o Streamlit tem dificuldade com caminhos locais em HTML, usamos o método padrão mas com CSS fixo
        st.image("meninas.png", use_container_width=True)
    except:
        st.write("🧜‍♀️ (Meninas.png)")
    
    # Botão Iniciar sobre a imagem
    st.markdown('<div class="btn-iniciar-container">', unsafe_allow_html=True)
    if st.button("INICIAR 🚀", key="iniciar_btn"):
        st.session_state.pagina = "Mapa"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- PÁGINA DO MAPA ---
else:
    # Título Pequeno Alicia Homework
    try:
        _, col_tit, _ = st.columns([1, 0.8, 1])
        with col_tit: st.image("aliciahomework.png", use_container_width=True)
    except:
        st.markdown('<h2 style="text-align:center;">ALICIA HOMEWORK</h2>', unsafe_allow_html=True)

    # Botões de Controle
    if 'modo' not in st.session_state: st.session_state.modo = "Aprender"
    c1, c2, c3 = st.columns([2, 2, 1])
    if c1.button("📖 APRENDER"): st.session_state.modo = "Aprender"
    if c2.button("🎮 JOGAR"): 
        st.session_state.modo = "Jogar"
        st.session_state.reset_quiz = True
    if c3.button("🏠 VOLTAR"):
        st.session_state.pagina = "Inicial"
        st.rerun()

    st.write("---")
    col_mapa, col_info = st.columns([2, 1])

    with col_mapa:
        if st.session_state.modo == "Aprender":
            m = folium.Map(location=[-15.0, -55.0], zoom_start=4, tiles="CartoDB positron",
                          zoom_control=False, scrollWheelZoom=False, dragging=False)
            folium.GeoJson(geojson_brasil, style_function=lambda x: {
                'fillColor': estados_brasil.get(x['properties']['sigla'], {}).get('cor', '#eee'),
                'color': 'white', 'weight': 1, 'fillOpacity': 0.8
            }).add_to(m)
            output = st_folium(m, width=700, height=600, key="mapa_aprender")
        else:
            if 'estado_quiz' not in st.session_state or st.session_state.get('reset_quiz'):
                st.session_state.estado_quiz = random.choice(list(estados_brasil.keys()))
                st.session_state.reset_quiz = False
                st.session_state.respondido = False
                
                sigla_alvo = st.session_state.estado_quiz
                info_alvo = estados_brasil[sigla_alvo]
                correta = f"{info_alvo['nome']} - {info_alvo['regiao']}"
                
                opcoes = [correta]
                regiao_errada = random.choice([r for r in regioes_lista if r != info_alvo['regiao']])
                opcoes.append(f"{info_alvo['nome']} - {regiao_errada}")
                
                outros_estados = random.sample([s for s in estados_brasil.keys() if s != sigla_alvo], 3)
                for s in outros_estados:
                    info_s = estados_brasil[s]
                    reg = random.choice(regioes_lista)
                    opcoes.append(f"{info_s['nome']} - {reg}")
                
                random.shuffle(opcoes)
                st.session_state.opcoes_quiz = opcoes

            sigla_alvo = st.session_state.estado_quiz
            m_quiz = folium.Map(location=[-15.0, -55.0], zoom_start=4, tiles="CartoDB positron",
                               zoom_control=False, scrollWheelZoom=False, dragging=False)
            folium.GeoJson(geojson_brasil, style_function=lambda x: {
                'fillColor': '#3b82f6' if x['properties']['sigla'] == sigla_alvo else '#f3f4f6',
                'color': 'white', 'weight': 2, 'fillOpacity': 0.9 if x['properties']['sigla'] == sigla_alvo else 0.4
            }).add_to(m_quiz)
            st_folium(m_quiz, width=700, height=600, key="mapa_quiz")

    with col_info:
        if st.session_state.modo == "Aprender":
            st.markdown('<div class="sereia-msg">🧜‍♀️ "Alicia, toque no mapa!"</div>', unsafe_allow_html=True)
            if output and output.get("last_active_drawing"):
                sigla = output["last_active_drawing"]["properties"]["sigla"]
                info = estados_brasil[sigla]
                st.success(f"### 📍 {info['nome']}\n**Capital:** {info['capital']}\n**Região:** {info['regiao']}")
        else:
            st.markdown('<div class="sereia-msg">🧜‍♀️ "Qual é o estado em azul e sua região?"</div>', unsafe_allow_html=True)
            info_alvo = estados_brasil[st.session_state.estado_quiz]
            resposta_correta = f"{info_alvo['nome']} - {info_alvo['regiao']}"
            escolha = st.radio("Escolha a opção correta:", st.session_state.opcoes_quiz)
            
            if st.button("CONFIRMAR ✅"):
                if escolha == resposta_correta:
                    st.snow(); st.success("PARABÉNS! 🐠"); st.session_state.respondido = True
                else:
                    st.error("Quase! Tente de novo! 🧜‍♀️")

            if st.session_state.get('respondido'):
                if st.button("PRÓXIMO ➡️"):
                    st.session_state.reset_quiz = True; st.rerun()

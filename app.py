import streamlit as st
from PIL import Image
import requests

# Configurações da Página
st.set_page_config(page_title="Alicia School Homework", layout="wide")

# --- ESTILO CUSTOMIZADO ---
st.markdown("""
    <style>
    .stApp {
        background-color: #fdf6e3; /* Cor de papel antigo para combinar com a imagem */
    }
    /* Estilo para os botões à esquerda */
    .sidebar-btns {
        position: fixed;
        left: 20px;
        top: 200px;
        z-index: 100;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    div.stButton > button {
        width: 180px;
        height: 60px;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 10px;
        border: 2px solid #d97706;
        background-color: #fef3c7;
        color: #92400e;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Dados das Capitais (Baseado nas siglas da imagem)
capitais = {
    "AC": "Rio Branco", "AM": "Manaus", "RR": "Boa Vista", "RO": "Porto Velho",
    "PA": "Belém", "AP": "Macapá", "TO": "Palmas", "MA": "São Luís",
    "PI": "Teresina", "CE": "Fortaleza", "RN": "Natal", "PB": "João Pessoa",
    "PE": "Recife", "AL": "Maceió", "SE": "Aracaju", "BA": "Salvador",
    "MT": "Cuiabá", "MS": "Campo Grande", "GO": "Goiânia", "DF": "Brasília",
    "MG": "Belo Horizonte", "ES": "Vitória", "RJ": "Rio de Janeiro", "SP": "São Paulo",
    "PR": "Curitiba", "SC": "Florianópolis", "RS": "Porto Alegre"
}

# --- INTERFACE ---
if 'modo' not in st.session_state: st.session_state.modo = "Aprender"

# Botões na lateral esquerda
with st.container():
    col_lateral, col_mapa = st.columns([1, 4])
    
    with col_lateral:
        st.write("### MENU")
        if st.button("📖 APRENDER"): st.session_state.modo = "Aprender"
        if st.button("🎮 JOGAR QUIZ"): 
            st.session_state.modo = "Jogar"
            st.session_state.reset = True

    with col_mapa:
        # Carregar e mostrar a imagem principal
        try:
            img = Image.open("mapa_alicia.png")
            st.image(img, use_container_width=True)
        except:
            st.error("Por favor, suba a imagem com o nome 'mapa_alicia.png' para o seu GitHub!")

        # Área de Interação abaixo da imagem
        if st.session_state.modo == "Aprender":
            st.info("🧜‍♀️ Escolha um estado na lista abaixo para ver a capital!")
            sigla = st.selectbox("Selecione a Sigla que você vê no mapa:", sorted(list(capitais.keys())))
            if sigla:
                st.success(f"A Capital de {sigla} é: **{capitais[sigla]}**")
        
        else:
            if 'alvo' not in st.session_state or st.session_state.get('reset'):
                st.session_state.alvo = random.choice(list(capitais.keys()))
                st.session_state.reset = False
            
            alvo = st.session_state.alvo
            st.warning(f"🎯 Alicia, qual é a capital da sigla **{alvo}** que está no mapa?")
            
            opcoes = [capitais[alvo]] + random.sample([c for c in capitais.values() if c != capitais[alvo]], 2)
            random.shuffle(opcoes)
            
            escolha = st.radio("Escolha a capital certa:", opcoes, horizontal=True)
            if st.button("CONFIRMAR ✅"):
                if escolha == capitais[alvo]:
                    st.balloons()
                    st.success("PARABÉNS, ALICIA! VOCÊ É A MELHOR! 🧜‍♀️✨")
                    if st.button("PRÓXIMO ➡️"):
                        st.session_state.reset = True
                        st.rerun()
                else:
                    st.error("Quase! Tente de novo, você consegue!")

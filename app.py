import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="Calibração da Alicia", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fdf6e3; }
    .debug-box {
        background-color: #fffbeb;
        padding: 20px;
        border: 2px solid #d97706;
        border-radius: 10px;
        font-size: 24px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧜‍♀️ Modo de Calibração da Alicia")
st.write("Clique exatamente no meio das siglas no mapa abaixo e anote os números!")

try:
    img = Image.open("mapa_alicia.png")
    
    # Captura o clique
    value = streamlit_image_coordinates(img, key="calibracao")
    
    if value:
        # MOSTRA OS NÚMEROS GRANDES PARA VOCÊ LER
        st.markdown(f"""
            <div class="debug-box">
                📍 Você clicou em:  

                <b>X: {value['x']}</b> | <b>Y: {value['y']}</b>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Aguardando seu clique no mapa...")

    # Mostra a imagem centralizada
    st.image(img, use_container_width=True)

except Exception as e:
    st.error("Certifique-se de que 'mapa_alicia.png' está no GitHub!")

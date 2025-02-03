import streamlit as st  
from geppetto import Geppetto  
import os  
import base64

# Initialisation de Geppetto si ce n'est pas déjà fait  
if 'geppetto' not in st.session_state:
    api_key_path = os.path.join(os.path.dirname(__file__), 'api_key.txt')
    st.session_state.geppetto = Geppetto()

# Chargement de l'image de fond avec gestion d'erreurs  
try:
    image_path = os.path.join(os.path.dirname(__file__), 'background.jpeg')
    with open(image_path, "rb") as f:
        background_image = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
                .stApp {{
                    background-image: url(data:image/jpeg;base64,{background_image});
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    height: 100vh;
                }}
            </style>
        """, unsafe_allow_html=True)
except Exception as e:
    st.warning(f"Impossible de charger l'image de fond : {str(e)}")

# Titre de l'application  
st.title("🗨️ Polo - Votre assistant virtuel")

# Description de l'application  
st.markdown("""
Bienvenue sur **Polo**!  
Une chatBox interactive utilisant l'API Gemini de GOOGLE.  
Posez-lui des questions et obtenez des réponses instantanées.
""")

# Ajouter un séparateur  
st.markdown("---")

# Stocker l'historique des messages dans une session de Streamlit  
if 'history' not in st.session_state:
    st.session_state.history = []

# Entrée utilisateur avec un label stylisé  
user_input = st.text_input("🗣️ Parlez à Polo", "")

# Bouton d'envoi  
if st.button("Envoyer", key='send_button'):
    if user_input:
        with st.spinner('Polo est en train de répondre...'):
            response = st.session_state.geppetto.talk(user_input)
            # Ajouter la question et la réponse à l'historique  
            st.session_state.history.append(f"Vous : {user_input}")
            st.session_state.history.append(f"Polo : {response}")

# CSS pour les messages en bulles
st.markdown("""
<style>
/* Style des messages utilisateur */
.user_message {
    background-color: #DCF8C6;
    border-radius: 20px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: right;
    margin-right: 10px;
    max-width: 60%;
    float: right;
    clear: both;
}

/* Style des messages de Geppetto */
.geppetto_message {
    background-color: #FFFFFF;
    border-radius: 20px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: left;
    margin-left: 10px;
    max-width: 60%;
    float: left;
    clear: both;
}
</style>
""", unsafe_allow_html=True)

# Afficher l'historique des messages en ordre inverse
if st.session_state.history:
    st.markdown("### 🗨️ Discussion")
    for message in reversed(st.session_state.history):
        if "Vous :" in message:
            st.markdown(f"<div class='user_message'>{message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='geppetto_message'>{message}</div>", unsafe_allow_html=True)

# Ajouter un pied de page  
st.markdown("---")
st.markdown("🛠️ Powered by [Paul Stephane ENGONE MOUITY](https://www.psengonemouity.fr)")
import streamlit as st
from geppetto import Geppetto
import os
import base64
from datetime import datetime  # Pour l'horodatage

# Initialisation des clés de session
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "geppetto" not in st.session_state:
    api_key_path = os.path.join(os.path.dirname(__file__), "api_key.txt")
    st.session_state.geppetto = Geppetto()
    st.session_state.geppetto.preprompt("admin_preprompt")

# Caching pour éviter de recharger l'image
@st.cache_data
def load_background_image():
    try:
        image_path = os.path.join(os.path.dirname(__file__), "background.jpeg")
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        st.warning(f"Impossible de charger l'image de fond : {str(e)}")
        return None

background_image = load_background_image()
if background_image:
    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url(data:image/jpeg;base64,{background_image});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                height: 100vh;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Fonction pour ajouter un message à l'historique
def add_to_history(user_message, response_message):
    timestamp = datetime.now().strftime("%H:%M:%S")  # Format horodatage
    st.session_state.history.append(
        f"Vous : {user_message} <small style='color:grey;'>{timestamp}</small>"
    )
    st.session_state.history.append(
        f"Polo : {response_message} <small style='color:grey;'>{timestamp}</small>"
    )

# Fonction pour envoyer un message
def send_message():
    if st.session_state.user_input.strip():  # Validation (non vide)
        with st.spinner("Polo est en train de répondre..."):
            response = st.session_state.geppetto.talk(st.session_state.user_input.strip())
            add_to_history(st.session_state.user_input, response)  # Ajout à l'historique
        st.session_state.user_input = ""  # Réinitialisation du champ
    else:
        st.warning("Veuillez entrer un message valide.")

# Bouton pour réinitialiser la discussion
if st.button("Réinitialiser la discussion", key="reset_button"):
    if st.session_state.history:  # Vérifie si l'historique n'est pas vide
        st.session_state.history = []  # Réinitialisation de l'historique
        st.success("La discussion a été réinitialisée.")
    else:
        st.warning("Aucune discussion à effacer.")

# Barre de saisie utilisateur avec envoi via "Entrée"
st.text_input(
    "🗣️ Parlez à Polo",
    key="user_input",
    placeholder="Votre message ici...",
    on_change=send_message,  # Appel de la fonction sur Entrée
)

# Ajouter un message d'instructions
st.caption("Appuyez sur Entrée pour envoyer. Utilisez Shift + Entrée pour aller à la ligne.")

# Bouton d'envoi (optionnel)
if st.button("Envoyer", key="send_button"):
    send_message()

# CSS pour les messages en bulles
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# Afficher l'historique des messages
if st.session_state.history:
    st.markdown("### 🗨️ Discussion")
    for message in reversed(st.session_state.history):  # Afficher du plus récent au plus ancien
        if "Vous :" in message:
            st.markdown(
                f"<div class='user_message'>{message}</div>", unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='geppetto_message'>{message}</div>", unsafe_allow_html=True
            )

# Ajouter un pied de page
st.markdown("---")
st.markdown("🛠️ Powered by [Paul Stephane ENGONE MOUITY](https://www.psengonemouity.fr)")

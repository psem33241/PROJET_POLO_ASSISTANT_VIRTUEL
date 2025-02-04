import streamlit as st  
from geppetto import Geppetto  
import os  
import base64  
from datetime import datetime

# Initialisation de Geppetto
if 'geppetto' not in st.session_state:
    api_key_path = os.path.join(os.path.dirname(__file__), 'api_key.txt')
    st.session_state.geppetto = Geppetto()
    st.session_state.geppetto.preprompt("admin_preprompt")
    #st.session_state.geppetto.preprompt("bienvenue_projet_3")

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

# Fonction pour ajouter un message à l'historique avec horodatage  
def add_to_history(user_message, response_message):
    timestamp = datetime.now().strftime("%H:%M:%S")  # Formatage de l'horodatage
    st.session_state.history.append(f"Vous : {user_message} <small style='color:grey;'>{timestamp}</small>")
    st.session_state.history.append(f"Polo : {response_message} <small style='color:grey;'>{timestamp}</small>")

# Fonction pour gérer l'envoi de messages
def send_message():
    if st.session_state.user_input.strip():  # Validation de l'entrée (non vide)
        with st.spinner('Polo est en train de répondre...'):
            response = st.session_state.geppetto.talk(st.session_state.user_input.strip())
            add_to_history(st.session_state.user_input, response)  # Ajout à l'historique
        st.session_state.user_input = ""  # Réinitialisation du champ
    else:
        st.warning("Veuillez entrer un message valide.")

# Fonction pour simuler "Shift + Entrée" comme retour à la ligne
def handle_input(key):
    if st.session_state.user_input.endswith("\n"):  # Si l'utilisateur appuie sur Entrée
        if len(st.session_state.user_input.strip()) > 0:
            send_message()
        else:
            st.session_state.user_input = ""  # Réinitialisation pour Entrée simple
    elif key == "Shift+Enter":  # Gestion de Shift+Entrée pour retour à la ligne
        st.session_state.user_input += "\n"

# Bouton pour réinitialiser la discussion AVANT la barre de saisie
if st.button("Réinitialiser la discussion", key='reset_button'):
    if st.session_state.history:  # Vérifie si l'historique n'est pas vide  
        st.session_state.history = []  # Réinitialisation de l'historique  
        st.success("La discussion a été réinitialisée.")
    else:
        st.warning("Aucune discussion à effacer.")

# Barre de saisie utilisateur avec gestion de l'envoi via "Entrée"  
st.text_area(
    "🗣️ Parlez à Polo",
    key="user_input",
    placeholder="Votre message ici...",
    on_change=send_message
)

# Ajout d'instructions pour éviter les confusions avec "Shift + Entrée"  
st.caption("Appuyez sur Shift + Entrée pour envoyer. Utilisez Entrée pour aller à la ligne.")

# Bouton d'envoi (optionnel, visible mais non obligatoire)  
if st.button("Envoyer", key='send_button'):
    send_message()

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
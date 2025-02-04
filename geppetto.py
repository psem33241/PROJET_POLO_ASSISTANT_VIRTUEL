import json  
import google.generativeai as genai  
import os  
from gtts import gTTS  
import playsound
import streamlit as st

class Geppetto:
    def __init__(self, api_key=st.secrets["API_KEY_VALID"], name_model="gemini-1.5-flash", temperature=1):
        self.api_key = api_key
        self.model = None  
        self.name_model = name_model  
        self.temperature = temperature  
        self.preprompt('admin_preprompt')  # Lire le préprompt administrateur  

    def _read_api_key(self, api_key_file):
        if not isinstance(api_key_file, str):
            raise ValueError("Le nom du fichier doit être une chaîne.")
            
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, api_key_file)
        
        try:
            with open(file_path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier {api_key_file} est introuvable à l'emplacement {file_path}.")

    def _configure(self):
        genai.configure(api_key=self.api_key)  # Configurer l'API avec la clé fournie  
        self.model = genai.GenerativeModel(self.name_model).start_chat()  # Initialiser le modèle et démarrer le chat
        self.talk(self.admin_preprompt)

    def talk(self, message: str) -> str:    
        try:
            response = self.model.send_message(message)  # Utiliser le message paramétré  
            assistant_response = response.text.strip().replace('\\', '')
            return assistant_response  
        except Exception as e:
            print(f"Une erreur est survenue lors de l'envoi du message: {e}")
            return "Une erreur est survenue."
    def preprompt(self, cle_dico):
        self._load_preprompt(cle_dico)
        self._configure()

    def _load_preprompt(self, cle_dico: str) -> str:
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, 'preprompt.json')
        try:
            with open(file_path, 'r') as file:
                prompts = json.load(file)  # Charger le fichier JSON contenant les préprompts  
                if cle_dico in prompts:
                    self.admin_preprompt  = prompts[cle_dico]  # Récupérer le prémessage  
                else:
                    raise ValueError("Clé introuvable dans le préprompt")
        except FileNotFoundError:
            raise FileNotFoundError(f"Le fichier {file_path} est introuvable.")
        except json.JSONDecodeError:
            raise ValueError("Erreur lors du décodage du fichier JSON.")

    def voice_talk(self, message: str):
        response = self.talk(message)
        if response != "Une erreur est survenue.":
            tts = gTTS(response, lang='fr')
            tts.save('response.mp3')
            playsound.playsound('response.mp3')  # Jouer le fichier audio  
            return 'response.mp3'
        else:
            print("Erreur lors de la génération de la réponse audio.")
            return None
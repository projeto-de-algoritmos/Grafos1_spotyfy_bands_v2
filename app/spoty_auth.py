import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Import client keys json
CLIENT = json.load(open('conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret']

# ... Configuração de credenciais e autenticação do Spotify ...

# Configurar as credenciais da API do Spotify
# CLIENT_ID = 'f216308e304c4ba3be3fb4ce0f23ceb9'
# CLIENT_SECRET = '44a9e6e761f94ceaaa8a09e607f292b5'

# Configurar a autenticação Auth do Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri="http://localhost:8888/callback"))

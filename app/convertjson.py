import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spoty_auth

sp = spoty_auth.sp


def obter_nome_e_imagem(artist_id):
    try:
        artist_info = sp.artist(artist_id)
        artist_name = artist_info['name']

        image_url = None
        if artist_info['images']:
            image_url = artist_info['images'][0]['url']

        return artist_name, image_url
    except Exception as e:
        print(f"Erro ao buscar informações para o artista com ID {artist_id}: {str(e)}")
        return None, None


input_csv = '../GRAFO_JSON/grafo_nodes.csv'
output_csv = '../GRAFO_JSON/artistas_com_info.csv'


with open(input_csv, 'r', newline='', encoding='utf-8') as csv_in, \
        open(output_csv, 'w', newline='', encoding='utf-8') as csv_out:
    reader = csv.reader(csv_in)
    writer = csv.writer(csv_out)

    writer.writerow(['ID', 'Nome', 'Imagem'])

    for row in reader:
        artist_id = row[0]

        artist_name, image_url = obter_nome_e_imagem(artist_id)

        writer.writerow([artist_id, artist_name, image_url])

import json
import networkx as nx
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import deque
import spoty_auth

# ... Configuração de credenciais e autenticação do Spotify ...



# Configurar a autenticação OAuth do Spotify
sp = spoty_auth.sp
# Função para criar um grafo de artistas relacionados usando busca em profundidade (DFS)
def criar_grafo_artistas_relacionados(artist_name, max_depth):
    # Inicializa um grafo vazio
    G = nx.Graph()
    # Conjunto para rastrear artistas já visitados
    artistas_visitados = set()
    # Pilha para a busca em profundidade (DFS) com informações de profundidade
    pilha = [(artist_name, 0)]  # Inicializa com profundidade 0 para o artista inicial

    # Realiza a busca em profundidade (DFS)
    while pilha:
        # Remove o próximo artista e profundidade da pilha
        current_artist, current_depth = pilha.pop()

        # Verifica se a profundidade atual é menor ou igual à profundidade máxima
        if current_depth <= max_depth:
            # Verifica se o artista atual já foi visitado para evitar visitas duplicadas.
            if current_artist not in artistas_visitados:
                # Adiciona o artista atual à lista de artistas visitados.
                artistas_visitados.add(current_artist)

                # Tenta pesquisar por informações do artista no Spotify
                try:
                    artist_info = sp.search(q=f'artist:{current_artist}', type='artist', limit=1)['artists']['items'][0]
                    artist_id = artist_info['id']
                    artist_image = artist_info['images'][0]['url']
                    artist_name = artist_info['name']

                    # Adiciona o nó ao grafo com as informações do artista
                    G.add_node(artist_id, name=artist_name, image=artist_image, id=artist_id)

                    # Obtém artistas relacionados
                    related_artists = sp.artist_related_artists(artist_id)

                    # Itera sobre os artistas relacionados encontrados.
                    for related_artist in related_artists['artists']:
                        related_artist_name = related_artist['name']
                        related_artist_id = related_artist['id']
                        
                        # Adiciona uma aresta entre o artista atual e os relacionados
                        G.add_edge(artist_id, related_artist_id)
                        # Adiciona o artista relacionado à pilha com profundidade aumentada em 1 para continuar a busca em profundidade (DFS)
                        pilha.append((related_artist_name, current_depth + 1))
                except IndexError:
                    # Caso nenhum resultado seja encontrado, continue com o próximo artista na pilha
                    pass

    return G

# Função para salvar o grafo em formato JSON
def salvar_grafo_para_json(grafo, nome_arquivo):
    data = nx.node_link_data(grafo)
    with open(nome_arquivo, 'w') as arquivo_json:
        json.dump(data, arquivo_json, indent=4)

def plotar_grafo_expandido(grafo):
    # Define o tamanho da figura (largura x altura) conforme necessário
    plt.figure(figsize=(12, 9))
    
    # Layout do grafo (usando o Kamada-Kawai para uma visualização melhor)
    pos = nx.kamada_kawai_layout(grafo)
    
    # Desenha o grafo com rótulos, tamanho de nó maior e cores personalizadas
    nx.draw(grafo, pos, with_labels=True, node_size=200, node_color='lightblue', font_size=10, font_color='black')
    
    # Aumenta o tamanho da fonte dos rótulos dos nós para torná-los mais legíveis
    labels = nx.get_node_attributes(grafo, 'label')
    nx.draw_networkx_labels(grafo, pos, labels, font_size=12)
    
    # Exibe o gráfico sem eixos
    plt.axis('off')
    plt.show()

# Exemplo de uso
artista_inicial = 'Oasis'
profundidade_maxima = 2  # Limite a profundidade desejada aqui
# Cria o grafo de artistas relacionados com a profundidade especificada usando busca em profundidade (DFS)
grafo_artistas = criar_grafo_artistas_relacionados(artista_inicial, max_depth=profundidade_maxima)
# Salva o grafo em um arquivo JSON
nome_arquivo_json = './../GRAFO_JSON/grafo_id_'+ artista_inicial.replace( " ", "_")+'_dfs.json'
salvar_grafo_para_json(grafo_artistas, nome_arquivo_json)

# Plota o grafo de forma expandida
plotar_grafo_expandido(grafo_artistas)
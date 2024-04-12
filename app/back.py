from flask import Flask, jsonify
from neo4j import GraphDatabase
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))


def obter_artistas_ids():
    query = "MATCH (a:Node) RETURN a.id AS artist_id"

    with driver.session() as session:
        result = session.run(query)
        artistas_ids = [record["artist_id"] for record in result]

    return artistas_ids


@app.route('/artist_ids')
def artist_ids():
    artistas_ids = obter_artistas_ids()
    return jsonify({'artist_ids': artistas_ids})


def menor_caminho(artist_id1, artist_id2):
    with driver.session() as session:
        result = session.run("""
            MATCH path = shortestPath((a1:Node {id: $artist_id1})<-[:LINK*]->(a2:Node {id: $artist_id2}))
            RETURN [node in nodes(path) | {id: node.id, nome: node.nome, imagem_url: node.imagem_url}] AS path
            """, artist_id1=artist_id1, artist_id2=artist_id2)
        shortest_path = result.single()["path"]
        return shortest_path


@app.route('/shortest_path/<artist_id1>/<artist_id2>')
def shortest_path(artist_id1, artist_id2):
    path = menor_caminho(artist_id1, artist_id2)
    return jsonify({'path': path})


def buscar_imagem_do_artista(artist_id):
    try:
        query = "MATCH (a:Node {id: $artist_id}) RETURN a.imagem_url AS image_url"
        with driver.session() as session:
            result = session.run(query, artist_id=artist_id)
            image_url = result.single()["image_url"]
        return image_url
    except Exception as e:
        return str(e)


def buscar_nome_do_artista(artist_id):
    try:
        query = "MATCH (a:Node {id: $artist_id}) RETURN a.nome AS artist_name"
        with driver.session() as session:
            result = session.run(query, artist_id=artist_id)
            artist_name = result.single()["artist_name"]
        return artist_name
    except Exception as e:
        return str(e)


@app.route('/artist_image/<artist_id>')
def get_artist_image(artist_id):
    image_url = buscar_imagem_do_artista(artist_id)
    return jsonify({'image_url': image_url})


@app.route('/artist_name/<artist_id>')
def get_artist_name(artist_id):
    artist_name = buscar_nome_do_artista(artist_id)
    return jsonify({'artist_name': artist_name})


if __name__ == '__main__':
    app.run(debug=True, port=5001)

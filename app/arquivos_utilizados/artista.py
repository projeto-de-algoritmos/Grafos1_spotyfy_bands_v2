from neo4j import GraphDatabase


def carregar_nos(session, arquivo_csv):
    with open(arquivo_csv, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            node_id, nome, imagem_url = [value.strip() for value in line.split(';')]
            query = "CREATE (:Node {id: $node_id, nome: $nome, imagem_url: $imagem_url})"
            session.run(query, node_id=node_id, nome=nome, imagem_url=imagem_url)


def carregar_arestas(session, arquivo_csv):
    with open(arquivo_csv, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            source_id, target_id = line.strip().split(',')
            query = "MATCH (source:Node {id: $source_id}), (target:Node {id: $target_id}) " \
                    "CREATE (source)-[:LINK]->(target)"
            session.run(query, source_id=source_id, target_id=target_id)


uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))


with driver.session() as session:
    carregar_nos(session, 'artistas_com_info.csv')
    carregar_arestas(session, 'grafo_links.csv')


driver.close()

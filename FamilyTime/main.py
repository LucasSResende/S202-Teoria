from database import Graph

graph = Graph(uri='bolt://54.146.184.100:7687', user='neo4j', password='buoys-shore-theories')


# CRIANDO OS NÓS

def criar_nos():
    query = [
        'CREATE (:PESSOA:CONTADORA{nome:"Rose", sexo:"F", idade:"58"})',
        'CREATE (:PESSOA:ENGENHEIRO{nome:"Lucas", sexo:"M", idade:"34"})',
        'CREATE (:PESSOA:PSICOLOGO{nome:"William", sexo:"M", idade:"34"})',
        'CREATE (:PESSOA:ESTUDANTE{nome:"Cecilia", sexo:"F", idade:"18"})',
        'CREATE (:PESSOA:APOSENTADA{nome:"Maria", sexo:"F", idade:"84"})',
        'CREATE (:PESSOA:PROFESSORA{nome:"Luzia", sexo:"F", idade:"70"})',
		'CREATE (:PESSOA:INTERDITADA{nome:"Fátima", sexo:"F", idade:"65"})',
        'CREATE (:PESSOA:TECNICO_MECANICO{nome:"Celso", sexo:"M", idade:"70"})',
        'CREATE (:PESSOA:ADMINISTRADORA{nome:"Gisele", sexo:"F", idade:"38"})',
        'CREATE (:PET:DOG{nome:"Menina", sexo:"F", brinquedo:"galinha de borracha"})',
        'CREATE (:PET:CAT{nome:"Clew", sexo:"M", brinquedo:"vara de pescar"})'
    ]
    for q in query:
        graph.write(query=q)


# CRIANDO OS RELACIONAMENTOS
def criar_relacionamentos():
    query = [
        'MATCH (p:PESSOA:CONTADORA),(p1:PESSOA:ENGENHEIRO)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:CONTADORA),(p1:PESSOA:ESTUDANTE)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:ENGENHEIRO),(p1:PESSOA:PSICOLOGO)CREATE (p)-[:BOYFRIEND_OF{since:"12/2021"}]->(p1)',
        'MATCH (p:PESSOA:PSICOLOGO),(p1:PESSOA:ADMINISTRADORA)CREATE (p)-[:BROTHER_OF]->(p1)',
		'MATCH (p:PESSOA:INTERDITADA),(p1:PESSOA:PSICOLOGO)CREATE (p)-[:AUNT_OF]->(p1)',
        'MATCH (p:PESSOA:ENGENHEIRO),(p1:PESSOA:ESTUDANTE)CREATE (p)-[:BROTHER_OF]->(p1)',
        'MATCH (p:PESSOA:PROFESSORA),(p1:PESSOA:PSICOLOGO)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:PROFESSORA),(p1:PESSOA:ADMINISTRADORA)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:APOSENTADA),(p1:PESSOA:CONTADORA)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:PROFESSORA),(p1:PESSOA:TECNICO_MECANICO)CREATE (p)-[:MARRIED_OF{since:"1982"}]->(p1)',
        'MATCH (p:PESSOA:TECNICO_MECANICO),(p1:PESSOA:ADMINISTRADORA)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:TECNICO_MECANICO),(p1:PESSOA:PSICOLOGO)CREATE (p)-[:PARENT_OF]->(p1)',
        'MATCH (p:PESSOA:ESTUDANTE),(d:PET:DOG) CREATE (p)-[:OWNER_OF]->(d)',
        'MATCH (p:PESSOA:PSICOLOGO),(c:PET:CAT) CREATE (p)-[:OWNER_OF]->(c)'
    ]
    for q in query:
        graph.write(query=q)


# LIMPANDO GRAFO
def limpar_grafo():
    graph.execute_query("MATCH(n) DETACH DELETE n;")


# EXECUTANDO
def executar():
    limpar_grafo()
    criar_nos()
    criar_relacionamentos()


executar()

# buscar no grafo para responder no mínimo 3 perguntas

# QUEM É ENGENHEIRO?
query = 'MATCH(p:ENGENHEIRO) RETURN COLLECT(p.nome) AS Engenheiro'
result = graph.read(query)
for r in result:
    print(r)

# QUEM É PAI DE QUEM?
query = 'MATCH(p:PESSOA)-[:PARENT_OF]->(p1:PESSOA) RETURN p1.nome AS Filho, COLLECT(p.nome) AS Pais;'
result = graph.read(query)
for r in result:
    print(r)

# WILLIAM NAMORA COM QUEM DESDE QUANDO?
query = 'MATCH(p:PESSOA)<-[r:BOYFRIEND_OF]-(p1:PESSOA:ENGENHEIRO) WHERE p.nome="William" RETURN p1.nome AS NAMORADO, r.since AS Desde;'
result = graph.read(query)
for r in result:
    print(r)

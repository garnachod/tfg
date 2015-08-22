from Neo4j.ConexionNeo4j import ConexionNeo4j
if __name__ == '__main__':
	grafo = ConexionNeo4j().getGraph()
	query = "MATCH (n) return n"
	objetos = grafo.cypher.execute(query)
	fOutNodes = open("nodes.csv", "w")
	fOutEdges = open("edges.csv", "w")

	for objeto in objetos:
		fOutNodes.write(str(objeto[0].properties["id_twitter"]))
		fOutNodes.write("\n")
	

	query = "MATCH (a)-[r]->(b) return a,r,b"
	objetos = grafo.cypher.execute(query)
	for objeto in objetos:
		fOutEdges.write(str(objeto[0].properties["id_twitter"]))
		fOutEdges.write(";")
		fOutEdges.write(str(objeto[2].properties["id_twitter"]))
		fOutEdges.write("\n")

	fOutNodes.close()
	fOutEdges.close()
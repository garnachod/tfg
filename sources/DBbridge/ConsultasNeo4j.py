from Neo4j.ConexionNeo4j import ConexionNeo4j
from blist import blist
from py2neo import cypher

class ConsultasNeo4j(object):
	"""docstring for ConsultasNeo4j"""
	def __init__(self):
		super(ConsultasNeo4j, self).__init__()
		self.graph = ConexionNeo4j().getGraph()

	def getListaIDsSeguidoresByUserID(self, user_id):
		queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user {id_twitter : {ID}}) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

	def getListaIDsSiguendoByUserID(self, user_id):
		queryNeo4j = "MATCH (u:user {id_twitter : {ID}})-[r:FOLLOW]->(a) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

	def getListaIDsFavsByUserID(self, user_id):
		queryNeo4j = "MATCH (u:user {id_twitter : {ID}})-[r:FAV]->(a:tweet) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_twitter"]))

		return identificadores

		
if __name__ == '__main__':
	consultas = ConsultasNeo4j()
	#funcionando
	print consultas.getListaIDsSeguidoresByUserID(2383366169)

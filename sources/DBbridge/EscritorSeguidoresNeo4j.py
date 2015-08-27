from Escritor import Escritor
from Neo4j.ConexionNeo4j import ConexionNeo4j
from py2neo import Node, Relationship, cypher
from ConsultasGeneral import ConsultasGeneral
import time 

class EscritorSeguidoresNeo4j(Escritor):
	"""docstring for EscritorSeguidoresNeo4j"""
	def __init__(self, searchID):
		super(EscritorSeguidoresNeo4j, self).__init__(searchID)
		self.graph = ConexionNeo4j().getGraph()
		self.consultas = ConsultasGeneral()

		
	def escribe(self, data):
		nodos_crear = []
		relaciones_crear = []
		## datos y filtros antes de realizar las escrituras
		query = self.consultas.getQueryFromSearchID(self.searchID)
		if query == False:
			return

		if query[0] == "@":
			query = query[1:]

		user_id = -1
		try:
			user_id = long(query)
			print user_id
		except Exception, e:
			user_id = self.consultas.getUserIDByScreenName(query)
		
		if user_id == -1 or user_id is None:
			return
		
		##################################################
		## usuario a crear relaciones
		nodos_crear.append(user_id)
		
		################################
		## Bucle que recorre todos los seguidores
		for identificador in data:
			nodos_crear.append(identificador)
			
		self.write(nodos_crear, data, user_id)

	def write(self, nodos_crear, todos_nodos_ids, nodo_principal_id):
		tx = self.graph.cypher.begin()
		
		for i, nodoCrea in enumerate(nodos_crear):
			query = "MERGE (n:user {id_twitter:" +str(nodoCrea) +"})"
			tx.append(query)
			if i % 100 == 0:
				tx.process()
		tx.process()
		tx.commit()

		#########################
		## Una vez tenemos los nodos se crea el camino si no existe
		#print "usuarios creados"
		
		tx = self.graph.cypher.begin()
		for i, identificador in enumerate(todos_nodos_ids):
			query = "MATCH (np { id_twitter: "+str(nodo_principal_id)+" }),(nf { id_twitter: "+str(identificador)+"}) MERGE (nf)-[r:FOLLOW]->(np) ON CREATE SET r.since = timestamp()" 
			#query = "MATCH (np { id_twitter: "+str(nodo_principal_id)+" }),(nf { id_twitter: "+str(identificador)+"}) CREATE UNIQUE (nf)-[r:FOLLOW {since:"+str(time.time())+"}]->(np)"			
			tx.append(query)
			if i % 50 == 0:
				tx.process()
		tx.process()
		tx.commit()
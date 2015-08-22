from Escritor import Escritor
from Neo4j.ConexionNeo4j import ConexionNeo4j
from py2neo import Node, Relationship
from ConsultasGeneral import ConsultasGeneral
import time 

class EscritorSeguidoresNeo4j(Escritor):
	"""docstring for EscritorSeguidoresNeo4j"""
	def __init__(self, searchID):
		super(EscritorSeguidoresNeo4j, self).__init__(searchID)
		self.graph = ConexionNeo4j().getGraph()
		self.consultas = ConsultasGeneral()
		
	def escribe(self, data):
		## datos y filtros antes de realizar las escrituras
		query = self.consultas.getQueryFromSearchID(self.searchID)
		if query == False:
			return

		if query[0] == "@":
			query = query[1:]

		user_id = self.consultas.getUserIDByScreenName(query)
		
		if user_id == -1 or user_id is None:
			return
		##################################################
		## usuario a crear relaciones
		user_node = self.graph.find_one('user',
                             property_key='id_twitter',
                             property_value=user_id)
		if user_node is None:
			try:
				user_node = Node("user", id_twitter=user_id)
				self.graph.create(user_node)
			except Exception, e:
				print e
		################################
		## Bucle que recorre todos los seguidores
		for identificador in data:
			## nodo seguidor
			follower_node = self.graph.find_one('user',
                             property_key='id_twitter',
                             property_value=identificador)

			if follower_node is None:
				try:
					follower_node = Node("user", id_twitter=identificador)
					self.graph.create(follower_node)
				except Exception, e:
					print e
			#########################
			## Una vez tenemos los nodos se crea el camino si no existe
			follower_follow_user = self.graph.match_one(start_node=follower_node, end_node=user_node)
			if follower_follow_user is None:
				follower_follow_user = Relationship(follower_node, "FOLLOW", user_node, since=time.time())
				try:
					self.graph.create_unique(follower_follow_user)
				except Exception, e:
					print e
			###########################################################
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
		#graph.cypher.execute("CREATE (c:Person {name:{N}}) RETURN c", {"N": "Carol"})
		query = self.consultas.getQueryFromSearchID(self.searchID)
		if query == False:
			return

		if query[0] == "@":
			query = query[1:]

		user_id = self.consultas.getUserIDByScreenName(query)
		
		if user_id == -1 or user_id is None:
			return


		#query_create_user = "CREATE (c:user {id_twitter:{ID}})"
		user_node = Node("user", id_twitter=user_id)
		try:
			#user_node = graph.create("CREATE (c:user {id_twitter:{ID}})
			self.graph.create(user_node)
		except Exception, e:
			user_node = self.graph.find_one('user',
                             property_key='id_twitter',
                             property_value=user_id)
			#statement = "MATCH (n:user {id_twitter:{ID}}) RETURN n"
			#user_node_ext = self.graph.cypher.execute(statement, {"ID":user_id})[0]

			print user_node
			#print user_node.graph
		
		for identificador in data:
			follower_node = Node("user", id_twitter=identificador)
			try:
				self.graph.create(follower_node)
			except Exception, e:
				follower_node = self.graph.find_one('user',
                             property_key='id_twitter',
                             property_value=identificador)
				#statement = "MATCH (n:user {id_twitter:{ID}}) RETURN n"
				#follower_node = self.graph.cypher.execute(statement, {"ID":identificador})[0]
				#print follower_node.graph

			follower_follow_user = self.graph.match_one(start_node=follower_node, end_node=user_node)
			if follower_follow_user is None:
				follower_follow_user = Relationship(follower_node, "FOLLOW", user_node, since=time.time())
				try:
					self.graph.create_unique(follower_follow_user)
				except Exception, e:
					print e
				#print follower_follow_user.graph
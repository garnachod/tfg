from Escritor import Escritor
from PostgreSQL.ConexionSQL import ConexionSQL
class EscritorBusquedaTweets(Escritor):
	"""docstring for EscritorTweets"""
	def __init__(self, searchID):
		super(EscritorBusquedaTweets, self).__init__(searchID)
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()

	def escribe(self, data):
		for tweet in data:
			id_api_twitter = tweet["id"]
			self.insertaJoinTable(self.searchID, id_api_twitter)

	def insertaJoinTable(self, id_search, id_tweet):
		query = """INSERT INTO join_search_tweet (id_search, id_tweet) SELECT %s, %s
					WHERE NOT EXISTS (SELECT * FROM join_search_tweet WHERE id_search=%s AND id_tweet=%s);"""
		try:
			self.cur.execute(query, [id_search, id_tweet, id_search, id_tweet])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en insertaJoinTable Twitter"
			print str(e)
			return False
from Cassandra.ConexionCassandra import ConexionCassandra
import codecs

class ConsultasCassandra(object):
	"""docstring for ConsultasCassandra"""
	def __init__(self):
		super(ConsultasCassandra, self).__init__()
		self.session_cassandra = ConexionCassandra().getSession()
		
	def getTweetsUsuarioCassandra(self, twitterUser, use_max_id=False, max_id=0, limit=1000):
		user_id = self.getUserIDByScreenNameCassandra(twitterUser)
		if user_id is None:
			return []

		query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls FROM tweets WHERE tuser = %s LIMIT %s;"""

		try:
			return self.session_cassandra.execute(query, [user_id, limit])
		except Exception, e:
			print e
			return []
		
	def getUserIDByScreenNameCassandra(self, twitterUser):
		query = """SELECT id_twitter FROM users WHERE screen_name = %s LIMIT 1;"""
		try:
			return long(self.session_cassandra.execute(query, [twitterUser])[0].id_twitter)
		except Exception, e:
			return None

	def getLastTweetCollectedScreenNameCassandra(self, twitterUser):
		query = """SELECT last_tweet_collected FROM users WHERE screen_name = %s LIMIT 1;"""
		try:
			return long(self.session_cassandra.execute(query, [twitterUser])[0].last_tweet_collected)
		except Exception, e:
			print e
			return 0
	
	def setLastTweetCollectedScreenNameCassandra(self, twitterUser, maximo):
		user_id = self.getUserIDByScreenNameCassandra(twitterUser)
		query = "UPDATE users SET last_tweet_collected = %s WHERE id_twitter = %s;"
		try:
			self.session_cassandra.execute(query, (maximo, user_id))
			return True
		except Exception, e:
			print e
			return False


	"""PRUEBAS"""
	def getTweetsUserAndPrintFile(self, filename, twitterUser):
		"""obtiene los tweets y los imprime en un fichero para que se puedan hacer pruebas con los textos"""
		fOut = codecs.open(filename, "w", "utf-8")
		tweets = self.getTweetsUsuarioCassandra(twitterUser, limit=10000)
		for tweet in tweets:
			texto = tweet.status
			texto = texto.replace("\n", " ")
			fOut.write(texto)
			fOut.write("\n")

		fOut.close()

if __name__ == '__main__':
	consultas = ConsultasCassandra()
	print "test de getUserIDByScreenNameCassandra"
	print consultas.getUserIDByScreenNameCassandra("WillyrexYT")
	print "test de getTweetsUsuarioCassandra"
	print consultas.getTweetsUsuarioCassandra("WillyrexYT", limit=10000)[0]
	#print "test de setLastTweetCollectedScreenNameCassandra"
	#print consultas.setLastTweetCollectedScreenNameCassandra("WillyrexYT", 0)
	print "test de getLastTweetCollectedScreenNameCassandra"
	print consultas.getLastTweetCollectedScreenNameCassandra("WillyrexYT")

	testCompleto = False
	if testCompleto == True:
		arrayUsuarios = ["WillyrexYT", "Alvaro845", "Thetoretegg", "Fernanfloo", "Nestle_es", "yuyacst", "AlexMonthy", "Wigetta", "Xodaaaa", "Gameloft_Spain", "NexxuzHD", "AudazCarlos", "xPekeLoL", "steam_games", "vegetta777", "bysTaXx", "bysTaXx", "PlayStationES", "mangelrogel", "Outconsumer"]
		for usuario in arrayUsuarios:
			consultas.getTweetsUserAndPrintFile("/home/dani/ficherosPrueba_plsa/"+usuario+".txt",usuario)
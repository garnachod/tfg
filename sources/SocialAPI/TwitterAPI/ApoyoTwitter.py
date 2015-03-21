from DBbridge.ConexionSQL import ConexionSQL

class ApoyoTwitter(object):
	"""docstring for ApoyoTwitter"""
	def __init__(self):
		super(ApoyoTwitter, self).__init__()
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()

	def getLastTweetCollected(self, screen_name):
		if screen_name[0] == '@':
			screen_name = screen_name[1:]

		query = "SELECT last_tweet_collected FROM users WHERE screen_name=%s;"
		try:
			self.cur.execute(query, [screen_name, ])
			row = self.cur.fetchone()
			if row is None:
				return 0
			if row[0] is None:
				return 0
			return row[0]
		except Exception, e:
			print str(e)
			return 0
		

	def setLastUserTweet(self, screen_name, maximo):
		if screen_name[0] == '@':
			screen_name = screen_name[1:]

		query = "UPDATE users SET last_tweet_collected=%s WHERE screen_name=%s;"
		try:
			self.cur.execute(query, [maximo, screen_name])
			self.conn.commit()

			return True
		except Exception, e:
			print str(e)
			return False
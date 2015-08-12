from PostgreSQL.ConexionSQL import ConexionSQL 

class ConsultasSQL(object):
	"""docstring for ConsultasSQL"""
	def __init__(self):
		super(ConsultasSQL, self).__init__()
		conSql = ConexionSQL()
		self.conn_sql = conSql.getConexion()
		self.cur_sql = conSql.getCursor()


	def getTweetsUsuarioSQL(self, twitterUser, use_max_id=False, max_id=0, limit=1000):
		if use_max_id == True:
			query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name FROM tweets as t, users as u WHERE u.screen_name = %s and u.id_twitter = t.tuser order by t.created_at DESC LIMIT %s;"
			try:
				self.cur_sql.execute(query, [twitterUser, ])
				row = self.cur_sql.fetchall()
				
				return row
			except Exception, e:
				print str(e)
				return False
		else:
			query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name FROM tweets as t, users as u WHERE u.screen_name = %s and u.id_twitter = t.tuser order by t.created_at DESC LIMIT %s;"
			try:
				self.cur_sql.execute(query, [twitterUser, limit])
				row = self.cur_sql.fetchall()
				
				return row
			except Exception, e:
				print str(e)
				return False
		
	def getUserIDByScreenNameSQL(self, twitterUser):
		query = "SELECT id_twitter FROM users WHERE screen_name = %s LIMIT 1;"

		try:
			self.cur_sql.execute(query, [twitterUser,])
			row = self.cur_sql.fetchone()
			
			return row[0]
		except Exception, e:
			print str(e)
			return 0

	def getLastTweetCollectedScreenNameSQL(self, screen_name):
		query = "SELECT last_tweet_collected FROM users WHERE screen_name=%s;"
		try:
			print screen_name
			self.cur.execute(query, [screen_name, ])
			row = self.cur.fetchone()
			if row is None:
				return 0
			if row[0] is None:
				return 0

			#print long(row[0])
			return long(row[0])
		
		except Exception, e:
			print str(e)
			return 0

	def setLastTweetCollectedScreenNameSQL(self, screen_name, maximo):
		query = "UPDATE users SET last_tweet_collected=%s WHERE screen_name=%s;"
		try:
			self.cur.execute(query, [maximo, screen_name])
			self.conn.commit()

			return True
		except Exception, e:
			print str(e)
			return False
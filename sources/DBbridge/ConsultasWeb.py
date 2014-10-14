from ConexionSQL import ConexionSQL

class ConsultasWeb():
	"""docstring for ConsultasWeb"""
	def __init__(self):
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()
		
	def getUserConexionData(self, username):
		query = "SELECT username, pasw, id FROM app_users WHERE username = %s"

		try:
			self.cur.execute(query, [username, ])
			row = self.cur.fetchone()

			user = row[0]
			pasword = row[1]
			user_id = row[2]

			return user, pasword, user_id
			
		except Exception, e:
			return None, None, None
		
	def isAdministrator(self, user_id):
		query = "SELECT role FROM app_users WHERE id = %s"
		try:
			self.cur.execute(query, [user_id, ])
			row = self.cur.fetchone()

			role = row[0]
			print role
			if role == "admin":
				return True
			else:
				return False
			
		except Exception, e:
			return False

	def insertNewUser(self, name, mail, inst, role, username, pasw):
		query = "INSERT INTO app_users (name,mail,institution,role,username,pasw) VALUES (%s,%s,%s,%s,%s,%s);"
		try:
			self.cur.execute(query, [name, mail, inst, role, username, pasw])
			self.conn.commit()
			return True
			
		except Exception, e:
			print str(e)
			return False

	def insertNewApiKey(self, apik, apiks, acstoken, acstokens, oauth):
		query = "INSERT INTO twitter_tokens (api_key,api_key_secret,access_token,access_token_secret,oauth) VALUES (%s,%s,%s,%s,%s);"
		try:
			self.cur.execute(query, [apik, apiks, acstoken, acstokens, oauth])
			self.conn.commit()
			return True
			
		except Exception, e:
			print str(e)
			return False

	def getTweetsUsuario(self, twitterUser):
		if twitterUser[0] == '@':
			twitterUser = twitterUser[1:]

		query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url FROM tweets as t, users as u WHERE u.screen_name = %s and u.id = t.tuser order by t.created_at DESC;"
		try:
			self.cur.execute(query, [twitterUser, ])
			row = self.cur.fetchall()
			
			return row
		except Exception, e:
			print str(e)
			return False

	def getTweetsTopics(self, topics):
		#SELECT * from tweets WHERE status LIKE '%beta%' or status LIKE '%@garnachod%'

		query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name "
		query += "FROM tweets as t, users as u "
		query += "WHERE ("
		i = 0
		for topic in topics:
			topics[i] = '%' + topic + '%'
			if i == 0:
				query += " status LIKE %s"
			else:
				query += " or status LIKE %s"
			i = i + 1

		query += "  ) and orig_tweet is null and (lang = 'es' or lang = 'en') and t.tuser = u.id order by t.created_at DESC LIMIT 2000;"
		print query
		print topics
		try:
			self.cur.execute(query, topics)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False
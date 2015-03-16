from ConexionSQL import ConexionSQL
from ConsultasGeneral import ConsultasGeneral

class ConsultasWeb(ConsultasGeneral): 
	"""docstring for ConsultasWeb"""
	def __init__(self):
		super(self.__class__, self).__init__()
		
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
			#print role
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

		query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name FROM tweets as t, users as u WHERE u.screen_name = %s and u.id = t.tuser order by t.created_at DESC;"
		try:
			self.cur.execute(query, [twitterUser, ])
			row = self.cur.fetchall()
			
			return row
		except Exception, e:
			print str(e)
			return False

	def getTweetsEntrenamientoListar(self, identificador):
		query = """SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name, t.id, te.clase 
				FROM tweets as t, users as u, tweets_entrenamiento as te , listas_entrenamiento as li
				WHERE te.clase != 'no_usar' and li.id = id_lista and li.id = %s and te.id_tweet = t.id and u.id = t.tuser order by te.id DESC;
				"""
		
		try:
			self.cur.execute(query, [identificador, ])
			rows = self.cur.fetchall()
			
			return rows
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
			if " " in topic:
				subtopics = topic.split(" ")
				topics[i] = '%'
				for subtopic in subtopics:
					topics[i] += subtopic + '%'
			else:
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

	def getTweetsAsincSearc(self, searchID, last_id, limit):
		query = "SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name, t.id "
		query+= "FROM tweets as t, users as u, join_search_tweet as j "
		query+= "WHERE t.id = j.id_tweet and t.tuser = u.id and j.id_search = %s "
		if last_id == 0:
			query+= "order by t.created_at DESC LIMIT %s;"
		else:
			query+= "and t.id > %s order by t.created_at DESC LIMIT %s;"

		try:
			if last_id == 0:
				self.cur.execute(query, [searchID, limit])
			else:
				self.cur.execute(query, [searchID, last_id, limit])

			rows = self.cur.fetchall()
			return rows

		except Exception, e:
			print str(e)
			return False

	

	def isFinishedAsincSearch(self, searchID):
		query = "SELECT search_time FROM app_searches WHERE id = %s LIMIT 1"
		try:
			print searchID
			self.cur.execute(query, [searchID, ])
			row = self.cur.fetchone()

			if row[0] is None:
				return False
			else:
				return True

		except Exception, e:
			print str(e)
			return False

	def setAppSearchAndGetId(self, search_string, user_id):
		query = "INSERT INTO app_searches (search_string, id_user) VALUES (%s,%s) RETURNING id;"
		try:
			self.cur.execute(query, [search_string, user_id])
			searchId = self.cur.fetchone()[0]
			self.conn.commit()

			return searchId
			
		except Exception, e:
			print str(e)
			return -1

	def altaTarea(self, tipo, id_search, tiempo, id_lista):
		query = "INSERT INTO tareas_programadas (tipo, id_search, tiempo_fin, id_lista_entrenamiento) VALUES (%s,%s,(CURRENT_TIMESTAMP + \'" + str(tiempo) + " days\'), %s)"
		try:
			self.cur.execute(query, [tipo, id_search, id_lista])
			self.conn.commit()

			return True
			
		except Exception, e:
			print str(e)
			return False

	def getTareasTerminadasListado(self):
		query = "SELECT t.id, tipo, tiempo_inicio, tiempo_fin, search_string from tareas_programadas as t, app_searches as a where t.tiempo_fin < CURRENT_TIMESTAMP and t.id_search = a.id;"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False


	def getTareasPendientesListado(self):
		query = "SELECT t.id, tipo, tiempo_inicio, tiempo_fin, search_string from tareas_programadas as t, app_searches as a where t.tiempo_fin > CURRENT_TIMESTAMP and t.id_search = a.id;"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	#seccion de estadisticas

	def getNumTweetsNoRT(self):
		query ="SELECT count(id) FROM tweets WHERE is_retweet = FALSE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsSiRT(self):
		query ="SELECT count(id) FROM tweets WHERE is_retweet = TRUE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsNoMedia(self):
		query ="SELECT count(id) FROM tweets WHERE media_url = '' and is_retweet = FALSE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsSiMedia(self):
		query ="SELECT count(id) FROM tweets WHERE media_url != '' and is_retweet = FALSE;"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getPorcentajeFalloTrainTweets(self):
		query = "SELECT porcentaje_fallo FROM entrenamientos WHERE tipo = 'tweet' order by fecha DESC LIMIT 1"
		try:
			self.cur.execute(query)
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	#fin seccion de estadisticas

	#resumen de tareas programadas
	def countTweetsRecuperadosTarea(self, identificador):
		query = "SELECT count(id_tweet) FROM join_search_tweet as j, tareas_programadas as t where t.id = %s and t.id_search = j.id_search"

		try:
			self.cur.execute(query, [identificador, ])
			num = self.cur.fetchone()[0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getTipoTarea(self, identificador):
		query = "SELECT tipo FROM tareas_programadas WHERE id = %s"

		try:
			self.cur.execute(query, [identificador, ])
			tipo = self.cur.fetchone()[0]
			
			return tipo
		except Exception, e:
			print str(e)
			return False

	def getTweetsAlDiaTarea(self, identificador):
		query = "SELECT created_at::DATE , count(*) from tweets as tw, join_search_tweet as j, tareas_programadas as t where t.id = %s and t.id_search = j.id_search and tw.id = j.id_tweet and tw.is_retweet = FALSE group by created_at::DATE order by created_at::DATE asc;"
		try:
			self.cur.execute(query, [identificador, ])
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTweetsAlDiaTareaAnalisis(self, identificador):
		query = """SELECT created_at::DATE , count(*) 
				   from tweets as tw, join_search_tweet as j, tareas_programadas as t, clasificaciontweets as c
				   where t.id = %s and t.id_search = j.id_search and c.id_tweet = j.id_tweet and c.clase = 'relevante' and tw.id = j.id_tweet and tw.is_retweet = FALSE group by created_at::DATE order by created_at::DATE asc;"""
		try:
			self.cur.execute(query, [identificador, ])
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTweetsRecuperadosTareaID(self, identificador):
		query =  """SELECT tw.status, tw.favorite_count, tw.retweet_count, tw.is_retweet, tw.media_url, u.screen_name 
					From tweets as tw, join_search_tweet as j, tareas_programadas as t , users as u
					where t.id = %s and t.id_search = j.id_search and tw.id = j.id_tweet and tw.is_retweet = FALSE and u.id = tw.tuser;
					"""

		try:
			self.cur.execute(query, [identificador, ])
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTweetsRecuperadosTareaAnalisisID(self, identificador):
		query =  """SELECT tw.status, tw.favorite_count, tw.retweet_count, tw.is_retweet, tw.media_url, u.screen_name 
					From tweets as tw, join_search_tweet as j, tareas_programadas as t , users as u, clasificaciontweets as c
					where t.id = %s and t.id_search = j.id_search and tw.id = j.id_tweet and c.id_tweet = j.id_tweet and c.clase = 'relevante' and tw.is_retweet = FALSE and u.id = tw.tuser;
					"""

		try:
			self.cur.execute(query, [identificador, ])
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getEstadisticaUsoAplicacionConsultas(self):
		query = """SELECT tiempo::DATE , count(*) 
				   from tokens_count 
				   where simulado=TRUE AND tiempo > (current_timestamp -  interval '31 days') group by tiempo::DATE order by tiempo::DATE asc;"""

		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False
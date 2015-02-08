from ConexionSQL import ConexionSQL

class ConsultasGeneral(object): 
	"""docstring for ConsultasGeneral"""
	def __init__(self):
		conSql = ConexionSQL()
		self.conn = conSql.getConexion()
		self.cur = conSql.getCursor()

	def setAppSearchTime(self, searchID, time):
		query = "UPDATE app_searches SET search_time=%s WHERE id=%s;"
		try:
			self.cur.execute(query, [time, searchID])
			self.conn.commit()

			return True
		except Exception, e:
			print str(e)
			return False

	def getTareasPendientesTotal(self):
		query = "SELECT * from tareas_programadas where tiempo_fin > CURRENT_TIMESTAMP"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def getTareasTerminadasTotal(self):
		query = "SELECT * from tareas_programadas where tiempo_fin < CURRENT_TIMESTAMP"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False


	def getBusquedaFromIdBusqueda(self, idbusqueda):
		query = "SELECT search_string, id_user FROM app_searches where id = %s;"
		try:
			self.cur.execute(query, [idbusqueda, ])
			row = self.cur.fetchone()
			print row[0]
			print row[1]

			return row[0], row[1]
		except Exception, e:
			print str(e)
			return False

	def getTweetDebugMachineLearning(self, identificador):
		query = "SELECT status FROM tweets WHERE id = %s;"
		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print str(e)
			return False

	def getTweetStatus(self, identificador):
		query = "SELECT status FROM tweets as t WHERE t.id = %s;"
		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()

			return row[0]
		except Exception, e:
			print str(e)
			return False

	def getIDTweetsTrainList(self):
		query = "SELECT id_tweet FROM tweets_entrenamiento as tw WHERE tw.clase != 'no_usar'"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()
			lista = []
			for row in rows:
				lista.append(row[0])

			return lista
		except Exception, e:
			print str(e)
			return False

	def getTweetsAndClassTrain(self):
		query = "SELECT status, clase FROM tweets as t, tweets_entrenamiento as tw WHERE t.id = tw.id_tweet and tw.clase != 'no_usar'"
		try:
			self.cur.execute(query)
			rows = self.cur.fetchall()

			return rows
		except Exception, e:
			print str(e)
			return False


	def getTweetIDLarge(self, identificador):
		query = """SELECT t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name 
				   FROM tweets as t, users as u 
				   WHERE t.id = %s and t.tuser = u.id LIMIT 1;"""
		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()

			return row
		except Exception, e:
			print str(e)
			return False

	def getIDsTweetsTrain(self, topics, limit):
		query = "SELECT t.id "
		query += "FROM tweets as t "
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

		query += "  ) and is_retweet = False and id not in (SELECT id_tweet FROM tweets_entrenamiento) and (lang = 'es' or lang = 'en') order by t.created_at DESC LIMIT %s;"

		parameters = list(topics)
		parameters.append(limit)
		try:
			self.cur.execute(query, parameters)
			rows = self.cur.fetchall()
			
			return rows
		except Exception, e:
			print str(e)
			return False

	def setTweetTrainID(self, identificador, clase):
		query = """INSERT INTO tweets_entrenamiento (id_tweet, clase)
       				SELECT %s, %s 
       				WHERE NOT EXISTS (SELECT id FROM tweets_entrenamiento WHERE id_tweet=%s);"""



		#query = "INSERT INTO tweets_entrenamiento (id_tweet,clase) VALUES (%s,%s);"

		try:
			self.cur.execute(query, [identificador, clase, identificador])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en setTweetTrainID"
			print str(e)
			return False

	def getClaseTrainID(self, identificador):
		query = """SELECT clase FROM tweets_entrenamiento WHERE id_tweet = %s;"""

		try:
			self.cur.execute(query, [identificador, ])
			row = self.cur.fetchone()
			if row is None:
				return False

			return row
		except Exception, e:
			print "error en getClaseTrainID"
			print str(e)
			return False

	def changeClaseTweet(self, identificador, clase):
		query = """UPDATE tweets_entrenamiento SET clase = %s WHERE id_tweet = %s;"""

		try:
			self.cur.execute(query, [clase, identificador])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en changeClaseTweet"
			print str(e)
			return False

	def creaEntrenamientoRetID(self, tipo):
		query = """INSERT INTO entrenamientos (tipo) VALUES (%s) RETURNING id;"""
		try:
			self.cur.execute(query, [tipo,])
			Id = self.cur.fetchone()[0]
			self.conn.commit()

			return Id
			
		except Exception, e:
			print str(e)
			return -1

	def editEntrenamiento(self, identificador, ficheroARFF, ficheroJSON, error):
		query = """UPDATE entrenamientos SET fichero_arff = %s, fichero_json = %s, porcentaje_fallo = %s WHERE id = %s;"""

		try:
			self.cur.execute(query, [ficheroARFF, ficheroJSON, error, identificador])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en editEntrenamiento"
			print str(e)
			return False

	def getFilesLastTrainTweet(self):
		query = "SELECT fichero_arff, fichero_json FROM entrenamientos WHERE tipo = 'tweet' and fichero_arff != '' ORDER BY id DESC LIMIT 1;"
		try:
			self.cur.execute(query)
			row = self.cur.fetchone()

			return row
		except Exception, e:
			print "error en getFilesLastTrainTweet"
			print str(e)
			return False

	def getTweetsIdBusquedaNoAnalizada(self, searchID):
		query = "SELECT j.id_tweet FROM join_search_tweet as j WHERE j.id_search = %s AND j.id_tweet NOT IN (SELECT c.id_tweet from clasificaciontweets as c)"
		try:
			self.cur.execute(query, [searchID, ])
			rows = self.cur.fetchall()

			return rows
		except Exception, e:
			print "error en getFilesLastTrainTweet"
			print str(e)
			return False
	def insertTweetAnalizado(self, id_tweet, clase):
		query = """INSERT INTO clasificaciontweets (id_tweet, clase) VALUES (%s, %s)"""
		try:
			self.cur.execute(query, [id_tweet, clase])
			self.conn.commit()

			return True
		except Exception, e:
			print "error en setTweetTrainID"
			print str(e)
			return False
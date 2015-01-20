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
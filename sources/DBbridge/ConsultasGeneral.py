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

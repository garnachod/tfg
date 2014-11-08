import psycopg2

class ConexionSQL(): 
	"""docstring for ConexionSQL"""
	def __init__(self):
		self.conn = psycopg2.connect(database="twitter", user="usrtwitter", password="postgres_tfg", host="localhost")
	def getConexion(self):
		return self.conn
	def getCursor(self):
		return self.conn.cursor()
		
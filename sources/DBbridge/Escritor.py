class Escritor(object):
	"""docstring for Escritor"""
	def __init__(self, conexionSQL, searchID):
		super(Escritor, self).__init__()
		self.conexionSQL = conexionSQL
		self.conn = self.conexionSQL.getConexion()
		self.cur = self.conexionSQL.getCursor()
		self.searchID = searchID

	def escribe(self, data):
		raise NotImplementedError( "Should have implemented this" )
		
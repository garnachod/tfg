
class TareaProgramada():
	#clase abstracta que define la funcionalidad posible de un tipo de tarea
	def __init__(self):
		self.identificador = 0
		self.tipo = ""
		self.search_id = 0

	def setId(self, identificador):
		self.identificador = identificador

	def setSearchID(self, search_id):
		self.search_id = search_id

	def doSearch(self):
		raise NotImplementedError( "Should have implemented this" )

	def doPostProc(self):
		raise NotImplementedError( "Should have implemented this" )

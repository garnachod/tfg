class Instances(object):
	"""docstring for Instances"""
	def __init__(self):
		super(Instances, self).__init__()
		self.clases = []
		self.columna = []
		self.columnaTipo = {}
		self.instances = []

	def setClases(self, clasesPar):
		self.clases = list(clasesPar)
	def addClase(self, clase):
		self.clases.append(clase)

	
		
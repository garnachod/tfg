import random
import math
class Instances(object):
	"""docstring for Instances"""
	def __init__(self):
		super(Instances, self).__init__()
		self.clases = []
		self.columnas = []
		self.columnaTipo = {}
		self.instances = []

	def setClases(self, clasesPar):
		self.clases = list(clasesPar)

	def addClase(self, clase):
		self.clases.append(clase)

	def getClases(self):
		return self.clases

	def getNumeroColumnas(self):
		return len(self.columnas)

	def getNumeroInstances(self):
		return len(self.instances)

	def addInstance(self, instance):
		self.instances.append(instance)
		instance.setInstances(self)

	def getListInstances(self):
		return self.instances
		
	def addColumna(self, nombreColumna, tipoColumna):
		self.columnas.append(nombreColumna)
		self.columnaTipo[nombreColumna] = tipoColumna

	def setColumnas(self, columnaList, columnaTipo):
		self.columnas = columnaList
		self.columnaTipo = columnaTipo

	def getColumnasTipo(self):
		return self.columnaTipo

	def getColumnasList(self):
		return self.columnas

	def getTipoColumnaByIndex(self, index):
		return self.columnaTipo[self.columnas[index]]

	def getTipoColumnaByNombre(self, nombre):
		return self.columnaTipo[nombre]

	def shuffle(self):
		random.shuffle(self.instances)

	def normaliza(self):
		media = []
		desv = []
		nColumnas = self.getNumeroColumnas()

		for i in range(0, nColumnas):
			media.append(0.0)
			desv.append(0.0)

		for instance in self.instances:
			for i in range(0, nColumnas):
				media[i] += instance.getElementAtPos(i)

		for i in range(0, nColumnas):
			media[i] = media[i]/float(self.getNumeroInstances())

		for instance in self.instances:
			for i in range(0, nColumnas):
				desv[i] += pow(instance.getElementAtPos(i) - media[i], 2)

		for i in range(0, nColumnas):
			desv[i] = desv[i]/float(self.getNumeroInstances())
			desv[i] = math.sqrt(desv[i])

		#normalizar
		for instance in self.instances:
			for i in range(0, nColumnas):
				elemento = instance.getElementAtPos(i)
				elemento = (elemento - media[i])/desv[i]
				instance.setElementAtPos(elemento, i)
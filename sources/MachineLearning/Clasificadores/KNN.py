from heapq import heappush, heappop
from Instance import Instance
from Instances import Instances
from operator import add,mul
import math

class KNN(object):
	"""docstring for Clasificador"""
	def __init__(self):
		super(KNN, self).__init__()
		self.vecinos = 5
		self.data = None

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""
	def setParameters(self, parametros):
		raise NotImplementedError( "Should have implemented this" )
		
	"""data es un array de instancias"""
	def buildClassifier(self, data):
		self.data = data

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instance):
		h = []
		#heappush(h, (5, 'clase'))
		#heappop(h)
		for instance_comp in self.data.getListInstances():
			#distancia = self.distanciaEuclideaCuadrado(instance, instance_comp)
			distancia = 1.0 - self.coseno(instance, instance_comp)
			#print distancia
			heappush(h, (distancia, instance_comp.getClase()))

		clases_rep = {}
		for i in range(0, self.vecinos):
			tupla = heappop(h)
			clase = tupla[1]
			if clase in clases_rep:
				clases_rep[clase] = clases_rep[clase] + 1
			else:
				clases_rep[clase] = 1

		mejor_clase = ""
		mejor_rep = 0
		for clase in clases_rep:
			if clases_rep[clase] > mejor_rep:
				mejor_rep = clases_rep[clase]
				mejor_clase = clase

		return mejor_clase


	def distanciaEuclideaCuadrado(self, instance, instance_comp):
		elem1 = list(instance.getAllElements())
		elem1.pop()
		elem2 = list(instance_comp.getAllElements())
		elem2.pop()

		return reduce(add, map((lambda x, y: (x-y)**2),elem1 ,elem2))

	def distanciaEuclideaCuadradoImprov(self, instance, instance_comp):
		elem1 = list(instance.getAllElements())
		elem1.pop()
		elem2 = list(instance_comp.getAllElements())
		elem2.pop()
		
		pesos = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

		return reduce(add, map((lambda x, y, z: ((x-y)*z)**2),elem1 ,elem2, pesos))

	def coseno(self, instance, instance_comp):
		elem1 = list(instance.getAllElements())
		elem1.pop()
		elem2 = list(instance_comp.getAllElements())
		elem2.pop()

		suma = reduce(add, map((lambda x, y: x * y ),elem1 ,elem2))
		modulo1 = math.sqrt(reduce(add, map((lambda x: x**2), elem1)))
		modulo2 = math.sqrt(reduce(add, map((lambda x: x**2), elem2)))
		return suma/float(modulo2 * modulo1)
		

	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		raise NotImplementedError( "Should have implemented this" )

	def restoreClassifierFromJSON(self, jsonObj):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )

	"""Hace que el clasificador entre en modo debug o no"""
	def setDebug(self, value):
		raise NotImplementedError( "Should have implemented this" )


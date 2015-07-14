import random
import math   # This will import math module
from src.Instance import Instance
from src.Instances import Instances
from operator import add,mul
from heapq import heappush, heappop

class IndividuoKNN(object):
	"""docstring for IndividuoKNN"""
	def __init__(self, len_pesos, data):
		super(IndividuoKNN, self).__init__()
		self.len_pesos = len_pesos
		self.data = data
		self.pesos = []
		self.probMutacion = 0.01
		self.probCruce = 0.5
		self.cantCambio = 0.2
		self.vecinos = 21

	def inicializaRandom(self):
		for i in range(0, self.len_pesos):
			self.pesos.append(random.random())
	
	def mutacion(self):
		for i in range(0, self.len_pesos):
			if random.random() <= self.probMutacion:
				if random.random() <= 0.5:
					if self.pesos[i] <= 0.0:
						self.pesos[i] = 0.0
					else:
						self.pesos[i] -= self.cantCambio
				else:
					self.pesos[i] += self.cantCambio


	def cruce(self, individuo):

		if random.random() <= self.probCruce:
			punto_cruce = random.randint(1, self.len_pesos - 1)
			arraypesosU = self.pesos
			arraypesosD = individuo.pesos
			arrayU, arrayD = self.cruzaUnPunto(arraypesosU, arraypesosD, punto_cruce, self.len_pesos)

			self.pesos = arrayU
			individuo.pesos = arrayD


	def cruzaUnPunto(self, arrayUno, arrayDos, punto, tam):
		arrayU = []
		arrayD = []

		for i in range(0, tam):
			if i < punto:
				arrayU.append(arrayUno[i])
				arrayD.append(arrayDos[i])
			else:
				arrayU.append(arrayDos[i])
				arrayD.append(arrayUno[i])

		return arrayU, arrayD
	

	def duplica(self):
		indv = IndividuoKNN(self.len_pesos, self.data)
		indv.pesos = list(self.pesos)
		return indv


	def clasifica(self, instance):
		h = []
		#heappush(h, (5, 'clase'))
		#heappop(h)
		for instance_comp in self.data.getListInstances():
			distancia = self.distanciaEuclideaCuadradoImprov(instance, instance_comp)
			#distancia = 1.0 - self.coseno(instance, instance_comp)
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


	def distanciaEuclideaCuadradoImprov(self, instance, instance_comp):
		elem1 = list(instance.getAllElements())
		elem1.pop()
		elem2 = list(instance_comp.getAllElements())
		elem2.pop()

		return reduce(add, map((lambda x, y, z: ((x-y)*z)**2),elem1 ,elem2, self.pesos))
		
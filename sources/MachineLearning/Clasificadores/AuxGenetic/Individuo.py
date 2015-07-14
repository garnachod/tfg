import random
import math   # This will import math module
from src.Instance import Instance
from src.Instances import Instances
class Individuo(object):
	"""docstring for Individuo"""
	def __init__(self, aClases, nColum):
		super(Individuo, self).__init__()
		self.nRepPorClase = 3
		self.nRepPorColumna = 1
		self.nColumnas = nColum
		self.nColumnasFin = nColum * self.nRepPorColumna
		self.clases = aClases
		self.nClasesTotal = len(aClases) * self.nRepPorClase
		self.matrizPesos = []
		self.arrayClases = []
		self.probMutacion = 0.6
		self.probCruce = 0.2

	def mutacion(self):
		for j in range(0,self.nClasesTotal):
			for i in range(0, self.nColumnasFin):
				if random.random() <= self.probMutacion:
					self.matrizPesos[j][i] += (random.random() - 0.5) 

	def cruce(self, individuo):

		for i in range(0, self.nClasesTotal):
			if random.random() <= self.probCruce:
				arraypesosU = self.matrizPesos[i]
				arraypesosD = individuo.matrizPesos[i]
				tam = self.nColumnasFin
				punto_cruce = random.randint(1, tam - 1)
				arrayU, arrayD = cruzaUnPunto(arraypesosU, arraypesosD, punto_cruce)

				self.matrizPesos[i] = arrayU
				individuo.matrizPesos[i] = arrayD
			else:
				pass

	def inicializaRandom(self):
		for j in range(0, self.nClasesTotal):
			self.matrizPesos.append([])
			for i in range(0, self.nColumnasFin):
				self.matrizPesos[j].append(random.random() - 0.5)

	def duplica(self):
		indv = Individuo(self.clases, self.nColumnas)
		for j in range(0, self.nClasesTotal):
			indv.matrizPesos.append(list(self.matrizPesos[j]))

		return indv

	"""
	def clasifica(self, instancia):
		mejorClase = 0
		mejorDatoClase = -100000000000
		arrayDatos = instancia.getAllElements()
		
		for j in range(0, self.nClasesTotal):
			suma = 0
			pesos = self.matrizPesos[j]
			for i in range(0, self.nColumnasFin):
				dato = arrayDatos[i % self.nColumnas]
				peso = pesos[i]
				suma += dato * peso

			if suma > mejorDatoClase:
				mejorClase = self.clases[j % len(self.clases)]
				mejorDatoClase = suma


		return mejorClase
	"""

	def clasifica(self, instancia):
		mejorClase = 0
		mejorDatoClase = -100000000000
		arrayDatos = instancia.getAllElements()

		probClase = {}

		for clase in self.clases:
			probClase[clase] = 0
		
		for j in range(0, self.nClasesTotal):
			suma = 0
			pesos = self.matrizPesos[j]
			for i in range(0, self.nColumnasFin):
				dato = arrayDatos[i % self.nColumnas]
				peso = pesos[i]
				suma += dato * peso

			acc = (2.0/(1.0 + math.exp( - suma))) - 1.0
			probClase[self.clases[j % len(self.clases)]] += acc

		for clase in probClase:
			if probClase[clase] > mejorDatoClase:
				mejorDatoClase = probClase[clase]
				mejorClase = clase
			


		return mejorClase


	def correctas(self, instancias):
		listaInstancias = instancias.getListInstances()
		nInstancias = instancias.getNumeroInstances()
		correctas = 0
		for instancia in listaInstancias:
			clase = self.clasifica(instancia)
			if clase == instancia.getClase():
				correctas += 1

		return correctas

def cruzaUnPunto(arrayUno, arrayDos, punto):
	arrayU = []
	arrayD = []

	for i in range(0, len(arrayUno)):
		if i < punto:
			arrayU.append(arrayUno[i])
			arrayD.append(arrayDos[i])
		else:
			arrayU.append(arrayDos[i])
			arrayD.append(arrayUno[i])

	return arrayU, arrayD
import random
import math   # This will import math module
from src.Instance import Instance
from src.Instances import Instances
from operator import add
class IndividuoNCapasECM(object):
	"""docstring for IndividuoNCapasECM"""
	def __init__(self, aClases, nColum):
		super(IndividuoNCapasECM, self).__init__()
		self.nRepPorClase = 3
		self.nRepPorColumna = 1
		self.nCapas = 2
		self.nColumnas = nColum
		self.nColumnasFin = nColum * self.nRepPorColumna
		self.clases = aClases
		self.nClases = len(aClases)
		self.matricesPesos = [[] for x in range(self.nCapas)]
		self.repeticionesPorCapa = [4, 1, 10, 1, 3, 3, 3, 3, 3, 3, 3]
		self.probMutacion = 0.6
		self.probCruce = 0.2

	def mutacion(self):
		for k in range(0, self.nCapas):
			nNeuronas = self.repeticionesPorCapa[k] * self.nClases
			if random.random() <= self.probMutacion:
				for j in range(0, nNeuronas):
					if k == 0:
						npesos = self.nColumnasFin
					else:
						npesos = self.repeticionesPorCapa[k-1] * self.nClases

					for i in range(0, npesos):
						if random.random() <= self.probMutacion:
							self.matricesPesos[k][j][i] += (random.random() - 0.5)

	def cruce(self, individuo):
		for k in range(0, self.nCapas):
			nNeuronas = self.repeticionesPorCapa[k] * self.nClases
			if random.random() <= self.probCruce:
				for j in range(0, nNeuronas):
					if random.random() <= self.probCruce:
						arraypesosU = self.matricesPesos[k][j]
						arraypesosD = individuo.matricesPesos[k][j]
						tam = self.nColumnasFin
						punto_cruce = random.randint(1, tam - 1)
						arrayU, arrayD = cruzaUnPunto(arraypesosU, arraypesosD, punto_cruce)

						self.matricesPesos[k][j] = arrayU
						individuo.matricesPesos[k][j] = arrayD
					else:
						pass


	def inicializaRandom(self):
		for k in range(0, self.nCapas):
			nNeuronas = self.repeticionesPorCapa[k] * self.nClases
			for j in range(0, nNeuronas):
				self.matricesPesos[k].append([])
				if k == 0:
					npesos = self.nColumnasFin
				else:
					npesos = self.repeticionesPorCapa[k-1] * self.nClases

				for i in range(0, npesos+1):
					self.matricesPesos[k][j].append(random.random() - 0.5)

	def duplica(self):
		indv = IndividuoNCapasECM(self.clases, self.nColumnas)
		for k in range(0, self.nCapas):
			nNeuronas = self.repeticionesPorCapa[k] * self.nClases
			for j in range(0, nNeuronas):
				indv.matricesPesos[k].append([])
				indv.matricesPesos[k][j] = list(self.matricesPesos[k][j])
		#for j in range(0, self.nClasesTotal):
			#indv.matrizPesos.append(list(self.matrizPesos[j]))

		return indv

	

	def clasifica(self, instancia):
		arrayDatos = instancia.getAllElements()

		probClase = {}

		for clase in self.clases:
			probClase[clase] = 0

		activEpocaAnterior = []
		for k in range(0, self.nCapas):
			#primera capa
			if k == 0:
				nNeuronas = self.repeticionesPorCapa[k] * self.nClases
				activEpocaAnterior = [1]
				for j in range(0, nNeuronas):
					suma = 0
					pesos = self.matricesPesos[k][j]
					for i in range(0, self.nColumnasFin+1):
						if i == 0:
							dato = 1
						else:
							dato = arrayDatos[i-1 % self.nColumnas]
						peso = pesos[i]
						suma += dato * peso

					acc = (2.0/(1.0 + math.exp( - suma))) - 1.0
					activEpocaAnterior.append(acc)
			#ultima capa
			if k == self.nCapas - 1:
				nNeuronas = self.repeticionesPorCapa[k] * self.nClases
				for j in range(0, nNeuronas):
					suma = 0
					pesos = self.matricesPesos[k][j]
					i = 0
					for dato in activEpocaAnterior:
						peso = pesos[i]
						suma += dato * peso
						i+=1

					acc = (2.0/(1.0 + math.exp( - suma))) - 1.0
					probClase[self.clases[j % len(self.clases)]] += acc

			#otra capa
			if k != self.nCapas - 1 and k != 0:
				nNeuronas = self.repeticionesPorCapa[k] * self.nClases
				actvEpoca = [1]
				for j in range(0, nNeuronas):
					suma = 0
					pesos = self.matricesPesos[k][j]
					i = 0
					for dato in activEpocaAnterior:
						peso = pesos[i]
						suma += dato * peso
						i+=1

					acc = (2.0/(1.0 + math.exp( - suma))) - 1.0
					actvEpoca.append(acc)

				activEpocaAnterior = actvEpoca

		vectorProb = []
		for clase in self.clases:
			vectorProb.append(probClase[clase])

		ecmInstancia = reduce(add, map((lambda x, y: (x - y)**2), instancia.getBipolarVectorObjetivoSalida(self.clases), vectorProb))

		mejorDatoClase = -100000000000
		mejorClase = 0
		for clase in probClase:
			if probClase[clase] > mejorDatoClase:
				mejorDatoClase = probClase[clase]
				mejorClase = clase
			


		return mejorClase, ecmInstancia


	def correctas(self, instancias):
		listaInstancias = instancias.getListInstances()
		nInstancias = instancias.getNumeroInstances()
		correctas = 0
		ecm = 0
		for instancia in listaInstancias:
			clase, ecmInstancia = self.clasifica(instancia)
			ecm += ecmInstancia
			if clase == instancia.getClase():
				correctas += 1

		return correctas, (ecm/nInstancias)

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
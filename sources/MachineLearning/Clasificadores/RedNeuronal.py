# -*- coding: utf-8 -*-
from MachineLearning.Instance import Instance
from MachineLearning.Instances import Instances
from Clasificador import Clasificador
from operator import add,mul
from MachineLearning.Particionado.DivisionPorcentual import DivisionPorcentual
from MachineLearning.Particionado.Particion import Particion
import random
import math   # This will import math module
import json

class RedNeuronal(Clasificador):
	"""docstring for RedNeuronal"""
	def __init__(self):
		super(RedNeuronal, self).__init__()
		self.clases = []
		self.columnas = []
		self.nColumnas = 0
		self.nFilasTrain = 0
		self.nClases = 0
		self.capaEntrada = []
		self.pesosCapaOculta = []
		self.pesosCapaSalida = []
		self.neuronasCapaOculta = 20
		self.bipolar = True
		self.nEpocas = 1000
		self.alpha = 0.1
		self.porcentaje_validacion = 0.2
		self.debug = False
		self.debugFile = None
		self.debugFileName = "debugMLP.txt"
		self.activo_control_fin = False
		self.conjuntoValidacion = None
		self.lastError = 100;

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""

	"""nNeuronas=10"""
	"""alpha=0.1"""
	"""nEpocas=1000"""
	def setParameters(self, parametros):
		if '=' in parametros:
			cadenas = parametros.split('=')
			if cadenas[0] == 'nNeuronas':
				self.neuronasCapaOculta = int(cadenas[1])
			elif cadenas[0] == 'alpha':
				self.alpha = float(cadenas[1])
			elif cadenas[0] == 'nEpocas':
				self.nEpocas = int(cadenas[1])
			else:
				Exception('setParameters', 'Error en la introduccion de parametros')
		else:
			raise Exception('setParameters', 'Error en la introduccion de parametros')
		
	"""data es un objeto de tipo Instances"""
	def buildClassifier(self, data):
		self.clases = list(data.getClases())
		self.nClases = len(self.clases)
		self.columnas = list(data.getColumnasList())
		self.nColumnas = len(self.columnas)
		self.nFilasTrain = data.getNumeroInstances()

		if data.getNumeroInstances() >= 100:
			self.activo_control_fin = True
			particionado = DivisionPorcentual()
			particionado.setPorcentajeTrain(0.8)
			particion = particionado.generaParticionesProporcional(data)
			data = particion.getTrain()
			self.conjuntoValidacion = particion.getTest()

		#creamos las neuronas de entrada
		self.capaEntrada = [1 for x in range(0, self.nColumnas + 1)]
		#self.capaEntrada = map((lambda x: 1), range(0, self.nColumnas + 1))
		#inicializamos los pesos de manera aleatoria
		#por cada neurona de la capa oculta
		for indNeurona in range(0, self.neuronasCapaOculta):
			#por cada neurona de la capa de entrada
			self.pesosCapaOculta.append([])
			self.pesosCapaOculta[indNeurona] = map((lambda x: (random.random() - 0.5)), range(0, self.nColumnas + 1))

		#inicializamos los pesos de la capa de salida
		for indNeurona in range(0, self.nClases):
			self.pesosCapaSalida.append([])
			self.pesosCapaSalida[indNeurona] = map((lambda x: (random.random() - 0.5)), range(0, self.neuronasCapaOculta + 1))

		self.NguyenWidrow()

		#generamos todos los vectores objetivos
		vectoresObjetivos = {}
		for instancia in data.getListInstances():
			vectoresObjetivos[instancia] = self.generaVectorObjetivoSalida(instancia.getClase())

		instancias = data.getListInstances()

		#paso1
		for epoca in range(0, self.nEpocas):
			cuadratico_epoca = 0
			#paso2 por cada instancia en train
			for instancia in instancias:
				#***********inicio de Feedforward**********************************
				#paso 3, valores de entrada
				for indNeurona in range(1, self.nColumnas + 1):
					self.capaEntrada[indNeurona] = instancia.getElementAtPos(indNeurona - 1)
				#paso 4, salida neuronas capa oculta, vector Z
				#z0 siempre es 1
				salidaCapaOculta = [1]
				#por cada neurona realizamos una salida
				for indNeurona in range(0, self.neuronasCapaOculta):
					suma = 0
					for indNeuronaEntr in range(0, self.nColumnas + 1):
						suma += (self.pesosCapaOculta[indNeurona][indNeuronaEntr] * self.capaEntrada[indNeuronaEntr])
					#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
					if self.bipolar == False:
						#f1 
						if suma > 40:
							salidaCapaOculta.append(1)
						elif suma < -40:
							salidaCapaOculta.append(0)
						else:
							salidaCapaOculta.append(1.0/(1.0 + math.exp( - suma)))
					else:
						#f2
						if suma > 40:
							salidaCapaOculta.append(1)
						elif suma < -40:
							salidaCapaOculta.append(-1)
						else:
							salidaCapaOculta.append((2.0/(1.0 + math.exp( - suma))) - 1.0)

				#paso 5, calculamos las respuestas de las neuronas de la capa de salida, vector Y
				salidaFinal = []
				for indNeurona in range(0, self.nClases):
					suma = 0
					for indNeuronaOculta in range(0, self.neuronasCapaOculta + 1):
						suma += (self.pesosCapaSalida[indNeurona][indNeuronaOculta] * salidaCapaOculta[indNeuronaOculta])
					#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
					if self.bipolar == False:
						#f1
						if suma > 40:
							salidaFinal.append(1)
						elif suma < -40:
							salidaFinal.append(0)
						else:
							salidaFinal.append(1.0/(1.0 + math.exp( - suma)))
					else:
						#f2
						if suma > 40:
							salidaFinal.append(1)
						elif suma < -40:
							salidaFinal.append(-1)
						else:
							salidaFinal.append((2.0/(1.0 + math.exp( - suma))) - 1.0)
				#***********fin de Feedforward **********************************
				#calculo del error cuadratico medio
				cuadratico_instancia = reduce(add, map((lambda x, y: (x - y)**2), vectoresObjetivos[instancia], salidaFinal))
				cuadratico_epoca += cuadratico_instancia
				#***********inicio Retropropagación del error *******************
				
				#paso 6
				if self.bipolar == False:
					#Tk - Yk * f1`(Yin)
					deltaMinusculaK = map((lambda x, y: (x - y) * (y * (1.0 - y))), vectoresObjetivos[instancia], salidaFinal)
				else:
					#Tk - Yk * f2`(Yin)
					deltaMinusculaK = map((lambda x, y: (x - y) * (0.5 * ((1 + y) * (1.0 - y)))), vectoresObjetivos[instancia], salidaFinal)
				
				deltaMayusculaJK = []
				for indNeuronaSalida in range(0, self.nClases):
					#calculamos delta mayuscula
					deltaMayusculaJK.append([])
					aux = deltaMinusculaK[indNeuronaSalida] * self.alpha
					deltaMayusculaJK[indNeuronaSalida] = map((lambda x: aux*x), salidaCapaOculta)
				#paso 7
				
				deltaMinInj = [0 for x in range(0, self.neuronasCapaOculta)]
				for indNeurona in range(0, self.nClases):
					for indNeuronaOculta  in range(1, self.neuronasCapaOculta + 1):
						deltaMinInj[indNeuronaOculta - 1] += self.pesosCapaSalida[indNeurona][indNeuronaOculta] * deltaMinusculaK[indNeurona]

				deltaMinusculaJ = []
				if self.bipolar == False:
					#f`1
					deltaMinusculaJ = map((lambda x, y: x * (y * (1.0 - y))),deltaMinInj, salidaCapaOculta[1:])
				else:
					#f`2
					deltaMinusculaJ = map((lambda x, y: x *(0.5* ((1.0 + y) * (1.0 - y)))),deltaMinInj, salidaCapaOculta[1:])
				
				deltaMayusculaIJ = []
				for indNeuronaOculta  in range(0, self.neuronasCapaOculta):
					deltaMayusculaIJ.append([])
					aux = self.alpha*deltaMinusculaJ[indNeuronaOculta]
					deltaMayusculaIJ[indNeuronaOculta] = map((lambda x: aux*x),  self.capaEntrada)
					
				#paso 8
				#Actualizar pesos y sesgos
				for indiceClase in range(0, self.nClases):
					self.pesosCapaSalida[indiceClase] = map(add, self.pesosCapaSalida[indiceClase], deltaMayusculaJK[indiceClase])

				for indiceNOculta in range(0, self.neuronasCapaOculta):
					self.pesosCapaOculta[indiceNOculta] = map(add, self.pesosCapaOculta[indiceNOculta] ,deltaMayusculaIJ[indiceNOculta])

				#comprobar condicion de finalizacion
				#fin de bucle de instancias
			if self.debug == True:
				self.debugFile.write(str(epoca) + '\t' + str(cuadratico_epoca) + '\n')

			#if cuadratico_epoca < 0.05:
			#	return
			if self.activo_control_fin == True and epoca % 5 == 0:
				error = self.getErrorFromInstances(self.conjuntoValidacion)
				if self.lastError < error:
					break
				else:
					print str(epoca)+ '\t' + str(error)
					self.lastError = error

	#private
	def generaVectorObjetivoSalida(self, claseIn):
		vector = []
		for clase in self.clases:
			if clase == claseIn:
				vector.append(1)
			else:
				if self.bipolar == False:	
					vector.append(0)
				else:
					vector.append(-1)
		return vector

	def getErrorFromInstances(self, instances):
		error = 0.0

		for instance in instances.getListInstances():
			clase = instance.getClase()
			prediccion = self.classifyInstance(instance)
			if prediccion != clase:
				error += 1.0
	
		return error / float(instances.getNumeroInstances())


	def NguyenWidrow(self):
		beta = 0.7 * math.pow(self.neuronasCapaOculta, 1.0 / self.nColumnas)

		for j in range(0, self.neuronasCapaOculta):
			modulo = math.sqrt(reduce(add, map(lambda x: math.pow(x, 2), self.pesosCapaOculta[j])))
			preCalculo = beta / modulo
		
			self.pesosCapaOculta[j][1:] = map(lambda x: x * preCalculo, self.pesosCapaOculta[j][1:])
			self.pesosCapaOculta[j][0] = random.uniform(-beta, beta)
		

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instancia):
		#***********inicio de Feedforward**********************************
		#paso 3, valores de entrada
		for indNeurona in range(1, self.nColumnas + 1):
			self.capaEntrada[indNeurona] = instancia.getElementAtPos(indNeurona - 1)
		#paso 4, salida neuronas capa oculta, vector Z
		#z0 siempre es 1
		salidaCapaOculta = [1]
		#por cada neurona realizamos una salida
		for indNeurona in range(0, self.neuronasCapaOculta):
			suma = 0
			for indNeuronaEntr in range(0, self.nColumnas + 1):
				suma += (self.pesosCapaOculta[indNeurona][indNeuronaEntr] * self.capaEntrada[indNeuronaEntr])
			#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
			if self.bipolar == False:
				#f1 
				if suma > 40:
					salidaCapaOculta.append(1)
				elif suma < -40:
					salidaCapaOculta.append(0)
				else:
					salidaCapaOculta.append(1.0/(1.0 + math.exp( - suma)))
			else:
				#f2
				if suma > 40:
					salidaCapaOculta.append(1)
				elif suma < -40:
					salidaCapaOculta.append(-1)
				else:
					salidaCapaOculta.append((2.0/(1.0 + math.exp( - suma))) - 1.0)

		#paso 5, calculamos las respuestas de las neuronas de la capa de salida, vector Y
		salidaFinal = []
		for indNeurona in range(0, self.nClases):
			suma = 0
			for indNeuronaOculta in range(0, self.neuronasCapaOculta + 1):
				suma += (self.pesosCapaSalida[indNeurona][indNeuronaOculta] * salidaCapaOculta[indNeuronaOculta])
			#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
			if self.bipolar == False:
				#f1
				if suma > 40:
					salidaFinal.append(1)
				elif suma < -40:
					salidaFinal.append(0)
				else:
					salidaFinal.append(1.0/(1.0 + math.exp( - suma)))
			else:
				#f2
				if suma > 40:
					salidaFinal.append(1)
				elif suma < -40:
					salidaFinal.append(-1)
				else:
					salidaFinal.append((2.0/(1.0 + math.exp( - suma))) - 1.0)
		#***********fin de Feedforward **********************************
		#print salidaFinal
		mejorClase = None
		mejorProb = -1.0
		for i in range(0, self.nClases):
			if salidaFinal[i] > mejorProb:
				mejorClase = self.clases[i]
				mejorProb = salidaFinal[i]

		return mejorClase


	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		redJSON = {}
		redJSON['n_neuronas'] = self.neuronasCapaOculta
		redJSON['n_entradas'] = self.nColumnas
		redJSON['n_clases'] = self.nClases
		redJSON['clases'] = list(self.clases)
		redJSON['pesos_entrada_oculta'] = self.pesosCapaOculta
		redJSON['pesos_oculta_salida'] = self.pesosCapaSalida

		return redJSON

	def restoreClassifierFromJSON(self, jsonObj):
		self.neuronasCapaOculta = jsonObj['n_neuronas']
		self.nColumnas = jsonObj['n_entradas']
		self.nClases = jsonObj['n_clases']
		self.clases = jsonObj['clases']
		self.pesosCapaOculta = jsonObj['pesos_entrada_oculta']
		self.pesosCapaSalida = jsonObj['pesos_oculta_salida']

		#creamos las neuronas de entrada
		for indNeurona in range(0, self.nColumnas + 1):
			self.capaEntrada.append(1)


	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		cadena = 'Puedes introducir estos parámetros:\n'
		cadena += """\tnNeuronas=10\n"""
	 	cadena += """\talpha=0.1\n"""
	 	cadena += """\tnEpocas=1000\n"""
	 	return cadena

	"""Hace que el clasificador entre en modo debug o no"""
	def setDebug(self, value):
		self.debug = value
		if self.debug == True:
			self.debugFile = open(self.debugFileName, 'w')
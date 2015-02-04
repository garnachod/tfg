from Clasificadores.RedNeuronal import RedNeuronal
from Particionado.DivisionPorcentual import DivisionPorcentual
from Particionado.Particion import Particion
from RW.LectorARFF import LectorARFF
from RW.GeneradorARFF import GeneradorARFF
from DBbridge.ConsultasGeneral import ConsultasGeneral
from MachineLearning.Instance import Instance
from MachineLearning.Instances import Instances
import json
import threading

class EntrenamientoTweets(object):
	"""docstring for EntrenamientoTweets"""
	def __init__(self):
		super(EntrenamientoTweets, self).__init__()
		self.consultas = ConsultasGeneral()

	def lanzar(self):
		identificador = self.consultas.creaEntrenamientoRetID("tweet")
		if identificador == -1:
			return 'ERR'
		ficheroARFF = "MachineLearning/historial_entrenamiento/tweet_" + str(identificador) + ".arff"
		ficheroJSON = "MachineLearning/historial_entrenamiento/tweet_" + str(identificador) + ".json"
		self.lanzarPrivate(identificador, ficheroARFF, ficheroJSON)


	def lanzarPrivate(self, identificador, ficheroARFF, ficheroJSON):
		generador = GeneradorARFF()
		generador.entrenamientoTweets(ficheroARFF)

		lector = LectorARFF()
		instances = lector.leerFichero(ficheroARFF)
		

		particionado = DivisionPorcentual()
		particionado.setPortcentajeTrain(0.7)
		particion = particionado.generaParticionesProporcional(instances)


		clasificador = RedNeuronal()
		clasificador.buildClassifier(particion.getTrain())

		error = 0
		erroresPorClase = {}
		aciertosPorClase = {}
		for clase in instances.getClases():
			erroresPorClase[clase] = 0
			aciertosPorClase[clase] = 0

		for instance in particion.getTest().getListInstances():
			clase = instance.getClase()
			if clasificador.classifyInstance(instance) != clase:
				erroresPorClase[clase] += 1
				error += 1
			else:
				aciertosPorClase[clase] += 1 

		procentajeError = error / float(particion.getTest().getNumeroInstances())
		#print 'Error: ' + str(procentajeError)
		#for clase in instances.getClases():
		#	print 'Error '+ clase + ': ' + str(erroresPorClase[clase] ) + ' aciertos: ' + str(aciertosPorClase[clase])

		nombre_fichero = ficheroJSON
		f = open(nombre_fichero,'w')
		f.write(json.dumps(clasificador.saveClassifierToJSON()))
		f.close()

		self.guardarEnDB(identificador, ficheroARFF, ficheroJSON, procentajeError)

	def guardarEnDB(self, identificador, ficheroARFF, ficheroJSON, error):
		self.consultas.editEntrenamiento(identificador, ficheroARFF, ficheroJSON, error)
		

class EntrenamientoTweets_ASINC(threading.Thread):
	def run(self):
		entr = EntrenamientoTweets()
		entr.lanzar()
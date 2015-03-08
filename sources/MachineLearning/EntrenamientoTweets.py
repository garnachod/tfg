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

	def lanzar(self, id_lista_entrenamiento):
		identificador = self.consultas.creaEntrenamientoRetID("tweet", id_lista_entrenamiento)
		if identificador == -1:
			return 'ERR'
		ficheroARFF = "MachineLearning/historial_entrenamiento/tweet_" + str(identificador) + ".arff"
		ficheroJSON = "MachineLearning/historial_entrenamiento/tweet_" + str(identificador) + ".json"
		self.lanzarPrivate(identificador, ficheroARFF, ficheroJSON, id_lista_entrenamiento)


	def lanzarPrivate(self, identificador, ficheroARFF, ficheroJSON, id_lista_entrenamiento):
		generador = GeneradorARFF()
		generador.entrenamientoTweets(ficheroARFF, id_lista_entrenamiento)

		lector = LectorARFF()
		instances = lector.leerFichero(ficheroARFF)
		instances.normaliza()
		
		particionado = DivisionPorcentual()
		particionado.setPorcentajeTrain(0.8)
		particion = particionado.generaParticionesProporcional(instances)


		clasificador = RedNeuronal()
		clasificador.setParameters('nNeuronas=5')
		clasificador.setParameters('alpha=0.1')
		clasificador.setParameters('nEpocas=500')
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
	def __init__(self, identificador):
		super(EntrenamientoTweets_ASINC, self).__init__()
		self.identificador_lista = identificador

	def run(self):
		entr = EntrenamientoTweets()
		entr.lanzar(self.identificador_lista)
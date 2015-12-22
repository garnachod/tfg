# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
import json
from GeneradorDocumentosTwitter import *
from DBbridge.ConsultasCassandra import ConsultasCassandra

class NubePalabrasJSON(luigi.Task):
	"""
		genera un json con formato nube de NubePalabras

		[{text:"",weight:""},...]
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnaliticasPorContenido NubePalabrasJSON --query ...
	"""
	query = luigi.Parameter()

	def requires(self):
		return GeneradorTextoPorContenidoSinLem(self.query)

	def output(self):
		return luigi.LocalTarget(path='ficheros/NubePalabras(%s).json'%self.query)
	
	def run(self):
		diccionarioConteo = {}
		with self.input().open('r') as in_file:
			for palabra in in_file.read().replace("\n", " ").split():
				if palabra not in diccionarioConteo:
					diccionarioConteo[palabra] = 0

				diccionarioConteo[palabra] += 1

		retornoToSort = []
		for palabra in diccionarioConteo:
			#aplicar smooth aqui o en cliente? 
			retornoToSort.append((palabra.encode("utf-8"),diccionarioConteo[palabra]))

		retornoSorted = sorted(retornoToSort, key=lambda x: x[1], reverse=True)


		retorno = []
		for palabra in retornoSorted[:200]:
			#aplicar smooth aqui o en cliente? 
			retorno.append({"text":palabra[0], "weight":palabra[1]})
		
		with self.output().open('w') as out_file:
				out_file.write(json.dumps(retorno))

class ActividadPorUsuarioEnContenido(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnaliticasPorContenido ActividadPorUsuarioEnContenido --query ...
	"""
	query = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/ActividadPorUsuarioEnContenido(%s)'%self.query)

	def requires(self):
		return GetActividadPorContenidoTweet(self.query)

	def run(self):
		diccionarioActividad = {}
		consultas = ConsultasCassandra()

		with self.input().open("r") as in_file:
			dicc = json.loads(in_file.read())

			for tw in dicc:
				autor = tw["autor"]
				if autor not in diccionarioActividad:
					diccionarioActividad[autor] = {"tweets": 0, "retweets":0}

				diccionarioActividad[autor]["tweets"] += 1

				for rt in tw["rts"]:
					autorRT = rt[0]
					autorRT = consultas.getScreenNameByUserIDCassandra(autorRT)
					if autorRT not in diccionarioActividad:
						diccionarioActividad[autorRT] = {"tweets": 0, "retweets":0}

					diccionarioActividad[autorRT]["retweets"] += 1

		retorno = []
		for usuario in diccionarioActividad:
			retorno.append({"usuario":usuario, 
							"tweets":diccionarioActividad[usuario]["tweets"],
							"retweets":diccionarioActividad[usuario]["retweets"]})


		with self.output().open('w') as out_file:
				out_file.write(json.dumps(retorno))

class ActividadPorUsuarioEnContenidoTiempo(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnaliticasPorContenido ActividadPorUsuarioEnContenidoTiempo --query ...
	"""
	query = luigi.Parameter()
	inicio = luigi.Parameter()
	fin = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/ActividadPorUsuarioEnContenidoTiempo(%s_%s)'%(self.query,self.inicio))

	def requires(self):
		return GetActividadPorContenidoTweet(self.query)

	def run(self):
		diccionarioActividad = {}
		consultas = ConsultasCassandra()
		self.inicio = parser.parse(self.inicio)
		self.fin = parser.parse(self.fin)

		with self.input().open("r") as in_file:
			dicc = json.loads(in_file.read())

			for tw in dicc:
				fecha = parser.parse(tw["fecha"])
				if fecha < self.inicio or fecha > self.fin:
					continue

				autor = tw["autor"]
				if autor not in diccionarioActividad:
					diccionarioActividad[autor] = {"tweets": 0, "retweets":0}

				diccionarioActividad[autor]["tweets"] += 1

				for rt in tw["rts"]:
					autorRT = rt[0]
					autorRT = consultas.getScreenNameByUserIDCassandra(autorRT)
					if autorRT not in diccionarioActividad:
						diccionarioActividad[autorRT] = {"tweets": 0, "retweets":0}

					diccionarioActividad[autorRT]["retweets"] += 1

		retorno = []
		for usuario in diccionarioActividad:
			retorno.append({"usuario":usuario, 
							"tweets":diccionarioActividad[usuario]["tweets"],
							"retweets":diccionarioActividad[usuario]["retweets"]})


		with self.output().open('w') as out_file:
				out_file.write(json.dumps(retorno))

class HistogramaAccionesTwitter(luigi.Task):
	"""    
		IntervaloMinutos deve ser un divisor o multiplo de 60,y tiene que ser MINUTOS.
		InicioHistograma y FinHistograma deven ser de la forma "MM/DD/AAAA HH:MM"

		En cada intervalo ponemos el numero de acciones totales.
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnaliticasPorContenido HistogramaAccionesTwitter --query ... --AnchuraIntervalo 1 --InicioHistograma "12/13/2015 00:00" --FinHistograma "12/13/2015 23:59"
	"""

	query = luigi.Parameter()
	#IntervaloMinutos deve ser un divisor o multiplo de 60.
	AnchuraIntervalo = luigi.Parameter()
	InicioHistograma = luigi.Parameter()
	FinHistograma = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/HistogramaAccionesTwitter(%s)'%self.query)

	def requires(self):
		return GetActividadPorContenidoTweet(self.query)

	def run(self):
		#Hay que parsear las fechas que son parametro de luigi??????
		# self.InicioHistograma = parser.parse(self.InicioHistograma)
		# InicioHistograma = parser.parse(self.InicioHistograma)
		self.AnchuraIntervalo = int(self.AnchuraIntervalo)
		self.InicioHistograma = parser.parse(self.InicioHistograma)
		self.FinHistograma = parser.parse(self.FinHistograma)



		#OJO aqui le llamo ArrayPuntos al rio de datos que me va a llegar del JSON.
		td = (self.FinHistograma - self.InicioHistograma)
		ceros = [0 for i in xrange(int(td.seconds/60)/self.AnchuraIntervalo)]
		

		with self.input().open("r") as in_file:
			dicc = json.loads(in_file.read())

			for elem in dicc:
				tw_hour = parser.parse(elem["fecha"])
				if tw_hour < self.InicioHistograma or tw_hour > self.FinHistograma:
					pass
				else:
					td = (tw_hour - self.InicioHistograma)
					ceros[int(td.seconds/60)/self.AnchuraIntervalo] += 1

					for rt in elem["rts"]:
						tw_hour = parser.parse(rt[1])
						if tw_hour < self.InicioHistograma or tw_hour > self.FinHistograma:
							pass
						else:
							td = (tw_hour - self.InicioHistograma)
							ceros[int(td.seconds/60)/self.AnchuraIntervalo] += 1


			#La salida será un JSON ¿NO?    out_file.write(json.dumps(ceros))   hay que hacer que que ceros sea un array de diccionarios. ¿
			# en la clave del diccionario quiero que ponga
			retornoJSON = {"fechainicio": str(self.InicioHistograma),
						   "intervalo":self.AnchuraIntervalo,
						   "valores": list(ceros)}

			with self.output().open("w") as out_file:
				out_file.write(json.dumps(retornoJSON))
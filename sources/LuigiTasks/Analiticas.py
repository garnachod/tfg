# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from GeneradorDocumentosTwitter import *
from AnalisisTextos import *
import codecs
import random
import math
from dateutil import parser
import datetime
from blist import blist
import json

"""
	TO DO:
		OPTIMIZACIONES

"""
class GraficaEventosBrutosTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaEventosBrutosTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			cadenaPuntos = u"["
			with self.input().open('r') as in_file:
				primerPunto = False
				for line in in_file:
					puntos = line.replace("\n", "").split(",")[1:]
					for punto in puntos:
						if primerPunto == True:
							cadenaPuntos += u",["+ str((parser.parse(punto) - datetime.datetime.today()).total_seconds()) + "," + str(random.random()*100.0) + u"]"
						else:
							cadenaPuntos += u"["+ str((parser.parse(punto) - datetime.datetime.today()).total_seconds()) + "," + str(random.random()*100.0) + u"]"
							primerPunto = True

			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)

class GraficaEventosAcumuladosOptimizadoTwitter(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas GraficaEventosAcumuladosOptimizadoTwitter --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaEventosAcumuladosOptimizadoTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntos = blist([])
			with self.input().open('r') as in_file:
				for line in in_file:
					puntos = line.replace("\n", "").split(",")[1:]
					for punto in puntos:
						ArrayPuntos.append((parser.parse(punto) - datetime.datetime.today()).total_seconds())

			ArrayPuntos_sorted = sorted(ArrayPuntos)
			primerPunto = False

			cadenaPuntos = u"["
			for i, punto in enumerate(ArrayPuntos_sorted):
				if primerPunto == True:
					if i % 1000 == 0:
						cadenaPuntos += u",["+ str(punto) + "," + str(i) + u"]"
				else:
					cadenaPuntos += u"["+ str(punto) + "," + str(i) + u"]"
					primerPunto = True
			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)

'''
Vamos a hacer la derivada discreta de la acumulada para que se vean mejor los picos de actividad.
'''
class GraficaEventosAcumuladosDerivadaTwitter(luigi.Task):

	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas GraficaEventosAcumuladosDerivadaTwitter --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaEventosAcumuladosDerivadaTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		#Creamos una lista con los datos ordenados.
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntos = blist([])
			with self.input().open('r') as in_file:
				for line in in_file:
					puntos = line.replace("\n", "").split(",")[1:]
					for punto in puntos:
						microsegundo = (parser.parse(punto) - datetime.datetime.today()).total_seconds()
						ArrayPuntos.append(microsegundo)
						
			ArrayPuntos_sorted = sorted(ArrayPuntos)
			#Hacemos la derivada discreta.
			primerPunto = False

			cadenaPuntos = u"["
			rango = 1000
			for i in xrange(0, len(ArrayPuntos_sorted), rango):
				if primerPunto == True:
					cadenaPuntos += u",["+ str((ArrayPuntos_sorted[i]+ArrayPuntos_sorted[i-rango])/2 ) + "," + str(1/(ArrayPuntos_sorted[i]-ArrayPuntos_sorted[i-rango]) )  + u"]"
				else:
					cadenaPuntos += u"[0,0]"
					primerPunto = True
			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)

class RelevanciaSeguidoresUsuarioAlTopic(luigi.Task):
	"""
		Problemas de redondeo fijo
		Uso:
			PYTHONPATH='' luigi --module Analiticas RelevanciaSeguidoresUsuarioAlTopic --usuario ... --matrizCorreccion ...
	"""
	usuario = luigi.Parameter()
	#matrizCorreccion = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='relevancia/RelevanciaSeguidoresUsuarioAlTopic(%s)'%self.usuario)

	def requires(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			seguidores = consultasNeo4j.getListaIDsSeguidoresByUserID(identificador)
			arrayTareas = [GeneradorTextoUsuario(seguidor) for seguidor in seguidores]
			arrayTareas.append(CreaMatrizCorreccionTwitterUserPrimerTopic(self.usuario))
			return arrayTareas
		else:
			return []



	def run(self):
		header = True
		matriz_diccionario = {}
		#cargamos la matriz de correcion
		for input in self.input():
			if "MatrizCorreccion" in input.path:
				with input.open('r') as matriz_texto:
					for i, linea in enumerate(matriz_texto):
						if i == 0:
							if header:
								continue

						if len(linea) < 10:
							continue

						columnas = linea.replace("\n", "").split(",")

						termino = columnas[0]
						pesos = [float(x) for x in columnas[1:]]

						matriz_diccionario[termino] = pesos



		#una vez cargada miramos el topic definido, haciendo la suma de todas las palabras y normalizamos con el numero de palabras
		#usuarios es un array de tuplas (usuario, peso)
		indice = 0
		usuarios = []
		for input in self.input():
			usuarioPeso = 0.0
			usuarioLongitud = 0
			usuarioId = input.path.replace("ficheros/GeneradorTextoUsuario(", "").replace(")", "")
			with input.open('r') as in_file:
				if "MatrizCorreccion" not in input.path:
					for linea in in_file:
						linea = linea.replace("\n", "")
						palabras = linea.split(" ")
						for palabra in palabras:
							if palabra in matriz_diccionario:
								usuarioPeso += matriz_diccionario[palabra][indice]
								usuarioLongitud += 1

					if usuarioLongitud > 0:
						usuarios.append((usuarioId, usuarioPeso/math.log(usuarioLongitud)))
					else:
						usuarios.append((usuarioId, 0.0))


		usuarios_sorted = sorted(usuarios, key=lambda usuario: usuario[1], reverse=True)
		with self.output().open('w') as out_file:
			for usuario_id, peso in usuarios_sorted:
				out_file.write(usuario_id + ","+ str(peso)+ "\n")

class RelevanciaSeguidoresUsuarioByNameAlTopic(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas RelevanciaSeguidoresUsuarioByNameAlTopic --usuario ... --matrizCorreccion ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='relevancia/RelevanciaSeguidoresUsuarioByNameAlTopic(%s)'%self.usuario)

	def requires(self):
		return RelevanciaSeguidoresUsuarioAlTopic(self.usuario)

	def run(self):
		consultasCassandra = ConsultasCassandra()

		with self.output().open('w') as out_file:
			with self.input().open('r') as in_file:
				for line in in_file:
					elementos = line.replace("\n", "").split(",")
					usuarioId = long(elementos[0])
					peso = elementos[1]
					usuario_screenName = consultasCassandra.getScreenNameByUserIDCassandra(usuarioId)
					if usuario_screenName is not None:
						out_file.write(usuario_screenName + ","+ str(peso)+ "\n")

class RelevanciaSeguidoresUsuarioByNameAlTopicJSON(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas RelevanciaSeguidoresUsuarioByNameAlTopicJSON --usuario ... --matrizCorreccion ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='relevancia/RelevanciaSeguidoresUsuarioByNameAlTopicJSON(%s)'%self.usuario)

	def requires(self):
		return RelevanciaSeguidoresUsuarioByNameAlTopic(self.usuario)

	def run(self):
		JsonObj = {}
		with self.output().open('w') as out_file:
			with self.input().open('r') as in_file:
				for line in in_file:
					elementos = line.replace("\n", "").split(",")
					if len(elementos) > 1:
						usuario = elementos[0]
						pesos = [float(elemento) for elemento in elementos[1:]]
						JsonObj[usuario] = pesos

			out_file.write(json.dumps(JsonObj))
					

class RelevanciaSeguidoresUsuarioTodosTopics(luigi.Task):
	"""
		Problemas de redondeo fijo
		Uso:
			PYTHONPATH='' luigi --module Analiticas RelevanciaSeguidoresUsuarioTodosTopics --usuario ... --matrizCorreccion ...
	"""
	usuario = luigi.Parameter()
	#matrizCorreccion = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='relevancia/RelevanciaSeguidoresUsuarioTodosTopics(%s)'%self.usuario)

	def requires(self):
		consultasNeo4j = ConsultasNeo4j()
		consultasCassandra = ConsultasCassandra()

		# si no es un identificador, se intenta conseguir desde cassandra
		identificador = 0
		try:
			identificador = long(self.usuario)
		except Exception, e:
			if self.usuario[0] == "@":
				self.usuario = self.usuario[1:]
			identificador = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)

		#solo puede no existir ese identificador si es privado, pero debemos controlarlo
		if identificador > 0:
			seguidores = consultasNeo4j.getListaIDsSeguidoresByUserID(identificador)
			arrayTareas = [GeneradorTextoUsuario(seguidor) for seguidor in seguidores]
			arrayTareas.append(CreaMatrizCorreccionTwitterUserTodosTopics(self.usuario))
			return arrayTareas
		else:
			return []



	def run(self):
		header = True
		matriz_diccionario = {}
		#cargamos la matriz de correcion
		for input in self.input():
			if "MatrizCorreccion" in input.path:
				with input.open('r') as matriz_texto:
					for i, linea in enumerate(matriz_texto):
						if i == 0:
							if header:
								continue

						if len(linea) < 10:
							continue

						columnas = linea.replace("\n", "").split(",")

						termino = columnas[0]
						pesos = [float(x) for x in columnas[1:]]

						matriz_diccionario[termino] = pesos



		#una vez cargada miramos el topic definido, haciendo la suma de todas las palabras y normalizamos con el numero de palabras
		#usuarios es un array de tuplas (usuario, peso)
		indices = [i for i in range(7)]
		usuarios = []
		for input in self.input():
			usuarioPesos = [0.0 for i in range(7)]
			usuarioLongitud = 0
			usuarioId = input.path.replace("ficheros/GeneradorTextoUsuario(", "").replace(")", "")
			with input.open('r') as in_file:
				if "MatrizCorreccion" not in input.path:
					for linea in in_file:
						linea = linea.replace("\n", "")
						palabras = linea.split(" ")
						for palabra in palabras:
							if palabra in matriz_diccionario:
								for indice in indices:
									usuarioPesos[indice] += matriz_diccionario[palabra][indice]
								usuarioLongitud += 1

					if usuarioLongitud > 0:
						usuarios.append((usuarioId, [usuarioPeso/math.log(usuarioLongitud) for usuarioPeso in usuarioPesos]))
					else:
						usuarios.append((usuarioId, usuarioPesos))


		with self.output().open('w') as out_file:
			for usuario_id, pesos in usuarios:
				out_file.write(usuario_id)
				for peso in pesos:
					out_file.write(","+ str(peso))
				out_file.write("\n")


class RelevanciaSeguidoresUsuarioByNameAlTodosTopics(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas RelevanciaSeguidoresUsuarioByNameAlTodosTopics --usuario ... --matrizCorreccion ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='relevancia/RelevanciaSeguidoresUsuarioByNameAlTodosTopics(%s)'%self.usuario)

	def requires(self):
		return RelevanciaSeguidoresUsuarioTodosTopics(self.usuario)

	def run(self):
		consultasCassandra = ConsultasCassandra()

		with self.output().open('w') as out_file:
			with self.input().open('r') as in_file:
				for line in in_file:
					elementos = line.replace("\n", "").split(",")
					usuarioId = long(elementos[0])
					pesos = elementos[1:]
					usuario_screenName = consultasCassandra.getScreenNameByUserIDCassandra(usuarioId)
					if usuario_screenName is not None:
						out_file.write(usuario_screenName)
						for peso in pesos:
							out_file.write(',' + peso)

						out_file.write("\n")

class RelevanciaSeguidoresUsuarioByNameAlTodosTopicsJSON(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas RelevanciaSeguidoresUsuarioByNameAlTodosTopicsJSON --usuario ... --matrizCorreccion ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='relevancia/RelevanciaSeguidoresUsuarioByNameAlTodosTopicsJSON(%s)'%self.usuario)

	def requires(self):
		return RelevanciaSeguidoresUsuarioByNameAlTodosTopics(self.usuario)

	def run(self):
		JsonObj = {}
		with self.output().open('w') as out_file:
			with self.input().open('r') as in_file:
				for line in in_file:
					elementos = line.replace("\n", "").split(",")
					if len(elementos) > 1:
						usuario = elementos[0]
						pesos = [float(elemento) for elemento in elementos[1:]]
						JsonObj[usuario] = pesos

			out_file.write(json.dumps(JsonObj))

class GraficaAccionesUsuariosMesesTwitter(luigi.Task):

	"""
	Vamos a cribar la muestra de acciones para luego pasarsela a otra tarea de Luigi y que pinte la derivada discreta del acumulado.

Entonces no hay que escupìr grafica.

		Uso:
			PYTHONPATH='' luigi --module Analiticas GraficaAccionesUsuariosMesesTwitter --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		#la salida seria cadenaPuntos
		return luigi.LocalTarget(path='graficas/GraficaAccionesUsuariosMesesTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntos = blist([])
			with self.input().open('r') as in_file:
				ArrayPuntosTotales = blist([])
				with self.input().open('r') as in_file:
					for line in in_file:
						ArrayPuntosUsuario = []
						puntos = line.replace("\n", "").split(",")[1:]
						for punto in puntos:
							microsegundo = (parser.parse(punto) - datetime.datetime.today()).total_seconds()
							ArrayPuntosUsuario.append(microsegundo)

						ArrayPuntosUsuarioSorted = sorted(ArrayPuntosUsuario)

						TiempoCompara = None
						ArrayPuntosUsuarioSortedMes = []
						for puntoUsuario in ArrayPuntosUsuarioSorted:
							if puntoUsuario > - (60*60*24*15):
								if TiempoCompara is None:
									TiempoCompara = puntoUsuario
									ArrayPuntosTotales.append(TiempoCompara)
								else:
									if (TiempoCompara - puntoUsuario) > (-15 * 60):
										pass
									else:
										ArrayPuntosTotales.append(puntoUsuario)
										TiempoCompara = puntoUsuario

			ArrayPuntos_sorted = sorted(ArrayPuntosTotales)
			primerPunto = False

			cadenaPuntos = u"["
			rango = 2
			for i in xrange(0, len(ArrayPuntos_sorted), rango):
				if primerPunto == True:
					#OJO: Aqui se lee cada accion dos veces, esto es ineficiente.					
					cadenaPuntos += u",["+ str((ArrayPuntos_sorted[i]+ArrayPuntos_sorted[i-rango])/2 ) + "," + str(1/(ArrayPuntos_sorted[i]-ArrayPuntos_sorted[i-rango]) )  + u"]"
				else:
					cadenaPuntos += u"[0,0]"
					primerPunto = True
			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)



class GraficaAccionesModuloDiaTwitter(luigi.Task):

	"""
		Probar, que no se si esta bien. 
		Aqui tambien pintamos la derivada, pero esta vez de las acciones de la lista que contiene todas las acciones que han ocurrido en un dia 
		concreto de la semana, por ejemplo pintaría la grafica de todos los lunes de un mes.

		Uso:
			PYTHONPATH='' luigi --module Analiticas GraficaAccionesModuloDiaTwitter --usuario ... --dia ...
	"""

	usuario = luigi.Parameter()
	dia = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaAccionesModuloDiaTwitter(%s,%s).html'%(self.usuario, self.dia), format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		dia = int(self.dia)
		with self.output().open('w') as out_file:
			ArrayPuntosTotales = blist([])
			with self.input().open('r') as in_file:
				for line in in_file:
					ArrayPuntosUsuario = []
					puntos = line.replace("\n", "").split(",")[1:]

				### Esta parte es la ORIGINAL de este codigo, el resto tambien se usa en otros.
					for punto in puntos:
						tiempo = parser.parse(punto)
						if tiempo.weekday() == dia:
							#weekday, hour, minute, second, microsecond, and tzinfo.
							microsegundo = ((tiempo.hour * 60 * 60 * 1000000) + (tiempo.minute * 60 * 1000000) + (tiempo.second * 1000000)+ tiempo.microsecond)/1000000.0
							ArrayPuntosUsuario.append(microsegundo)
				###

					#Aqui pego el SMOOZEITOR3000
					ArrayPuntosUsuarioSorted = sorted(ArrayPuntosUsuario)

					for puntoUsuario in ArrayPuntosUsuarioSorted:
						ArrayPuntosTotales.append(puntoUsuario)
								
			ArrayPuntos_sorted = sorted(ArrayPuntosTotales)
			primerPunto = False


			ArrayPuntosDerivada = []
			rango = 500
			for i in xrange(0, len(ArrayPuntos_sorted), rango):
				punto = (((ArrayPuntos_sorted[i]+ArrayPuntos_sorted[i-rango])/2 ), (1/(ArrayPuntos_sorted[i]-ArrayPuntos_sorted[i-rango])))
				ArrayPuntosDerivada.append(punto)

			smootRange = 3
			ArrayPuntosSmoot = []
			tamPuntos = len(ArrayPuntosDerivada)
			for i, punto in enumerate(ArrayPuntosDerivada):
				if i < smootRange:
					ArrayPuntosSmoot.append(punto)
				elif i > tamPuntos - smootRange:
					ArrayPuntosSmoot.append(punto)
				else:
					media = 0
					for j in range(i - smootRange, i + smootRange):
						media += ArrayPuntosDerivada[j][1]

					media = media / (smootRange*2 + 1)
					ArrayPuntosSmoot.append((punto[0], media))

			cadenaPuntos = u"["
			
			for i, punto in enumerate(ArrayPuntosSmoot):
				if i != 0:
					#OJO: Aqui se lee cada accion dos veces, esto es ineficiente.		
					# Ademas ahora queremos hacer una media movil para suavizarlo todo.			
					cadenaPuntos += u",["+ str(punto[0]) + "," + str(punto[1])  + u"]"
				else:
					cadenaPuntos += u"[0,0]"
					primerPunto = True
			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)




class GraficaAccionesModuloSemanaTwitterSmooth(luigi.Task):

	"""
		Juntamos las acciones de todo el periodo en una grafica de puntos. La altura de cada punto viene determinada por la media de las alturas de 
		los puntos de alrededor (smooth) en la lista de las derivadas discretas. 
		Uso:
			PYTHONPATH='' luigi --module Analiticas GraficaAccionesModuloSemanaTwitterSmooth --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		#la salida seria cadenaPuntos
		return luigi.LocalTarget(path='graficas/GraficaAccionesModuloSemanaTwitterSmooth(%s).html'%(self.usuario), format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntosTotales = blist([])
			with self.input().open('r') as in_file:
				for line in in_file:
					ArrayPuntosUsuario = []
					puntos = line.replace("\n", "").split(",")[1:]

					for punto in puntos:
						tiempo = parser.parse(punto)
						#hour, minute, second, microsecond, and tzinfo.
						microsegundo = ((tiempo.weekday() * 24 * 60 * 60 * 1000000) +(tiempo.hour * 60 * 60 * 1000000) + (tiempo.minute * 60 * 1000000) + (tiempo.second * 1000000)+ tiempo.microsecond)/1000000.0
						ArrayPuntosUsuario.append(microsegundo)

					ArrayPuntosUsuarioSorted = sorted(ArrayPuntosUsuario)

					for puntoUsuario in ArrayPuntosUsuarioSorted:
						ArrayPuntosTotales.append(puntoUsuario)
								
			ArrayPuntos_sorted = sorted(ArrayPuntosTotales)
			primerPunto = False

			#me esta dando fallo con cosas tipo rango 1 o 3 y smootrange 31 (ojo que para rango 40 y smoothrange 91 no falla)
			ArrayPuntosDerivada = []
			rango = 100
			for i in xrange(0, len(ArrayPuntos_sorted), rango):
				punto = (((ArrayPuntos_sorted[i]+ArrayPuntos_sorted[i-rango])/2 ), (1/(ArrayPuntos_sorted[i]-ArrayPuntos_sorted[i-rango])))
				ArrayPuntosDerivada.append(punto)

			smootRange = 31
			ArrayPuntosSmoot = []
			tamPuntos = len(ArrayPuntosDerivada)
			for i, punto in enumerate(ArrayPuntosDerivada):
				if i < smootRange:
					ArrayPuntosSmoot.append(punto)
				elif i > tamPuntos - smootRange:
					ArrayPuntosSmoot.append(punto)
				else:
					media = 0
					for j in range(i - smootRange, i + smootRange):
						media += ArrayPuntosDerivada[j][1]

					media = media / (smootRange*2 + 1)
					ArrayPuntosSmoot.append((punto[0], media))

			cadenaPuntos = u"["
			
			for i, punto in enumerate(ArrayPuntosSmoot):
				if i != 0:
					#OJO: Aqui se lee cada accion dos veces, esto es ineficiente.		
					# Ademas ahora queremos hacer una media movil para suavizarlo todo.			
					cadenaPuntos += u",["+ str(punto[0]) + "," + str(punto[1])  + u"]"
				else:
					cadenaPuntos += u"[0,0]"
					primerPunto = True
			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)



class HistogramaEventosSemanaTwitter(luigi.Task):

	"""
			Uso:
			PYTHONPATH='' luigi --module Analiticas HistogramaEventosSemanaTwitter --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/HistogramaEventosSemanaTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		#Creamos una lista con los datos sin ordenar, porque al almacenarlos en la lista de intervalos los vamos a ordenar.
		template = codecs.open("templates/TemplateGoogleHistogram.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntos = blist([])
			with self.input().open('r') as in_file:
				for line in in_file:
					puntos = line.replace("\n", "").split(",")[1:]
					for punto in puntos:
						ArrayPuntos.append(parser.parse(punto))

			print "ok leer"
			hMinutos= 20
			ceros = [0 for i in xrange(7*24*60/hMinutos)]

			for accion in ArrayPuntos:
				ceros[int(((accion.weekday()*24*60)/hMinutos)+((accion.hour*60)/hMinutos))+int(math.floor(accion.minute/hMinutos))] += 1



			# Creamos una lista con el numero de acciones por intervalo, por ahora el h será homogeneo.
			cadenaPuntos=u"["
			for i in xrange(1, int(math.floor(7*24*60/hMinutos)-1) ):
				if i != 1:		
					cadenaPuntos += u",["+ str(i) + "," + str(ceros[i])  + u"]"
				else:
					cadenaPuntos += u"[000,"+ str(ceros[0]) +"]"
					primerPunto = True
			cadenaPuntos += "]"

			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)

class HistogramaPonderadoSeguidoresLDATopicTwitter(luigi.Task):
	"""docstring for HistogramaPonderadoLDATopic"""
	"""
	
		Uso:
			PYTHONPATH='' luigi --module Analiticas HistogramaPonderadoSeguidoresLDATopicTwitter --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/HistogramaPonderadoSeguidoresLDATopicTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return [GeneradorEventosSeguidoresPuntosUsuario(self.usuario), RelevanciaSeguidoresUsuarioAlTopic(self.usuario)]

	def run(self):
		#Creamos una lista con los datos sin ordenar, porque al almacenarlos en la lista de intervalos los vamos a ordenar.
		template = codecs.open("templates/TemplateGoogleHistogram.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntos = {}
			PesoUsuarioTopic = {}
			for input in self.input():
				with input.open('r') as in_file:
					if "RelevanciaSeguidores" not in input.path:
						for line in in_file:
							linea = line.replace("\n", "").split(",")
							puntos = linea[1:]
							usuario = linea[0]
							ArrayPuntos[usuario] = blist([])
							for punto in puntos:
								ArrayPuntos[usuario].append(parser.parse(punto))
					else:
						for line in in_file:
							linea = line.replace("\n", "").split(",")
							peso = linea[1]
							usuario = linea[0]
							PesoUsuarioTopic[usuario] = float(peso)

			print "ok leer"
			hMinutos= 15
			ceros = [0 for i in xrange(7*24*60/hMinutos)]

			for usuario in ArrayPuntos:
				if usuario in PesoUsuarioTopic:
					peso = PesoUsuarioTopic[usuario]
					for accion in ArrayPuntos[usuario]:
						ceros[int(((accion.weekday()*24*60)/hMinutos)+((accion.hour*60)/hMinutos))+int(math.floor(accion.minute/hMinutos))] += peso



			cadenaPuntos=u"["
			for i in xrange(1, int(math.floor(7*24*60/hMinutos)-1) ):
				if i != 1:		
					cadenaPuntos += u",["+ str(i) + "," + str(ceros[i])  + u"]"
				else:
					cadenaPuntos += u"[0,"+ str(ceros[0]) +"]"
					primerPunto = True
			cadenaPuntos += "]"

			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)
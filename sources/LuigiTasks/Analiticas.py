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
from dateutil import parser
import datetime
from blist import blist

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

class GraficaEventosAcumuladosTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaEventosAcumuladosTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

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
					cadenaPuntos += u",["+ str(punto) + "," + str(i) + u"]"
				else:
					cadenaPuntos += u"["+ str(punto) + "," + str(i) + u"]"
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
			arrayTareas.append(CreaMatrizCorreccionTwitterUser(self.usuario))
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
						usuarios.append((usuarioId, usuarioPeso/usuarioLongitud))
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

class FiltradoAccionesUsuariosTwitter(luigi.Task):

	"""
	Vamos a cribar la muestra de acciones para luego pasarsela a otra tarea de Luigi y que pinte la derivada discreta del acumulado.

Entonces no hay que escupìr grafica.

		Uso:
			PYTHONPATH='' luigi --module Analiticas FiltradoAccionesUsuariosTwitter --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		#la salida seria cadenaPuntos
		return luigi.LocalTarget(path='graficas/FiltradoAccionesUsuariosTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

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
						for puntoUsuario in ArrayPuntosUsuarioSorted:
							#if puntoUsuario > - (60*60*24*62):
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
			rango = 20
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




class FiltradoAccionesUsuariosMesesTwitter(luigi.Task):

	"""
	Vamos a cribar la muestra de acciones para luego pasarsela a otra tarea de Luigi y que pinte la derivada discreta del acumulado.

Entonces no hay que escupìr grafica.

		Uso:
			PYTHONPATH='' luigi --module Analiticas FiltradoAccionesUsuariosMesesTwitter --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		#la salida seria cadenaPuntos
		return luigi.LocalTarget(path='graficas/FiltradoAccionesUsuariosMesesTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

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




class GraficaUsuariosDiaDerivadaTwitter(luigi.Task):

	"""
		Uso:
			PYTHONPATH='' luigi --module Analiticas GraficaUsuariosDiaDerivadaTwitter --usuario ...
	"""
"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaUsuariosDiaDerivadaTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		#Aqui queremos solo un par de meses.
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			ArrayPuntos = blist([])
			with self.input().open('r') as in_file:
				cadenaPuntos += u"["
				for usuario in in_file:


# Aqui queremos recorrer las acciones de cada usuario, ir metiendolas en 7 listas distintas (una para cada dia de la semana) de la siguiente forma:
			for i in xrange(0, len(accionesusuarioporpornerlealgunnombre), rango):
				if primerPunto == True:
#OJO: Aqui se lee cada accion dos veces, esto es ineficiente.					
					cadenaPuntos += u",["+ str((ArrayPuntos_sorted[i]+ArrayPuntos_sorted[i-rango])/2 ) + "," + str(1/(ArrayPuntos_sorted[i]-ArrayPuntos_sorted[i-rango]) )  + u"]"
				else:
					cadenaPuntos += u"[0,0]"
					primerPunto = True



				cadenaPuntos += "]"
				salida = template_content.replace("{{}}", cadenaPuntos)
				out_file.write(salida)


"""
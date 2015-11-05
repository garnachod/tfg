# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from GeneradorDocumentosTwitter import *
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
			return [GeneradorTextoUsuario(seguidor) for seguidor in seguidores]
		else:
			return []



	def run(self):
		header = True
		#cargamos la matriz de correcion
		matriz_texto = codecs.open("matrices_correcion/MatrizCorreccionMolins.csv", "r", "utf-8")
		matriz_diccionario = {}

		for i, linea in enumerate(matriz_texto):
			if i == 0:
				if header:
					continue

			if len(linea) < 10:
				continue

			columnas = linea.split(" ")

			termino = columnas[0].replace("\"", "").replace("terms.", "")
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


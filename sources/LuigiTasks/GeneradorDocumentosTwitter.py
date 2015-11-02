# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from time import time, sleep
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasCassandra import ConsultasCassandra

from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets
from RecolectorTwitter import *


class GeneradorTextoUsuario(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoUsuario(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def run(self):
		"""
		Realiza una busqueda en la base de datos

		Recolecta los tweets de un usuario dado por nombre de usuario
		o identificador, imprime cada tweet en una linea, han sido limpiados
		"""
		cs = ConsultasCassandra()

		tweets = []
		try:
			tweets = cs.getTweetsUsuarioCassandra(self.usuario, limit=1000)
		except Exception, e:
			pass

		#print len(self.output())
		with self.output().open('w') as out_file:
			for tweet in tweets:
				out_file.write(LimpiadorTweets.clean(tweet.status))
				out_file.write(u"\n")

class TestGeneradorTextoUsuario(luigi.Task):
	def requires(self):
		return GeneradorTextoUsuario("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestGeneradorTextoUsuario()')

class GeneradorTextoSeguidoresUsuario(luigi.Task):
	"""docstring for GeneradorTextoSeguidoresUsuario"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoSeguidoresUsuario(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))
	
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
		with self.output().open('w') as out_file:
			for input in self.input():
				with input.open('r') as in_file:
					for line in in_file:
						out_file.write(line)
			

class TestGeneradorTextoSeguidoresUsuario(luigi.Task):
	def requires(self):
		return GeneradorTextoSeguidoresUsuario("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestGeneradorTextoSeguidoresUsuario()')

if __name__ == "__main__":
	luigi.run()
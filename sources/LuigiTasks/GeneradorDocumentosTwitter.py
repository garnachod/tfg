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
				tweetLimpio = LimpiadorTweets.clean(tweet.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
				tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tweet.lang)
				out_file.write(tweetStemmed)
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
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoSeguidoresUsuario --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		"""
			Importante:
				Aquí podemos ver como se genera un fichero utf-8 el Luigi, como son textos, lo necesitamos

		"""
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
						if len(line) > 10:
							out_file.write(line.replace("\n", ""))

					out_file.write(u"\n")
			

class TestGeneradorTextoSeguidoresUsuario(luigi.Task):
	def requires(self):
		return GeneradorTextoSeguidoresUsuario("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestGeneradorTextoSeguidoresUsuario()')

class GeneradorEventosSeguidoresUsuario(luigi.Task):
	"""Genera un fichero con los eventos de los seguidores de un usuario

		ej.
		identificador,número de eventos,(eventoTipo, fechaEvento),...,(eventoTipo, fechaEvento)
		donde evento tipo puede ser:
			fav
			rt
			tw
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorEventosSeguidoresUsuario(%s)'%self.usuario)

	def run(self):
		"""
		Realiza una busqueda en la base de datos de los seguidores de un usuario

		Por cada usuario genera una fila del formato mostrado en la clase, 
			Primero se solicitan los tweets y RTs
			Despues se piden los favoritos
		"""
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
			with self.output().open('w') as out_file:
				for seguidor in seguidores:
					eventos = consultasCassandra.getOrigTweetAndCreatedAtFromTweetsByUser(seguidor)
					out_file.write(str(seguidor))
					for evento in eventos:
						if evento.orig_tweet == 0:
							out_file.write(",(tw;"+str(evento.created_at)+")")
						else:
							out_file.write(",(rt;"+str(evento.created_at)+")")

					#ya hemos impreso los TW y RT, ahora buscamos los favoritos
					favoritos_ids = consultasNeo4j.getListaIDsFavsByUserID(seguidor)
					eventos_favoritos = consultasCassandra.getOrigTweetAndCreatedAtFromTweetsByListIDSTweets(favoritos_ids)
					for evento in eventos_favoritos:
						out_file.write(",(fav;"+str(evento.created_at)+")")
						
					out_file.write("\n")

class TestGeneradorEventosSeguidoresUsuario(luigi.Task):
	def requires(self):
		return GeneradorEventosSeguidoresUsuario("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestGeneradorEventosSeguidoresUsuario()')

class GeneradorEventosSeguidoresPuntosUsuario(luigi.Task):
	"""Genera un fichero con los eventos de los seguidores de un usuario
		En este fichero solo hay horas en bruto

		ej.
		identificador,fechaEvento,...,fechaEvento
	"""
	usuario = luigi.Parameter()

	def requires(self):
		return GeneradorEventosSeguidoresUsuario(self.usuario)

	def run(self):
		with self.output().open('w') as out_file:
			with self.input().open('r') as in_file:
				for line in in_file:
					#primer elemento nombre de usuario
					array_eventos = line.replace("\n", "").split(",")
					out_file.write(array_eventos[0])
					for evento in array_eventos[1:]:
						evento_split = evento.replace("(", "").replace(")", "").split(";")
						out_file.write(","+ evento_split[1])

					out_file.write("\n")

	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorEventosSeguidoresPuntosUsuario(%s)'%self.usuario)


class GeneradorTextoCorpusIdioma(luigi.Task):
	"""docstring for GeneradorTextoCorpusIdioma"""
	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorDocumentosTwitter GeneradorTextoCorpusIdioma --idioma ...
	"""
	idioma = luigi.Parameter(default="es")

	def run(self):
		consultasCassandra = ConsultasCassandra()
		diccionarioUsuarios = {}

		tweets = consultasCassandra.getAllStatusAndIDUserFiltrateLang(self.idioma)
		for tweet in tweets:
			strusuario = str(tweet.tuser)
			
			if strusuario not in diccionarioUsuarios:
				diccionarioUsuarios[strusuario] = []

			tweetLimpio = LimpiadorTweets.clean(tweet.status)
			tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tweet.lang)
			tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tweet.lang)

			diccionarioUsuarios[strusuario].append(tweetStemmed)

		with self.output().open('w') as out_file:
			for usuario in diccionarioUsuarios:
				for tweet in diccionarioUsuarios[usuario]:
					out_file.write(tweet + u" ")

				out_file.write(u"\n")



	def output(self):
		return luigi.LocalTarget(path='ficheros/GeneradorTextoCorpusIdioma(%s)'%self.idioma, format=luigi.format.TextFormat(encoding='utf8'))
		
	

if __name__ == "__main__":
	luigi.run()
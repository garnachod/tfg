# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from DBbridge.EscritorSeguidoresNeo4j import EscritorSeguidoresNeo4j
from DBbridge.EscritorFavoritosNeo4j import EscritorFavoritosNeo4j
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasCassandra import ConsultasCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsStatusStream import RecolectorTweetsStatusStream
from SocialAPI.TwitterAPI.RecolectorTweetsUsersStream import RecolectorTweetsUsersStream
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from SocialAPI.TwitterAPI.RecolectorFavoritosUser import RecolectorFavoritosUser
from SocialAPI.TwitterAPI.RecolectorSiguiendoShort import RecolectorSiguiendoShort
from SocialAPI.TwitterAPI.RecolectorSeguidoresShort import RecolectorSeguidoresShort
import luigi
from time import time, sleep

class RecolectorUsuarioTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorUsuarioTwitter(%s)'%self.usuario)

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los tweets de un usuario dado por nombre de usuario
		o identificador
		"""
		escritorList = []
		escritorList.append(EscritorTweetsCassandra(-1))
		recolector = RecolectorTweetsUser(escritorList)

		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(identificador=identificador)

				break
			except Exception, e:
				if "LIMITE" in e:
					sleep(1*60)
				else:
					raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")

class RecolectorContenidoTweet(luigi.Task):
	"""
		Realiza una busqueda en TwitterAPI

		Recolecta los tweets que contienen la busqueda, pueden ser hastags, menciones o lo que sea
		default 1.000.000 tardara unas 6 horas si existen ese millon o twiter nos los da
		si el limite es -1 no habra limite (MUCHO CUIDADO)

		OTRO MUCHO CUIDADO
			LUIGI no admite # en la entrada de parametros, no pasa nada, borradlos
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorContenidoTweet --busqueda ... --limitedescarga ...
	"""
	busqueda = luigi.Parameter()
	limitedescarga = luigi.Parameter(default="1000000")

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorContenidoTweet(%s)'%self.busqueda)

	def run(self):
		escritorList = []
		escritorList.append(EscritorTweetsCassandra(-1))
		recolector = RecolectorTweetsTags(escritorList)
		limite = 1000000
		try:
			limite = int(self.limitedescarga)
		except Exception, e:
			limite = 1000000
		if limite == -1:
			limite = 10000000

		try:
			#recoleccion pura y dura
			for busq in self.busqueda.replace(" ", "").split(","):
				recolector.recolecta(busq, limite = limite)
		except Exception, e:
			if "LIMITE" in e:
				sleep(1*60)
			else:
				raise e


"""
class TestRecolectorUsuarioTwitter(luigi.Task):
	def requires(self):
		return [RecolectorUsuarioTwitter(usuario) for usuario in ["@garnachod", "@p_molins", 2383366169]]

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")

	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorUsuarioTwitter()')"""

class RecolectorSeguidoresTwitter(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorSeguidoresTwitter --usuario ...
	"""
	usuario = luigi.Parameter()
	forcecomplete = luigi.Parameter(default="True")

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorSeguidoresTwitter(%s)'%self.usuario)

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los seguidores de un usuario dado por nombre de usuario
		o identificador
		"""
		escritores = [EscritorSeguidoresNeo4j(-1)]
		recolector = RecolectorSeguidoresShort(escritores)
		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					if self.forcecomplete == "True":
						recolector.recolecta(query=self.usuario, complete=True)
					else:
						recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(id_user=identificador)
				break
			except Exception, e:
				if "LIMITE" in e:
					sleep(1*60)
				#else:
				#	raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")
"""
class TestRecolectorSeguidoresTwitter(luigi.Task):
	def requires(self):
		return [RecolectorSeguidoresTwitter(usuario) for usuario in ["@garnachod", "@p_molins", 2383366169]]

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorSeguidoresTwitter()')"""

class RecolectorSiguiendoTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorSiguiendoTwitter(%s)'%self.usuario)

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los siguiendos de un usuario dado por nombre de usuario
		o identificador
		"""
		escritores = [EscritorSeguidoresNeo4j(-1)]
		recolector = RecolectorSiguiendoShort(escritores)
		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(id_user=identificador)
				break
			except Exception, e:
				if "LIMITE" in e:
					sleep(1*60)
				else:
					raise e

		with self.output().open('w') as out_file:
			out_file.write("OK")
		
class TestRecolectorSiguiendoTwitter(luigi.Task):
	def requires(self):
		return [RecolectorSiguiendoTwitter(usuario) for usuario in ["@garnachod", "@p_molins", 2383366169]]

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorSiguiendoTwitter()')


class RecolectorSiguendoDeSeguidoresTwitter(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorSiguendoDeSeguidoresTwitter --usuario  ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorSiguendoDeSeguidoresTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorUsuarioTwitter(self.usuario), RecolectorSeguidoresTwitter(self.usuario)]

	def run(self):
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
			for siguiendo in seguidores:
				yield RecolectorSiguiendoTwitter(siguiendo)

		with self.output().open('w') as out_file:
			out_file.write("OK")

		

class RecolectorFavoritosTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorFavoritosTwitter(%s)'%self.usuario)

	def run(self):
		"""
		Realiza una busqueda en TwitterAPI

		Recolecta los favoritos de un usuario dado por nombre de usuario
		o identificador
		"""
		escritores = [EscritorFavoritosNeo4j(-1), EscritorTweetsCassandra(-1)]
		recolector = RecolectorFavoritosUser(escritores)
		while True:
			try:
				identificador = 0
				try:
					identificador = long(self.usuario)
				except Exception, e:
					pass	

				if identificador == 0:
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(id_user=identificador)
				break
			except Exception, e:
				print e
				sleep(1*60)

		with self.output().open('w') as out_file:
			out_file.write("OK")
		
class TestRecolectorFavoritosTwitter(luigi.Task):
	def requires(self):
		return [RecolectorFavoritosTwitter(usuario) for usuario in ["@garnachod"]]

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorSiguiendoTwitter()')


class RecolectorTweetsSiguendoTwitter(luigi.Task):
	"""
		Recolecta en un primer momento los siguiendo de un usuario
		a continuacion descarga todos los tweets de esos siguiendo
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorTweetsSiguendoTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorSiguiendoTwitter(self.usuario), RecolectorUsuarioTwitter(self.usuario)]

	def run(self):
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
			siguiendos = consultasNeo4j.getListaIDsSiguiendoByUserID(identificador)
			for siguiendo in siguiendos:
				yield RecolectorUsuarioTwitter(siguiendo)

		with self.output().open('w') as out_file:
			out_file.write("OK")

class TestRecolectorTweetsSiguendoTwitter(luigi.Task):
	def requires(self):
		return RecolectorTweetsSiguendoTwitter("@garnachod")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorTweetsSiguendoTwitter()')

class RecolectorTweetsSeguidoresTwitter(luigi.Task):
	"""
		Recolecta en un primer momento los siguiendo de un usuario
		a continuacion descarga todos los tweets de esos siguiendo
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorTweetsSeguidoresTwitter --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorTweetsSeguidoresTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorSeguidoresTwitter(self.usuario), RecolectorUsuarioTwitter(self.usuario)]

	def run(self):
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
			for seguidor in seguidores:
				yield RecolectorUsuarioTwitter(seguidor)

		with self.output().open('w') as out_file:
			out_file.write("OK")

class TestRecolectorTweetsSeguidoresTwitter(luigi.Task):
	def requires(self):
		return RecolectorTweetsSeguidoresTwitter("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorTweetsSeguidoresTwitter()')

class RecolectorFavoritosSeguidoresTwitter(luigi.Task):
	"""
		Recolecta en un primer momento los siguiendo de un usuario
		a continuacion descarga todos los tweets de esos siguiendo
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorFavoritosSeguidoresTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorSeguidoresTwitter(self.usuario), RecolectorUsuarioTwitter(self.usuario)]

	def run(self):
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
			for seguidor in seguidores:
				yield RecolectorFavoritosTwitter(seguidor)

		with self.output().open('w') as out_file:
			out_file.write("OK")

class TestRecolectorFavoritosSeguidoresTwitter(luigi.Task):
	def requires(self):
		return RecolectorFavoritosSeguidoresTwitter("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorFavoritosSeguidoresTwitter()')
		
class RecolectorFavoritosSiguiendoTwitter(luigi.Task):
	"""
		Recolecta en un primer momento los siguiendo de un usuario
		a continuacion descarga todos los tweets de esos siguiendo
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorFavoritosSiguiendoTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorSiguiendoTwitter(self.usuario), RecolectorUsuarioTwitter(self.usuario)]

	def run(self):
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
			seguidores = consultasNeo4j.getListaIDsSiguiendoByUserID(identificador)
			for seguidor in seguidores:
				yield RecolectorFavoritosTwitter(seguidor)

		with self.output().open('w') as out_file:
			out_file.write("OK")

class TestRecolectorFavoritosSiguiendoTwitter(luigi.Task):
	def requires(self):
		return RecolectorFavoritosSiguiendoTwitter("@p_molins")

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorFavoritosSiguiendoTwitter()')

class RecolectorTweetsSiguendoStreamTwitter(luigi.Task):
	"""docstring for RecolectorTweetsSiguendoTwitter"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorTweetsSiguendoStreamTwitter --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorTweetsSiguendoStreamTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorSiguiendoTwitter(self.usuario), RecolectorUsuarioTwitter(self.usuario)]


	def run(self):
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
			seguidores = consultasNeo4j.getListaIDsSiguiendoByUserID(identificador)
			escritorList = []
			escritorList.append(EscritorTweetsCassandra(-1))
			recolector = RecolectorTweetsUsersStream(escritorList)
			recolector.recolecta(seguidores)


		with self.output().open('w') as out_file:
			out_file.write("OK")

class RecolectorTweetsSeguidoresStreamTwitter(luigi.Task):
	"""docstring for RecolectorTweetsSiguendoTwitter"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorTweetsSeguidoresStreamTwitter --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget('tasks/RecolectorTweetsSeguidoresStreamTwitter(%s)'%self.usuario)

	def requires(self):
		return [RecolectorSiguiendoTwitter(self.usuario), RecolectorUsuarioTwitter(self.usuario)]


	def run(self):
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
			escritorList = []
			escritorList.append(EscritorTweetsCassandra(-1))
			recolector = RecolectorTweetsUsersStream(escritorList)
			recolector.recolecta(seguidores)


		with self.output().open('w') as out_file:
			out_file.write("OK")
		
if __name__ == "__main__":
	luigi.run()
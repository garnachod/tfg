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
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
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
				sleep(1*60)

		with self.output().open('w') as out_file:
			out_file.write("OK")


class TestRecolectorUsuarioTwitter(luigi.Task):
	def requires(self):
		return [RecolectorUsuarioTwitter(usuario) for usuario in ["@garnachod", "@p_molins", 2383366169]]

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")

	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorUsuarioTwitter()')

class RecolectorSeguidoresTwitter(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitter RecolectorSeguidoresTwitter --usuario ...
	"""
	usuario = luigi.Parameter()

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
					recolector.recolecta(query=self.usuario)
				else:
					recolector.recolecta(id_user=identificador)
				break
			except Exception, e:
				print e
				sleep(1*60)

		with self.output().open('w') as out_file:
			out_file.write("OK")
		
class TestRecolectorSeguidoresTwitter(luigi.Task):
	def requires(self):
		return [RecolectorSeguidoresTwitter(usuario) for usuario in ["@garnachod", "@p_molins", 2383366169]]

	def run(self):
		with self.output().open('w') as out_file:
			out_file.write("OK")
			
	def output(self):
		return luigi.LocalTarget('tasks/TestRecolectorSeguidoresTwitter()')

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
				print e
				sleep(1*60)

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
			siguiendos = consultasNeo4j.getListaIDsSiguendoByUserID(identificador)
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
			seguidores = consultasNeo4j.getListaIDsSiguendoByUserID(identificador)
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
		
if __name__ == "__main__":
	luigi.run()
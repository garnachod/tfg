# -*- coding: utf-8 -*-
from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython
from time import time

class RecolectorFavoritosUser(Recolector):
	def __init__(self, escritor):
		super(RecolectorFavoritosUser, self).__init__(escritor)
		self.authorizator = GetAuthorizations(15)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 6
		self.inicializa()

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, query=None, id_user=-1):
		#TODO recolectar todos los favoritos si flag activa
		if query is None and id_user == -1:
			raise Exception('Al menos debe haber un parametro usable')

		if query is not None:
			if query[0] == '@':
				query = query[1:]

			id_user = self.apoyo.getUserIDByScreenName(query)
			if id_user == None:
				raise Exception('El usuario debe estar en la base de datos')

		print id_user
		tweets = self.privateRealizaConsulta(id_user)

		relaciones = []
		for tweet in tweets:
			#el usuario1 -[:FAV]-> el tweet X
			relaciones.append((id_user, tweet["id"]))

		self.guarda(tweets, relaciones)
	

	def guarda(self, arrayDatos, relaciones):
		#mal diseño sorry
		for escritor in self.escritores:
			if "EscritorTweets" in escritor.__class__.__name__:
				escritor.escribe(arrayDatos)
			else:
				escritor.escribe(relaciones)



	def privateRealizaConsulta(self, identificador):
		count = 200
		if self.authorizator.is_limit_api(self.tipo_id):
			return []

		try:
			retorno = self.twitter.get_favorites(user_id=identificador, count=count)
			self.authorizator.add_query_to_key(self.tipo_id)

			return retorno
		except Exception, e:
			print e
			self.authorizator.add_query_to_key(self.tipo_id)
			if "429" in str(e):
				raise Exception('LIMITE')



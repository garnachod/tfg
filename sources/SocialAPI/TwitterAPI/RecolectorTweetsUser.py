# -*- coding: utf-8 -*-
from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython
from time import time

class RecolectorTweetsUser(Recolector):
	"""docstring for RecolectorTweetsUser"""
	def __init__(self, escritor):
		super(RecolectorTweetsUser, self).__init__(escritor)
		self.authorizator = GetAuthorizations(300)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 1
		self.inicializa()
		

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, query):
		#start_time = time()
		#tiempo_baseDatos = 0
		#tiempo_api = 0

		arrayFinal = []
		if query[0] == '@':
			query = query[1:]
		minimo = self.apoyo.getLastTweetCollected(query)
		maximo = 0
		maximoGlobal = long(0)

		cont = 0
		while True:
			#tiempo_api_ini = time()
			statuses = self.privateRealizaConsulta(query, maxi=maximo, mini=minimo)
			#tiempo_api_fin = time()
			#tiempo_api += tiempo_api_fin - tiempo_api_ini
			

			if len(statuses) == 0:
				break

			for status in statuses:
				arrayFinal.append(status)

			#fin de for
			maximo = self.getMinIDtweets(arrayFinal, query)
			maximo -= 1
			if len(arrayFinal) > 50:
				#tiempo_baseDatos_ini = time()
				self.guarda(arrayFinal)
				#tiempo_baseDatos_fin = time()
				#tiempo_baseDatos += tiempo_baseDatos_fin - tiempo_baseDatos_ini
				auxMax = self.getMaxIDtweets(arrayFinal, query)
				if auxMax > maximoGlobal:
					maximoGlobal = auxMax
					
				cont += len(arrayFinal)
				arrayFinal = []
			

			#limite de la api
			if len(arrayFinal) > 3200:
				break

		#fin del while
		#tiempo_baseDatos_ini = time()
		self.guarda(arrayFinal)
		#tiempo_baseDatos_fin = time()
		#tiempo_baseDatos += tiempo_baseDatos_fin - tiempo_baseDatos_ini
		if maximoGlobal != 0:
			self.apoyo.setLastUserTweet(query, maximoGlobal)

		#elapsed_time = time() - start_time
		#print("Elapsed time total: %0.10f seconds." % elapsed_time)
		#print("Elapsed time DB: %0.10f seconds." % tiempo_baseDatos)
		#print("Elapsed time API: %0.10f seconds." % tiempo_api)

	def guarda(self, arrayDatos):
		for escritor in self.escritores:
			escritor.escribe(arrayDatos)
		

	def getMinIDtweets(self, tweets, query):

		minimo = long(10**20)
		for tweet in tweets:
			if tweet["user"]["screen_name"] == query:
				if minimo > tweet["id"]:
					minimo = tweet["id"]
		if minimo == long(10**20):
			return 0

		return minimo

	def getMaxIDtweets(self, tweets, query):

		maximo = long(0)
		for tweet in tweets:
				if tweet["id"] > maximo:
					maximo = tweet["id"]

		return maximo


	def privateRealizaConsulta(self, query, maxi=0, mini=0):
		if self.authorizator.is_limit_api(self.tipo_id):
				return []

		try:
			if maxi == 0 and mini == 0: 
				retorno = self.twitter.get_user_timeline(screen_name=query, count='200')
			elif maxi == 0 and mini > 0:
				retorno = self.twitter.get_user_timeline(screen_name=query, since_id=mini, count='200')
			elif maxi > 0 and mini == 0:
				retorno = self.twitter.get_user_timeline(screen_name=query, max_id=maxi, count='200')
			else:
				retorno = self.twitter.get_user_timeline(screen_name=query, max_id=maxi, since_id=mini, count='200')

			self.authorizator.add_query_to_key(self.tipo_id)
			return retorno
		except Exception, e:
			print e
			return []
			

	def privateParseaStatus(self, status):
		arrayTweets = []
		
		arrayTweets.append(status)

		return arrayTweets

	def privateParseaUserFormStatus(self, userAPI):
		user = {}
		#id
		user["id"] = userAPI["id"]
		#name
		user["name"] = userAPI["name"]
		#screen name
		user["screen_name"] = userAPI["screen_name"]
		#location
		user["location"] = userAPI["location"]
		#followers_count
		user["followers_count"] = userAPI["followers_count"]
		#created_at
		user["created_at"] = userAPI["created_at"]

		return user
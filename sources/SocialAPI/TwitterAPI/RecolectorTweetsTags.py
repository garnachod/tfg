from RecolectorTweetsUser import RecolectorTweetsUser

class RecolectorTweetsTags(RecolectorTweetsUser):
	"""docstring for RecolectorTweetsTags"""
	def __init__(self, escritor):
		super(RecolectorTweetsTags, self).__init__(escritor)


	def recolecta(self, query):
		arrayFinal = []
		maximo = long(0)
		cont = 0
		while True:
			statuses = self.privateRealizaConsulta(query, maxi=maximo)
			self.authorizator.add_query_to_key()

			if len(statuses) == 0:
				break

			for status in statuses:
				#parseo del retorno a array de objetos que entiende el escritor
				arrayTemporal = self.privateParseaStatus(status)

				for tweet in arrayTemporal:
					arrayFinal.append(tweet)
			#fin de for
			maximo = self.getMinIDtweets(arrayFinal, query)
			maximo -= 1
			if len(arrayFinal) > 50:
				self.guarda(arrayFinal)
				cont += len(arrayFinal)
				arrayFinal = []
				
			#limite puesto por defecto
			if cont > 2000:
				break

		#fin del while
		self.guarda(arrayFinal)


	def privateRealizaConsulta(self, query, maxi=0, mini=0):
		if self.authorizator.is_limit_api():
				return []

		try:
			if maxi == 0 and mini == 0: 
				retorno = self.twitter.search(q=query, count='100')
			elif maxi == 0 and mini > 0:
				retorno = self.twitter.search(q=query, since_id=mini, count='100')
			elif maxi > 0 and mini == 0:
				retorno = self.twitter.search(q=query, max_id=maxi, count='100')
			else:
				retorno = self.twitter.search(q=query, max_id=maxi, since_id=mini, count='100')

			return retorno["statuses"]
		except Exception, e:
			print e
			return []


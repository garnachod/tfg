from RecolectorTweetsUser import RecolectorTweetsUser
from time import time

class RecolectorTweetsTags(RecolectorTweetsUser):
	"""docstring for RecolectorTweetsTags"""
	def __init__(self, escritor):
		super(RecolectorTweetsTags, self).__init__(escritor)
		self.authorizator.set_limit_api(450)
		self.tipo_id = 2


	def recolecta(self, query):
		#start_time = time()
		#tiempo_baseDatos = 0
		#tiempo_api = 0

		arrayFinal = []
		maximo = long(0)
		cont = 0
		while True:
			#tiempo_api_ini = time()
			statuses = self.privateRealizaConsulta(query, maxi=maximo)
			#tiempo_api_fin = time()
			#tiempo_api += tiempo_api_fin - tiempo_api_ini
			

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
			if len(arrayFinal) > 100:
				#tiempo_baseDatos_ini = time()
				self.guarda(arrayFinal)
				#tiempo_baseDatos_fin = time()
				#tiempo_baseDatos += tiempo_baseDatos_fin - tiempo_baseDatos_ini
				cont += len(arrayFinal)
				arrayFinal = []
				
			#limite puesto por defecto
			if cont > 2000:
				break

		#fin del while
		#tiempo_baseDatos_ini = time()
		self.guarda(arrayFinal)
		#tiempo_baseDatos_fin = time()
		#tiempo_baseDatos += tiempo_baseDatos_fin - tiempo_baseDatos_ini

		#elapsed_time = time() - start_time
		#print("Elapsed time total: %0.10f seconds." % elapsed_time)
		#print("Elapsed time DB: %0.10f seconds." % tiempo_baseDatos)
		#print("Elapsed time API: %0.10f seconds." % tiempo_api)


	def privateRealizaConsulta(self, query, maxi=0, mini=0):
		if self.authorizator.is_limit_api(self.tipo_id):
				return []

		#try:
		if maxi == 0 and mini == 0: 
			retorno = self.twitter.search(q=query, count='100')
		elif maxi == 0 and mini > 0:
			retorno = self.twitter.search(q=query, since_id=mini, count='100')
		elif maxi > 0 and mini == 0:
			retorno = self.twitter.search(q=query, max_id=maxi, count='100')
		else:
			retorno = self.twitter.search(q=query, max_id=maxi, since_id=mini, count='100')

		self.authorizator.add_query_to_key(self.tipo_id)
		return retorno["statuses"]
		#except Exception, e:
		#	print e
		#	return []


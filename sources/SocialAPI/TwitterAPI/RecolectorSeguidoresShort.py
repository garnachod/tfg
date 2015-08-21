from SocialAPI.Recolector import Recolector
from ApoyoTwitter import ApoyoTwitter
from getAuthorizations import GetAuthorizations
from twython import Twython

class RecolectorSeguidoresShort(Recolector):
	def __init__(self, escritores):
		super(RecolectorSeguidoresShort, self).__init__(escritores)
		self.authorizator = GetAuthorizations(15)
		self.twitter = None
		self.apoyo = ApoyoTwitter()
		self.tipo_id = 4
		self.inicializa()
		self.cursor = -1
		

	def inicializa(self):
		self.authorizator.load_twitter_token(self.tipo_id)
		api_key, access_token = self.authorizator.get_twython_token()
		self.twitter = Twython(api_key, access_token=access_token)

	def recolecta(self, query):
		self.cursor = -1
		arrayUsuarios = []

		if query[0] == '@':
			query = query[1:]

		while True:
			retorno = self.privateRealizaConsulta(query)
			if retorno == []:
				return

			self.cursor = retorno["next_cursor"]
			break

		self.guarda(retorno["ids"])

	def guarda(self, arrayDatos):
		for escritor in self.escritores:
			escritor.escribe(arrayDatos)

	def privateRealizaConsulta(self, query):
		if self.authorizator.is_limit_api(self.tipo_id):
				return []

		try:
			retorno = self.twitter.get_followers_ids(screen_name=query, cursor=self.cursor, count='5000')
			self.authorizator.add_query_to_key(self.tipo_id)

			if len(retorno["ids"]) == 0:
				return []

			return retorno
		except Exception, e:
			print e
			return []
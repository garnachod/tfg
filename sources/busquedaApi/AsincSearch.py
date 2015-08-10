#from Skynet import Skynet
from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorTweets import EscritorTweets
from DBbridge.EscritorBusquedaTweets import EscritorBusquedaTweets
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
import threading
import time

class AsincSearch(threading.Thread):  
	def __init__(self, tipo, texto, user_id, searchID):
		threading.Thread.__init__(self)
		self.tipo = tipo
		self.texto = texto
		self.user_id = user_id
		self.consultas = ConsultasGeneral()
		self.searchID = searchID
  
	def run(self):
		inicio = time.time()
		if self.tipo == 'suser':
			#skynet = Skynet(self.user_id)
			#skynet.research_user(self.texto, self.searchID)
			escritorList = []
			escritorList.append(EscritorTweets(self.searchID))
			escritorList.append(EscritorBusquedaTweets(self.searchID))
			recolector = RecolectorTweetsUser(escritorList)
			recolector.recolecta(self.texto)

			fin = time.time()
			self.consultas.setAppSearchTime(self.searchID, fin - inicio)
		elif self.tipo == 'topic':
			escritorList = []
			escritorList.append(EscritorTweets(self.searchID))
			escritorList.append(EscritorBusquedaTweets(self.searchID))
			recolector = RecolectorTweetsTags(escritorList)
			recolector.recolecta(self.texto)

			fin = time.time()
			self.consultas.setAppSearchTime(self.searchID, fin - inicio)
		else:
			return 'ERR'
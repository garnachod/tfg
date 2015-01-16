from Skynet import Skynet
from DBbridge.ConsultasGeneral import ConsultasGeneral
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
			skynet = Skynet(self.user_id)
			skynet.research_user(self.texto, self.searchID);
			fin = time.time()

			self.consultas.setAppSearchTime(self.searchID, fin - inicio)
		elif self.tipo == 'topic':
			skynet = Skynet(self.user_id)
			lista_keywords = self.texto.replace(" ", "").split(",")
			skynet.research_keywords(lista_keywords, self.searchID);
			fin = time.time()

			self.consultas.setAppSearchTime(self.searchID, fin - inicio)
		else:
			return 'ERR'
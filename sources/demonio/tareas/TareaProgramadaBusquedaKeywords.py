from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorTweets import EscritorTweets
from DBbridge.ConexionSQL import ConexionSQL
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from TareaProgramada import TareaProgramada

class TareaProgramadaBusquedaKeywords(TareaProgramada):
	def __init__(self):
		super(TareaProgramadaBusquedaKeywords, self).__init__()
		self.tipo = "BusquedaSencillaKeywords"
		self.consultas = ConsultasGeneral()

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id);
		#skynet = Skynet(user_id)
		#lista_keywords = cadenaBusqueda.replace(" ", "").split(",")
		#skynet.research_keywords(lista_keywords, self.search_id);
		escritorList = []
		escritorList.append(EscritorTweets(ConexionSQL(), self.searchID))
		escritorList.append(EscritorBusquedaTweets(ConexionSQL(), self.searchID))
		recolector = RecolectorTweetsTags(escritorList)
		recolector.recolecta(cadenaBusqueda)

		
		return True

	def doPostProc(self):
		return None

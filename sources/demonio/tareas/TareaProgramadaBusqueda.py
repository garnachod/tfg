from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorTweets import EscritorTweets
from DBbridge.ConexionSQL import ConexionSQL
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from TareaProgramada import TareaProgramada

class TareaProgramadaBusqueda(TareaProgramada):
	def __init__(self):
		super(TareaProgramadaBusqueda, self).__init__()
		self.tipo = "BusquedaSencillaUsuario"
		self.consultas = ConsultasGeneral()

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id)
		#skynet = Skynet(user_id)
		#skynet.research_user(cadenaBusqueda, self.search_id);
		escritorList = []
		escritorList.append(EscritorTweets(self.searchID))
		escritorList.append(EscritorBusquedaTweets(self.searchID))
		recolector = RecolectorTweetsUser(escritorList)
		recolector.recolecta(cadenaBusqueda)

		return True

	def doPostProc(self):
		return None

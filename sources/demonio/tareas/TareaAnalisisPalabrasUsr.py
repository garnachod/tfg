from TareaAnalisisPalabrasK import TareaAnalisisPalabrasK
from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorTweets import EscritorTweets
from DBbridge.ConexionSQL import ConexionSQL
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from MachineLearning.ClasificadorTweets import ClasificadorTweets


class TareaAnalisisPalabrasUsr(TareaAnalisisPalabrasK):
	"""docstring for TareaAnalisisPalabrasK"""
	def __init__(self):
		super(TareaAnalisisPalabrasUsr, self).__init__()
		self.tipo = "AnalisisPalabrasUsuario"

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id)
		escritorList = []
		escritorList.append(EscritorTweets(ConexionSQL(), self.searchID))
		escritorList.append(EscritorBusquedaTweets(ConexionSQL(), self.searchID))
		recolector = RecolectorTweetsUser(escritorList)
		recolector.recolecta(cadenaBusqueda)
		return True

from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorTweets import EscritorTweets
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from DBbridge.EscritorBusquedaTweets import EscritorBusquedaTweets
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from TareaProgramada import TareaProgramada

class TareaProgramadaBusqueda(TareaProgramada):
	def __init__(self):
		super(TareaProgramadaBusqueda, self).__init__()
		self.tipo = "BusquedaSencillaUsuario"
		self.consultas = ConsultasGeneral()
		self.cassandra_active = True

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id)
		
		escritorList = []
		if self.cassandra_active:
			escritorList.append(EscritorTweetsCassandra(self.search_id))
		else:
			escritorList.append(EscritorTweets(self.search_id))
		escritorList.append(EscritorBusquedaTweets(self.search_id))

		recolector = RecolectorTweetsUser(escritorList)
		recolector.recolecta(query=cadenaBusqueda)

		return True

	def doPostProc(self):
		return None

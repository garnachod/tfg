from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorTweets import EscritorTweets
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from DBbridge.EscritorBusquedaTweets import EscritorBusquedaTweets
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from TareaProgramada import TareaProgramada

class TareaProgramadaBusquedaKeywords(TareaProgramada):
	def __init__(self):
		super(TareaProgramadaBusquedaKeywords, self).__init__()
		self.tipo = "BusquedaSencillaKeywords"
		self.consultas = ConsultasGeneral()
		self.cassandra_active = True

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id);
		
		escritorList = []
		if self.cassandra_active:
			escritorList.append(EscritorTweetsCassandra(self.search_id))
		else:
			escritorList.append(EscritorTweets(self.search_id))
		escritorList.append(EscritorBusquedaTweets(self.search_id))

		recolector = RecolectorTweetsTags(escritorList)
		recolector.recolecta(cadenaBusqueda)

		
		return True

	def doPostProc(self):
		return None

from TareaProgramada import TareaProgramada
from DBbridge.ConsultasGeneral import ConsultasGeneral
from DBbridge.EscritorSeguidoresNeo4j import EscritorSeguidoresNeo4j
from SocialAPI.TwitterAPI.RecolectorSeguidoresShort import RecolectorSeguidoresShort

class TareaProgramadaSeguidores(object):
	"""docstring for TareaProgramadaSeguidores"""
	def __init__(self):
		super(TareaProgramadaSeguidores, self).__init__()
		self.tipo = "BusquedaSeguidores"
		self.consultas = ConsultasGeneral()

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id)

		escritores = [EscritorSeguidoresNeo4j(self.search_id)]
		recolector = RecolectorSeguidoresShort(escritores)
		recolector.recolecta(cadenaBusqueda)
		
		return True

	def doPostProc(self):
		return None
from Skynet import Skynet
from DBbridge.ConsultasGeneral import ConsultasGeneral
from TareaProgramada import TareaProgramada

class TareaProgramadaBusquedaKeywords(TareaProgramada):
	def __init__(self):
		super(TareaProgramadaBusquedaKeywords, self).__init__()
		self.tipo = "BusquedaSencillaKeywords"
		self.consultas = ConsultasGeneral()

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id);
		skynet = Skynet(user_id)
		lista_keywords = cadenaBusqueda.replace(" ", "").split(",")
		skynet.research_keywords(lista_keywords, self.search_id);
		return True

	def doPostProc(self):
		return None

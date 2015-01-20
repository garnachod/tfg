from Skynet import Skynet
from DBbridge.ConsultasGeneral import ConsultasGeneral
from TareaProgramada import TareaProgramada

class TareaProgramadaBusqueda(TareaProgramada):
	def __init__(self):
		super(TareaProgramadaBusqueda, self).__init__()
		self.tipo = "BusquedaSencillaUsuario"
		self.consultas = ConsultasGeneral()

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id);
		skynet = Skynet(user_id)
		skynet.research_user(cadenaBusqueda, self.search_id);
		return True

	def doPostProc(self):
		return None

from TareaAnalisisPalabrasK import TareaAnalisisPalabrasK
from DBbridge.ConsultasGeneral import ConsultasGeneral
from MachineLearning.ClasificadorTweets import ClasificadorTweets
from Skynet import Skynet


class TareaAnalisisPalabrasUsr(TareaAnalisisPalabrasK):
	"""docstring for TareaAnalisisPalabrasK"""
	def __init__(self):
		super(TareaAnalisisPalabrasUsr, self).__init__()
		self.tipo = "AnalisisPalabrasUsuario"

	def doSearch(self):
		cadenaBusqueda, user_id = self.consultas.getBusquedaFromIdBusqueda(self.search_id);
		skynet = Skynet(user_id)
		skynet.research_user(cadenaBusqueda, self.search_id);
		return True

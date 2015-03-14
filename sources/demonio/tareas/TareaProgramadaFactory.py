from TareaProgramadaBusqueda import TareaProgramadaBusqueda
from TareaProgramadaBusquedaKeywords import TareaProgramadaBusquedaKeywords
from TareaAnalisisPalabrasK import TareaAnalisisPalabrasK
from TareaAnalisisPalabrasUsr import TareaAnalisisPalabrasUsr

class TareaProgramadaFactory():
	"""docstring for TareaProgramadaFactory"""
	@staticmethod
	def generaTarea(tipo):
		if tipo == "BusquedaSencillaUser":
			return TareaProgramadaBusqueda()
		elif tipo == "BusquedaSencillaKeywords":
			return TareaProgramadaBusquedaKeywords()
		elif tipo == "AnalisisPalabrasKeywords":
			return TareaAnalisisPalabrasK()
		elif tipo == "AnalisisPalabrasUser":
			return TareaAnalisisPalabrasUsr()
		else:
			return None
		
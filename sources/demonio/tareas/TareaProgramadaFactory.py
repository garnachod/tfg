from TareaProgramadaBusqueda import TareaProgramadaBusqueda


class TareaProgramadaFactory():
	"""docstring for TareaProgramadaFactory"""
	@staticmethod
	def generaTarea(tipo):
		if tipo == "BusquedaSencillaUser":
			return TareaProgramadaBusqueda()
		else:
			return None
		
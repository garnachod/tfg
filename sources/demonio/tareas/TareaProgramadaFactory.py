from TareaProgramadaBusqueda import TareaProgramadaBusqueda


class TareaProgramadaFactory():
	"""docstring for TareaProgramadaFactory"""
	@staticmethod
	def generaTarea(tipo):
		if tipo == "BusquedaSencilla":
			return TareaProgramadaBusqueda()
		else:
			return None
		
from TareaProgramadaFactory import TareaProgramadaFactory
from TareaProgramada import TareaProgramada
from DBbridge.ConsultasGeneral import ConsultasGeneral

class GeneraTareasDesdeDB():
	def __init__(self):
		self.consultas = ConsultasGeneral()

	def genera(self):
		rows = self.consultas.getTareasPendientesTotal()

		if rows == False:
			return None

		tareas = []
		for row in rows:
			tarea = TareaProgramadaFactory.generaTarea(row[1])
			tarea.setId(int(row[0]))
			tarea.setSearchID(int(row[2]))
			tareas.append(tarea)

		return tareas

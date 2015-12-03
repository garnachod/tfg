# -*- coding: utf-8 -*-
#Para prueba unitarias
import os
import sys
lib_path = os.path.abspath('/home/dani/tfg/sources')
sys.path.append(lib_path)

import luigi
from AnalisisTextosInvestigacion import *
from Analiticas import *
from Grafos import *

class InformeVersionDiciembre(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Informes InformeVersionDiciembre --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='./informes/%s/json/terms.json'%self.usuario)

	def requires(self):
		return [LDAvisJSONUsuario(self.usuario), 
				SimilitudSeguidoresTodosTopicLDA2Doc2VecJSON(self.usuario), 
				HistogramaAccionesParagraphVectorTopicsSemanaTwitter(self.usuario),
				GeneradorUsuariosPropiedadesToJSON(self.usuario)]

	def run(self):
		diccionario = {"SimilitudSeguidores" : "users.json", 
						"LDAvis":"terms.json",
						"HistogramaAcciones" : "hours.json",
						"GeneradorUsuarios": "stats.json"}

		rutaRelativa = './informes/%s/json/'%self.usuario

		if not os.path.exists(rutaRelativa):
			os.makedirs(rutaRelativa)


		for input in self.input():
			with input.open("r") as in_file:
				for elemento in diccionario:
					if elemento in input.path:
						if elemento == "LDAvis":
							with self.output().open("w") as out_file:
								contenido = in_file.read()
								out_file.write(contenido)
						else:
							with open(rutaRelativa + diccionario[elemento],"w") as out_file:
								contenido = in_file.read()
								out_file.write(contenido)

class UploadInformeVersionDiciembre(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module Informes UploadInformeVersionDiciembre --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='./informes/UploadInformeVersionDiciembre(%s)'%self.usuario)

	def requires(self):
		return InformeVersionDiciembre(self.usuario)

	def run(self):
		print os.system("/home/dani/tfg/sources/LuigiTasks/subirCliente.sh " + self.usuario)
						
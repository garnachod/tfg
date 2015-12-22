# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
import json

from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j


class GetPropiedadesVariosUsuarios(luigi.Task):
	"""genera un json de propiedades de usuarios 
	   Donde [{"usuario":nombre,"#followers":numero,"#following":numero,"#tw":numero,"#fav":numero, "#rtw"}]"""

	"""
		Uso:
			PYTHONPATH='' luigi --module PropiedadesUsuarios GetPropiedadesVariosUsuarios --nombrefichero ...
	"""

	nombrefichero = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='propiedades_usuarios/GetPropiedades%s'%self.nombrefichero)

	def run(self):
		#contiene una matriz de lineas
		lineas = []
		with open('propiedades_usuarios/%s'%self.nombrefichero) as in_file:
			for i, line in enumerate(in_file):
				if i == 0:
					pass
				else:
					lineas.append(line.replace("\n", "").split(","))

		cs = ConsultasCassandra()
		neo = ConsultasNeo4j()


		retornoJSON = []
		for linea in lineas:
			objJSON = {"usuario":linea[0]}
			#followers
			if linea[1] == "1":
				try:
					objJSON["#followers"] = cs.getFollowersByUserID(cs.getUserIDByScreenNameCassandra(linea[0]))[0][0]
				except Exception, e:
					objJSON["#followers"] = 0
			#following
			if linea[2] == "1":
				try:
					objJSON["#following"] = cs.getFollowingByUserID(cs.getUserIDByScreenNameCassandra(linea[0]))[0][0]
				except Exception, e:
					objJSON["#following"] = 0
			#numero tws
			if linea[3] == "1":
				try:
					twts = cs.getTweetsUsuarioCassandra(linea[0], limit=10000)
					i = 0
					for tw in twts:
						i += 1
					objJSON["#tw"] = i
				except Exception, e:
					objJSON["#tw"] = 0

			#numero fav
			if linea[4] == "1":
				try:
					objJSON["#fav"] = len(neo.getListaIDsFavsByUserID(cs.getUserIDByScreenNameCassandra(linea[0])))
				except Exception, e:
					objJSON["#fav"] = 0

			#numero tws
			if linea[5] == "1":
				try:
					twts = cs.getTweetsUsuarioCassandra(linea[0], limit=10000)
					i = 0
					for tw in twts:
						if tw.orig_tweet != 0:
							i += 1
					objJSON["#rtw"] = i
				except Exception, e:
					objJSON["#rtw"] = 0

			retornoJSON.append(objJSON)


		with self.output().open("w") as out_file:
			out_file.write(json.dumps(retornoJSON))
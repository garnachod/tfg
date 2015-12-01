# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import networkx as nx

import luigi
import time

from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasCassandra import ConsultasCassandra

from GeneradorDocumentosTwitter import *


class GeneradorGrafoCSVUsuario(luigi.Task):
	"""
		Genera un grafo csv
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module Grafos GeneradorGrafoCSVUsuario --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='grafos/GeneradorGrafoCSVUsuario(%s)'%self.usuario)

	def run(self):
		consultasCassandra = ConsultasCassandra()
		consultasGrafo = ConsultasNeo4j()

		start = time.clock()

		user_id = consultasCassandra.getUserIDByScreenNameCassandra(self.usuario)
		poblacion = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)
		poblacion.append(user_id)
		screenNames = [consultasCassandra.getScreenNameByUserIDCassandra(ide) for ide in poblacion]
		G = nx.DiGraph()
		G.add_nodes_from(screenNames) #  Se puede sustituir por G = nx.DiGraph(poblacion) 
		dicPoblacion = dict ( zip ( poblacion, screenNames ) )
		# Como hablamos, he definido la poblacion como un diccionario para que...
		duracion1 = time.clock() - start

		dicTiemposConsultas = {}
		duracion2 = 0
		for nodo in poblacion:
			start = time.clock()
			padresNodo = consultasGrafo.getListaIDsSiguiendoByUserID( nodo )
			for padre in padresNodo:
				if padre in dicPoblacion: # ...esto fuese mas eficiente
					G.add_edge( dicPoblacion[nodo] , dicPoblacion[padre] )
			dicTiemposConsultas[ dicPoblacion[nodo] ] = time.clock() - start
			duracion2 += time.clock() - start


		# PARTE 2: Escritura en CSV
		
		start = time.clock()
		nodos = G.nodes()
		with self.output().open('w') as fichero:
			# En la primera fila del csv guardo los nodos, podria guardarse en un CSV a parte
			fichero.write( str(nodos[0]) )
			for nodo in nodos[1:]:
				fichero.write(",")
				fichero.write( str(nodo) )
			fichero.write("\n")
			
			dicTiemposEscritura = []
			seguidores_raros = []
			n = 0
			# En la (n+1)-esima fila del csv guardo los padre del n-esimo nodo
			for lista in G.adjacency_list():
				start = time.clock()
				if len(lista) > 0:
					fichero.write( str(lista[0]) )
					for padre in lista[1:]:
						fichero.write(",")
						fichero.write( str(padre))
				else:
					seguidores_raros.append( nodos[n] )
				n += 1
				fichero.write("\n")
				dicTiemposEscritura.append( time.clock() - start )

class GeneradorGrafoGephiUsuario(luigi.Task):
	"""
		Genera un grafo csv
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module Grafos GeneradorGrafoGephiUsuario --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='grafos/GeneradorGrafoGephi_Nodos(%s)'%self.usuario)

	def requires(self):
		return GeneradorGrafoCSVUsuario(self.usuario)

	def run(self):
		nodos = {}
		nodosAristas = {}
		with self.input().open('r') as in_file:
			for i, linea in enumerate(in_file):
				nodosLista = linea.replace("\n", "").split(",")
				if i == 0:
					for j, nodo in enumerate(nodosLista):
						nodos[nodo] = j
						nodosAristas[nodo] = []
				else:
					nodoToAppend = nodosLista[0]
					for nodo in nodosLista[1:]:
						nodosAristas[nodoToAppend].append(nodos[nodo])

		with self.output().open('w') as out_file:
			out_file.write("Id,Label\n")
			for nodo in nodos:
				if nodo != "None":
					out_file.write(str(nodos[nodo]))
					out_file.write(",")
					out_file.write(nodo)
					out_file.write("\n")

		with open('grafos/GeneradorGrafoGephi_Aristas(%s)'%self.usuario,'w') as out_file:
			out_file.write("source,target\n")
			for nodo in nodosAristas:
				for arista in nodosAristas[nodo]:
					out_file.write(str(nodos[nodo]))
					out_file.write(",")
					out_file.write(str(arista))
					out_file.write("\n")


class GeneradorGrafoGephiUsuarioPropiedades(luigi.Task):
	"""
		Genera un grafo csv
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module Grafos GeneradorGrafoGephiUsuarioPropiedades --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='grafos/GeneradorGrafoGephiPropiedades_Nodos(%s)'%self.usuario)

	def requires(self):
		return [GeneradorGrafoGephiUsuario(self.usuario), AcumulaEventosSeguidoresUsuarioTiempo(self.usuario)]

	def run(self):
		nodos = {}
		consultasCassandra = ConsultasCassandra()
		
		for input in self.input():
			with input.open('r') as in_file:
				#leemos el grafo
				if "GeneradorGrafo" in input.path:
					for i, linea in enumerate(in_file):
						nodosLista = linea.replace("\n", "").split(",")
						if nodosLista[1] not in nodos:
							nodos[nodosLista[1]] = {}

						nodos[nodosLista[1]]["id_gephi"] = nodosLista[0]

				#leemos los eventos
				#e.j. 598725062,(rt;0),(tw;0),(fav;0)
				elif "AcumulaEventos" in input.path:
					for i, linea in enumerate(in_file):
						lineaSplit = linea.replace("\n", "").split(",")
						id_usuario = lineaSplit[0]
						nombreUsuario = consultasCassandra.getScreenNameByUserIDCassandra(long(id_usuario))
						if nombreUsuario is None:
							continue

						actividadTotal = 0
						for actividad in lineaSplit[1:]:
							ac = actividad.replace("(", "").replace(")", "").split(";")
							tipo = ac[0]
							numero = int(ac[1])
							actividadTotal += numero

						if nombreUsuario not in nodos:
							nodos[nombreUsuario] = {}

						nodos[nombreUsuario]["actividad"] = actividadTotal

		#ahora conseguimos los followers
		for usuario in nodos:
			usuario_id = consultasCassandra.getUserIDByScreenNameCassandra(usuario)
			if usuario_id is None:
				nodos[usuario]["followers"] = 0
			else:
				nodos[usuario]["followers"] = consultasCassandra.getFollowersByUserID(usuario_id)[0].followers

		with self.output().open('w') as out_file:
			out_file.write("Id,Label,Actividad,Followers\n")
			for nodo in nodos:
				if "actividad" not in nodos[nodo] or "followers" not in nodos[nodo] or "id_gephi" not in nodos[nodo]:
					continue
				out_file.write(str(nodos[nodo]["id_gephi"]))
				out_file.write(",")
				out_file.write(nodo)
				out_file.write(",")
				out_file.write(str(nodos[nodo]["actividad"]))
				out_file.write(",")
				out_file.write(str(nodos[nodo]["followers"]))
				out_file.write("\n")


if __name__ == "__main__":
	luigi.run()
# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from Neo4j.ConexionNeo4j import ConexionNeo4j
from blist import blist
from py2neo import cypher

class ConsultasNeo4jInstagram(object):
	"""docstring for ConsultasNeo4j"""
	def __init__(self):
		super(ConsultasNeo4jInstagram, self).__init__()
		self.graph = ConexionNeo4j().getGraph()

	def getListaIDsSeguidoresByUserID(self, user_id):
		queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user_insta {id_insta : {ID}}) return a"
		nodos = self.graph.cypher.execute(queryNeo4j, {"ID":user_id})
		identificadores = blist([])
		for nodo in nodos:
			identificadores.append(long(nodo[0].properties["id_insta"]))

		return identificadores


if __name__ == '__main__':
	print ConsultasNeo4jInstagram().getListaIDsSeguidoresByUserID(2230241197)
# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

import networkx as nx
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasWeb import ConsultasWeb

import scipy as sp
from scipy.sparse import linalg


if __name__ == '__main__':
	consultas = ConsultasWeb()
	user_id = consultas.getUserIDByScreenName("p_molins")
	print user_id
	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)

	#G=nx.DiGraph()
	G=nx.Graph()
	G.add_node(user_id)
	for i, ide in enumerate(identificadores):
		G.add_node(ide)
		G.add_edge(ide,user_id)
		ident2 = consultasGrafo.getListaIDsSeguidoresByUserID(ide)
		for ide2 in ident2:
			G.add_node(ide2)
			G.add_edge(ide2, ide)

		if i > 200:
			break

	print nx.pagerank_scipy(G, max_iter=100, weight=None)
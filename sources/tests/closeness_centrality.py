# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import networkx as nx
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from DBbridge.ConsultasWeb import ConsultasWeb

if __name__ == '__main__':
	consultas = ConsultasWeb()
	user_id = consultas.getUserIDByScreenName("p_molins")
	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)

	#G=nx.DiGraph()
	G=nx.Graph()
	G.add_node(user_id)
	for ide in identificadores:
		G.add_node(ide)
		G.add_edge(ide,user_id)
		ident2 = consultasGrafo.getListaIDsSeguidoresByUserID(ide)
		for ide2 in ident2:
			G.add_node(ide2)
			G.add_edge(ide2, ide)


	print "closeness_centrality"
	nx.closeness_centrality(G)
	print "betweenness_centrality"
	nx.betweenness_centrality(G, k=200)
	print "katz_centrality"
	nx.katz_centrality(G, tol=1e-02)
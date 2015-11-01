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

		if i > 30:
			break


	print G.number_of_nodes()
	print "closeness_centrality"
	#nx.closeness_centrality(G)
	print "betweenness_centrality"
	#nx.betweenness_centrality(G, k=200)
	print "katz_centrality"

	M = nx.to_scipy_sparse_matrix(G, nodelist=G.nodes(), weight='weight',dtype=float)
	eigenvalue, eigenvector = linalg.eigs(M.T, k=1, which='LR')
	largest = eigenvector.flatten().real
	M = False

	dicc = nx.katz_centrality_numpy(G, alpha=(1.0/(largest+1)))

	array_tuples = []
	for key in dicc:
		array_tuples.append((key, dicc[key]))

	sortedArray = sorted(array_tuples, key=lambda tuple: tuple[1], reverse=True)

	for i in range(50):
		print str(sortedArray[i][0]) + " -> " + str(sortedArray[i][1])
	#nx.katz_centrality(G, tol=1e-02)



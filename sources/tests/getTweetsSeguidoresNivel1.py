# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra
from DBbridge.Neo4j.ConexionNeo4j import ConexionNeo4j
import datetime
from time import time, sleep


def recopila(lista_ids):
	#busqueda
	if len(lista_ids) == 0:
		return 

	escritorList = []
	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsUser(escritorList)

	ids_no_recopilados = []
	#bucle de usuarios
	for identificador in lista_ids:
		print identificador
		try:
			recolector.recolecta(identificador=identificador)
		except Exception, e:
			print e
			ids_no_recopilados.append(identificador)
			sleep(5*60)

	recopila(ids_no_recopilados)

if __name__ == '__main__':
	consultas = ConsultasCassandra()
	user_id = consultas.getUserIDByScreenNameCassandra("p_molins")

	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)

	recopila(identificadores)



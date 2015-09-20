# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra
from Neo4j.ConexionNeo4j import ConexionNeo4j
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
	user_id = 2383366169 #p_molins en otros test hacerlo con la cadena
	grafo = ConexionNeo4j().getGraph()

	queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user {id_twitter : "+ str(user_id) +"}) return a"
	nodos = grafo.cypher.execute(queryNeo4j)
	identificadores = []
	for nodo in nodos:
		identificadores.append(long(nodo[0].properties["id_twitter"]))

	

	recopila(identificadores)



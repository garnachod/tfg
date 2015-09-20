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


if __name__ == '__main__':
	user_id = 2383366169 #p_molins en otros test hacerlo con la cadena
	grafo = ConexionNeo4j().getGraph()

	queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user {id_twitter : "+ str(user_id) +"}) return a"
	nodos = grafo.cypher.execute(queryNeo4j)
	identificadores = []
	for nodo in nodos:
		identificadores.append(long(nodo[0].properties["id_twitter"]))


	#TODO recogida de cassandra
	#TODO aggregación
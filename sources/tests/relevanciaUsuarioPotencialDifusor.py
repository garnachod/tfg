# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from Neo4j.ConexionNeo4j import ConexionNeo4j
import datetime

def getRTMByScreenName(consultas, screen_name):
	#todos los tweets de un usuario
	tweets = consultas.getTweetsUsuario(screen_name, limit=10000)
	countRTs = 0.0

	for tweet in tweets:
		if tweet.orig_tweet != 0:
			countRTs += 1

	c = tweets[0].created_at - tweets[len(tweets)-1].created_at
	if countRTs != 0.0:
		return countRTs/c.days
	else:
		return 0.0

if __name__ == '__main__':
	user_id = 2383366169 #p_molins en otros test hacerlo con la cadena
	grafo = ConexionNeo4j().getGraph()
	#TODO función en consultas
	queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user {id_twitter : "+ str(user_id) +"}) return a"
	nodos = grafo.cypher.execute(queryNeo4j)
	identificadores = []
	for nodo in nodos:
		identificadores.append(long(nodo[0].properties["id_twitter"]))

	consultas = ConsultasWeb()
	relevancia = 0.0
	for identificador in identificadores:
		screen_name = consultas.getScreenNameByUserID(identificador)
		if screen_name is None:
			continue

		user = consultas.getUserByIDLargeCassandra(identificador)
		
		rtm = getRTMByScreenName(consultas, screen_name)
		if rtm != 0.0:
			#sumatorio de relevancia 
			relevancia += (rtm) * user.followers

	screen_name = consultas.getScreenNameByUserID(user_id)
	user = consultas.getUserByIDLargeCassandra(user_id)
	rtm = getRTMByScreenName(consultas, screen_name)
	#ultimos 2 terminos
	print (relevancia + user.followers) * rtm
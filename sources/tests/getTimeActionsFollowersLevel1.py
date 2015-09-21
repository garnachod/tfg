# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from Neo4j.ConexionNeo4j import ConexionNeo4j
import datetime
from time import time, sleep
import math


if __name__ == '__main__':
	user_id = 2383366169 #p_molins en otros test hacerlo con la cadena
	grafo = ConexionNeo4j().getGraph()

	queryNeo4j = "MATCH (a)-[r:FOLLOW]->(u:user {id_twitter : "+ str(user_id) +"}) return a"
	nodos = grafo.cypher.execute(queryNeo4j)
	identificadores = []
	for nodo in nodos:
		identificadores.append(long(nodo[0].properties["id_twitter"]))


	consultas = ConsultasWeb()
	fOut = open("salida.csv", "w")
	#recogida de cassandra
	for identificador in identificadores:
		screen_name = consultas.getScreenNameByUserID(identificador)
		if screen_name is None:
			continue

		#todos los tweets de un usuario
		tweets = consultas.getTweetsUsuario(screen_name, limit=10000)
		#aggregación
		#############

		#inicializamos a 0
		horas = []
		nFragmentosPorHora = 4
		nFragmentosSemanales = 7 * 24 * nFragmentosPorHora
		for i in range(nFragmentosSemanales):
			horas.append(0.0)

		for tweet in tweets:
			index = (tweet.created_at.weekday() + 1) * (tweet.created_at.hour + 1) * (math.ceil(tweet.created_at.minute / (60/nFragmentosPorHora)) + 1)
			horas[int(index)-1] += 1
			#print tweet.created_at.weekday()
			#print tweet.created_at.hour
			#print tweet.created_at.minute
			#print math.ceil(tweet.created_at.minute / (60/nFragmentosPorHora))

		for i in range(nFragmentosSemanales):
			if horas[i] != 0.0:
				horas[i] = horas[i] / len(tweets)

			fOut.write(str(horas[i]) + ";")
		fOut.write("\n")
			

		



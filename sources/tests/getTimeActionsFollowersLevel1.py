# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
import datetime
from time import time, sleep
import math


if __name__ == '__main__':
	consultas = ConsultasWeb()
	user_id = consultas.getUserIDByScreenName("p_molins")
	
	consultasGrafo = ConsultasNeo4j()
	
	identificadores = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)
	
	
	fOut_tweets = open("salida_tweets.csv", "w")
	fOut_rts = open("salida_rts.csv", "w")
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
		horas_tweet = []
		count_tweets = 0
		horas_rts = []
		count_rts = 0
		nFragmentosPorHora = 4
		nFragmentosSemanales = 7 * 24 * nFragmentosPorHora
		for i in range(nFragmentosSemanales):
			horas_tweet.append(0)
			horas_rts.append(0)

		for tweet in tweets:
			index = (tweet.created_at.weekday() + 1) * (tweet.created_at.hour + 1) * (math.ceil(tweet.created_at.minute / (60/nFragmentosPorHora)) + 1)
			if tweet.orig_tweet == 0:
				horas_tweet[int(index)-1] += 1
				count_tweets += 1
			else:
				horas_rts[int(index)-1] += 1
				count_rts += 1


		fOut_tweets.write(screen_name + ";")
		fOut_rts.write(screen_name + ";")
		fOut_tweets.write(str(count_tweets) + ";")
		fOut_rts.write(str(count_rts) + ";")

		for i in range(nFragmentosSemanales):
			fOut_tweets.write(str(horas_tweet[i]) + ";")
			fOut_rts.write(str(horas_rts[i]) + ";")

		fOut_tweets.write("\n")
		fOut_rts.write("\n")
			

		



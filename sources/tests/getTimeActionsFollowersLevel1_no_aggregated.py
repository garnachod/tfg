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
		count_tweets = 0
		count_rts = 0

		for tweet in tweets:
			if tweet.orig_tweet == 0:
				count_tweets += 1
			else:
				count_rts += 1


		fOut_tweets.write(screen_name + ";")
		fOut_rts.write(screen_name + ";")
		fOut_tweets.write(str(count_tweets) + ";")
		fOut_rts.write(str(count_rts) + ";")

		for tweet in tweets:
			if tweet.orig_tweet == 0:
				fOut_tweets.write(str(tweet.created_at) + ";")
			else:
				fOut_rts.write(str(tweet.created_at) + ";")

		fOut_tweets.write("\n")
		fOut_rts.write("\n")
			

		



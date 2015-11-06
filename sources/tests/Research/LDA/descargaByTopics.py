# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra
import datetime
from time import time, sleep

if __name__ == '__main__':
	escritorList = []
	topics = ["shaver","braun","shave"]


	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsTags(escritorList)
	tiempo_inicio = time()

	for i in range(100):
		for topic in topics:
			print topic
			recolector.recolecta(topic)
			sleep(16*60)

	tiempo_fin = time()
	print "tiempo recoleccion y escritura"
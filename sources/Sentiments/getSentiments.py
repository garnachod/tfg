# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandraSpark import ConsultasCassandraSpark
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
import codecs
import time
import random


def guarda():
	lista_descarga = [':-)', ':)',':-(', ':(']
	random.shuffle(lista_descarga)
	escritorList = []
	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsTags(escritorList)
	tiempo_rec = time.time()
	for texto in lista_descarga:
		recolector.recolecta(texto)

	print "Tiempo recolección:"
	print time.time() - tiempo_rec


if __name__ == '__main__':
	
	for i in range(120):
		print i
		guarda()
		print "Esperando para la siguente ejecucion 5 minutos:"
		time.sleep(60*5)

	#buscaDB()
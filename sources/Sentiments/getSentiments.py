# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandraSpark import ConsultasCassandraSpark
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsTags import RecolectorTweetsTags
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra
import codecs
import time
import random


def guardaYBusca():
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

	cs = ConsultasCassandraSpark()
	fOut_pos = codecs.open("tweets_pos.txt", "w", "utf-8")
	fOut_neg = codecs.open("tweets_neg.txt", "w", "utf-8")

	for tweet in cs.getTweetContainsTextCS(':-)'):
		tweet = tweet.replace("\n", ".")
		fOut_pos.write(tweet)
		fOut_pos.write("\n")

	for tweet in cs.getTweetContainsTextCS(':)'):
		tweet = tweet.replace("\n", ".")
		fOut_pos.write(tweet)
		fOut_pos.write("\n")

	for tweet in cs.getTweetContainsTextCS(';)'):
		tweet = tweet.replace("\n", ".")
		fOut_pos.write(tweet)
		fOut_pos.write("\n")

	for tweet in cs.getTweetContainsTextCS(':-('):
		tweet = tweet.replace("\n", ".")
		fOut_neg.write(tweet)
		fOut_neg.write("\n")

	for tweet in cs.getTweetContainsTextCS(':('):
		tweet = tweet.replace("\n", ".")
		fOut_neg.write(tweet)
		fOut_neg.write("\n")

	for tweet in cs.getTweetContainsTextCS(';('):
		tweet = tweet.replace("\n", ".")
		fOut_neg.write(tweet)
		fOut_neg.write("\n")

	fOut_pos.close()
	fOut_neg.close()

if __name__ == '__main__':
	
	for i in range(20):
		print i
		guardaYBusca()
		print "Esperando para la siguente ejecucion 5 minutos:"
		time.sleep(60*5)
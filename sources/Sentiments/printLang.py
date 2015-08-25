# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandraSpark import ConsultasCassandraSpark
import codecs

def buscaDB():
	cs = ConsultasCassandraSpark()
	fOut = codecs.open("tweets_es.txt", "w", "utf-8")

	for tweet in cs.getAllTweetsNoRtStatusFiltrLangCS('es'):
		tweet = tweet.replace("\n", ".")
		fOut.write(tweet)
		fOut.write("\n")

	fOut.close()

if __name__ == '__main__':
	buscaDB()
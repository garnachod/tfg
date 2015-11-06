# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandraSpark import ConsultasCassandraSpark
import codecs

def buscaDB():
	cs = ConsultasCassandraSpark()
	fOut_pos = codecs.open("tweets_pos.txt", "w", "utf-8")
	fOut_neg = codecs.open("tweets_neg.txt", "w", "utf-8")

	for tweet in cs.getTweetContainsTextAndLangCS(':-)', 'es'):
		tweet = tweet.replace("\n", ".")
		fOut_pos.write(tweet)
		fOut_pos.write("\n")

	for tweet in cs.getTweetContainsTextAndLangCS(':)', 'es'):
		tweet = tweet.replace("\n", ".")
		fOut_pos.write(tweet)
		fOut_pos.write("\n")

	for tweet in cs.getTweetContainsTextAndLangCS(';)', 'es'):
		tweet = tweet.replace("\n", ".")
		fOut_pos.write(tweet)
		fOut_pos.write("\n")

	for tweet in cs.getTweetContainsTextAndLangCS(':-(', 'es'):
		tweet = tweet.replace("\n", ".")
		fOut_neg.write(tweet)
		fOut_neg.write("\n")

	for tweet in cs.getTweetContainsTextAndLangCS(':(', 'es'):
		tweet = tweet.replace("\n", ".")
		fOut_neg.write(tweet)
		fOut_neg.write("\n")

	for tweet in cs.getTweetContainsTextAndLangCS(';(', 'es'):
		tweet = tweet.replace("\n", ".")
		fOut_neg.write(tweet)
		fOut_neg.write("\n")

	fOut_pos.close()
	fOut_neg.close()

if __name__ == '__main__':
	buscaDB()
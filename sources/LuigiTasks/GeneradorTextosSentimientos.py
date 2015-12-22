# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from blist import blist

from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasCassandraSpark import ConsultasCassandraSpark
from ProcesadoresTexto.LimpiadorTweets import LimpiadorTweets

from time import time

class SentimientosPorIdioma(luigi.Task):
	lang = luigi.Parameter(default="es")

	"""
		Uso:
			PYTHONPATH='' luigi --module GeneradorTextosSentimientos SentimientosPorIdioma (--lang ...)
	"""

	def output(self):
		return luigi.LocalTarget(path='sentimientos/SentimientosPorIdioma(%s)'%self.lang, format=luigi.format.TextFormat(encoding='utf8'))

	def run(self):
		i = 0
		positivos = blist([])
		negativos = blist([])
		otros = blist([])
		cs = ConsultasCassandra()
		tiempo_ini = time()
		tws = cs.getTweetsTextAndLang(self.lang, limit=5000000)
		for tw in tws:
			if ":)" in tw.status or ":-)" in tw.status:
				positivos.append(tw)
			elif ":(" in tw.status or ":-(" in tw.status:
				negativos.append(tw)
			else:
				otros.append(tw)
		print tiempo_ini - time()

		with self.output().open("w") as out_file:
			for i, tw in enumerate(positivos):
				out_file.write(u"ps_"+str(i)+u"\n")
				tweetLimpio = LimpiadorTweets.clean(tw.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tw.lang)
				tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tw.lang)
				out_file.write(tweetStemmed)
				out_file.write(u"\n")

			for i, tw in enumerate(negativos):
				out_file.write(u"ng_"+str(i)+u"\n")
				tweetLimpio = LimpiadorTweets.clean(tw.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tw.lang)
				tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tw.lang)
				out_file.write(tweetStemmed)
				out_file.write(u"\n")

			for i, tw in enumerate(otros):
				out_file.write(u"ns_"+str(i)+u"\n")
				tweetLimpio = LimpiadorTweets.clean(tw.status)
				tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, tw.lang)
				tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, tw.lang)
				out_file.write(tweetStemmed)
				out_file.write(u"\n")
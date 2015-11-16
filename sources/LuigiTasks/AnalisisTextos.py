# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from GeneradorDocumentosTwitter import *
import gensim
from blist import blist
import codecs
import numpy



class LDAIdiomaGenerico(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos LDAIdiomaGenerico
	"""
	idioma = luigi.Parameter(default="es")

	def output(self):
		return luigi.LocalTarget(path='textos/LDAIdiomaGenerico(%s)'%self.idioma)

	def requires(self):
		return GeneradorTextoCorpusIdioma(self.idioma)

	def run(self):
		usuarios = blist([])

		with self.input().open('r') as in_file:
			for line in in_file:
				usuarios.append(line.split())


		print len(usuarios)

		dictionary = gensim.corpora.Dictionary([doc for doc in usuarios])
		dictionary.compactify()
		dictionary.save("textos/dictionary.dict")

		corpus = [dictionary.doc2bow(doc) for doc in usuarios]
		gensim.corpora.MmCorpus.serialize('textos/corpus.mm', corpus)

		#corpus = gensim.corpora.MmCorpus('test.mm')
		#dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

		print "entrenando"
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, chunksize=200000, passes=10)

		lda.save('textos/model.lda')


		with self.output().open('w') as out_file:
			out_file.write("OK")
		


class LDATwitterUser(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos LDATwitterUser --usuario ...
	"""
	usuario = luigi.Parameter()
	idioma = luigi.Parameter(default="es")

	def output(self):
		return luigi.LocalTarget(path='textos/LDATwitterUser(%s)'%self.usuario)

	def requires(self):
		return GeneradorTextoUsuario(self.usuario)

	def run(self):
		tweets = blist([])

		with self.input().open('r') as in_file:
			for line in in_file:
				palabras = line.replace("\n", "").split()
				if len(palabras) > 2:
					tweets.append(palabras)


		print len(tweets)

		dictionary = gensim.corpora.Dictionary([doc for doc in tweets])
		dictionary.compactify()
		dictionary.save("textos/dictionary_%s.dict"%self.usuario)

		corpus = [dictionary.doc2bow(doc) for doc in tweets]
		gensim.corpora.MmCorpus.serialize('textos/corpus_%s.mm'%self.usuario, corpus)

		#corpus = gensim.corpora.MmCorpus('test.mm')
		#dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

		print "entrenando"
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=7, chunksize=200000, passes=200)

		lda.save('textos/model_%s.lda'%self.usuario)


		with self.output().open('w') as out_file:
			out_file.write("OK")

class CreaMatrizCorreccionTwitterUser(luigi.Task):
	"""docstring for CreaMatrizCorreccion"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos CreaMatrizCorreccionTwitterUser --usuario ...
	"""
	"""
		TODO: generalizar
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/CreaMatrizCorreccionTwitterUser(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return [LDATwitterUser(self.usuario), LDAIdiomaGenerico()]

	def run(self):
		nTopics = 100
		lda = gensim.models.LdaModel.load('textos/model_p_molins.lda')
		
		topic = lda.show_topic(0, topn=len(lda.state.sstats[0]))

		corpus = gensim.corpora.MmCorpus('textos/corpus.mm')
		dictionary = gensim.corpora.Dictionary.load("textos/dictionary.dict")
		lda = gensim.models.LdaModel.load('textos/model.lda')

		vectorTopic = [0.0 for i in range(0, nTopics)]
		acumulado = 0.0
		for tupla in topic:
			vectorPalabra = []
			idPalabra = False
			try:
				idPalabra = dictionary.doc2bow([tupla[1]])[0][0]
			except Exception, e:
				pass

			if idPalabra == False:
				continue

			pesoPalabra = tupla[0]

			acumulado += pesoPalabra

			for indice in range(0, nTopics):
				vectorPalabra.append(lda.state.sstats[indice][idPalabra]*pesoPalabra)

			for i, elemento in enumerate(vectorPalabra):
				vectorTopic[i] += elemento

			if acumulado >= 0.9:
				break

		matrizIdentidad = numpy.zeros((nTopics, nTopics))
		for i in range(0, nTopics):
			matrizIdentidad[i][i] = 1.0

		#anadimos la primera columna
		for i in range(0, nTopics):
			matrizIdentidad[i][0] = vectorTopic[i]

		matrizIdentidadInv = numpy.linalg.inv(matrizIdentidad)

		MatrizCorrecionFinal = numpy.dot(matrizIdentidadInv, lda.state.sstats)


		with self.output().open('w') as out_file:
			for i in xrange(0, len(MatrizCorrecionFinal[0])):
				out_file.write(dictionary[i] + "," + str(MatrizCorrecionFinal[0][i]))
				out_file.write(u"\n")







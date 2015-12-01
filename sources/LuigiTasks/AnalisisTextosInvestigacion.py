# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from GeneradorDocumentosTwitter import *
import gensim
# gensim modules
from gensim import utils, matutils
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

from AnalisisTextos import *

from blist import blist
import codecs
import numpy
import time
import random
import json
import nltk

import pyLDAvis.gensim
import pyLDAvis



class Word2VecIdiomaGenerico(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion Word2VecIdiomaGenerico
	"""
	idioma = luigi.Parameter(default="es")

	def output(self):
		return luigi.LocalTarget(path='textos/Word2VecIdiomaGenerico(%s)'%self.idioma)

	def requires(self):
		return GeneradorTextoCorpusIdioma(self.idioma)

	def run(self):
		usuarios = blist([])

		with self.input().open('r') as in_file:
			for line in in_file:
				usuarios.append(line.replace("\n", "").split())


		print len(usuarios)

		sentences = usuarios
		print "entrenando"
		model = gensim.models.Word2Vec(sentences, min_count=3, workers=6, iter=20)
		model.save('textos/model.w2v')
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, chunksize=200000, passes=10)

		


		with self.output().open('w') as out_file:
			out_file.write("OK")

class LabeledLineSentence(object):
	def __init__(self, source):
		self.source = source
		self.sentences = None
		
	def to_array(self):
		if self.sentences is None:
			self.sentences = blist()
			with utils.smart_open(self.source) as fIn:
				last_identif = 0
				for item_no, line in enumerate(fIn):
					line = line.replace("\n", "")
					if item_no % 2 == 0:
						last_identif = long(line)
					else:
						palabras = utils.to_unicode(line).split()
						palabras_clean = []
						for palabra in palabras:
							if len(palabra)> 1:
								palabras_clean.append(palabra)
						self.sentences.append(TaggedDocument(palabras_clean, [str(last_identif)]))
					
		return self.sentences
		

	def sentences_perm(self):
		random.shuffle(self.sentences)
		return self.sentences

class Doc2VecSeguidoresYUsuario(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion Doc2VecSeguidoresYUsuario --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/Doc2VecSeguidoresYUsuario(%s)'%self.usuario)

	def requires(self):
		return GeneradorTextoSeguidoresDoc2Vec(self.usuario)


	def run(self):
		dimension = 50
		sentences = LabeledLineSentence(self.input().path)

		total_start = time.time()

		dbow = True
		if dbow:
			model = Doc2Vec(min_count=1, window=7, size=dimension, sample=1e-3, negative=5, dm=0 ,workers=6, alpha=0.04)
			
			print "inicio vocab"
			model.build_vocab(sentences.to_array())
			print "fin vocab"
			first_alpha = model.alpha
			last_alpha = 0.01
			next_alpha = first_alpha
			epochs = 30
			for epoch in range(epochs):
				start = time.time()
				print "iniciando epoca DBOW:"
				print model.alpha
				model.train(sentences.sentences_perm())
				end = time.time()
				next_alpha = (((first_alpha - last_alpha) / float(epochs)) * float(epochs - (epoch+1)) + last_alpha)
				model.alpha = next_alpha
				print "tiempo de la epoca " + str(epoch) +": " + str(end - start)

			model.save('./textos/model_' + self.usuario + '.d2v')
			#model.save_word2vec_format('./textos/tweet_dbow'



		total_end = time.time()

		print "tiempo total:" + str((total_end - total_start)/60.0)
		with self.output().open('w') as out_file:
			out_file.write("OK")


class SimilitudUnTopicLDA2Doc2Vec(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion SimilitudUnTopicLDA2Doc2Vec --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/SimilitudUnTopicLDA2Doc2Vec(%s)'%self.usuario)

	def requires(self):
		return [Doc2VecSeguidoresYUsuario(self.usuario), LDATwitterUser(self.usuario)]

	def run(self):
		lda = gensim.models.LdaModel.load('textos/model_' + self.usuario + '.lda')
		w2v = gensim.models.Doc2Vec.load('./textos/model_' + self.usuario + '.d2v')

		#print w2v["pp"]

		topic = lda.show_topic(0, topn=len(lda.state.sstats[0]))
		#print topic
		lda = None
		nTopics = 50

		vectorTopic = [0.0 for i in range(0, nTopics)]
		acumulado = 0.0
		for tupla in topic:
			vectorPalabra = []

			palabra = tupla[0]
			pesoPalabra = tupla[1]

			acumulado += pesoPalabra
			vector = None
			try:
				vector = w2v[palabra]
			except Exception, e:
				vector = None

			if vector is None:
				continue
			
			for indice in range(0, nTopics):
				vectorPalabra.append(vector[indice]*pesoPalabra)

			for i, elemento in enumerate(vectorPalabra):
				vectorTopic[i] += elemento

			if acumulado >= 0.9:
				break

		vectorTopic = numpy.array(vectorTopic)
		print vectorTopic

		similitudes = []
		for doctag in w2v.docvecs.doctags:
			similitud = numpy.dot(w2v.docvecs[doctag],vectorTopic)/numpy.linalg.norm(w2v.docvecs[doctag])/numpy.linalg.norm(vectorTopic)
			similitudes.append((doctag, (similitud + 1.0)*5.0))

		similitudes = sorted(similitudes, key=lambda similitud: similitud[1], reverse=True)

		with self.output().open('w') as out_file:
			for usuario_id, peso in similitudes:
				out_file.write(usuario_id + ","+ str(peso)+ "\n")


class SimilitudSeguidoresTodosTopicsLDA2Doc2Vec(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion SimilitudSeguidoresTodosTopicsLDA2Doc2Vec --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/SimilitudSeguidoresTodosTopicsLDA2Doc2Vec(%s)'%self.usuario)

	def requires(self):
		return [Doc2VecSeguidoresYUsuario(self.usuario), LDATwitterUser(self.usuario)]

	def run(self):
		lda = gensim.models.LdaModel.load('textos/model_' + self.usuario + '.lda')
		w2v = gensim.models.Doc2Vec.load('./textos/model_' + self.usuario + '.d2v')

		#print w2v["pp"]
		nTopicsInicio = 7
		sumaTotalBetas = 0.3

		similitudesPorUsuario = {}

		for doctag in w2v.docvecs.doctags:
			similitudesPorUsuario[doctag] = []

		for idTopic in range(nTopicsInicio):
			topic = lda.show_topic(idTopic, topn=len(lda.state.sstats[0]))
			#print len(topic)
			nTopics = 50

			vectorTopic = [0.0 for i in range(0, nTopics)]
			acumulado = 0.0
			nPalabrasAcumuladas = 0
			for tupla in topic:
				vectorPalabra = []

				palabra = tupla[0]
				pesoPalabra = tupla[1]

				acumulado += pesoPalabra
				nPalabrasAcumuladas += 1
				vector = None
				try:
					vector = w2v[palabra]
				except Exception, e:
					vector = None

				if vector is None:
					continue
				
				for indice in range(0, nTopics):
					vectorPalabra.append(vector[indice]*pesoPalabra)

				for i, elemento in enumerate(vectorPalabra):
					vectorTopic[i] += elemento

				if acumulado >= sumaTotalBetas:
					#print nPalabrasAcumuladas
					break

			vectorTopic = numpy.array(vectorTopic)

			#print vectorTopic

			
			for doctag in w2v.docvecs.doctags:
				similitud = numpy.dot(w2v.docvecs[doctag],vectorTopic)/numpy.linalg.norm(w2v.docvecs[doctag])/numpy.linalg.norm(vectorTopic)
				similitudesPorUsuario[doctag].append((similitud + 1.0)*5.0)

		#exit()
		with self.output().open('w') as out_file:
			for usuario_id in similitudesPorUsuario:
				out_file.write(usuario_id)
				for peso in similitudesPorUsuario[usuario_id]:
					out_file.write(","+ str(peso))
				out_file.write("\n")

class SimilitudSeguidoresTodosTopicsLDASinLem2Doc2Vec(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion SimilitudSeguidoresTodosTopicsLDASinLem2Doc2Vec --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/SimilitudSeguidoresTodosTopicsLDASinLem2Doc2Vec(%s)'%self.usuario)

	def requires(self):
		return [Doc2VecSeguidoresYUsuario(self.usuario), LDATwitterUserSinLem(self.usuario)]

	def run(self):
		lda = gensim.models.LdaModel.load('textos/model_nolem_' + self.usuario + '.lda')
		w2v = gensim.models.Doc2Vec.load('./textos/model_' + self.usuario + '.d2v')

		#print w2v["pp"]
		nTopicsInicio = 7
		sumaTotalBetas = 0.3
		stemmer = nltk.stem.snowball.SnowballStemmer("spanish")

		similitudesPorUsuario = {}

		for doctag in w2v.docvecs.doctags:
			similitudesPorUsuario[doctag] = []

		for idTopic in range(nTopicsInicio):
			topic = lda.show_topic(idTopic, topn=len(lda.state.sstats[0]))
			#print len(topic)
			nTopics = 50

			vectorTopic = [0.0 for i in range(0, nTopics)]
			acumulado = 0.0
			nPalabrasAcumuladas = 0
			for tupla in topic:
				vectorPalabra = []

				palabra = tupla[0]
				palabra = stemmer.stem(palabra)
				pesoPalabra = tupla[1]

				acumulado += pesoPalabra
				nPalabrasAcumuladas += 1
				vector = None
				try:
					vector = w2v[palabra]
				except Exception, e:
					vector = None

				if vector is None:
					continue
				
				for indice in range(0, nTopics):
					vectorPalabra.append(vector[indice]*pesoPalabra)

				for i, elemento in enumerate(vectorPalabra):
					vectorTopic[i] += elemento

				if acumulado >= sumaTotalBetas:
					print nPalabrasAcumuladas
					break

			vectorTopic = numpy.array(vectorTopic)

			#print vectorTopic

			
			for doctag in w2v.docvecs.doctags:
				similitud = numpy.dot(w2v.docvecs[doctag],vectorTopic)/numpy.linalg.norm(w2v.docvecs[doctag])/numpy.linalg.norm(vectorTopic)
				similitudesPorUsuario[doctag].append((similitud + 1.0)*5.0)

		#exit()
		with self.output().open('w') as out_file:
			for usuario_id in similitudesPorUsuario:
				out_file.write(usuario_id)
				for peso in similitudesPorUsuario[usuario_id]:
					out_file.write(","+ str(peso))
				out_file.write("\n")



#prueba de inferir vectores de topics desde unas palabras.
#model.infer_vector(words, steps=self.steps, alpha=self.alpha)
class SimilitudSeguidoresTodosTopicsLDASinLem2Doc2VecInfiere(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion SimilitudSeguidoresTodosTopicsLDASinLem2Doc2VecInfiere --usuario ...
	"""

	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/SimilitudSeguidoresTodosTopicsLDASinLem2Doc2VecInfiere(%s)'%self.usuario)

	def requires(self):
		return [Doc2VecSeguidoresYUsuario(self.usuario), LDATwitterUserSinLem(self.usuario)]

	def run(self):
		lda = gensim.models.LdaModel.load('textos/model_nolem_' + self.usuario + '.lda')
		w2v = gensim.models.Doc2Vec.load('./textos/model_' + self.usuario + '.d2v')

		#print w2v["pp"]
		nTopicsInicio = 7
		sumaTotalBetas = 0.3
		stemmer = nltk.stem.snowball.SnowballStemmer("spanish")

		similitudesPorUsuario = {}

		for doctag in w2v.docvecs.doctags:
			similitudesPorUsuario[doctag] = []

		for idTopic in range(nTopicsInicio):
			topic = lda.show_topic(idTopic, topn=len(lda.state.sstats[0]))
			#print len(topic)
			nTopics = 50

			palabras = []
			acumulado = 0.0
			nPalabrasAcumuladas = 0
			for tupla in topic:
				palabra = tupla[0]
				palabra = stemmer.stem(palabra)
				pesoPalabra = tupla[1]

				vector = None
				try:
					vector = w2v[palabra]
				except Exception, e:
					vector = None

				if vector is None:
					continue

				acumulado += pesoPalabra
				nPalabrasAcumuladas += 1
				palabras.append(palabra)

				if acumulado >= sumaTotalBetas:
					print nPalabrasAcumuladas
					break

			print palabras
			vectorTopic = numpy.array(w2v.infer_vector(palabras, steps=3, alpha=0.1))

			#print vectorTopic

			
			for doctag in w2v.docvecs.doctags:
				similitud = numpy.dot(w2v.docvecs[doctag],vectorTopic)/numpy.linalg.norm(w2v.docvecs[doctag])/numpy.linalg.norm(vectorTopic)
				similitudesPorUsuario[doctag].append((similitud + 1.0)*5.0)

		#exit()
		with self.output().open('w') as out_file:
			for usuario_id in similitudesPorUsuario:
				out_file.write(usuario_id)
				for peso in similitudesPorUsuario[usuario_id]:
					out_file.write(","+ str(peso))
				out_file.write("\n")


class SimilitudSeguidoresTodosTopicLDA2Doc2VecJSON(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion SimilitudSeguidoresTodosTopicLDA2Doc2VecJSON --usuario ...
	"""

	usuario = luigi.Parameter()
	lematizar = luigi.Parameter(default="F")

	def output(self):
		return luigi.LocalTarget(path='textos/SimilitudSeguidoresTodosTopicLDA2Doc2VecJSON(%s_%s)'%(self.usuario, self.lematizar))

	def requires(self):
		if self.lematizar == "T":
			return SimilitudSeguidoresTodosTopicsLDA2Doc2Vec(self.usuario)
		else:
			#return SimilitudSeguidoresTodosTopicsLDASinLem2Doc2Vec(self.usuario)
			return SimilitudSeguidoresTodosTopicsLDASinLem2Doc2VecInfiere(self.usuario)
			

	def run(self):
		consultasCassandra = ConsultasCassandra()

		JsonObj = {}

		with self.input().open('r') as in_file:
			for line in in_file:
				elementos = line.replace("\n", "").split(",")
				usuarioId = long(elementos[0])
				pesos = elementos[1:]
				usuario_screenName = consultasCassandra.getScreenNameByUserIDCassandra(usuarioId)
				if usuario_screenName is not None:
					JsonObj[usuario_screenName] = [float(peso) for peso in pesos]
		


		with self.output().open('w') as out_file:
			out_file.write(json.dumps(JsonObj))

class SimilitudSeguidoresTodosTopicLDA2Doc2VecCSV(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion SimilitudSeguidoresTodosTopicLDA2Doc2VecCSV --usuario ...
	"""

	usuario = luigi.Parameter()
	lematizar = luigi.Parameter(default="F")

	def output(self):
		return luigi.LocalTarget(path='textos/SimilitudSeguidoresTodosTopicLDA2Doc2VecCSV(%s_%s)'%(self.usuario, self.lematizar))

	def requires(self):
		if self.lematizar == "T":
			return SimilitudSeguidoresTodosTopicsLDA2Doc2Vec(self.usuario)
		else:
			return SimilitudSeguidoresTodosTopicsLDASinLem2Doc2VecInfiere(self.usuario)
			#return SimilitudSeguidoresTodosTopicsLDASinLem2Doc2Vec(self.usuario)

	def run(self):
		consultasCassandra = ConsultasCassandra()

		JsonObj = {}

		with self.input().open('r') as in_file:
			for line in in_file:
				elementos = line.replace("\n", "").split(",")
				usuarioId = long(elementos[0])
				pesos = elementos[1:]
				usuario_screenName = consultasCassandra.getScreenNameByUserIDCassandra(usuarioId)
				if usuario_screenName is not None:
					JsonObj[usuario_screenName] = [float(peso) for peso in pesos]
		


		with self.output().open('w') as out_file:
			for usuario in JsonObj:
				out_file.write(usuario)

				for peso in JsonObj[usuario]:
					out_file.write("," + str(peso))

				out_file.write("\n")


class LDAvisJSONUsuario(luigi.Task):
	"""docstring for LDAvisUsuario"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion LDAvisJSONUsuario --usuario ...
	"""
	usuario = luigi.Parameter()
	lematizar = luigi.Parameter(default="F")

	def output(self):
		return luigi.LocalTarget(path='textos/LDAvisUsuario(%s_%s).json'%(self.usuario, self.lematizar))

	def requires(self):
		if self.lematizar == "T":
			return LDATwitterUser(self.usuario)
		else:
			return LDATwitterUserSinLem(self.usuario)

	def run(self):
		corpus = None
		dictionary = None
		lda = None
		if self.lematizar == "T":
			corpus = gensim.corpora.MmCorpus('textos/corpus_' + self.usuario + '.mm')
			dictionary = gensim.corpora.Dictionary.load('textos/dictionary_' + self.usuario + '.dict')
			lda = gensim.models.LdaModel.load('textos/model_' + self.usuario + '.lda')
		else:
			corpus = gensim.corpora.MmCorpus('textos/corpus_nolem_' + self.usuario + '.mm')
			dictionary = gensim.corpora.Dictionary.load('textos/dictionary_nolem_' + self.usuario + '.dict')
			lda = gensim.models.LdaModel.load('textos/model_nolem_' + self.usuario + '.lda')

		#pyLDAvis.enable_notebook()
		vis_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
		#pyLDAvis.display(vis_data)
		pyLDAvis.save_json(vis_data, self.output().path)
		
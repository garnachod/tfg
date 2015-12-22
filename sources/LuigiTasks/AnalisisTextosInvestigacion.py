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
from GeneradorTextosSentimientos import *

from blist import blist
import codecs
import numpy
import time
import random
import json
import nltk

import pyLDAvis.gensim
import pyLDAvis

import sklearn
from sklearn.externals import joblib
from sklearn.ensemble import RandomForestClassifier


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

		with self.output().open('w') as out_file:
			out_file.write("OK")

class LabeledLineSentence(object):
	"""
		ides:
			Number	
			String
	"""
	def __init__(self, source, ides="Number"):
		self.source = source
		self.sentences = None
		self.ides = ides
		
	def to_array(self):
		if self.sentences is None:
			self.sentences = blist()
			with utils.smart_open(self.source) as fIn:
				last_identif = 0
				for item_no, line in enumerate(fIn):
					line = line.replace("\n", "")
					if item_no % 2 == 0:
						if self.ides == "Number":
							last_identif = long(line)
						else:
							last_identif = line
					else:
						palabras = utils.to_unicode(line).split()
						palabras_clean = []
						for palabra in palabras:
							if len(palabra) > 1:
								palabras_clean.append(palabra)
						if len(palabras_clean) > 0:
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

		total_end = time.time()

		print "tiempo total:" + str((total_end - total_start)/60.0)
		with self.output().open('w') as out_file:
			out_file.write("OK")

class Doc2VecDMSeguidoresYUsuario(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion Doc2VecDMSeguidoresYUsuario --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/Doc2VecDMSeguidoresYUsuario(%s)'%self.usuario)

	def requires(self):
		return GeneradorTextoSeguidoresDoc2Vec(self.usuario)

	def run(self):
		dimension = 50
		sentences = LabeledLineSentence(self.input().path)

		total_start = time.time()

		#model = Doc2Vec(min_count=1, window=10, size=dimension, sample=1e-3, negative=5, workers=6, dm_mean=1, alpha=0.04)
		model = Doc2Vec(min_count=1, window=7, size=dimension, sample=1e-3, negative=5, workers=6, alpha=0.04)
		#model = Doc2Vec(min_count=1, window=7, size=dimension, sample=1e-3, negative=5, workers=6, alpha=0.04, dm_concat=1)
		#
		print "inicio vocab"
		model.build_vocab(sentences.to_array())
		print "fin vocab"
		first_alpha = model.alpha
		last_alpha = 0.01
		next_alpha = first_alpha
		epochs = 30
		for epoch in range(epochs):
			start = time.time()
			print "iniciando epoca DM:"
			print model.alpha
			model.train(sentences.sentences_perm())
			end = time.time()
			next_alpha = (((first_alpha - last_alpha) / float(epochs)) * float(epochs - (epoch+1)) + last_alpha)
			model.alpha = next_alpha
			print "tiempo de la epoca " + str(epoch) +": " + str(end - start)

		model.save('./textos/model_DM_' + self.usuario + '.d2v')

		total_end = time.time()

		print "tiempo total:" + str((total_end - total_start)/60.0)
		with self.output().open('w') as out_file:
			out_file.write("OK")

class ComparaModelosDoc2Vec(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion ComparaModelosDoc2Vec --usuario ...
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/ComparaModelosDoc2Vec(%s)'%self.usuario)

	def requires(self):
		return [GeneradorTextoSeguidoresDoc2Vec(self.usuario), Doc2VecDMSeguidoresYUsuario(self.usuario), Doc2VecSeguidoresYUsuario(self.usuario)]

	def run(self):
		sentences = None
		for input in self.input():
			if "Generador" in input.path:
				print "generando sentencias"
				sentences = LabeledLineSentence(input.path)

		if sentences is None:
			exit()

		sentencias_array = sentences.to_array()

		modelos = {"d2v_dbow":'./textos/model_' + self.usuario + '.d2v', "d2v_dm":'./textos/model_DM_' + self.usuario + '.d2v'}
		errores = {}
		
		for modelo in modelos:
			#computa el error cuadratico del coseno de cada uno de los modelos y los imprime
			w2v = gensim.models.Doc2Vec.load(modelos[modelo])
			steps = [1, 2, 3, 4, 5, 6, 8, 10]
			
			for step in steps:
				ecm = 0.0
				for sentencia in sentencias_array:
					palabras = sentencia.words
					vectorInferido = numpy.array(w2v.infer_vector(palabras, steps=step, alpha=0.1))
					vectorReal = w2v.docvecs[sentencia.tags[0]]
					similitud = numpy.dot(vectorReal,vectorInferido)/numpy.linalg.norm(vectorReal)/numpy.linalg.norm(vectorInferido)
					ecm += (1.0 - similitud)**2

			
				ecm = ecm / len(sentencias_array)
				if str(step) not in errores:
					errores[str(step)] = []
			 			
			 	errores[str(step)].append(ecm)

		print "epocas,DM,DBOW"
		for error in errores:
			print error + "," + str(errores[error][0]) + "," + str(errores[error][1])


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
					if usuario_screenName == self.usuario:
						pass
					else:
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
		


class EntrenamientoSentimientos(luigi.Task):
	"""docstring for EntrenamientoSentimientos"""
	"""
		Genera vectores con paragraph vector y lo lleva a un clasificador
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion EntrenamientoSentimientos --lang ...
	"""

	lang = luigi.Parameter(default="es")

	def requires(self):
		return SentimientosPorIdioma(self.lang)

	def output(self):
		return luigi.LocalTarget(path='sentimientos/EntrenamientoSentimientos(%s)'%self.lang)

	def run(self):
		sentences = LabeledLineSentence(self.input().path, ides="String")

		dimension = 20

		total_start = time.time()

		#model = Doc2Vec(min_count=1, window=7, size=dimension, sample=1e-3, negative=5, dm=0 ,workers=6, alpha=0.04)
		model = Doc2Vec(min_count=1, window=7, size=dimension, sample=1e-3, negative=5, workers=6, alpha=0.04)
		
		if os.path.isfile('./sentimientos/model_' + self.lang + '.d2v'):
			pass
		else:
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

			model.save('./sentimientos/model_' + self.lang + '.d2v')

		total_end = time.time()

		print "tiempo total d2v:" + str((total_end - total_start)/60.0)

		model = gensim.models.Doc2Vec.load('./sentimientos/model_' + self.lang + '.d2v')

		

		matr = []
		vec = []
		for sentencia in sentences.to_array():
			if "ns" not in sentencia.tags[0]:
				vectoGenerated = numpy.array(model.infer_vector(sentencia.words, steps=3, alpha=0.1))
				matr.append(vectoGenerated)
				if "ps" in sentencia.tags[0]:
					vec.append(0)
				else:
					vec.append(1)

		
		numpyMatrTrain = numpy.matrix(matr)
		numpyArrayTrain = numpy.array(vec)
		#numpyMatrTrain = numpy.matrix([numpy.array(model.infer_vector(sentencia.words, steps=3, alpha=0.1)) for sentencia in sentences.to_array()])
		#numpyArrayTrain = numpy.array([0 if ""  else '' for sentencia in sentences.to_array()])
		print numpyMatrTrain
		print numpyArrayTrain

		#clasif = sklearn.linear_model.LogisticRegression(tol=1e-6, class_weight='balanced')
		clasif = sklearn.linear_model.LogisticRegression(tol=1e-6)
		#clasif = sklearn.svm.SVC()

		clasif.fit(numpyMatrTrain, numpyArrayTrain)
		print "LogisticRegression"
		print clasif.score(numpyMatrTrain,numpyArrayTrain)

		joblib.dump(clasif, './sentimientos/model_' + self.lang + '.clf')
		"""
		clasif = RandomForestClassifier(n_estimators=31, max_depth=6)
		clasif.fit(numpyMatrTrain, numpyArrayTrain)
		print "RandomForestClassifier"
		print clasif.score(numpyMatrTrain,numpyArrayTrain)
		exit()"""

		with self.output().open('w') as out_file:
			out_file.write("OK")

class ClasificaSentimientosPorContenidoYMenciones(luigi.Task):
	#textos = luigi.Parameter(default="es")
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion ClasificaSentimientosPorContenidoYMenciones --lang ...
			PYTHONPATH='' luigi --module AnalisisTextosInvestigacion ClasificaSentimientosPorContenidoYMenciones --contenidotweet EnCasaDeElisa --menciones "salvadostv;psoe"
	"""

	"""
		"salvadostv;PPopular"
	"""
	lang = luigi.Parameter(default="es")
	contenidotweet = luigi.Parameter()
	menciones = luigi.Parameter()

	def requires(self):
		return [EntrenamientoSentimientos(self.lang), GetActividadPorContenidoTweet(self.contenidotweet)]

	def output(self):
		return luigi.LocalTarget(path='sentimientos/ClasificaSentimientosPorContenidoYMenciones(%s_%s_%s)'%(self.lang,self.contenidotweet,self.menciones))

	def run(self):
		consultasCassandra = ConsultasCassandra()
		clasif = ClasificaSentimientosFiles('./sentimientos/model_' + self.lang + '.d2v',
										    './sentimientos/model_' + self.lang + '.clf', 
										    self.lang)

		diccionarioTweetsYEvaluacion = {}
		for conjuntoMenciones in self.menciones.replace(" ", "").replace("\"", "").lower().split(";"):
			diccionarioTweetsYEvaluacion[conjuntoMenciones.replace(",", "-")] = {"tweets":[],
																				 "evaluacionPositiva":0.5}

		for input in self.input():
			if "GetActividad" in input.path:
				with input.open("r") as in_file:
					jsonTws = json.loads(in_file.read())

					for tweet in jsonTws:
						for grupo in diccionarioTweetsYEvaluacion:
							integrantes = grupo.split("-")
							flag = False
							for integrante in integrantes:
								for mencion in tweet["menciones"]:
									#print integrante + "-" + mencion.lower()
									if integrante in mencion.lower():
										flag = True
							if flag:
								texto = consultasCassandra.getTweetStatusCassandra(tweet["id"])
								diccionarioTweetsYEvaluacion[grupo]["tweets"].append(texto)

		#print diccionarioTweetsYEvaluacion

		for grupo in diccionarioTweetsYEvaluacion:
			clasificado = clasif.clasifica(diccionarioTweetsYEvaluacion[grupo]["tweets"])
			if clasificado[0] != 0 and clasificado[1] != 0:
				porcentajePos = clasificado[0]/float(clasificado[0]+clasificado[1])
				diccionarioTweetsYEvaluacion[grupo]["evaluacionPositiva"] = porcentajePos
		
		retorno = {}
		for grupo in diccionarioTweetsYEvaluacion:
			retorno[grupo] = diccionarioTweetsYEvaluacion[grupo]["evaluacionPositiva"]

		with self.output().open("w") as out_file:
			out_file.write(json.dumps(retorno))


class ClasificaSentimientosFiles(object):
	"""Clasifica los sentimientos de una lista de textos, retorna un array con count[0] contador positivos
		Count[1] contador de negativos"""
	def __init__(self, modeloD2VFile, modeloClasfFile, lang):
		super(ClasificaSentimientosFiles, self).__init__()
		self.clasif = joblib.load(modeloClasfFile)
		self.model = gensim.models.Doc2Vec.load(modeloD2VFile)
		self.lang = lang

	def clasifica(self, arrayTextos):
		#count 0 == Positivo
		count = [0, 0]

		for tw in arrayTextos:
			tweetLimpio = LimpiadorTweets.clean(tw)
			tweetSinStopWords = LimpiadorTweets.stopWordsByLanguagefilter(tweetLimpio, self.lang)
			tweetStemmed = LimpiadorTweets.stemmingByLanguage(tweetSinStopWords, self.lang)

			vectoGenerated = numpy.array(self.model.infer_vector(tweetStemmed.split(), steps=3, alpha=0.1))
			count[self.clasif.predict([vectoGenerated])[0]] += 1

		return count



		
	

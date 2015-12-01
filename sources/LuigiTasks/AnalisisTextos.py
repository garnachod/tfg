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
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=7, chunksize=200000, passes=500, alpha='auto')

		lda.save('textos/model_%s.lda'%self.usuario)


		with self.output().open('w') as out_file:
			out_file.write("OK")

class LDATwitterUserSinLem(luigi.Task):
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos LDATwitterUserSinLem --usuario ...
	"""
	usuario = luigi.Parameter()
	idioma = luigi.Parameter(default="es")

	def output(self):
		return luigi.LocalTarget(path='textos/LDATwitterUserSinLem(%s)'%self.usuario)

	def requires(self):
		return GeneradorTextoUsuarioSinLem(self.usuario)

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
		dictionary.save("textos/dictionary_nolem_%s.dict"%self.usuario)

		corpus = [dictionary.doc2bow(doc) for doc in tweets]
		gensim.corpora.MmCorpus.serialize('textos/corpus_nolem_%s.mm'%self.usuario, corpus)

		#corpus = gensim.corpora.MmCorpus('test.mm')
		#dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

		print "entrenando"
		#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
		lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=7, chunksize=200000, passes=500, alpha='auto')

		lda.save('textos/model_nolem_%s.lda'%self.usuario)


		with self.output().open('w') as out_file:
			out_file.write("OK")

class CreaMatrizCorreccionTwitterUserPrimerTopic(luigi.Task):
	"""docstring for CreaMatrizCorreccion"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos CreaMatrizCorreccionTwitterUserPrimerTopic --usuario ...
	"""
	"""
		TODO: generalizar
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/CreaMatrizCorreccionTwitterUserPrimerTopic(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

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

		"""autovalores = numpy.linalg.eigvals(matrizIdentidad)
		mayorAutovalor = autovalores[0]
		menorAutovalor = autovalores[0]
		for autovalor in autovalores:
			print autovalor
			if mayorAutovalor < autovalor:
				mayorAutovalor = autovalor

			if menorAutovalor > autovalor:
				menorAutovalor = autovalor

		print "K es:"
		print mayorAutovalor/menorAutovalor"""

		matrizIdentidadInv = numpy.linalg.inv(matrizIdentidad)

		MatrizCorrecionFinal = numpy.dot(matrizIdentidadInv, lda.state.sstats)


		with self.output().open('w') as out_file:
			for i in xrange(0, len(MatrizCorrecionFinal[0])):
				out_file.write(dictionary[i] + "," + str(MatrizCorrecionFinal[0][i]))
				out_file.write(u"\n")

def Gram_Schmidt1(vecs, row_wise_storage=True):
	"""
	Apply the Gram-Schmidt orthogonalization algorithm to a set
	of vectors. vecs is a two-dimensional array where the vectors
	are stored row-wise, or vecs may be a list of vectors, where
	each vector can be a list or a one-dimensional array.
	An array basis is returned, where basis[i,:] (row_wise_storage
	is True) or basis[:,i] (row_wise_storage is False) is the i-th
	orthonormal vector in the basis.
	This function does not handle null vectors, see Gram_Schmidt
	for a (slower) function that does.
	"""
	from numpy.linalg import inv
	from math import sqrt

	vecs = numpy.asarray(vecs)  # transform to array if list of vectors
	m, n = vecs.shape
	basis = numpy.array(numpy.transpose(vecs))
	eye = numpy.identity(n).astype(float)

	basis[:,0] /= sqrt(numpy.dot(basis[:,0], basis[:,0]))
	for i in range(1, m):
		v = basis[:,i]/sqrt(numpy.dot(basis[:,i], basis[:,i]))
		U = basis[:,:i]
		P = eye - numpy.dot(U, numpy.dot(inv(numpy.dot(numpy.transpose(U), U)), numpy.transpose(U)))
		basis[:, i] = numpy.dot(P, v)
		basis[:, i] /= sqrt(numpy.dot(basis[:, i], basis[:, i]))

	return numpy.transpose(basis) if row_wise_storage else basis

def Gram_Schmidt(vecs, row_wise_storage=True, tol=1E-10,
				 normalize=False, remove_null_vectors=False,
				 remove_noise=False):
	"""
	Apply the Gram-Schmidt orthogonalization algorithm to a set
	of vectors. vecs is a two-dimensional array where the vectors
	are stored row-wise, or vecs may be a list of vectors, where
	each vector can be a list or a one-dimensional array.
	The argument tol is a tolerance for null vectors (the absolute
	value of all elements must be less than tol to have a null
	vector).
	If normalize is True, the orthogonal vectors are normalized to form
	an orthonormal basis.
	If remove_null_vectors is True, all null vectors are removed from
	the resulting basis.
	If remove_noise is True, all elements whose absolute values are
	less than tol are set to zero.
	An array basis is returned, where basis[i,:] (row_wise_storage
	is True) or basis[:,i] (row_wise_storage is False) is the i-th
	orthogonal vector in the basis.
	This function handles null vectors, see Gram_Schmidt1
	for a (faster) function that does not.
	"""
	# The algorithm below views vecs as a matrix A with the vectors
	# stored as columns:
	vecs = numpy.asarray(vecs)  # transform to array if list of vectors
	if row_wise_storage:
		A = numpy.transpose(vecs).copy()
	else:
		A = vecs.copy()

	m, n = A.shape
	V = numpy.zeros((m,n))

	for j in xrange(n):
		v0 = A[:,j]
		v = v0.copy()
		for i in xrange(j):
			vi = V[:,i]

			if (abs(vi) > tol).any():
				v -= (numpy.vdot(v0,vi)/numpy.vdot(vi,vi))*vi
		V[:,j] = v

	if remove_null_vectors:
		indices = [i for i in xrange(n) if (abs(V[:,i]) < tol).all()]
		V = V[ix_(range(m), indices)]

	if normalize:
		for j in xrange(V.shape[1]):
			V[:,j] /= linalg.norm(V[:,j])

	if remove_noise:
		V = cut_noise(V, tol)

	return numpy.transpose(V) if row_wise_storage else V


class CreaMatrizCorreccionTwitterUserTodosTopics(luigi.Task):
	"""docstring for CreaMatrizCorreccion"""
	"""
		Uso:
			PYTHONPATH='' luigi --module AnalisisTextos CreaMatrizCorreccionTwitterUserTodosTopics --usuario ...
	"""
	"""
		TODO: generalizar
	"""
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='textos/CreaMatrizCorreccionTwitterUserTodosTopics(%s)'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return [LDATwitterUser(self.usuario), LDAIdiomaGenerico()]

	def run(self):
		nTopics = 100
		lda = gensim.models.LdaModel.load('textos/model_p_molins.lda')
		
		topics = []
		for i in range(7):
			topic = lda.show_topic(i, topn=len(lda.state.sstats[0]))
			topics.append(topic)


		corpus = gensim.corpora.MmCorpus('textos/corpus.mm')
		dictionary = gensim.corpora.Dictionary.load("textos/dictionary.dict")
		lda = gensim.models.LdaModel.load('textos/model.lda')

		vectoresTopics = []
		for topic in topics:
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

			vectoresTopics.append(vectorTopic)

		#print vectoresTopics
		#vectoresTopicsGS = Gram_Schmidt(vectoresTopics)
		#print vectoresTopicsGS

		matrizIdentidad = numpy.zeros((nTopics, nTopics))
		for i in range(0, nTopics):
			matrizIdentidad[i][i] = 1.0

		#anadimos las N primeras columnas
		for j, vectorTopic in enumerate(vectoresTopics):
			for i in range(0, nTopics):
				matrizIdentidad[i][j] = vectorTopic[i]

		#print matrizIdentidad
		matrizIdentidad = Gram_Schmidt(matrizIdentidad)
		#print matrizIdentidad
		"""
		autovalores = numpy.linalg.eigvals(matrizIdentidad)
		mayorAutovalor = autovalores[0]
		menorAutovalor = autovalores[0]
		for autovalor in autovalores:
			print autovalor
			if mayorAutovalor < autovalor:
				mayorAutovalor = autovalor

			if menorAutovalor > autovalor:
				menorAutovalor = autovalor

		print "K es:"
		print mayorAutovalor/menorAutovalor
		
		exit()"""

		matrizIdentidadInv = numpy.linalg.inv(matrizIdentidad)

		MatrizCorrecionFinal = numpy.dot(matrizIdentidadInv, lda.state.sstats)


		with self.output().open('w') as out_file:
			for i in xrange(0, len(MatrizCorrecionFinal[0])):
				out_file.write(dictionary[i])
				for j in range(7):
					out_file.write(u"," + str(MatrizCorrecionFinal[j][i]))
				out_file.write(u"\n")






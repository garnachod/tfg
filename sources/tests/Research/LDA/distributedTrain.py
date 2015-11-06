import gensim
from blist import blist
import codecs

if __name__ == '__main__':
	#generateDictAndCorpus = True
	#if generateDictAndCorpus == True:
	"""
	tweets = blist([])

	fIn = codecs.open("lowcorpus.txt", "r", "utf-8")
	for line in fIn:
		tweets.append(line.split())


	print len(tweets)

	dictionary = gensim.corpora.Dictionary([doc for doc in tweets])
	dictionary.compactify()
	#dictionary.save("dictionary.dict")

	corpus = [dictionary.doc2bow(doc) for doc in tweets]
	#gensim.corpora.MmCorpus.serialize('test.mm', corpus)"""

	corpus = gensim.corpora.MmCorpus('test.mm')
	dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

	print "entrenando"
	#exportar en todas las terminales
	"""
	export PYRO_SERIALIZERS_ACCEPTED="pickle"
	export PYRO_SERIALIZER="pickle"
	"""
	lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50,chunksize=20000, distributed=True)
	lda.save('model.lda')
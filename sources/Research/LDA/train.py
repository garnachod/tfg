import gensim
from blist import blist
import codecs

if __name__ == '__main__':
	#generateDictAndCorpus = True
	#if generateDictAndCorpus == True:
	tweets = blist([])

	fIn = codecs.open("lowcorpus.txt", "r", "utf-8")
	for line in fIn:
		tweets.append(line.split())


	print len(tweets)

	dictionary = gensim.corpora.Dictionary([doc for doc in tweets])
	dictionary.compactify()
	dictionary.save("dictionary.dict")

	corpus = [dictionary.doc2bow(doc) for doc in tweets]
	gensim.corpora.MmCorpus.serialize('test.mm', corpus)

	#corpus = gensim.corpora.MmCorpus('test.mm')
	#dictionary = gensim.corpora.Dictionary.load("dictionary.dict")

	print "entrenando"
	#lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, distributed=True)
	lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=50, chunksize=2000)
	lda.save('model.lda')

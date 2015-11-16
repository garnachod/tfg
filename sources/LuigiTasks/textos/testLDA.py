import gensim

if __name__ == '__main__':

	corpus = gensim.corpora.MmCorpus('corpus.mm')
	dictionary = gensim.corpora.Dictionary.load("dictionary.dict")
	lda = gensim.models.LdaModel.load('model.lda')

	print lda.print_topics(num_topics=10, num_words=10)



	print len(dictionary.items())
	print dictionary.doc2bow(["no"])
	print len(lda.state.sstats[0])
	print len(lda.state.sstats)

	corpus = gensim.corpora.MmCorpus('corpus_p_molins.mm')
	dictionary = gensim.corpora.Dictionary.load("dictionary_p_molins.dict")
	lda = gensim.models.LdaModel.load('model_p_molins.lda')

	print lda.print_topics(num_topics=7, num_words=10)



	print len(dictionary.items())
	print lda.show_topic(0, topn=100)
	print dictionary.doc2bow(["no"])
	print dictionary[0]
	print len(lda.state.sstats[0])
	print len(lda.state.sstats)
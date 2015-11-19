import gensim
import pyLDAvis.gensim
import pyLDAvis


if __name__ == '__main__':
	"""
	corpus = gensim.corpora.MmCorpus('corpus.mm')
	dictionary = gensim.corpora.Dictionary.load("dictionary.dict")
	lda = gensim.models.LdaModel.load('model.lda')

	vis_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
	#pyLDAvis.display(vis_data)
	pyLDAvis.show(vis_data, ip='0.0.0.0', port=8082, n_retries=50, local=True, open_browser=False)

	print lda.print_topics(num_topics=10, num_words=10)



	print len(dictionary.items())
	print dictionary.doc2bow(["no"])
	print len(lda.state.sstats[0])
	print len(lda.state.sstats)"""
	"""
	"""
	corpus = gensim.corpora.MmCorpus('corpus_nolem_p_molins.mm')
	dictionary = gensim.corpora.Dictionary.load("dictionary_nolem_p_molins.dict")
	lda = gensim.models.LdaModel.load('model_nolem_p_molins.lda')

	#pyLDAvis.enable_notebook()
	vis_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
	#pyLDAvis.display(vis_data)
	pyLDAvis.save_json(vis_data, "testLDAvis.json")
	#pyLDAvis.show(vis_data, ip='0.0.0.0', port=8082, n_retries=50, local=True, open_browser=False)

	"""print lda.print_topics(num_topics=7, num_words=10)



	print len(dictionary.items())
	print lda.show_topic(0, topn=100)
	print dictionary.doc2bow(["no"])
	print dictionary[0]
	print len(lda.state.sstats[0])
	print len(lda.state.sstats"""
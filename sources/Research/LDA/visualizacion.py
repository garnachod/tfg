import pyLDAvis.gensim
import gensim

if __name__ == '__main__':

	corpus = gensim.corpora.MmCorpus('test.mm')
	dictionary = gensim.corpora.Dictionary.load("dictionary.dict")
	lda = gensim.models.LdaModel.load('model.lda')

	followers_data =  pyLDAvis.gensim.prepare(lda, corpus, dictionary)
	print "guardando"
	pyLDAvis.save_html(followers_data, "vis.html")
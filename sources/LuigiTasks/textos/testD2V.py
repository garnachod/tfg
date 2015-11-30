import gensim
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

if __name__ == '__main__':
	"""modelo = gensim.models.Word2Vec.load('model.d2v')

	cosenos = modelo.most_similar(positive=['pp'], topn=30)
	for coseno in cosenos:
		print coseno[0] + "\t\t" + str(coseno[1]) """


	modelo = Doc2Vec.load('tweet_dbow.d2v')

	print modelo["pp"]

	cosenos = modelo.most_similar(positive=['pp'], topn=30)
	for coseno in cosenos:
		print coseno[0] + "\t\t" + str(coseno[1]) 


	#mario hernandez
	
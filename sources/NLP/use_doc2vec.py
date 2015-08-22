from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

if __name__ == '__main__':
	palabra_compara = "minecraft"
	model = Doc2Vec.load('tweet_dm.d2v')
	tuplas = model.most_similar(positive=[palabra_compara], topn=50)

	mayor_long = 0
	for palabra, coseno in tuplas:
		if len(palabra) > mayor_long:
			mayor_long = len(palabra)
	
	mayor_long += 5
	espacios = "                  "
	print "DM"
	print "Palabra" + ":" + espacios[:mayor_long-len("palabra")]+ "Coseno"
	for palabra, coseno in tuplas:
		print palabra + ":" + espacios[:mayor_long-len(palabra)]+ str(coseno)

	model = Doc2Vec.load('tweet_dbow.d2v')
	tuplas = model.most_similar(positive=[palabra_compara], topn=50)

	mayor_long = 0
	for palabra, coseno in tuplas:
		if len(palabra) > mayor_long:
			mayor_long = len(palabra)
	
	mayor_long += 5
	espacios = "                 "
	print "DBOW"
	print "Palabra" + ":" + espacios[:mayor_long-len("palabra")]+ "Coseno"
	for palabra, coseno in tuplas:
		print palabra + ":" + espacios[:mayor_long-len(palabra)]+ str(coseno)
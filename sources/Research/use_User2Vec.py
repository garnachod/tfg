import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandra import ConsultasCassandra

from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec

if __name__ == '__main__':
	user_compara = "230377004"
	model = Doc2Vec.load('/media/dani/data/trainedVecsTBYUser/tweet_dm.d2v')
	tuplas = model.docvecs.most_similar(positive=[user_compara], topn=50)

	mayor_long = 0
	for palabra, coseno in tuplas:
		if len(palabra) > mayor_long:
			mayor_long = len(palabra)
	
	mayor_long += 5
	espacios = "                  "
	print "DM"
	print "USUARIO" + ":" + espacios[:mayor_long-len("USUARIO")]+ "Coseno"

	cs = ConsultasCassandra()
	for user_id, coseno in tuplas:
		screen_name = cs.getUserByIDShortCassandra(long(user_id)).screen_name
		print screen_name + ":" + espacios[:mayor_long-len(screen_name)]+ str(coseno)
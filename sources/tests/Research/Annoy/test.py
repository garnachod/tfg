import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from annoy import AnnoyIndex
from gensim.models import Doc2Vec

if __name__ == '__main__':

	f = 50
	t = AnnoyIndex(f)  # Length of item vector that will be indexed

	model = Doc2Vec.load('/media/dani/data/trainedVecsTBYUser/tweet_dm.d2v')
	for i, tag in enumerate(model.docvecs.doctags):
		t.add_item(i, model.docvecs[tag])

	
	#for i in xrange(1000):
	#	v = [random.gauss(0, 1) for z in xrange(f)]
	print "creando"
	t.build(100) # 10 trees
	t.save('/media/dani/data/trainedVecsTBYUser/test.ann')

	print "guardado"

	u = AnnoyIndex(f)
	u.load('/media/dani/data/trainedVecsTBYUser/test.ann') # super fast, will just mmap the file

	print "cargado"
	#print(u.get_nns_by_item(0, 1000)) # will find the 1000 nearest neighbors
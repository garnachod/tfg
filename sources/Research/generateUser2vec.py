# gensim modules
from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from collections import namedtuple
import time
import random
from blist import blist


class LabeledLineSentence(object):
	def __init__(self, source):
		self.source = source
		self.sentences = None
		
	def to_array(self):
		if self.sentences is None:
			self.sentences = blist()
			with utils.smart_open(self.source) as fIn:
				last_identif = 0
				for item_no, line in enumerate(fIn):
					line = line.replace("\n", "")
					if item_no % 2 == 0:
						last_identif = long(line)
					else:
						palabras = utils.to_unicode(line).split()
						palabras_clean = []
						for palabra in palabras:
							if len(palabra)> 1:
								palabras_clean.append(palabra)
						self.sentences.append(TaggedDocument(palabras_clean, [str(last_identif)]))
					
		return self.sentences
		

	def sentences_perm(self):
		random.shuffle(self.sentences)
		return self.sentences

#raise NotImplementedError( "Should have implemented this" )

if __name__ == '__main__':
	dimension = 100
	sentences = LabeledLineSentence("/media/dani/data/tweetsByUser.txt")

	total_start = time.time()

	dbow = False
	if dbow:
		model = Doc2Vec(min_count=1, window=10, size=dimension, sample=1e-3, negative=5, dm=0 ,workers=6, alpha=0.04)
		
		print "inicio vocab"
		model.build_vocab(sentences.to_array())
		print "fin vocab"
		first_alpha = model.alpha
		last_alpha = 0.01
		next_alpha = first_alpha
		epochs = 30
		for epoch in range(epochs):
			start = time.time()
			print "iniciando epoca DBOW:"
			print model.alpha
			model.train(sentences.sentences_perm())
			end = time.time()
			next_alpha = (((first_alpha - last_alpha) / float(epochs)) * float(epochs - (epoch+1)) + last_alpha)
			model.alpha = next_alpha
			print "tiempo de la epoca " + str(epoch) +": " + str(end - start)

		model.save('./tweet_dbow.d2v')

	dm = True
	if dm:
		#model = Doc2Vec(min_count=1, window=10, size=dimension, sample=1e-3, negative=5, workers=6, dm_mean=1, alpha=0.04)
		model = Doc2Vec(min_count=1, window=10, size=dimension, sample=1e-3, negative=5, workers=6, alpha=0.04)
		#model = Doc2Vec(min_count=1, window=10, size=dimension, sample=1e-3, negative=5, workers=6, alpha=0.04, dm_concat=1)
		#
		print "inicio vocab"
		model.build_vocab(sentences.to_array())
		print "fin vocab"
		first_alpha = model.alpha
		last_alpha = 0.01
		next_alpha = first_alpha
		epochs = 20
		for epoch in range(epochs):
			start = time.time()
			print "iniciando epoca DM:"
			print model.alpha
			model.train(sentences.sentences_perm())
			end = time.time()
			next_alpha = (((first_alpha - last_alpha) / float(epochs)) * float(epochs - (epoch+1)) + last_alpha)
			model.alpha = next_alpha
			print "tiempo de la epoca " + str(epoch) +": " + str(end - start)

		model.save('./tweet_dm.d2v')
	
	total_end = time.time()

	print "tiempo total:" + str((total_end - total_start)/60.0)
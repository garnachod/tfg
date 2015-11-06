# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandra import ConsultasCassandra
import pickle


if __name__ == '__main__':
	namefile = "/media/dani/data/tweetsBin.b"
	cons = ConsultasCassandra()
	rows = cons.getAllStatusAndIDUser()
	objToPickle = []
	for row in rows:
		objToPickle.append(row)
		
	pickle.dump(objToPickle, open(namefile, "wb"))


	

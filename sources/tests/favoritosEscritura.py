# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorFavoritosNeo4j import EscritorFavoritosNeo4j
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorFavoritosUser import RecolectorFavoritosUser
import time

if __name__ == '__main__':
	consultas = ConsultasWeb()
	usuario = "@garnachod"
	#usuario = "@Dowrow"
	

	inicio = time.time()

	escritores = [EscritorTweetsCassandra(-1)]
	escritores.append(EscritorFavoritosNeo4j(-1))
	recolector = RecolectorFavoritosUser(escritores)
	recolector.recolecta(query=usuario)

	fin = time.time()
	print fin - inicio
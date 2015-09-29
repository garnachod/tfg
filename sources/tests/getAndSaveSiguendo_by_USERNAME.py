# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSiguiendoNeo4j import EscritorSiguiendoNeo4j
from SocialAPI.TwitterAPI.RecolectorSiguiendoShort import RecolectorSiguiendoShort
import time

if __name__ == '__main__':
	consultas = ConsultasWeb()
	usuario = "@Yihad_Global"
	#usuario = "@Dowrow"
	searchID = consultas.setAppSearchAndGetId(usuario, 1)
	

	inicio = time.time()

	escritores = [EscritorSiguiendoNeo4j(searchID)]
	recolector = RecolectorSiguiendoShort(escritores)
	recolector.recolecta(query=usuario)

	fin = time.time()
	consultas.setAppSearchTime(searchID, fin - inicio)

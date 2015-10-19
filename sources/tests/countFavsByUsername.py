# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.ConsultasNeo4j import ConsultasNeo4j


if __name__ == '__main__':
	consultas = ConsultasWeb()
	user_id = consultas.getUserIDByScreenName("Taxigate")
	
	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsFavsByUserID(user_id)
	print(len(identificadores))
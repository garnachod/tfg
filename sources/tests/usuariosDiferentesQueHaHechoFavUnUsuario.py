# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j


if __name__ == '__main__':
	consultas = ConsultasWeb()
	user_id = consultas.getUserIDByScreenName("Taxigate")
	
	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsFavsByUserID(user_id)

	cs = ConsultasCassandra()

	usuarios = {}
	for identificador in identificadores:
		idUser = cs.getTweetUserByTweetIDCassandra(identificador)
		strIdUser = str(idUser)
		if strIdUser in usuarios:
			usuarios[strIdUser] += 1
		else:
			usuarios[strIdUser] = 1

	for usuario in usuarios:
		print usuario
		print usuarios[usuario]

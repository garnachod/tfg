# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
from time import time, sleep



def recopila(lista_ids):
	#busqueda
	if len(lista_ids) == 0:
		return 

	escritorList = []
	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsUser(escritorList)

	ids_no_recopilados = []
	#bucle de usuarios
	for identificador in lista_ids:
		print identificador
		try:
			recolector.recolecta(identificador=identificador)
		except Exception, e:
			print e
			ids_no_recopilados.append(identificador)
			sleep(5*60)

	recopila(ids_no_recopilados)

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


	user_list = []
	for usuario in usuarios:
		user_list.append(long(usuario))
	
	recopila(user_list)
		

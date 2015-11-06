# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSeguidoresNeo4j import EscritorSeguidoresNeo4j
from DBbridge.ConsultasCassandra import ConsultasCassandra
from SocialAPI.TwitterAPI.RecolectorSiguiendoShort import RecolectorSiguiendoShort
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
import time


def recopila(lista_ids):
	#busqueda
	if len(lista_ids) == 0:
		return 


	escritores = [EscritorSeguidoresNeo4j(-1)]
	recolector = RecolectorSiguiendoShort(escritores)
	

	ids_no_recopilados = []
	#bucle de usuarios
	for identificador in lista_ids:
		print identificador
		try:
			recolector.recolecta(id_user=identificador)
		except Exception, e:
			print e
			ids_no_recopilados.append(identificador)
			sleep(5*60)

	recopila(ids_no_recopilados)


if __name__ == '__main__':
	consultas = ConsultasCassandra()
	usuario = "p_molins"
	#usuario = "@Dowrow"
	user_id = consultas.getUserIDByScreenNameCassandra(usuario)

	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)
	print len(identificadores)
	recopila(identificadores)

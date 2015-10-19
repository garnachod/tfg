# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSeguidoresSQL import EscritorSeguidoresSQL
from SocialAPI.TwitterAPI.RecolectorSeguidores import RecolectorSeguidores
from DBbridge.ConexionSQL import ConexionSQL
import time

if __name__ == '__main__':
	consultas = ConsultasWeb()
	usuario = "@Yihad_Global"
	searchID = consultas.setAppSearchAndGetId(usuario, 1)
	

	inicio = time.time()

	escritor = EscritorSeguidores(searchID)
	recolector = EscritorSeguidoresSQL(escritor)
	recolector.recolecta(usuario)

	fin = time.time()
	consultas.setAppSearchTime(searchID, fin - inicio)

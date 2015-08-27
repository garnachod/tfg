# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSeguidoresNeo4j import EscritorSeguidoresNeo4j
from SocialAPI.TwitterAPI.RecolectorSeguidoresShort import RecolectorSeguidoresShort
from Neo4j.ConexionNeo4j import ConexionNeo4j
import time


if __name__ == '__main__':
	consultas = ConsultasWeb()
	usuario = "@p_molins"
	

	grafo = ConexionNeo4j().getGraph()
	user_id = consultas.getUserIDByScreenName(usuario)

	query = "MATCH (x:user)-[:FOLLOW]->(n:user {id_twitter:" +str(user_id)+"}) return x"
	objetos = grafo.cypher.execute(query)
	for i, objeto in enumerate(objetos):
		id_consulta = objeto[0].properties["id_twitter"]
		if i < 34:
			continue
		searchID = consultas.setAppSearchAndGetId(id_consulta, 1)
		escritores = [EscritorSeguidoresNeo4j(searchID)]
		recolector = RecolectorSeguidoresShort(escritores)
		print "Recolectando: " + str(id_consulta) + "    " + str(i)
		recolector.recolecta(id_user=id_consulta)
		print "Durmiendo"
		time.sleep(65)

	
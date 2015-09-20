# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra
import datetime
from time import time, sleep

if __name__ == '__main__':
	escritorList = []

	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsUser(escritorList)
	tiempo_inicio = time()
	recolector.recolecta(query="intel")
	recolector.recolecta(identificador=2383366169)
	tiempo_fin = time()
	print "tiempo recoleccion y escritura"
	print  tiempo_fin - tiempo_inicio
	#session = ConexionCassandra().getSession()
	#query = """SELECT * FROM tweets where longitude > 0"""
	#print len(session.execute(query))
	#luceneQuery = """SELECT * FROM tweets WHERE lucene='{
    #	query  : {type:"phrase", field:"status", value:"tardan", slop:1}
	#	}' limit 100;"""
	#print session.execute(luceneQuery)


	testCompleto = False
	if testCompleto:
		arrayUsuarios = ["WillyrexYT", "Alvaro845", "Thetoretegg", "Fernanfloo", "Nestle_es", "yuyacst", "AlexMonthy", "Wigetta", "Xodaaaa", "Gameloft_Spain", "NexxuzHD", "AudazCarlos", "xPekeLoL", "steam_games", "vegetta777", "bysTaXx", "bysTaXx", "PlayStationES", "mangelrogel", "Outconsumer"]
		tiempo_total = 30 * 60 #30 minutos
		for i, usuario in enumerate(arrayUsuarios):
			print i
			recolector.recolecta(usuario)
			sleep(tiempo_total/len(arrayUsuarios))
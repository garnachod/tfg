from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra
import datetime
from time import time 

if __name__ == '__main__':
	escritorList = []

	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsUser(escritorList)
	tiempo_inicio = time()
	recolector.recolecta("WillyrexYT")
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
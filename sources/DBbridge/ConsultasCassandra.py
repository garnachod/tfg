# -*- coding: utf-8 -*-
from Cassandra.ConexionCassandra import ConexionCassandra
from collections import namedtuple
from blist import blist
import codecs

class ConsultasCassandra(object):
	"""docstring for ConsultasCassandra"""
	def __init__(self):
		super(ConsultasCassandra, self).__init__()
		self.session_cassandra = ConexionCassandra().getSession()
		
	def getTweetsUsuarioCassandra(self, twitterUser, use_max_id=False, max_id=0, limit=1000):
		user_id = self.getUserIDByScreenNameCassandra(twitterUser)
		if user_id is None:
			return []

		user = self.getUserByIDShortCassandra(user_id)

		Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter')
		if use_max_id:
			query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, id_twitter  FROM tweets WHERE tuser = %s AND id_twitter < %s ORDER BY id_twitter DESC LIMIT %s;"""

			try:
				retorno = blist([])
				rows = self.session_cassandra.execute(query, [user_id, max_id, limit])
				for row in rows:
					nuevaFila = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter)
					retorno.append(nuevaFila)
				return retorno
			except Exception, e:
				print "getTweetsUsuarioCassandra TRUE use_max_id"
				print e
				return []
		else:
			query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, id_twitter FROM tweets WHERE tuser = %s ORDER BY id_twitter DESC LIMIT %s;"""

			try:
				retorno = blist([])
				rows = self.session_cassandra.execute(query, [user_id, limit])
				for row in rows:
					nuevaFila = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter)
					retorno.append(nuevaFila)
				return retorno
			except Exception, e:
				print "getTweetsUsuarioCassandra FALSE use_max_id"
				print e
				return []
		
	def getUserIDByScreenNameCassandra(self, twitterUser):
		query = """SELECT id_twitter FROM users WHERE screen_name = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [twitterUser])
			if len(rows) == 0:
				return None
				
			return long(rows[0].id_twitter)
		except Exception, e:
			print "getUserIDByScreenNameCassandra"
			print e
			return None

	def getLastTweetCollectedScreenNameCassandra(self, twitterUser):
		query = """SELECT last_tweet_collected FROM users WHERE screen_name = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [twitterUser])
			if len(rows) == 0:
				return 0

			return long(rows[0].last_tweet_collected)
		except Exception, e:
			print "getLastTweetCollectedScreenNameCassandra"
			print e
			return 0
	
	def setLastTweetCollectedScreenNameCassandra(self, twitterUser, maximo):
		user_id = self.getUserIDByScreenNameCassandra(twitterUser)
		query = "UPDATE users SET last_tweet_collected = %s WHERE id_twitter = %s;"
		try:
			self.session_cassandra.execute(query, (maximo, user_id))
			return True
		except Exception, e:
			print "setLastTweetCollectedScreenNameCassandra"
			print e
			return False

	def getTweetStatusCassandra(self, identificador):
		query = "SELECT status FROM tweets WHERE id_twitter = %s LIMIT 1;"
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			row = rows[0]

			return row.status
		except Exception, e:
			print "getTweetStatusCassandra"
			print str(e)
			return False

	def getUserByIDLargeCassandra(self, identificador):
		query = """SELECT name, screen_name, followers, location, created_at FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			row = rows[0]

			return row
		except Exception, e:
			print "getUserByIDLargeCassandra"
			print str(e)
			return False

	def getUserByIDShortCassandra(self, identificador):
		query = """SELECT screen_name, profile_img FROM users WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			row = rows[0]

			return row
		except Exception, e:
			print "getUserByIDLargeCassandra"
			print str(e)
			return False

	def getTweetByIDLargeCassandra(self, identificador):
		query = """SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, tuser, id_twitter FROM tweets WHERE id_twitter = %s LIMIT 1;"""
		try:
			rows = self.session_cassandra.execute(query, [identificador])
			row = rows[0]
			user = self.getUserByIDShortCassandra(row.tuser)

			Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter')
			retorno = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter)
			return retorno
		except Exception, e:
			print "getTweetByIDLargeCassandra"
			print str(e)
			return False

	#TODO Problemas de seguridad?
	def getTweetsTopicsCassandra(self, topics, use_max_id=False, max_id=0, limit=100):
		query = "SELECT status, favorite_count, retweet_count, orig_tweet, media_urls, tuser, id_twitter, created_at FROM tweets WHERE lucene =\'{"
		if use_max_id:
			query += "filter : {type:\"boolean\", must:["
			query += "{type:\"match\", field:\"orig_tweet\", value:0}, "
			query += "{type:\"range\", field:\"id_twitter\", upper: "+str(max_id)+", include_upper:false} ] },"
		else:
			query += """filter : {type:\"boolean\", must:[
				   {type:"match", field:"orig_tweet", value:0} ] },"""
		query += "query : {type:\"phrase\", field:\"status\", value:\""+topics+"\", slop:1}, "
		query += "sort : {fields: [ {field:\"created_at\", reverse:true} ] }"
		query += "}\' limit %s;"
		

		Row = namedtuple('Row', 'status, favorite_count, retweet_count, orig_tweet, media_urls, screen_name, profile_img, id_twitter')

		try:
			rows = self.session_cassandra.execute(query, [limit])
			retorno = blist([])
			#JOIN
			for row in rows:
				user = self.getUserByIDShortCassandra(row.tuser)
				fila = Row(row.status, row.favorite_count, row.retweet_count, row.orig_tweet, row.media_urls, user.screen_name, user.profile_img, row.id_twitter)
				retorno.append(fila)
			return retorno
		except Exception, e:
			print "getTweetsTopicsCassandra"
			print str(e)
			return False

	#TODO Problemas de seguridad?
	def getIDsTweetsTrainCassandra(self, topics, limit):
		query = "SELECT id_twitter FROM tweets WHERE lucene =\'{"
		query += """filter : {type:\"boolean\", must:[
				   {type:"match", field:"orig_tweet", value:0} ] },"""
		query += "query : {type:\"phrase\", field:\"status\", value:\""+topics+"\", slop:1} "
		query += "}\' limit %s;"

		try:
			return self.session_cassandra.execute(query, [limit])
		except Exception, e:
			print "getTweetsTopicsCassandra"
			print str(e)
			return False

	"""estadisticas"""
	def getNumTweetsNoRTCassandra(self):
		query ="SELECT count(*) FROM tweets WHERE orig_tweet = 0 LIMIT 100000;"
		try:
			rows = self.session_cassandra.execute(query)

			num = rows[0][0]
			
			return num
		except Exception, e:
			print str(e)
			return False

	def getNumTweetsSiRTCassandra(self):
		query ="SELECT count(*) FROM tweets LIMIT 100000;"
		try:
			rows = self.session_cassandra.execute(query)
			num = rows[0][0]
			
			return num - self.getNumTweetsNoRTCassandra()
		except Exception, e:
			print str(e)
			return False

	"""PRUEBAS"""
	def getTweetsUserAndPrintFile(self, filename, twitterUser):
		"""obtiene los tweets y los imprime en un fichero para que se puedan hacer pruebas con los textos"""
		fOut = codecs.open(filename, "w", "utf-8")
		tweets = self.getTweetsUsuarioCassandra(twitterUser, limit=10000)
		for tweet in tweets:
			texto = tweet.status
			texto = texto.replace("\n", " ")
			fOut.write(texto)
			fOut.write("\n")

		fOut.close()

if __name__ == '__main__':
	consultas = ConsultasCassandra()
	print "test de getUserIDByScreenNameCassandra"
	print consultas.getUserIDByScreenNameCassandra("WillyrexYT")
	print "test de getTweetsUsuarioCassandra"
	print consultas.getTweetsUsuarioCassandra("WillyrexYT", limit=10000)[0]
	print consultas.getTweetsUsuarioCassandra("WillyrexYT", use_max_id=True, max_id=611207358266544128, limit=10000)[0]
	#print "test de setLastTweetCollectedScreenNameCassandra"
	#print consultas.setLastTweetCollectedScreenNameCassandra("WillyrexYT", 0)
	print "test de getLastTweetCollectedScreenNameCassandra"
	print consultas.getLastTweetCollectedScreenNameCassandra("WillyrexYT")
	print "test de getUserByIDLargeCassandra"
	print consultas.getUserByIDLargeCassandra(230377004)
	print consultas.getUserByIDLargeCassandra(230377004)[2]
	print "inspecion de los metodos de row"
	print "Es un namedtuple, por lo que haremos un join a mano"
	print "test de getTweetByIDLargeCassandra"
	print consultas.getTweetByIDLargeCassandra(631260309026553856)
	print "test de getTweetsTopicsCassandra"
	print consultas.getTweetsTopicsCassandra("galletas")[0]
	print consultas.getTweetsTopicsCassandra("@WillyrexYT Esto es mi día a día")[0]
	print consultas.getTweetsTopicsCassandra("galletas", use_max_id=True, max_id=631260309026553856, limit=100)[0]
	print "test de getIDsTweetsTrainCassandra"
	print consultas.getIDsTweetsTrainCassandra("galletas", 100)[0]
	print "test de getNumTweetsNoRTCassandra"
	print consultas.getNumTweetsNoRTCassandra()
	print "test de getNumTweetsSiRTCassandra"
	print consultas.getNumTweetsSiRTCassandra()


	testCompleto = False
	if testCompleto == True:
		arrayUsuarios = ["WillyrexYT", "Alvaro845", "Thetoretegg", "Fernanfloo", "Nestle_es", "yuyacst", "AlexMonthy", "Wigetta", "Xodaaaa", "Gameloft_Spain", "NexxuzHD", "AudazCarlos", "xPekeLoL", "steam_games", "vegetta777", "bysTaXx", "bysTaXx", "PlayStationES", "mangelrogel", "Outconsumer"]
		for usuario in arrayUsuarios:
			consultas.getTweetsUserAndPrintFile("/home/dani/ficherosPrueba_plsa/"+usuario+".txt",usuario)
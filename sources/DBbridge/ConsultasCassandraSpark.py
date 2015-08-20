# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('/home/dani/tfg/sources')
sys.path.append(lib_path)

from Cassandra.ConexionCassandra import ConexionCassandra
from spark.SparkContexto import SparkContexto
import time


class ConsultasCassandraSpark(object):
	"""docstring for ConsultasCassandraSpark"""
	def __init__(self):
		super(ConsultasCassandraSpark, self).__init__()
		self.session_cassandra = ConexionCassandra().getSession()
		self.sc = SparkContexto().getContexto()


	#tupla no_rt, si_rt
	def getNumTweetsRTCS(self):
		query ="SELECT orig_tweet FROM tweets;"
		try:

			rows = self.session_cassandra.execute(query)

			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_rt = lambda x: 1 if x[0] != 0 else 0
			filtro_no_rt = lambda x: 1 if x[0] == 0 else 0
			reduce_f = lambda x, y: x + y
			return rows_paralelas.map(filtro_no_rt).reduce(reduce_f), rows_paralelas.map(filtro_si_rt).reduce(reduce_f)
			
		except Exception, e:
			print str(e)
			return False

	#no_media , si_media
	def getNumTweetsMediaCS(self):
		query ="SELECT media_urls FROM tweets;"
		try:

			rows = self.session_cassandra.execute(query)

			rows_paralelas = self.sc.parallelize(rows)
			filtro_si_media = lambda x: 1 if x[0] is not None else 0
			filtro_no_media = lambda x: 0 if x[0] is not None else 1
			reduce_f = lambda x, y: x + y
			return rows_paralelas.map(filtro_no_media).reduce(reduce_f), rows_paralelas.map(filtro_si_media).reduce(reduce_f)
			
		except Exception, e:
			print str(e)
			return False


if __name__ == '__main__':
	ccs = ConsultasCassandraSpark()
	tiempo_inicio = time.time()
	print ccs.getNumTweetsMediaCS()
	tiempo_fin = time.time()
	print tiempo_fin - tiempo_inicio
	tiempo_inicio = time.time()
	print ccs.getNumTweetsRTCS()
	tiempo_fin = time.time()
	print tiempo_fin - tiempo_inicio
	#time.sleep(200)
	exit()
	"""
	export SPARK_HOME=/home/dani/spark/spark-1.4.0
	export PATH=$PATH:$SPARK_HOME
	"""
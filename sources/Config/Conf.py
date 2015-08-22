from collections import namedtuple

class Conf():
	"""docstring for SparkContexto"""
	class __impl:
		"""docstring for __impl"""
		def __init__(self):
			#cassandra
			self.cassandra_keyspace = 'twitter'
			#SQL
			self.sql_database = 'twitter'
			self.sql_user = 'tfg'
			self.sql_password = 'postgres_tfg'
			self.sql_host = 'localhost'
			#app
			self.abspath = '/home/dani/tfg/sources'
			#SPARK
			self.spark_home = '/home/dani/spark/spark-1.4.0'
			#Neo4j
			self.neo4j_password = 'tfg_neo4j'

		def getCassandraKeyspace(self):
			return self.cassandra_keyspace

		def getSparkHome(self):
			return self.spark_home

		def getSQLInfo(self):
			infoSQL = namedtuple('InfoSQL', 'database, user, password, host')
			return infoSQL(self.sql_database, self.sql_user, self.sql_password, self.sql_host)

		def  getNeo4jPassword(self):
			return self.neo4j_password


	# storage for the instance reference
	__instance = None

	def __init__(self):
		if Conf.__instance is None:
			Conf.__instance = Conf.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
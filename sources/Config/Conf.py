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

		def getCassandraKeyspace(self):
			return self.cassandra_keyspace


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
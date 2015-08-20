# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('/home/dani/spark/spark-1.4.0/python')
sys.path.append(lib_path)
from pyspark import SparkConf, SparkContext

class SparkContexto():
	"""docstring for SparkContexto"""
	class __impl:
		"""docstring for __impl"""
		def __init__(self):
			self.conf = (SparkConf()
			 .setMaster("local[4]")
			 .setAppName("My app")
			 .set("spark.executor.memory", "100m")
			 .setSparkHome('/home/dani/spark/spark-1.4.0/python'))
			self.sc = SparkContext(conf = self.conf)

		def getContexto(self):
			return self.sc


	# storage for the instance reference
	__instance = None

	def __init__(self):
		if SparkContexto.__instance is None:
			SparkContexto.__instance = SparkContexto.__impl()

	def __getattr__(self, attr):
		""" Delegate access to implementation """
		return getattr(self.__instance, attr)

	def __setattr__(self, attr, value):
		""" Delegate access to implementation """
		return setattr(self.__instance, attr, value)
			



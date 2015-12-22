# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from RecolectorTwitter import * 
import time


class RecolectorDesdeFichero(luigi.Task):
	nombrefichero = luigi.Parameter()
	"""
		Recolecta los usuarios y los datos definidos en un csv por:
		usuario,recolector tweets, recolector seguidores, recolector siguendo

		lee el fichero definiciones_descarga/nombre.csv
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitterVariosUsuarios RecolectorDesdeFichero --nombrefichero UsuariosParaDescargar.csv
	"""
	def output(self):
		return luigi.LocalTarget(path='definiciones_descarga/%s.ok'%self.nombrefichero)

	def requires(self):
		#contiene una matriz de lineas
		lineas = []
		with open('definiciones_descarga/%s'%self.nombrefichero) as in_file:
			for i, line in enumerate(in_file):
				if i == 0:
					pass
				else:
					lineas.append(line.replace("\n", "").replace(" ", "").split(","))

		#print len(lineas)
		tasks = []

		for linea in lineas:
			if linea[1] == "1":
				if linea[4] == "1":
					tasks.append(RecolectorUsuarioTwitter(linea[0], limite=200))
				else:
					tasks.append(RecolectorUsuarioTwitter(linea[0]))

		return tasks

	def run(self):
		#contiene una matriz de lineas
		lineas = []
		with open('definiciones_descarga/%s'%self.nombrefichero) as in_file:
			for i, line in enumerate(in_file):
				if i == 0:
					pass
				else:
					lineas.append(line.replace("\n", "").replace(" ", "").split(","))


		for linea in lineas:
			if linea[2] == "1":
				yield RecolectorSeguidoresTwitter(linea[0])

			if linea[3] == "1":
				yield RecolectorSiguiendoTwitter(linea[0])


		with self.output().open("w") as output:
			output.write("OK")





class RecolectorDesdeFicheroGeneral(luigi.Task):
	nombrefichero = luigi.Parameter()
	"""
		Recolecta los usuarios y los datos definidos en un csv por:
		usuario,recolector tweets, recolector seguidores, recolector siguendo, limite descarga, query. 

		Lee el fichero definiciones_descarga/nombre.csv
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitterVariosUsuarios RecolectorDesdeFicheroGeneral --nombrefichero UsuariosParaDescargar.csv
	"""
	def output(self):
		return luigi.LocalTarget(path='definiciones_descarga/%s.ok'%self.nombrefichero)

	def requires(self):
		#contiene una matriz de lineas
		lineas = []
		print 'definiciones_descarga/%s'%self.nombrefichero
		with open('definiciones_descarga/%s'%self.nombrefichero) as in_file:
			for i, line in enumerate(in_file):
				if i == 0:
					pass
				else:
					lineas.append(line.replace("\n", "").split(","))

		#print len(lineas)
		tasks = []

		for linea in lineas:
			if linea[1] == "1":
				if linea[4] == "1":
					tasks.append(RecolectorUsuarioTwitter(linea[0], limite=200))
				else:
					tasks.append(RecolectorUsuarioTwitter(linea[0]))

			if linea[2] == "1":
				tasks.append(RecolectorSeguidoresTwitter(linea[0]))

			if linea[3] == "1":
				tasks.append(RecolectorSiguiendoTwitter(linea[0]))

			if linea[5] == "1":
				tasks.append(RecolectorContenidoTweet(linea[0], limitedescarga=30))


		return tasks

	def run(self):
		with self.output().open("w") as output:
			output.write("OK")

		
class RecolectorSeguidoresNEpocasNUsuarios(luigi.Task):
	"""	
		nEpocas siempre numero, usuarios: usuarios separados por , y espacios si quieres
	"""
	"""
		Uso:
			PYTHONPATH='' luigi --module RecolectorTwitterVariosUsuarios RecolectorSeguidoresNEpocasNUsuarios --usuarios garnachod
	"""
	
	usuarios = luigi.Parameter()
	nepocas = luigi.Parameter(default="1")

	def output(self):
		return luigi.LocalTarget(path='definiciones_descarga/RecolectorSeguidoresNEpocasNUsuarios(%s_%s).ok'%(self.nepocas, self.usuarios))

	def run(self):

		for epoca in range(int(self.nepocas)):
			for usuario in self.usuarios.replace(" ", "").split(","):
				try:
					os.remove('tasks/RecolectorSeguidoresTwitter(%s)'%usuario)
					time.sleep(5)
				except Exception, e:
					print e
					pass

				yield RecolectorSeguidoresTwitter(usuario, forcecomplete="False")

				

	
		with self.output().open("w") as output:
			output.write("OK")
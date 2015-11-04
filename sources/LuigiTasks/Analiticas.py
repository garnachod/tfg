# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
import luigi
from GeneradorDocumentosTwitter import *
import codecs
import random
from dateutil import parser
import datetime

class GraficaEventosBrutosTwitter(luigi.Task):
	usuario = luigi.Parameter()

	def output(self):
		return luigi.LocalTarget(path='graficas/GraficaEventosBrutosTwitter(%s).html'%self.usuario, format=luigi.format.TextFormat(encoding='utf8'))

	def requires(self):
		return GeneradorEventosSeguidoresPuntosUsuario(self.usuario)

	def run(self):
		template = codecs.open("templates/TemplateGoogleChartsPoints.html", "r", "utf-8")
		template_content = template.read()
		template.close()
		with self.output().open('w') as out_file:
			cadenaPuntos = u"["
			with self.input().open('r') as in_file:
				primerPunto = False
				for line in in_file:
					puntos = line.replace("\n", "").split(",")[1:]
					for punto in puntos:
						if primerPunto == True:
							cadenaPuntos += u",["+ str((parser.parse(punto) - datetime.datetime.today()).total_seconds()) + "," + str(random.random()*100.0) + u"]"
						else:
							cadenaPuntos += u"["+ str((parser.parse(punto) - datetime.datetime.today()).total_seconds()) + "," + str(random.random()*100.0) + u"]"
							primerPunto = True

			cadenaPuntos += "]"
			salida = template_content.replace("{{}}", cadenaPuntos)
			out_file.write(salida)

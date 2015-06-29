# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from DBbridge.ConsultasWeb import ConsultasWeb
#from DBbridge.ConsultasWeb import ConsultasWeb
import hashlib


class AltaTarea():
	def __init__(self):
		self.consultas = ConsultasWeb()

	def alta(self):
		tipoTarea = request.form['tipoTarea']
		tipoBusqueda = request.form['tipoBusqueda']
		search = request.form['search']
		tiempoTarea = request.form['tiempoTarea']


		#if nombre is None or correo is None or institucion is None or usern is None or passw is None or passwr is None:
		if tipoTarea is None or tipoBusqueda is None or search is None or tiempoTarea is None:
			return False
		elif tipoTarea is '' or tipoBusqueda is '' or search is '' or tiempoTarea is '':
			return False
		else:
			tipoDB = ''
			if tipoTarea == 'sb':
				if tipoBusqueda == 'suser':
					#BusquedaSencillaUser
					tipoDB = 'BusquedaSencillaUser'
				else:
					#BusquedaSencillaTopic
					tipoDB = 'BusquedaSencillaKeywords'

				id_lista = -1
			elif tipoTarea == 'bp':
				if tipoBusqueda == 'suser':
					#AnalisisPalabrasUser
					tipoDB = 'AnalisisPalabrasUser'
				else:
					#AnalisisPalabrasKeywords
					tipoDB = 'AnalisisPalabrasKeywords'

				id_lista = request.form['lista_entrenamiento']
				#return False

			searchID = self.consultas.setAppSearchAndGetId(search, session['user_id'])

			tiempo = 0

			if tiempoTarea == 'semana':
				tiempo = 7
			elif tiempoTarea == 'dossemana':
				tiempo = 15
			else:
				tiempo = 30

			self.consultas.altaTarea(tipoDB, searchID, tiempo, id_lista)
			return True
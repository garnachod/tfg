# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Head import Head
from DBbridge.ConsultasWeb import ConsultasWeb
import threading
import hashlib
import json

class BusquedaAsinc():
	def __init__(self):
		self.consultas = ConsultasWeb()

	def toJsonSearch(self):
		if 'searchID' in session or session['searchID'] != 0:
			#records = []
			#record1 = {"name":"Bob", "email":"bob@email.com"}
			#records.append(record1)    
			#record2 = {"name":"Bob2", "email":"bob2@email.com"}
			#records.append(record2)
			#json.dumps
			search_id = session['searchID']
			limit = 100

			if 'last_id' in session:
				last_id = session['last_id']
			else:
				last_id = 0

			#una fila tiene
			#t.status, t.favorite_count, t.retweet_count, t.is_retweet, t.media_url, u.screen_name, t.id
			rows = self.consultas.getTweetsAsincSearc(search_id, last_id, limit)
			if rows == False:
				retorno = {"status":"false"}
				return json.dumps(retorno)


			#puede ser que aun no se hayan recibido los tweets o que no queden tweets por mostrar
			#por lo que lo comprobamos
			len_rows = len(rows)
			if len_rows == 0:
				if self.consultas.isFinishedAsincSearch(search_id) == True:
					retorno = {"status":"false", "tweets" : []}
					session.pop('last_id', None)
					session.pop('searchID', None)
				else:
					retorno = {"status":"true", "tweets" : []}
			else:
				#se recorren las filas para generar un json fantastico
				retorno = {"status":"true", "tweets" : []}
				for row in rows:
					tweet = {}
					tweet['text'] = str(row[0])
					tweet['fav'] = str(row[1])
					tweet['rt'] = str(row[2])
					tweet['is_rt'] = str(row[3])
					tweet['media'] = str(row[4])
					tweet['tuser'] = str(row[5])

					retorno['tweets'].append(tweet)

				session['last_id'] = rows[len_rows - 1][6]

			
			return json.dumps(retorno)
		else:
			retorno = {"status":"false"}
			return json.dumps(retorno)
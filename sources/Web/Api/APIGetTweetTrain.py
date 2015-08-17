from flask import Flask, session, request, redirect
from DBbridge.ConsultasWeb import ConsultasWeb
import json
from random import randint

class APIGetTweetTrain(object):
	"""docstring for APIGetTweetTrain"""
	def __init__(self):
		super(APIGetTweetTrain, self).__init__()
		self.consultas = ConsultasWeb()

	def toString(self):
		isAleat = request.form['aleat']
		search = request.form['search']
		#lista de entrenamiento
		lista_id = request.form['lista']
		
		if isAleat is None or search is None or lista_id is None:
			retorno = {"status":"false"}
			return json.dumps(retorno)
		elif isAleat is '' or search is '' or lista_id is '':
			retorno = {"status":"false"}
			return json.dumps(retorno)

		if isAleat == "true":
			isAleat = True
		else:
			isAleat = False

		#se debe comprobar que es suya y valida, la lista
		if self.consultas.isListasEntrenamientoFromUser(session['user_id'], lista_id) == False:
			retorno = {"status":"false"}
			return json.dumps(retorno)



		#deprecated solo SQL, se mueve el funcionamineto a la base de datos
		#lista_keywords = search.replace(", ", ",").split(",")

		limit = 1
		if isAleat == True:
			limit = 1000

		rows = self.consultas.getIDsTweetsTrain(search, limit, lista_id)
		if rows == False or len(rows) == 0:
				retorno = {"status":"false"}
				return json.dumps(retorno)

		identificador = 0
		if isAleat == True:
			identificador = randint(0,len(rows)-1)

		
		tweetRow = self.consultas.getTweetByIDLarge(rows[identificador][0])
		if tweetRow == False:
				retorno = {"status":"false"}
				return json.dumps(retorno)

		session['tweet_train_id'] = rows[identificador][0]

		retorno = {"status":"true", "tweets" : []}

		tweet = {}
		tweet['text'] = tweetRow[0]
		tweet['fav'] = str(tweetRow[1])
		tweet['rt'] = str(tweetRow[2])
		tweet['is_rt'] = str(tweetRow[3])
		tweet['media'] = str(tweetRow[4])
		tweet['tuser'] = str(tweetRow[5])

		retorno['tweets'].append(tweet)

		return json.dumps(retorno)



		
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
		if isAleat == "true":
			isAleat = True
		else:
			isAleat = False
		search = request.form['search']


		lista_keywords = search.replace(", ", ",").split(",")

		limit = 1
		if isAleat == True:
			limit = 1000

		rows = self.consultas.getIDsTweetsTrain(lista_keywords, limit)
		if rows == False or len(rows) == 0:
				retorno = {"status":"false"}
				return json.dumps(retorno)

		identificador = 0
		if isAleat == True:
			identificador = randint(0,len(rows)-1)

		session['tweet_train_id'] = rows[identificador][0]
		tweetRow = self.consultas.getTweetIDLarge(rows[identificador][0])
		if tweetRow == False:
				retorno = {"status":"false"}
				return json.dumps(retorno)

		retorno = {"status":"true", "tweets" : []}

		tweet = {}
		tweet['text'] = str(tweetRow[0])
		tweet['fav'] = str(tweetRow[1])
		tweet['rt'] = str(tweetRow[2])
		tweet['is_rt'] = str(tweetRow[3])
		tweet['media'] = str(tweetRow[4])
		tweet['tuser'] = str(tweetRow[5])

		retorno['tweets'].append(tweet)

		return json.dumps(retorno)



		
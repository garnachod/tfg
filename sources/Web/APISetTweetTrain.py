from flask import Flask, session, request, redirect
from DBbridge.ConsultasWeb import ConsultasWeb
import json

class APISetTweetTrain(object):
	"""docstring for APISetTweetTrain"""
	def __init__(self):
		super(APISetTweetTrain, self).__init__()
		self.consultas = ConsultasWeb()
	
	def toString(self):
		vote = request.form['vote']
		t_id = session['tweet_train_id']

		if vote is None or t_id is None:
			retorno = {"status":"false"}
			return json.dumps(retorno)

		if vote == "relevante":
			self.consultas.setTweetTrainID(t_id, "relevante");
		elif vote == "no_relevante":
			self.consultas.setTweetTrainID(t_id, "no_relevante");
		elif vote == "no_usar":
			self.consultas.setTweetTrainID(t_id, "no_usar");
		else:
			retorno = {"status":"false"}
			return json.dumps(retorno)

		retorno = {"status":"true"}
		return json.dumps(retorno)

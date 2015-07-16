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
		lista_id = request.form['lista']
		
		if vote is None or t_id is None:
			retorno = {"status":"false"}
			return json.dumps(retorno)
		elif vote is '' or t_id is '':
			retorno = {"status":"false"}
			return json.dumps(retorno)

		if vote == "relevante":
			self.consultas.setTweetTrainID(t_id, "relevante", lista_id);
		elif vote == "no_relevante":
			self.consultas.setTweetTrainID(t_id, "no_relevante", lista_id);
		elif vote == "no_usar":
			self.consultas.setTweetTrainID(t_id, "no_usar", lista_id);
		else:
			retorno = {"status":"false"}
			return json.dumps(retorno)

		retorno = {"status":"true"}
		return json.dumps(retorno)

	def toStringChange(self):
		identificador = request.form['change']


		if identificador is None:
			retorno = {"status":"false"}
			return json.dumps(retorno)
		elif identificador is '':
			retorno = {"status":"false"}
			return json.dumps(retorno)

		clase = self.consultas.getClaseTrainID(identificador)
		if clase == False:
			retorno = {"status":"false"}
			return json.dumps(retorno)

		clase = clase[0]
		if clase == "no_relevante":
			print identificador
			self.consultas.changeClaseTweet(identificador, "relevante")
		else:
			self.consultas.changeClaseTweet(identificador, "no_relevante")

		retorno = {"status":"true", "identificador":identificador}
		return json.dumps(retorno)
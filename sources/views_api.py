# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Web.Api.APIGetTweetTrain import APIGetTweetTrain 
from Web.Api.APISetTweetTrain import APISetTweetTrain
from Web.Api.APIGetSearchTweetsDB import APIGetSearchTweetsDB
from sources import app,consultasWeb


##API
getTweetTrain_web = APIGetTweetTrain()
setTweetTrain_web = APISetTweetTrain()
getTweetsSearchSinc = APIGetSearchTweetsDB()
##Fin de API
#busqueda
@app.route('/busqueda_sinc', methods=['GET', 'POST'])
def busquedaSinc():
	if request.method == 'POST':
		return getTweetsSearchSinc.toString()
	else:
		try:
			return getTweetsSearchSinc.toString()
		except Exception, e:
			print e
			return 'ERR'
#entrenamiento
@app.route('/busqueda_tweet_train' , methods=['GET', 'POST'])
def buscaTweetTrain():
	if 'username' in session:
		if request.method == 'POST':
			return getTweetTrain_web.toString()
		else:
			return redirect('/err?code=2')
	else:
		return 'err'

@app.route('/set_tweet_train' , methods=['GET', 'POST'])
def setTweetTrain():
	if 'username' in session:
		if request.method == 'POST':
			return setTweetTrain_web.toString()
		else:
			return redirect('/err?code=2')
	else:
		return 'err'
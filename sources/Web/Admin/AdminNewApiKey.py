# -*- coding: utf-8 -*-
from flask import Flask, request
from twython import Twython, TwythonError, TwythonAuthError, TwythonRateLimitError
from DBbridge.ConsultasWeb import ConsultasWeb
#from DBbridge.ConsultasWeb import ConsultasWeb
import hashlib


class AdminNewApiKey():
	def __init__(self):
		self.consultas = ConsultasWeb()

	def add(self):
		apik = request.form['apik']
		apiks = request.form['apiks']
		acstoken = request.form['acstoken']
		acstokens = request.form['acstokens']

		if apik is None or apiks is None or acstoken is None or acstokens is None:
			print "err"
			return False
		elif apik is '' or apiks is '' or acstoken is '' or acstokens is '':
			print "err"
			return False
		else:
			try:
				twitter = Twython(apik, apiks, oauth_version=2)
				oauth = twitter.obtain_access_token()

				return self.consultas.insertNewApiKey(apik, apiks, acstoken, acstokens, oauth)
			except Exception, e:
				print str(e)
				return False
# -*- coding: utf-8 -*-
class Tweet(object):
	"""docstring for Tweet"""
	@staticmethod
	def imprimeTweett(tweet, relevancia=True):
		palabras = tweet[0].split(" ")
		cadena = '<div class="delimitador"></div>'
		if relevancia == True:
			cadena += Tweet.imprimeTweettRelevancia(tweet)
		else:
			cadena += '<div class="tweet">'

		cadena += Tweet.imprimeTweettUsrIMG()

		cadena += '<div class="cont-tweet">'
		cadena += Tweet.imprimeTweetUsr(tweet)
		cadena += '<div class="tweet-text">'
		for palabra in palabras:
			#es un link
			if "http://" in palabra or "https://" in palabra:
				cadena += '<a class="link" href="'+ palabra+'" target="_blank">'+palabra+'</a> '
			#es un usuario de twitter
			elif "@" in palabra:
				user = Tweet.limpiaTwitterUser(palabra)
				cadena += '<a class="user" href="https://twitter.com/'+ user +'" target="_blank">'+palabra+'</a> '
			#cualquier otra cosa			
			else:
				cadena += palabra + " "

		cadena += '</div>'
		cadena += '<div class="contenedor-rf">'
		cadena += '<span class="fav-count">'
		cadena += str(tweet[1])
		cadena += '</span>'
		cadena += '<span class="retweet-count">'
		cadena += str(tweet[2])
		cadena += '</span>'
		cadena += '</div>'
		#tiene algún tipo de objeto multimedia
		if tweet[4] != '':
			cadena += Tweet.imprimeTweettMedia(tweet[4])
			
		cadena += '</div>'

		

		cadena += '</div>'
		return cadena
	@staticmethod
	def imprimeTweettUsrIMG():
		cadena = '<div class="cont-user-img">'
		cadena += '<img src="static/img/tweetuser.png">'
		cadena += '</div>'
		return cadena

	@staticmethod
	def imprimeTweetUsr(tweet):
		cadena = '<div class="cont-usr">'
		cadena += '<a href="https://twitter.com/'+tweet[5]+'" target="_blank">@'+tweet[5]+ '</a>'
		cadena += '</div>'
		return cadena

	@staticmethod
	def imprimeTweettRelevancia(tweet):
		imOrRt = ""

		if tweet[3] == True:
			imOrRt = "rt"
		else:
			imOrRt = "im"

		relevancia = (float(tweet[1]) * 0.75) + (float(tweet[2]) * 1.5)
		if relevancia == 0:
			return '<div class="tweet '+imOrRt+'1">'
		elif relevancia < 100:
			return '<div class="tweet '+imOrRt+'2">'
		elif relevancia < 750:
			return '<div class="tweet '+imOrRt+'3">'
		elif relevancia < 5000:
			return '<div class="tweet '+imOrRt+'4">'
		else:
			return '<div class="tweet '+imOrRt+'5">'

	@staticmethod
	def imprimeTweettMedia(media):
		cadena = ''

		if '.jpg' in media or '.png' in media:
			cadena += '<div class="cont-multi">'
			cadena += '<a href="'+ media +'" target="_blank">'
			cadena += '<div class="img_busqueda" style="background-image: url(\''
			#http://pbs.twimg.com/media/BziK-yaIIAA1uW2.jpg
			cadena += media 
			cadena += '\');">'
		
			cadena += '</div>'
			cadena += '</a>'
			cadena += '</div>'

		return cadena

	@staticmethod
	def limpiaTwitterUser(user):
		cadena = ''

		for caracter in user:
			if caracter != '@' and caracter != ':':
				cadena += caracter

		return cadena
		
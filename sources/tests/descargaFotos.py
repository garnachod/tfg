# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasWeb import ConsultasWeb
import urllib
import json

if __name__ == '__main__':
	user = "@garnachod"

	consultas = ConsultasWeb()
	tweets = consultas.getTweetsUsuario(user)

	for tweet in tweets:
		if tweet.media_urls is not None:
			#print tweet.media_urls["photo_1"]
			urllib.urlretrieve (tweet.media_urls["photo_1"], "/media/dani/data/fotos/"+tweet.media_urls["photo_1"].replace(":", "").replace("/", "_"))
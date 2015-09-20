# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
from DBbridge.EscritorTweetsCassandra import EscritorTweetsCassandra
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
import datetime
from time import time, sleep

if __name__ == '__main__':
	escritorList = []

	escritorList.append(EscritorTweetsCassandra(-1))
	recolector = RecolectorTweetsUser(escritorList)

	testCompleto = True
	if testCompleto:
		arrayUsuarios = ["LuthFlanagan", "i_3g0", "Dacosta_R", "Cobb314", "CiberPoliES", "MBia9", "rigugi", "SonyDeckard", "BridgesRalph", "iN0r1", "mrufian", "pedaguitu"]
		tiempo_total = 10 * 60 
		for i, usuario in enumerate(arrayUsuarios):
			print usuario
			recolector.recolecta(usuario)
			sleep(tiempo_total/len(arrayUsuarios))
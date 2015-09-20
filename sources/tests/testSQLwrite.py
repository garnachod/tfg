# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.EscritorTweets import EscritorTweets
from SocialAPI.TwitterAPI.RecolectorTweetsUser import RecolectorTweetsUser
from DBbridge.Cassandra.ConexionCassandra import ConexionCassandra

if __name__ == '__main__':
	escritorList = []

	escritorList.append(EscritorTweets(-1))
	recolector = RecolectorTweetsUser(escritorList)
	
	recolector.recolecta("garnachod")
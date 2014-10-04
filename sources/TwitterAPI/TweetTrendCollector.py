# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import twitter
import datetime
import threading
import time

from getAuthorizations import GetAuthorizations
from placefinder import geocode



# Similar a StreamCollector, para monitoriza cada minuto los trends topics de la región especificada

# Encargado de recoger periódicamente los trends topics de una región
# En principio España o el mundo, se pueden especificar otras regiones pero no hay seguridad de entender
# Se inicia con start y es un hilo independiente.
# get_trend_topics retorna lista de trend topics (strings)
# stop_querying detiene el hilo
# query_now obliga a refrescar los trends actuales (sin esperar los 5 minutos default)

class TweetTrendCollector(threading.Thread):
    def __init__(self, zone='Spain'):
        threading.Thread.__init__(self)
        self.place_id = geocode(zone)
        self.exit = False # configurable externamente
        self.pace = 300 # en segundos, configurable externamente
        self.stop = threading.Event()
        self.authorizator = GetAuthorizations()

    def run(self):
        self.authorizator.load_twitter_token()
        API_key, API_secret, access_token, access_token_secret = self.authorizator.get_twitter_secret()
        auth = twitter.oauth.OAuth(access_token, access_token_secret, API_key, API_secret)
        self.twitter_api = twitter.Twitter(auth=auth)
        while not self.exit:
            self.last_query = datetime.datetime.now().minute
            self.topics = self.internal_get_trends()
            #TODO: guardarlo en base de datos?
            self.stop.wait(self.pace)

    def query_now(self):
        self.stop.set()

    def stop_querying(self):
        self.stop.set()
        self.exit = True

    def get_trend_topics(self):
        return self.topics

    def internal_get_trends(self):
        trends = self.twitter_api.trends.place(_id=self.place_id)
        self.authorizator.add_query_to_key()
        trends_set = [trend['name'] for trend in trends[0]['trends']]
        return trends_set

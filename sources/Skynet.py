# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import time
from datetime import date, timedelta
import sys
import Utiles.debug
from threading import Thread
 
from TwitterAPI.TweetTrendCollector import TweetTrendCollector
from TwitterAPI.TweetTrendStreamCollector import TweetTrendStreamCollector

from Writers.consoleTweetRecorder import ConsoleTweetRecorder
from Writers.dbTweetRecorder import DbTweetRecorder
from DBbridge.PostgresLogWriter import PostgresLogWriter

from TwitterAPI.TwythonTweetCollector import TwythonTweetCollector
from DBbridge.PostgresReader import PostgresReader
#from TwitterAPI.getAuthorizations import load_twitter_tokens

# esta clase es el cerebro de la información extraida de Twitter.
# Toda petición de información debe pasar por aquí, para ver si
# ya está en al BBDD o si se debe buscar en Twiiter

class Skynet():

    def __init__(self, id_app_user=0):
        self.tweet_recorder = DbTweetRecorder()
        self.logger = PostgresLogWriter()
        self.tweet_collector = TwythonTweetCollector(self.tweet_recorder, self.logger)
        self.data_base_reader = PostgresReader()
        self.status = 'Esperando consultas'
        self.id_app_user = id_app_user

    def research_user(self, screen_name, searchID):
        return self.tweet_collector.get_tweets_user(screen_name, self.id_app_user, searchID)

    def init_trending_collection(self):
        self.spain_trend_collector = TweetTrendCollector('Spain')
        self.spain_trend_collector.start()
        self.spain_tweet_trend_stream = TweetTrendStreamCollector([ConsoleTweetRecorder()], self.spain_trend_collector)
        self.spain_tweet_trend_stream.start()

    def get_current_trends(self, place='Spain'):
        """
        place = {'Spain', 'World', ..}. Si es uno distinto a estos dos, se buscará sin garantias
        """
        if place == 'Spain':
            return self.spain_trend_collector.get_trend_topics()

    def research_keywords_between_dates(self, list_of_keywords,searchID, start_date, end_date):
        """
        Buscar y elaborar estadísticas sobre un tema, representado como lista de términos.
        :param list_of_keywords:lista de palabras claves a buscar. Si no tiene valor usar función con menos parámetros
        :param start_date nombre autoexplicativos. Si no tiene valor usar función con menos parámetros.
        :param end_date idem anterior. Si no tiene valor usar función con menos parámetros.
        :return:
        """

        resultado = dict()
        # Primer paso, actualizamos la info que tenemos en la base de datos
        self.status = 'Consultando a Twitter'
        resultado['number_new_tweets'] = self.tweet_collector.search_keywords(self.id_app_user, list_of_keywords, searchID)
        # Segundo paso: contar en la BD todos los tweets sobre los temas

        self.status = 'Analizando Base de Datos'
        for word in list_of_keywords:
            resultado[word] = dict()
            resultado[word]['num_tweets'] = self.data_base_reader.num_tweets_topic(word, start_date, end_date)
            resultado[word]['num_retweets'] = self.data_base_reader.num_retweets_topic(word, start_date, end_date)
            resultado[word]['autores'] = self.data_base_reader.autores_topic(word, start_date, end_date, 2, 100)
            resultado[word]['transmisores'] = self.data_base_reader.transmisores_topic(word, start_date, end_date, 2, 100)
            resultado[word]['mencionados'] = self.data_base_reader.mencionados_topic(word, start_date, end_date, 100)

        self.status = 'Esperando consultas'
        return resultado

    def advanced_research_keywords_dates(self, list_of_keywords,searchID, start_date, end_date):
        resultado = self.research_keywords_between_dates(list_of_keywords,searchID,start_date, end_date)
        self.status = 'Analizando Base de Datos'
        for word in list_of_keywords:
            resultado[word]['cloud_tag'] = self.data_base_reader.word_frequency_topic(word, start_date, end_date, 20)
            #todo: resultado[word]['procedencia']
            resultado[word]['time_line'] = self.data_base_reader.time_line_topic(word, 'day')
            #todo: resultado[word]['cloud_tag_time_line'] = "palabras usadas en distintos momentos"
            resultado[word]['top_followers'] = self.data_base_reader.most_followers_topic(word, start_date, end_date)
            resultado[word]['most_success'] = self.data_base_reader.most_success(word, start_date, end_date)
            resultado[word]['scope'] = self.data_base_reader.scope_topic(word, start_date, end_date)

        self.status = 'Esperando consultas'
        return resultado

    def advanced_research_keywords(self, list_of_keywords, searchID):
        """
        Método accesorio para facilitar parámetros default. La búsqueda se hará en los últimos 30 días
        :param list_of_keywords: lista de palabras claves a buscar
        :return:
        """
        return self.advanced_research_keywords_dates(list_of_keywords, searchID,(date.today() - timedelta(30)).isoformat(),
                                                     date.today().isoformat())

    def research_keywords(self, list_of_keywords, searchID):
        """
        Método accesorio para facilitar parámetros default. La búsqueda se hará en los últimos 30 días
        :param list_of_keywords: lista de palabras claves a buscar
        :return:
        """
        return self.research_keywords_between_dates(list_of_keywords,searchID, (date.today() - timedelta(30)).isoformat(),
                                                    date.today().isoformat())

    #########################
    #
    # Para uso asíncrono
    #
    ########################

    def research_keywords_in_background(self, list_of_keywords):
        """
        Idem research_keywords, but not blocking
        :param list_of_keywords:
        :return:
        """
        t = Thread(target='research_keywords', args=(list_of_keywords,))
        t.start()

    def get_number_new_tweets(self):
        return self.tweet_collector.newtweets_count


    def stop(self):
        self.spain_trend_collector.stop_querying()
        self.spain_tweet_trend_stream.stop_collecting()

    def retrieve_user(self, screen_name):
        """
        El objetivo es recuperar los tweets de un usuario.
        Devuelve el número de tweets recuperados (pueden no ser todos los del usuario y es posible que alguno ya
        estuviera en la base de datos.
        La comprobación del último tweet recuperado la hace el collector
        """
        resultado = self.tweet_collector.get_tweets_user(screen_name, self.id_app_user)
        if resultado[0] is not "OK":
            return resultado[0]
        new_tweets = resultado[1]


if __name__ == '__main__':
    #load_twitter_tokens()
    brain = Skynet()
    if sys.argv[1] == 'usuario':
        busqueda = brain.research_user(sys.argv[2])
    elif sys.argv[1] == 'topics':
        '''
        busqueda = brain.research_keywords(sys.argv[2].replace(" ", "").split(","))
        '''
    elif sys.argv[1] == 'advanced':
        '''
        busqueda = brain.advanced_research_keywords(sys.argv[2].replace(" ", "").split(","))
        '''
    else:
        '''
        brain.init_trending_collection()
        time.sleep(10)
        brain.get_current_trends('Spain')
        time.sleep(20)
        brain.stop()
        '''
    #print busqueda['number_new_tweets']
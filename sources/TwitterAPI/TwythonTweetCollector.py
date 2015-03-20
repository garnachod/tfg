# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

from twython import Twython, TwythonError, TwythonAuthError, TwythonRateLimitError
from getAuthorizations import GetAuthorizations

from threading import Thread


class TwythonTweetCollector():

    queries_for_window = 40

    def __init__(self, recorder, logger):
        self.recorder = recorder
        self.logger = logger
        self.twitter = None
        self.authorizator = GetAuthorizations()
        self.create_access()
        

    def create_access(self):
        self.authorizator.load_twitter_token()
        api_key, access_token = self.authorizator.get_twython_token()
        #api_key, access_token = get_twython_token()
        #api_key, access_token = get_twython_token_auth()
        #print api_key+" "+app_secret+" "+access_token+" "+access_token_secret
        #self.twitter = Twython(api_key, app_secret, access_token, access_token_secret)
        self.twitter = Twython(api_key, access_token=access_token)
        #self.twitter = Twython(api_key, access_token, oauth_version=2)
        #ACCESS_TOKEN = self.twitter.obtain_access_token()
        #print ACCESS_TOKEN
        #self.twitter.verify_credentials()


    def get_tweets_user(self, screen_name, id_app_user, searchID):
        """
        Get all tweets from a given user. It records the search on the DB (so it does not duplicate searches)
        Retorna tupla con código de resultado = {ok, rate_limit, private_user, other},
            número de consultas hechas a twitter y numero de new_tweets descargados en esas consultas
            [codigo, num1, num2]
        """
        self.logger.insert_log(id_app_user, "search_user", "twitter user:%s; app user:%s" % (screen_name, id_app_user))
        last_tweet_collected = self.logger.last_sequential_tweet_from_user(screen_name)


        try:
            #LIMITE DE API, si se da en este momento todas las apik están llenas
            if self.authorizator.is_limit_api():
                return 0
            user_timeline = self.twitter.get_user_timeline(screen_name=screen_name, min_id=last_tweet_collected)
            self.authorizator.add_query_to_key()
        except TwythonAuthError as e:
            self.logger.insert_log(id_app_user, "private_user",
                                   "El usuario %s requiere permisos para acceder a sus tweets" %
                                   (screen_name,), e.message)
            return ["private_user", 1, 0]
        except TwythonRateLimitError as e:
            self.logger.insert_log(id_app_user, "rate_limit", "Límite app alcanzado. API KEY: %s" % (self.API_key,),
                                   e.message)
            return ["rate_limit", 1, 0]
        except TwythonError as e:
            self.logger.insert_log(id_app_user, "other", "Error no definido", e.message)
            return ["other", 1, 0]

        self.logger.record_last_sequential_tweet_from_user(screen_name, user_timeline[0]['id_str'])
        newtweets_count = len(user_timeline)
        queries_count = 1

        for tweet in user_timeline:
            self.recorder.record_tweet(tweet, searchID)

        # Count could be less than 200, see: https://dev.twitter.com/discussions/7513
        ultimo_tweet_recolectado = user_timeline[len(user_timeline)-1]['id']
        while len(user_timeline) != 0: #TODO: tal vez evitar que se itere demasiado? Cortar antes de que de error?
            try:
                queries_count += 1
                if queries_count > 20:
                    return newtweets_count

                print 'max_id = '
                print user_timeline[len(user_timeline)-1]['id']
                #print 'min_id = ' + last_tweet_collected
                print 'min_id = '
                print last_tweet_collected

                if user_timeline[len(user_timeline)-1]['id'] > last_tweet_collected:
                    #LIMITE DE API
                    if self.authorizator.is_limit_api():
                        return len(user_timeline)

                    user_timeline = self.twitter.get_user_timeline(screen_name=screen_name,
                                                               max_id=user_timeline[len(user_timeline)-1]['id'],
                                                               min_id=last_tweet_collected)
                    
                    if user_timeline[len(user_timeline)-1]['id'] == ultimo_tweet_recolectado:
                        return newtweets_count
                    else:
                        ultimo_tweet_recolectado = user_timeline[len(user_timeline)-1]['id']

                    self.authorizator.add_query_to_key()
                else:
                    return newtweets_count
            # except TwythonAuthError as e:
            #     Utiles.debug.print_debug("El usuario %s requiere permisos para acceder a sus tweets" % (screen_name,))
            #     self.logger.insert_log(id_app_user, "private_user",
            #                            "El usuario %s requiere permisos para acceder a sus tweets" %
            #                            (screen_name,), e.message)
            #     return "private_user"
            except TwythonRateLimitError as e:
                self.logger.insert_log(id_app_user, "rate_limit", "Límite alcanzado app. API KEY: %s" % (self.API_key,),
                                       e.message)
                self.logger.insert_log(id_app_user, "search_user_result",
                                       "Tweets de usuario %s encontrados antes del error: %s" %
                                       (screen_name, newtweets_count))
                return ["rate_limit", queries_count, newtweets_count]
            except TwythonError as e:
                self.logger.insert_log(id_app_user, "other", "Error no definido", e.message)
                return ["other", queries_count, newtweets_count]

            for tweet in user_timeline:
                self.recorder.record_tweet(tweet, searchID)
                newtweets_count += 1
        #fuera del while
        self.logger.insert_log(id_app_user, "search_user_result",
                               "Tweets de usuario %s encontrados: %s" % (screen_name, newtweets_count))
        return newtweets_count

    def search_keywords_in_background(self, keyword_list):
        t = Thread(target='search_keywords', args=(keyword_list,))
        t.start()
        return t

    def search_keywords(self, id_app_user, keyword_list, searchID):
        """
        Get all tweets containing at least one word of the list (keyword_list)
        Retorna tupla con código de resultado = {ok, rate_limit, private_user, other},
            número de consultas hechas a twitter y numero de new_tweets descargados en esas consultas
            [codigo, num1, num2]
        """
        # ver doc https://dev.twitter.com/docs/api/1.1/get/search/tweets
        # límite actual: 450 queries cada 15 mins.

        # La idea es no repetir búsquedas ya hechas
        # Necesito comprobar si hay búsqueda para cada término. Si la hay, se busca sólo a partir
        # del último tweet encontrado en la anterior búsqueda
        last_tweet_collected_list = self.logger.last_sequential_tweet_for_search(keyword_list)
        #diccionario con el último tweet investigado para cada término.

        self.logger.insert_log(id_app_user, "search_keywords", "Lista de keywords: %s" % (keyword_list,))

        last_tweet_ids = last_tweet_collected_list.values()
        self.newtweets_count = 0
        first_search = True


        while keyword_list:
            try:
                next_min_id = max(last_tweet_ids)
                query_string = keyword_list[0]
                for keyword in keyword_list[1:]:
                    query_string += ' OR ' + keyword
                number, new_last_tweet, last_id = self._int_search_keywords(query_string, next_min_id, searchID)

                #se ha llegado al limite de la api, no forzamos más
                if number == 0:
                    return self.newtweets_count

                self.newtweets_count += number
                if first_search and new_last_tweet > '0':
                    first_search = False
                    self.logger.record_last_sequential_tweet_for_search(keyword_list, new_last_tweet)
                keyword_list = [key for key in keyword_list if last_tweet_collected_list[key] < next_min_id]
                last_tweet_ids = [id for id in last_tweet_ids if id < next_min_id]
            except TwythonRateLimitError as e:
                return "rate_limit"
            except TwythonError as e:
                self.logger.insert_log(id_app_user, "other", "TwythonError error({0}): {1}".format(e.message, e.args))
                return "other"

        #self.logger.insert_log("Total tweets con lista de keywords %s: %s" % (keyword_list, self.newtweets_count))
        return self.newtweets_count

    def _int_search_keywords(self, keywords_string, since_id, searchID):
        """

        :param keywords_string: string con los términos de búsqueda
        :param since_id: índice del último tweet que debe ser leido (más viejo)
        :return: tupla con número de tweets recuperados, número de consultas a Twitter y último tweet accedido
        """

        #LIMITE DE API, si se da en este momento todas las apik están llenas
        if self.authorizator.is_limit_api():
            return 0, 0, 0

        search = self.twitter.search(q=keywords_string, since_id=since_id, count='100')
        self.authorizator.add_query_to_key()
        newtweets_count = len(search['statuses'])
        queries_count = 1


        if len(search['statuses']) > 0:  # al menos uno encontró
            last_id = search['statuses'][0]['id_str']
        else:
            return newtweets_count, queries_count, '0'

        for result in search['statuses']:
            self.recorder.record_tweet(result, searchID)

        while len(search['statuses']) != 0 and queries_count < 20:
            #es obvio que no se debe dejar que de una sola consulta se agoten los queries
            #TODO el problema es que pueden quedar tweets sin descargar que *NUNCA* serán descargados.
            #TODO dejar para proceso background (despues de 15mins?) intentar descargar mas tweets
            max_id2 = search['statuses'][len(search['statuses'])-1]['id']-1
            #LIMITE DE API, si se da en este momento todas las apik están llenas
            if self.authorizator.is_limit_api():
                return 0, 0, 0
            #no ha llegado al limite
            search = self.twitter.search(q=keywords_string, max_id=max_id2, since_id=since_id, count='100')
            self.authorizator.add_query_to_key()
            queries_count += 1
            
            if 'statuses' not in search:
                break
            for tweet in search['statuses']:
                self.recorder.record_tweet(tweet, searchID)
                newtweets_count += 1

            # if newtweets_count > 200:
            #     return newtweets_count, last_id
        return newtweets_count, queries_count, last_id
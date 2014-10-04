# -*- coding: iso-8859-15 -*-

import tweepy
import Utiles

from getAuthorizations import get_tweepy_api_auth


# Clase que se dedica a recoger tweets.
# Parámetros: filtros de búsqueda (tags, users, locations)
# número máximo de tweets antes de terminar
# tiempo máximo de ejecución antes de terminar
# nombre del fichero donde escribir resultados (prefijo)
# número de aplicación (usado para las autorizaciones Twitter)
# número de tweets x fichero

search_window = 7  # dias


class _TweepyTweetCollector():
    def __init__(self, recorder):
        self.recorder = recorder
        #instanciable desde fuera
        self.debug = False
        self.tags = []
        self.usuarios = []
        self.lugares = []
        self.num_app = 2
        #fin instanciables

        auth = get_tweepy_api_auth(self.num_app)
        #self.twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
        self.twitter_api = tweepy.API(auth)

    def get_tweets_user(self, screen_name, newer_than=0):
        """
        Si newer_than > 0, se supone que los tweets más antiguos de este usuario ya se han recuperado y solo pedimos
        los más nuevos. Sino, pedimos todos.
        Retorna el id interno del último tweet recogido.
        """
        try:
            if newer_than > 0:
                cursor = tweepy.Cursor(self.twitter_api.user_timeline, id=screen_name, since_id=newer_than)
            else:
                cursor = tweepy.Cursor(self.twitter_api.user_timeline, id=screen_name)

            for tweet in cursor.items():
                #print tweet.text, tweet.retweet
                last = self.recorder.record_tweet(tweet)

        except tweepy.TweepError as e:
            if e.message == "Not authorized.":
                Utiles.debug.print_debug("El usuario %s requiere permisos para acceder a sus tweets" % (screen_name,))
                Utiles.debug.write_log("El usuario %s requiere permisos para acceder a sus tweets" % (screen_name,))
            else:
                Utiles.debug.print_debug("Twitter error({0}): {1}".format(e.message, e.args), True)

        else:
            return last

if __name__ == "__main__":
    Utiles.debug.init_log_file("logfile.txt")
    tc = _TweepyTweetCollector()
    tc.getTweetsUser('@a_ortigosa')
    Utiles.debug.close_log_file()
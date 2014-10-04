# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import threading
import twitter
from getAuthorizations import get_twitter_secret
from Utiles.debug import write_log, print_debug

# Clase que se dedica a recoger tweets.
# Parámetros: filtros de búsqueda (tags, users, locations)
# número máximo de tweets antes de terminar
# tiempo máximo de ejecución antes de terminar
# número de aplicación (usado para las autorizaciones Twitter)

#recorders es una colección de instancias de una sublclase de Writers.TweetRecorder
# Puede ser vacía

lugares = '-9,36,4,43.5'
# '-4, 40, 3.3, 41' #Madrid
# '-9, 36, 4, 43.5' #Espana

class TweetStreamCollector(threading.Thread):
    def __init__(self, recorder):
        threading.Thread.__init__(self)
        self.recorder = recorder
        #instanciable desde fuera
        self.debug = False
        self.tags = ''  # 'term1, term2'
        self.follows = '' # https://dev.twitter.com/docs/streaming-apis/parameters#follow
        self.locations = '-9,36,4,43.5'  # España. https://dev.twitter.com/docs/streaming-apis/parameters#locations
        self.app_num = 2
        self.seguir = True


    def run(self):
        """
        Aunque se pueden especificar lugares, usuarios y tags independientemente, como hace "o" de los
        términos el comportamiento se debe implementar usando tres streams distintos.
        Si tags <> '', usa tags. Sino, si follows <> '' usa follows. Sino, usa locations (hay que usar alguna)
        """
        API_key, API_secret, access_token, access_token_secret = get_twitter_secret(self.app_num)
        auth = twitter.oauth.OAuth(access_token, access_token_secret, API_key, API_secret)
        twitter_stream_api = twitter.TwitterStream(auth=auth)
        write_log("stream_open", "Track=%s; follows=%s; locations=%s" % (self.tags, self.follows, self.locations))
        if not self.tags == '':
            stream = twitter_stream_api.statuses.filter(track=self.tags)
        elif not self.follows == '':
            stream = twitter_stream_api.statuses.filter(follows=self.follows)
        else:
            stream = twitter_stream_api.statuses.filter(locations=self.locations)

        for tweet in stream:
            self.recorder.record_tweet(tweet)
            print_debug(tweet['text'])
            if not self.seguir:
                break


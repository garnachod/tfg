# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import threading
import twitter
from getAuthorizations import GetAuthorizations

# Las instancias de esta clase se dedican a recoger los tweets de los trend topics de una región determinada
# (determinada por el trend provider)

class TweetTrendStreamCollector(threading.Thread):
    # recorders es una colección de instancias de una sublclase de Writers.TweetRecorder. Puede ser vacía
    # trend_provider será una instancia de TweetTrendCollector
    def __init__(self, recorders, trend_provider):
        threading.Thread.__init__(self)
        self.app_num = 1
        self.seguir = True
        self.authorizator = GetAuthorizations()
        self.trend_provider = trend_provider


    def run(self):
        self.authorizator.load_twitter_token()
        API_key, API_secret, access_token, access_token_secret = self.authorizator.get_twitter_secret(self.app_num)
        auth = twitter.oauth.OAuth(access_token, access_token_secret, API_key, API_secret)
        twitter_stream_api = twitter.TwitterStream(auth=auth)
        stream = twitter_stream_api.statuses.filter(track=self.trend_provider.get_trend_topics())
        for tweet in stream:
             for r in self.recorders:
                 r.record_tweet(tweet)
             if not self.seguir:
                 break

    def stop_collecting(self):
        self.seguir = False
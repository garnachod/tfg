# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

# La idea es que si quiero usar más de un writter, los conpongo con este
# (Composite design pattern)

class CompositeTweetRecorder():
    def __init__(self, lista_writters=[]):
        self.writters = lista_writters

    def record_tweet(self, tweet):
        for w in self.writters:
            w.record_tweet(tweet)


    def record_json_tweet(self, tweet):
        for w in self.writters:
            w.record_json_tweet(tweet)

    def reset(self):
        for w in self.writters:
            w.reset()

    def addWritter(self, writter):
        self.writters.append(writter)

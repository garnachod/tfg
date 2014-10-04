# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import Utiles.debug
from TwitterAPI._TweepyTweetCollector import _TweepyTweetCollector
from TwitterAPI.TweetCollector import TweetCollector
from TwitterAPI.TweetStreamCollector import TweetStreamCollector
from TwitterAPI.TwythonTweetCollector import TwythonTweetCollector

from DBbridge.PostgresWriter import PostgresWriter
from DBbridge.PostgresReader import PostgresReader
from JasonProcessors.TweetFileReader import TweetFileReader
from Writers.dbTweetRecorder import DbTweetRecorder
from Skynet import Skynet

import time

filename = '../data/test.json'


def prueba_stream():
    Utiles.debug.open_log_file("prueba.log")
    tr = DbTweetRecorder()
    tc = TweetStreamCollector(tr)
    tc.start()
    time.sleep(10)
    tc.seguir = False
    Utiles.debug.close_log_file()

if __name__ == "__main__":


    Utiles.debug.open_log_file("prueba.log")
    brain = Skynet()
    brain.research_keywords(['Venezuela'])
    Utiles.debug.close_log_file()

    #"CasillasVeteDelMadrid"
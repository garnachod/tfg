# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

from TwitterAPI.TweetCollector import TweetCollector
from TwitterAPI.TweetStreamCollector import TweetStreamCollector
from Writers.consoleTweetRecorder import ConsoleTweetRecorder
import time
if __name__ == '__main__':
    #tc = TweetCollector()
    #tc.print_trends()
    #tc.searchHashes(tc.get_trends())
    #tc.searchHashes(['TeDoyUnConsejo', 'AmigosParaTodaLaVidaSonAquellosQue'])
    #tc.print_public_timeline()
    #tc.testStream()
    try:
        recorders = [ConsoleTweetRecorder()]
        tc = TweetStreamCollector(recorders)
        tc.start()
        time.sleep(6000000) #esta espera es para poder ser interrumpido
    except KeyboardInterrupt:
        tc.seguir = False
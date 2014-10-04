# -*- coding: iso-8859-15 -*-
import threading

import tweepy

from TwitterAPI import getAuthorizations
from TwitterAPI._oldSlistener import SListener
from Utiles.alarmClock import AlarmClock


# Clase que se dedica a recoger tweets.
# Parámetros: filtros de búsqueda (tags, users, locations)
# número máximo de tweets antes de terminar
# tiempo máximo de ejecución antes de terminar
# nombre del fichero donde escribir resultados (prefijo)
# número de aplicación (usado para las autorizaciones Twitter)
# número de tweets x fichero

class _oldStreamTweetCollector(threading.Thread):
    def __init__(self, recorder):
        threading.Thread.__init__(self)
        self.recorder = recorder
        #instanciable desde fuera
        self.debug = False
        self.tags = []
        self.usuarios = []
        self.lugares = []
        self.num_app = 2
        self.seguir=True
        #fin instanciables
        self.listen = ""
        self.cycling_time = 600 #10 minutos
        self.ac = None

    def run(self):

        #itero para renovar el stream cada tanto
        while self.seguir:
            auth = getAuthorizations.get_tweepy_api_auth(self.num_app)
            api = tweepy.API(auth)
            self.ac = AlarmClock(self.cycling_time, self)
            self.ac.start()
            self.listen = SListener(self.recorder, api, self.debug)
            stream = tweepy.Stream(auth, self.listen)
            #print "lugares " + str(self.lugares)
            stream.filter(track=self.tags, follow=self.usuarios, locations=self.lugares)
            stream.disconnect()

    def wakeup(self):
        self.listen.seguir = False
        #lo siguiente es si quiero también cambiar de fichero
        #self.recorder.reset()

    def finish(self):
        self.seguir = False
        self.listen.seguir = False
        self.ac.stopped = True
        self.ac.stop.set()
        print "pongo seguir en False"

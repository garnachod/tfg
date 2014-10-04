# -*- coding: iso-8859-15 -*-
from Utiles import debug

__author__ = 'ortigosa'
import json
import time

from DBbridge.PostgresWriter import PostgresWriter



# esta clase solo esta pensada para ser usada en pruebas
# y medir velocidad de carga de base de datos

class FileReader():
    def __init__(self):
        self.input = None
        self.total_read=0
        self.total_time=0

    def read_file(self, filename):
        bd = PostgresWriter()
        self.input = open(filename, 'r')
        start = time.time()
        self.total_read=0
        for line in self.input:
            if line is not None and line != "" and line != "\n":
                bd.process_tweet(json.loads(line))
                self.total_read += 1
        end = time.time()
        self.total_time = end-start

if __name__ == "__main__":
    fr = FileReader()
#    fr.read_file(sys.argv[1])
    debug.DEBUG = False
    fr.read_file("../data/closed/may-macbook.json")
    #fr.read_file("../data/closed/testc.json")
    print "leídos " + str(fr.total_read) + " tweets en " + str(fr.total_time) + " segundos"

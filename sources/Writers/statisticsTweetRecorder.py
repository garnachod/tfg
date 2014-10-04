# -*- coding: iso-8859-15 -*-
__author__ = 'ortigosa'

import datetime

from Utiles.debug import print_if_text


# Superclase de todos los tipos de tweet recorder.
# Si se usa directamente la clase, sirve solo para llevar frecuencia (no almacena)

class StatisticsTweetRecorder():
    def __init__(self):
        self.current_minute = datetime.datetime.now().minute
        self.total_minutes = 0
        self.total_count = 0
        self.record_by_minute = {}
        for i in range(0, 59):
            self.record_by_minute[i] = 0
        self.last_hour_total = 0  # se puede calcular, pero no quiero perder tiempo
        self.old_minute = 0

    def record_tweet(self, tweet):
        """
        tweet es un diccionario.
        """
        #print_debug("#" + str(self.total_count) + " - " + str(datetime.datetime.now()), True)
        if self.current_minute == datetime.datetime.now().minute:
            self.record_by_minute[self.current_minute] += 1
        else:  # cambio de minuto
            self.record_last_hour()
            self.print_frequencies()
            self.current_minute = datetime.datetime.now().minute
            self.record_by_minute[self.current_minute] = 1
        self.total_count += 1

    def print_frequencies(self):
        print_if_text("Hora " + str(datetime.datetime.now()) + " Frecuencia ultimo minuto:" +
                      str(self.record_by_minute[self.current_minute]) + " tweets por minuto")
        print_if_text("Frecuencia promedio ultima hora:" + str(self.last_hour_total / min(self.total_minutes, 60)))
        print_if_text("Total recolectado:" + str(self.total_count))

    def record_last_hour(self):
        self.total_minutes += 1
        if self.total_minutes < 60:  # first 59 times
            self.last_hour_total += self.record_by_minute[self.current_minute]
        elif self.total_minutes == 60:  # first hour complete
            self.last_hour_total += self.record_by_minute[self.current_minute]
            self.old_minute = self.record_by_minute[(self.current_minute + 1) % 60]
        else:
            self.last_hour_total += self.record_by_minute[self.current_minute] - self.old_minute
            self.old_minute = self.record_by_minute[(self.current_minute + 1) % 60]
        return self.last_hour_total

    def frequency(self):
        """
            Retorna el numero de tweets registrados en el minuto anterior
        """
        return self.record_by_minute[self.current_minute]

    def reset(self):
        #do nothing, para especializar
        return True
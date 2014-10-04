# -*- coding: iso-8859-15 -*-
__author__ = 'ortigosa'

import time
import threading

#esta clase es necesaria con unas de las bibliotecas de Twitter (streamTweetCollector)
class AlarmClock(threading.Thread):

    def __init__(self,time, subject):
        threading.Thread.__init__(self)
        self.time = time
        self.subject = subject
        self.stop = threading.Event()
        self.stopped = False

    def run(self):
        self.stop.wait(self.time)
        if not self.stopped:
            self.subject.wakeup()


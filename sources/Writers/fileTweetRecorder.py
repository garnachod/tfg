# -*- coding: iso-8859-15 -*-
__author__ = 'ortigosa'

import time
import json

import os

from Utiles.debug import print_debug


data_dir = '../data/'

class FileTweetRecorder():
    def __init__(self, fprefix = 'streamer', limit=20000):
        self.counter = 1
        self.fprefix = fprefix
        self.limit = limit
        self.filename = fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
        self.output = open(data_dir + 'current/' + self.filename, 'w')
        #self.delout = open(data_dir + 'delete.txt', 'a')
        self.seguir = True

    def record_tweet(self, tweet):
        data = json.dump(tweet)
        self.output.write(data + "\n")
        self.counter += 1
        if self.counter >= self.limit:
            self.output.close()
            os.rename(data_dir + 'current/' + self.filename, data_dir + 'closed/' + self.filename)
            self.filename = self.fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
            self.output = open(data_dir + 'current/' + self.filename, 'w')
            self.counter = 0
        return True

    def record_json_tweet(self, tweet):
        self.output.write(tweet + "\n")
        print_debug(self.fprefix + '(' + str(self.counter) + ')' + json.loads(tweet)['text'])
        self.counter += 1
        if self.counter >= self.limit:
            self.output.close()
            os.rename(data_dir + 'current/' + self.filename, data_dir + 'closed/' + self.filename)
            self.filename = self.fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
            self.output = open(data_dir + 'current/' + self.filename, 'w')
            self.counter = 0
        return True

    def reset(self):
        self.output.close()
        os.rename(data_dir + 'current/' + self.filename, './data/closed/' + self.filename)
        self.filename = self.fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json'
        self.output = open(data_dir + 'current/' + self.filename, 'w')
        self.counter = 0

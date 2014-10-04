# -*- coding: iso-8859-15 -*-
__author__ = 'ortigosa'

import json


class ConsoleTweetRecorder():

    def record_tweet(self, tweet):
        if 'text' in tweet:
            print tweet['text']

    def record_json_tweet(self, tweet):
        try:
            data = json.loads(tweet)
        except ValueError as detail:
            sys.stderr.write(detail.__str__() + "\n")
            return
        print data['text']

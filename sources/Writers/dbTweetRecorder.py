# -*- coding: iso-8859-15 -*-
__author__ = 'ortigosa'

import json
from DBbridge.PostgresWriter import PostgresWriter

class DbTweetRecorder():
    def __init__(self):
        #db instance of a subclass of DBConnection
        self.db = PostgresWriter()

    def record_tweet(self, tweet, searchID):
        # if not isinstance(tweet, dict):
        #     tweet = self.as_dict(tweet)

        self.db.process_tweet(tweet, searchID)

    def record_json_tweet(self, tweet):
        try:
            data = json.loads(tweet)
        except ValueError as detail:
            sys.stderr.write(detail.__str__() + "\n")
            return
        self.db.process_tweet(data)

    def as_dict(self, data):
        return_value = {}
        for attr in ['id_str', 'text', 'coordinates', 'created_at', 'lang']:
            return_value[attr] = data.__getattribute__(attr)
        print dir(data)
        #return_value['retweeted_status'] = self.as_dict(data)
        return_value['user'] = self.as_dict(data.user)
        return return_value

import json
import time
import sys

from tweepy import StreamListener

data_dir = '../data/'

class _SListener(StreamListener):

    def __init__(self, recorder, api=None, debug=False):
        self.api = api or API()
        self.delout = open(data_dir + 'delete.txt', 'a')
        self.debug = debug
        self.seguir = True
        self.recorder = recorder

    def on_data(self, data):

        if 'in_reply_to_status' in data:
            return self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return False

    def on_status(self, status):
        self.recorder.record_tweet(status)
        return self.seguir

    def on_delete(self, status_id, user_id):
        self.delout.write(str(status_id) + "\n")
        return

    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return 

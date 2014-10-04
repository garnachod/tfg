import json
import sys

from DBbridge.PostgresWriter import PostgresWriter
from Utiles.debug import print_debug


filename = 'test.json'


class TweetFileReader():
    def __init__(self, db):
        #db instance of subclass of DBConnection
        self.db = db
        self.contador=0

    def read_file(self, filename):
        f = open(filename, 'r')
        self.contador = 0
        for line in f:
            line = line.strip()
            if line is not None and line != "" and line != "\n":
                try:
                    data = json.loads(line)
                except ValueError as detail:
                    sys.stderr.write(detail.__str__() + "\n")
                    continue
                self.db.process_tweet(data)
                self.contador += 1
                print_debug(str(self.contador) + ",", data['text'])
            else:
                continue


if __name__ == '__main__':
    db = PostgresWriter()
    tfr = TweetFileReader(db)
    tfr.read_file(filename)

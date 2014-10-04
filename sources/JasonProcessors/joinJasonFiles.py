# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import os
import json

def join_files(dir, target):
    #sacar lista ficheros json del directorio
    #crear fichero target
    #por cada fichero de lista
    #por cada fila del fichero
    #añadir a la lista (dic indexado x clave) si no está

    #al final volcar lista en fichero target

    dir_files = [file for file in os.listdir(dir) if os.path.splitext(file)[1] == '.json']
    list_tweets = set()
    output_file = open(target, 'w')
    for file_name in dir_files:
        input = open(os.path.join(dir, file_name), 'r')
        for tweet in input:
            if tweet is not None and tweet != "" and tweet != "\n":
                tweet_obj = json.loads(tweet)
                tweet_id = tweet_obj['id_str']
                if not tweet_id in list_tweets:
                    list_tweets.add(tweet_id)
                    #list_tweets[tweet_id] = tweet_obj
                    output_file.write(tweet + "\n")
        input.close()
    output_file.close()

if __name__ == "__main__":
    join_files("../data/current/", "abdicaRey.json")
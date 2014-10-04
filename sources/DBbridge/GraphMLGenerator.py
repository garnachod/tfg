# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

#version para PostgreSQL
import psycopg2
import os


class GraphMLGenerator():
    def __init__(self):
        filtro = ''
        self.conn = psycopg2.connect("dbname=tweetCollection user=twitterCollector")
        self.cur = self.conn.cursor()

    def generate_file(self, filename):
        #genera header
        output_file = open(filename, 'w')
        output_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output_file.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"\n')
        output_file.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        output_file.write('xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns\n')
        output_file.write('http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        output_file.write('<key id="d1" for="node" attr.name="name" attr.type="string">\n')
        output_file.write('<default>no-name</default>\n')
        output_file.write('</key>\n')
        output_file.write('<key id="d2" for="node" attr.name="num_tweets" attr.type="int"/>\n')
        output_file.write('<key id="d3" for="node" attr.name="num_tweets_total" attr.type="int"/>\n')
        output_file.write('<key id="d4" for="node" attr.name="followers" attr.type="int"/>\n')
        output_file.write('<key id="d5" for="edge" attr.name="num_retweets" attr.type="int"/>\n')
        output_file.write('<graph id="G" edgedefault="directed">\n')

        #genera nodos
        self.cur.execute("select users.id, screen_name, count(*) as numTweets, statuses_count, followers from tweets, "
                         "users where tuser = users.id and status ilike '%19j%' "
                         "group by users.id order by numTweets DESC")
        rows = self.cur.fetchall()
        for row in rows:
            output_file.write('<node id="%s">\n' % (row[0],))
            output_file.write('<data key="d1">%s</data>\n' % (row[1],))
            output_file.write('<data key="d2">%s</data>\n' % (row[2],))
            #output_file.write('<data key="d3">%s</data>\n' % (row[3],))
            #output_file.write('<data key="d4">%s</data>\n' % (row[4],))
            output_file.write('</node>\n')

        #genera conexiones
        self.cur.execute("select t1.tuser, t2.tuser, count(*) num_retweets from tweets as t1, tweets as t2 "
                         "where t1.is_retweet AND t1.orig_tweet = t2.id and t2.status ilike '%19j%' "
                         "group by t1.tuser, t2.tuser")
        row = self.cur.fetchone()
        count = 0
        while row is not None:
            output_file.write('<edge id="%s" source="%s" target="%s">\n' % (str(count), row[0], row[1]))
            output_file.write('<data key="d5">%s</data>\n' % (row[2]))
            output_file.write('</edge>\n')
            row = self.cur.fetchone()
            count += 1

        #cierra fichero
        output_file.write('</graph>\n')
        output_file.write('</graphml>\n')

if __name__ == "__main__":
    GraphMLGenerator().generate_file("19j.graphml")


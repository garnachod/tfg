# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import psycopg2

from TextProcessors import WordLists

class PostgresReader():
    def __init__(self):
        self.conn = psycopg2.connect(database="twitter", user="superDB", password="postgres_tfg", host="localhost")
        self.cur = self.conn.cursor()

    def num_tweets_hashtag(self, hashtag, start_date, end_date):
        """
        :param hashtag:
        :param start_date:
        :param end_date:
        :return: número de tweets que mencional al hashtag
        """
        query = "SELECT count(*) FROM tweets, hashtags, uses_tags where tag_text ILIKE '%%' || %s || '%%' " \
                " and id_tag = hashtags.id AND id_tweet = tweets.id " \
                "AND NOT is_retweet AND created_at >= %s AND created_at <= %s"
        self.cur.execute(query, [hashtag[1:], start_date, end_date])
        return int(self.cur.fetchone()[0])

    def num_tweets_topic(self, word, start_date, end_date):
        """
        :param word:
        :param start_date:
        :param end_date:
        :return: número de tweets que mencionan al término
        """

        if word[0] == '#':
            return self.num_tweets_hashtag(word, start_date, end_date)

        query = "SELECT count(*) from Tweets WHERE status ILIKE '%%' || %s || '%%' " \
                "AND NOT is_retweet AND created_at >= %s AND created_at <= %s"
        self.cur.execute(query, [word, start_date, end_date])
        return int(self.cur.fetchone()[0])

    def num_retweets_topic(self, word, start_date, end_date):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param min_tweets cantidad mínima de tweets para ser seleccionados
        :return: tupla con el valor informado por tweeter y el valor calculado de la BBDD
        """
        #dos formas de hacerlo: contanto retweets en la base de datos o sumando retweets informados por Twitter
        query = "SELECT count(*) from Tweets WHERE status ILIKE '%%' || %s || '%%' " \
                "AND is_retweet AND created_at >= %s AND created_at <= %s"
        self.cur.execute(query, [word, start_date, end_date])
        calculado = int(self.cur.fetchone()[0])

        query = "SELECT sum(retweet_count) FROM Tweets where not is_retweet AND status ILIKE '%%' || %s || '%%' " \
                "AND created_at >= %s AND created_at <= %s"
        self.cur.execute(query, [word, start_date, end_date])
        informado = int(self.cur.fetchone()[0])
        return [informado, calculado]

    def autores_topic(self, word, start_date, end_date, min_tweets=1, max_usuarios=100):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param min_tweets cantidad mínima de tweets para ser seleccionados
        :return: lista de autores con más tweets en el tema
        """

        query = "SELECT screen_name, count(Users.id) as cantidad FROM Tweets, Users " \
                "WHERE tuser=users.id AND NOT is_retweet AND status ILIKE '%%' || %s || '%%' " \
                "AND Tweets.created_at >= %s AND Tweets.created_at <= %s" \
                "GROUP BY users.id HAVING count(Users.id) >= %s " \
                "ORDER BY cantidad DESC LIMIT %s"
        self.cur.execute(query, [word, start_date, end_date, min_tweets, max_usuarios])
        rows = self.cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append([row[0], int(row[1])])

        return resultado

    def transmisores_topic(self, word, start_date, end_date, min_tweets=1, max_usuarios=100):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param min_tweets cantidad mínima de tweets para ser seleccionados
        :return: lista de usuarios con más retweets
        """
        query = "SELECT screen_name, count(Users.id) as cantidad FROM Tweets, Users " \
                "WHERE tuser=users.id AND is_retweet AND status ILIKE '%%' || %s || '%%' " \
                "AND Tweets.created_at >= %s AND Tweets.created_at <= %s " \
                "GROUP BY users.id HAVING count(Users.id) >= %s "\
                "ORDER BY cantidad DESC LIMIT %s"
        self.cur.execute(query, [word, start_date, end_date, min_tweets, max_usuarios])
        rows = self.cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append([row[0], int(row[1])])
        return resultado

    def mencionados_topic(self, word, start_date, end_date, max_usuarios=100):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param max_usuarios
        :return: lista de usuarios más mencionados en los tweets de un topic dado
        """
        query = "SELECT screen_name, count(Users.id) as cantidad FROM Tweets, Users, Uses_user " \
                "WHERE NOT is_retweet AND status ILIKE '%%' || %s || '%%' " \
                "AND Tweets.created_at >= %s AND Tweets.created_at <= %s " \
                "AND uses_user.id_tweet = Tweets.id and uses_user.id_user=Users.id " \
                "GROUP BY users.id ORDER BY cantidad DESC LIMIT %s"
        self.cur.execute(query, [word, start_date, end_date, max_usuarios])
        rows = self.cur.fetchall()
        resultado = []
        for row in rows:
            resultado.append([row[0], int(row[1])])
        return resultado

    def word_frequency_topic(self, word, start_date, end_date, max_num_words=10):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param max_num_words: máxima cantidad de palabras a devolver
        :return: lista de palabras usadas en los tweets de un tema dado
        """
        query = "SELECT status FROM Tweets WHERE NOT is_retweet AND " \
                "status ILIKE '%%' || %s || '%%' " \
                "AND Tweets.created_at >= %s AND Tweets.created_at <= %s "
        self.cur.execute(query, [word, start_date, end_date])
        rows = self.cur.fetchall()
        status_texts = [row[0] for row in rows]
        words = [w
                 for t in status_texts
                    for w in t.split()
                 ]

        list_processor = WordLists.WordLists()
        return list_processor.more_frequents(words, max_num_words)

    def time_line_topic(self, word, interval='day'):
        """
        :param word: word to look for
        :param interval: ['day', 'hour', 'minute', 'week', 'month']
        :return: list [interval (year, month, day, hour, minute), number_tweets]
        """
        if interval not in ['day', 'hour', 'minute', 'week', 'month']:
            interval = 'day'
        query = "select date_trunc(%s, created_at) date, count(id) cant from Tweets " \
                "WHERE status ILIKE '%%' || %s || '%%' " \
                "group by date_trunc(%s, created_at) order by date ASC"
        self.cur.execute(query, [interval, word, interval])
        rows = self.cur.fetchall()
        return [[[row[0].year, row[0].month, row[0].day, row[0].hour, row[0].minute], int(row[1])] for row in rows]


    def most_followers_topic(self, word, start_date, end_date, max_users=10):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param max_users:
        :return: autores o transmisores con más seguidores que han escrito sobre el tema dado
        """
        query = "select count(*), users.screen_name, followers from Tweets, users " \
                    "where status ilike '%%' || %s || '%%' and tuser=users.id and followers is not null " \
                    "AND Tweets.created_at >= %s AND Tweets.created_at <= %s " \
                    "group by users.id order by followers DESC LIMIT %s"
        self.cur.execute(query, [word, start_date, end_date, max_users])
        rows = self.cur.fetchall()
        return [[int(row[0]), row[1], int(row[2])] for row in rows]

    def most_success(self, word, start_date, end_date, max_tweets=20):
        """
        :param word:
        :param start_date:
        :param end_date:
        :param max_tweets:
        :return: lista de tweets que más veces han sido retuiteados sobre el tema
        """
        query = "select t1.id, users.screen_name, t1.retweet_count exito, count(t2.status) from Tweets t1, Tweets t2, Users " \
                "where t1.status ilike '%%' || %s || '%%'  and not t1.is_retweet and users.id=t1.tuser and " \
                "t2.orig_tweet = t1.id AND t1.created_at >= %s AND t2.created_at <= %s " \
                "group by t1.id, users.screen_name order by exito DESC LIMIT %s"
        self.cur.execute(query, [word, start_date, end_date, max_tweets])
        rows = self.cur.fetchall()
        return [[int(row[0]), row[1], int(row[2]), int(row[3])] for row in rows]

    def scope_topic(self, word, start_date, end_date):
        """
        :param word:
        :param start_date:
        :param end_date:
        :return: numero de potenciales lectores (suma de los seguidores de los autores y transmisores del tema.
        """
        query = "select sum(followers) from Tweets, Users where status ilike '%%' || %s || '%%' and users.id=tuser " \
                "AND Tweets.created_at >= %s AND Tweets.created_at <= %s"
        self.cur.execute(query, [word, start_date, end_date])
        return int(self.cur.fetchone()[0])

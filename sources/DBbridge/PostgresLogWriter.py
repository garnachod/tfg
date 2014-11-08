# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import psycopg2
from ConexionSQL import ConexionSQL
from datetime import datetime

from Utiles.debug import print_debug


class PostgresLogWriter():
    def __init__(self):
        conSql = ConexionSQL()
        self.con = conSql.getConexion()
        self.cur = conSql.getCursor()
        try:
            self.cur.execute("INSERT INTO Logs (event_time, event_type, message) VALUES (%s, %s, %s) RETURNING id;",
                                 (datetime.now().isoformat(), "init_logger", ""))
            self.con.commit()
        except psycopg2.Error, e:
                print_debug("Error en invocación a Insert inicial into Logs " + e.pgerror, True)

    def record_app_search(self, search_string, id_user, number_new_tweets, number_recalled_tweets):
        self.cur.execute("INSERT INTO app_searches "
                         "(search_string, id_user, number_new_tweets, number_recalled_tweets, search_time) "
                         "VALUES (%s, %s, %s, %s, now()) RETURNING id",
                         (search_string, id_user, number_new_tweets, number_recalled_tweets))
        self.con.commit()

    def insert_log(self, id_user, event_type, message, exception_msg=""):
        try:
            self.cur.execute("INSERT INTO Logs (event_time, id_user, event_type, message, exception_msg) "
                             "VALUES (%s, %s, %s, %s, %s) RETURNING id;",
                             (datetime.now().isoformat(), id_user, event_type, message, exception_msg))

            self.con.commit()
        except psycopg2.Error, e:
                print_debug("Error en invocación a Insert into Logs " + e.pgerror, True)

    def record_last_sequential_tweet_for_search(self, list_of_words, tweet_id):

        for word in list_of_words:
            self.cur.execute('SELECT * FROM t_searches WHERE keyword=%s;', (word,))
            row = self.cur.fetchone()
            if row is None:
                self.cur.execute('INSERT INTO t_searches (keyword, collecting_time, '
                                 'last_tweet_collected, number_of_searches) '
                                 'VALUES (%s, now(), %s, %s)', (word, tweet_id, 1))
            else:
                self.cur.execute('UPDATE t_searches SET collecting_time=now(), last_tweet_collected=%s, '
                                 'number_of_searches = number_of_searches + 1'
                                 'WHERE keyword=%s AND last_tweet_collected < %s;',
                                 (tweet_id, word, tweet_id))

        self.con.commit()

    def record_last_sequential_tweet_from_user(self, screen_name, tweet_id):
        if screen_name[0] == '@':
            screen_name = screen_name[1:]
        self.cur.execute("UPDATE users SET last_tweet_collected=%s, collecting_time=now() WHERE screen_name=%s;",
                         (tweet_id, screen_name))
        self.con.commit()

    ###############################
    #
    # READING: recupera valores guardados en los logs
    #
    ###############################

    def last_sequential_tweet_for_search(self, list_of_words):
        """
        :param list_of_words:
        :return: dictionary with last id for each word of the list
        """
        list_of_limits = {key: 0 for key in list_of_words}
        self.cur.execute('SELECT keyword, last_tweet_collected FROM t_searches WHERE keyword = ANY(%s);', (list_of_words,))
        rows = self.cur.fetchall()
        for row in rows:
            list_of_limits[row[0]] = row[1]
        return list_of_limits

    def last_sequential_tweet_from_user(self, screen_name):
        """
        Retorna el id twitter del ultimo tweet recolectado en acceso secuencial
        en formato string (varchar(18))
        """
        if screen_name[0] == '@':
            screen_name = screen_name[1:]
        self.cur.execute('SELECT last_tweet_collected FROM Users WHERE screen_name=%s;', (screen_name,))
        row = self.cur.fetchone()
        if row is None:
            return 0
        else:
            if row[0] is None:
                return 0
            else:
                return row[0]


# -*- coding: iso-8859-15 -*-

import psycopg2
from ConexionSQL import ConexionSQL

from Utiles.debug import print_debug
#, write_log


#dado un tweet en formato jason, esta clase (método process_tweet) lo mete en la base de datos PostgreSQL


class PostgresWriter():

    def __init__(self):
        self.id = self.texto = self.coordinates = self.created_at = self.lang = self.place = ""
        self.is_retweet = False
        self.possibly_sensitive = False
        self.orig_id = None
        self.favorite_count = self.retweet_count = 0
        self.user_id = self.tweet_id = 0

        self.twitter_id = self.statuses_count = self.friends_count = self.followers_count = 0
        self.location = self.created_at = self.description = self.name = self.protected = ""
        self.screen_name = self.url = self.utc_offset = ""

        conSql = ConexionSQL()
        self.conn = conSql.getConexion()
        self.cur = conSql.getCursor()

    ###############################
    #
    # WRITING
    #
    ###############################


    ###############################
    #
    # TWEETS
    #
    ###############################

    def process_tweet(self, data, searchID):
        """
        data = tweet representado como un diccionario
        devuelve el id (interno) del tweet insertado en la base de datos
        :type data: int
        """

        if 'id_str' in data:
            id_str = data['id_str']
        else: #no puede hacer nada
            return None
        #Comprueba si ya esta
        self.cur.execute("SELECT id, favorite_count, retweet_count FROM Tweets where id_twitter = %s; ", (id_str,))
        row = self.cur.fetchone()
        if row is not None: #ya existia
            
            identificador = self._update_tweet(data, row)
            #no inserto searchID en la jointable, porque ya estaban en la base de datos por los que he debido mostrarlos
            return identificador
        else:
            identificador = self._process_new_tweet(data, searchID)
            #inserto searchID en la jointable
            query = "INSERT INTO join_search_tweet (id_search, id_tweet) VALUES (%s,%s);"
            self.cur.execute(query, [searchID, identificador])
            self.conn.commit()

            #fin de insercion
            return identificador

    def _process_new_tweet(self, data, searchID):
        coordinates = created_at = lang = place = place_name = ""
        is_retweet = False
        possibly_sensitive = False
        orig_id = None
        favorite_count = retweet_count = 0
        user_id = 0
        id_str = data['id_str']
        media_url = ''

        if 'text' in data:
            texto = data['text']
        else:
            #write_log("error_tweet_record", "Tweet sin contenido: " + id_str)
            return None

        if 'user' in data:
            user_id = self.process_user(data['user'])
        if 'coordinates' in data and data['coordinates'] is not None and 'coordinates' in data['coordinates']:
            coordinates = data['coordinates']['coordinates']
        if 'created_at' in data:
            created_at = data['created_at']  # Importante! se tomará como base para la actualización
        if 'lang' in data:
            lang = data['lang']
        if 'retweeted_status' in data: #es un retweet
            orig_id = self._store_retweet(data['retweeted_status'], searchID)
            is_retweet = True
        if 'place' in data and data['place'] is not None:
            place = data['place']['id']
            place_name = data['place']['name']
        #si lo grabo apenas sale, lo siguiente no tendría sentido, pero puede que llegue aquí como retweet
        if 'favorite_count' in data:
            favorite_count = data['favorite_count']
        if 'retweet_count' in data:
            retweet_count = data['retweet_count']
        if 'possibly_sensitive' in data:
            possibly_sensitive = data['possibly_sensitive']
        if 'entities' in data:
            if 'media' in data['entities']:
                #print data['entities']['media']
                if 'media_url' in data['entities']['media'][0]:
                    media_url = data['entities']['media'][0]['media_url']
        try:
            self.cur.execute("INSERT INTO Tweets (id_twitter, status, coordinates, created_at, lang, is_retweet, " \
                         "orig_tweet, place_id, place_name, favorite_count, retweet_count, "
                         "possibly_sensitive, tuser, media_url)  " \
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;",
                         (id_str, texto, coordinates, created_at, lang, is_retweet,
                          orig_id, place, place_name, favorite_count, retweet_count,
                          possibly_sensitive, user_id, media_url))
            tweet_id = self.cur.fetchone()[0]
        except psycopg2.Error as e:
            #write_log("error_tweet_record", "Tweet: " + data['text'], e.pgerror)
            return None

        if 'entities' in data:
            self.process_entities(data['entities'], tweet_id)
        self.commit()
        return tweet_id

    def _update_tweet(self, new_tweet, stored_tweet):
        orig_id = stored_tweet[0]
        insert = False
        if 'favorite_count' in new_tweet:
            favorite_count = new_tweet['favorite_count']
            if favorite_count > stored_tweet[1]:
                favorite_count = stored_tweet[1]
                insert = True
        if 'retweet_count' in new_tweet:
            retweet_count = new_tweet['retweet_count']
            if retweet_count > stored_tweet[2]:
                retweet_count = stored_tweet[2]
                insert = True

        if insert:
            self.cur.execute('UPDATE Tweets set favorite_count=%s, retweet_count=%s WHERE id=%s;',
                    (favorite_count, retweet_count, orig_id))
        return orig_id

    def _store_retweet(self, orig_tweet, searchID):
        """
        """
        self.cur.execute("SELECT id, favorite_count, retweet_count FROM Tweets where id_twitter = %s; ",
                         (orig_tweet['id_str'],))
        row = self.cur.fetchone()
        if row is None:
            return self.process_tweet(orig_tweet, searchID)

        return self._update_tweet(orig_tweet, row)

    ###############################
    #
    # USERS
    #
    ###############################

    def process_user(self, user):
        """
        devuelve el id interno (bd) del usuario
        """
        self.cur.execute("SELECT id, name, statuses_count, friends, followers "\
                         "FROM Users where id_twitter = %s; ", (user['id_str'],))
        row = self.cur.fetchone()

        statuses_count = user['statuses_count']
        friends_count = user['friends_count']
        followers_count = user['followers_count']

        if row is not None and row[1] != '':
            #el user ya esta almacenado, solo actualizo algunos datos si mas nuevos
            if statuses_count > row[2]:
                statuses_count = row[2]
            if friends_count > row[3]:
                friends_count = row[3]
            if followers_count > row[4]:
                followers_count = row[4]
            self.cur.execute('UPDATE users SET statuses_count=%s, friends=%s, followers=%s WHERE id=%s',
                            (statuses_count, friends_count, followers_count, row[0]))
            return row[0]

        location = user['location']
        if len(location) > 50:
            location = location[:49]
        created_at = user['created_at']
        description = user['description']
        name = user['name']
        protected = user['protected']
        screen_name = user['screen_name']
        url = user['url']
        utc_offset = user['utc_offset']

        if row is not None and row[1] == '':
            #solo tengo id_str
            self.cur.execute('UPDATE users SET statuses_count=%s, friends=%s, followers=%s, '
                         'location=%s, created_at=%s, description=%s, name=%s, protected=%s, '
                         'screen_name=%s, url=%s, utc_offset=%s WHERE id=%s',
                         (statuses_count, friends_count, followers_count, location,
                          created_at, description, name, protected, screen_name,
                          url, utc_offset, row[0]))
            return row[0]

        # the user does not exist in the database
        twitter_id = user['id_str']
        self.cur.execute('INSERT INTO users (id_twitter, name, screen_name, description, followers, ' \
                'friends, statuses_count, location, created_at, protected, url, utc_offset) ' \
                ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;', (twitter_id,
                    name, screen_name, description, followers_count,
                    friends_count, statuses_count, location, created_at, protected,
                    url, utc_offset))
        user_id = self.cur.fetchone()[0]
        return user_id

    ###############################
    #
    # ENTITIES
    #
    ###############################
    def process_entities(self, data, tweet_id):
        print_debug("Entra al process_entities")
        if 'user_mentions' in data:
            user_mentions = data['user_mentions']
            print_debug("antes del for de user_mentions")
            for um in user_mentions:
                print_debug("User mention " + um['id_str'])
                self.store_user_mentions(um, tweet_id)
        print_debug("antes del if de hashtags")
        if 'hashtags' in data:
            for hashtag in data['hashtags']:
                self.store_tag(hashtag['text'], tweet_id)
        print_debug("antes del if de urls")
        if 'urls' in data:
            for url in data['urls']:
                self.store_url(url['display_url'], tweet_id)

    def store_url(self, url, tweet_id):
        self.cur.execute('INSERT INTO URLs (url, id_tweet) VALUES (%s,%s) RETURNING id;', (url, tweet_id))
        #url_id = self.cur.fetchone()[0]
        #self.cur.execute('INSERT INTO Uses_urls VALUES (%s, %s);', (tweet_id, url_id))

    def store_user_mentions(self, user_mentioned, tweet_id):
        screen_name = user_mentioned['screen_name']
        name = user_mentioned['name']
        id_str = user_mentioned['id_str']
        self.cur.execute("SELECT id FROM Users where id_twitter =%s;", (id_str,))
        row = self.cur.fetchone()
        if row is None:
            try:
                self.cur.execute("INSERT INTO users (id_twitter, name, screen_name) VALUES (%s, %s, %s) RETURNING id;",
                                 (id_str, name, screen_name))
                self.conn.commit()
                id_user = self.cur.fetchone()[0]
                
            except psycopg2.Error, e:
                print_debug("Error en invocación a Insert into Users " + e.pgerror, True)

            
        else:
            id_user = row[0]
        try:
            self.cur.execute("INSERT INTO Uses_user SELECT %s, %s WHERE NOT EXISTS ("
                             "select * from Uses_user WHERE id_tweet=%s AND id_user=%s);",
                            (tweet_id, id_user, tweet_id, id_user))
        except psycopg2.Error, e:
            print_debug("Error en invocación a Insert into Uses_user " + e.pgerror, True)

    def store_tag(self, tag, tweet_id):
        self.cur.execute("SELECT id FROM Hashtags where tag_text=%s;", (tag,))
        row = self.cur.fetchone()
        if row is None:
            self.cur.execute("INSERT INTO Hashtags (tag_text) VALUES (%s) RETURNING id", (tag,))
            id_tag = self.cur.fetchone()[0]
        else:
            id_tag = row[0]
        self.cur.execute("INSERT INTO Uses_tags SELECT %s, %s WHERE NOT EXISTS (" \
                         "select * from Uses_tags WHERE id_tweet=%s AND id_tag=%s);",
                         (tweet_id, id_tag, tweet_id, id_tag))


    ###############################
    #
    # READING
    #
    ###############################


    def get_tweet_id(self, id_str):
        """
        Retorna el id de un tweet en la base de datos dado su id_str
        """
        self.cur.execute("SELECT id FROM Tweets where id_twitter = %s; ", (id_str,))
        row = self.cur.fetchone()
        if row is None:
            return None
        return row[0]

    def get_user_id_name(self, id_str):
        """
        Retorna el id y name de un usuario en la bd, si existe, dado su id twitter
        """
        self.cur.execute("SELECT id, name FROM Users where id_twitter = %s; ", (id_str,))
        row = self.cur.fetchone()
        if row is None:
            return None
        return row


    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()




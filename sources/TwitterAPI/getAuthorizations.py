# -*- coding: iso-8859-15 -*-
import tweepy
import psycopg2

twitter_tokens = None
max_twitter_app = 2
next_twitter_app = 0

#queue = multiprocessing.Manager()
#queue.start()
class GetAuthorizations():
    def __init__(self):
        self.conn = psycopg2.connect(database="twitter", user="superDB", password="postgres_tfg", host="localhost")
        self.cur = self.conn.cursor()

    def load_twitter_token(self):
        query = "SELECT id FROM twitter_tokens"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            query = "INSERT INTO tokens_count (id_token, simulado) VALUES (%s, true)"
            self.cur.execute(query, (row[0],))

        query = "SELECT id_token, count(id_token) as cuenta from (select * from tokens_count  where tiempo > current_timestamp - interval '15 minutes') as A  GROUP BY id_token order by cuenta DESC Limit 1"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        for row in rows:
            self.id = row[0]
            self.cuenta = row[1]


        query = "SELECT * FROM twitter_tokens WHERE id = %s"
        self.cur.execute(query, (self.id,))
        rows = self.cur.fetchall()
        for row in rows:
            #self.id = row[0]
            self.api_key = row[1]
            self.api_key_secret = row[2]
            self.access_token = row[3]
            self.access_token_secret = row[4]
            self.oauth = row[5]
            self.n_consultas = row[6]

    def add_query_to_key(self):
        query = "INSERT INTO tokens_count (id_token) VALUES (%s)"
        #comienzo de la transaccion
        self.cur.execute("BEGIN")    
        self.cur.execute(query, (self.id,))
        self.cur.execute("COMMIT")

    def get_twitter_secret(self):
        API_key = self.api_key
        API_secret = self.api_key_secret
        access_token = self.access_token
        access_token_secret = self.access_token_secret
        return [API_key, API_secret, access_token, access_token_secret]

    def get_tweepy_api_auth(self):
        API_key, API_secret, access_token, access_token_secret = get_twitter_secret()
        auth = tweepy.OAuthHandler(API_key, API_secret)
        auth.set_access_token(access_token, access_token_secret)
        return auth

    def get_twython_token(self):
        API_key = self.api_key
        access_token = self.oauth
        return [API_key, access_token]

    def get_twython_token_auth(self):
        API_key = self.api_key
        API_secret = self.api_key_secret
        return [API_key, API_secret]    

    def get_yahoo_geo_api_auth():
        return '1Uo7bs_V34FrwQuJJywk5PKHc8VAcm.Hy_jN6.X.rr4CSOVELWsnBdb2BJV8lpFBPUksgHT.GkudoeLnEs6L_w--'
'''
def load_twitter_tokens():
    global twitter_tokens
    f = open("../secret/TwitterTokens.txt", "r")
    twitter_tokens = []
    for x in range(1, max_twitter_app):
        twitter_tokens.append([f.readline()[:-1], f.readline()[:-1], f.readline()[:-1], f.readline()[:-1], f.readline()[:-1]])
        
    f.close()

#todo: llevar cuenta de queries x window?
'''

'''
def get_tweepy_api_auth():
    API_key, API_secret, access_token, access_token_secret = get_twitter_secret()
    auth = tweepy.OAuthHandler(API_key, API_secret)
    auth.set_access_token(access_token, access_token_secret)
    return auth

def get_twython_token():
    global next_twitter_app
    API_key = twitter_tokens[next_twitter_app][0]
    #API_secret = twitter_tokens[next_twitter_app][1]
    #access_token = twitter_tokens[next_twitter_app][2]
    access_token = twitter_tokens[next_twitter_app][4]
    next_twitter_app = (next_twitter_app + 1) % max_twitter_app
    print API_key
    print access_token
    return [API_key, access_token]

def get_twython_token_auth():
    API_key = twitter_tokens[next_twitter_app][0]
    API_secret = twitter_tokens[next_twitter_app][1]
    return [API_key, API_secret]

def get_yahoo_geo_api_auth():
    return '1Uo7bs_V34FrwQuJJywk5PKHc8VAcm.Hy_jN6.X.rr4CSOVELWsnBdb2BJV8lpFBPUksgHT.GkudoeLnEs6L_w--'
'''



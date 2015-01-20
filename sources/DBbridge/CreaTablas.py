# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

from ConexionSQL import ConexionSQL

def crea_tablas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()
    #conn = psycopg2.connect(database="twitter", user="superDB", password="postgres_tfg", host="localhost")
    #cur = conn.cursor()

    query = ('DROP TABLE IF EXISTS Users CASCADE;'
             'CREATE TABLE Users ('
             'id serial PRIMARY KEY'
             ', id_twitter varchar(10)'
             ', name varchar(20)'
             ', screen_name varchar(15)'
             ', description text'
             ', followers NUMERIC'
             ', friends NUMERIC'
             ', statuses_count NUMERIC'
             ', location varchar(50)'
             ', created_at date'
             ', protected varchar(5)'
             ', url text'
             ', utc_offset varchar(10)'
             ', last_tweet_collected varchar(18)'  # puede no ser el ultimo, sino el ultimo recogido sistemáticamente del usuario
             ', collecting_time timestamp'  # ultima vez que se hizo busqueda secuancial.
             ');'
             'CREATE UNIQUE INDEX users_idx ON Users(id_twitter);'
             'CREATE UNIQUE INDEX users_sn_idx ON Users(screen_name);'
    )
    cur.execute(query)
    query = ('DROP TABLE IF EXISTS Tweets CASCADE;'
             'CREATE TABLE Tweets ('
             'id serial PRIMARY KEY'
             ', id_twitter varchar(18)'
             ', status varchar(160)'
             ', tuser integer REFERENCES Users(id)'
             ', coordinates varchar(60)'
             ', created_at timestamp'
             ', lang char(3)'
             ', is_retweet boolean'
             ', orig_tweet integer REFERENCES Tweets(id)'
             ', place_id varchar(18)'
             ', place_name varchar(60)'
             ', favorite_count numeric'
             ', retweet_count numeric'
             ', possibly_sensitive boolean'
             ', media_url varchar(100)'
             ');'
             'CREATE UNIQUE INDEX tweets_idx ON Tweets (id_twitter);'
             'CREATE INDEX tweets_tu_idx ON Tweets (tuser);'
    )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS Hashtags CASCADE;'
             'CREATE TABLE Hashtags ('
             'id serial PRIMARY KEY'
             ', tag_text varchar(50)'
             ');'
             'CREATE UNIQUE INDEX hash_idx ON Hashtags (tag_text);'
    )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS Uses_tags;'
             'CREATE TABLE Uses_tags ('
             'id_tweet integer REFERENCES Tweets(id)'
             ', id_tag integer REFERENCES Hashtags(id)'
             ', CONSTRAINT tweet_tag PRIMARY KEY(id_tweet, id_tag)'
             ');'
    )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS Uses_user;'
             'CREATE TABLE Uses_user ('
             'id_tweet integer REFERENCES Tweets(id)'
             ', id_user integer REFERENCES Users(id)'
             ', CONSTRAINT tweet_user PRIMARY KEY(id_tweet, id_user));'
             #'CREATE INDEX tweet_idx ON Hashtags (id_tweet);'
             #'CREATE INDEX user_idx ON Hashtags (id_user);'
    )
    cur.execute(query)

    #el html sera futura referencia a tabla que guarde el html.
    query = ('DROP TABLE IF EXISTS URLs CASCADE;'
             'CREATE TABLE URLs ('
             'id serial PRIMARY KEY'
             ', id_tweet integer REFERENCES Tweets(id)'
             ', url text'
             ', html_page integer'
             ');'
    )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS t_searches CASCADE;'
             'CREATE TABLE t_searches (' # busquedas contra la API Twitter
             'id serial PRIMARY KEY'
             ', keyword varchar(500)'  # término buscado
             ', collecting_time timestamp'
             ', last_tweet_collected varchar(18)'  # puede no ser el ultimo, sino el ultimo recogido sistemáticamente
             ', number_of_searches integer'
             ');'
    )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS Logs CASCADE;'
             'CREATE TABLE Logs ('
             'id serial PRIMARY KEY'
             ', event_time timestamp'
             ', id_user integer REFERENCES app_users(id)'
             ', event_type varchar(20)'
             ', message varchar(200)'
             ', exception_msg varchar(200)'
             ');'
             'CREATE INDEX logs_msg_idx ON Logs(event_type);'
             )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS twitter_tokens CASCADE;'
             'CREATE TABLE twitter_tokens('
             'id serial PRIMARY KEY, '
             'api_key varchar(50), '
             'api_key_secret varchar(100), '
             'access_token varchar(100), '
             'access_token_secret varchar(100), '
             'oauth varchar(200)'
            ');'
             )
    cur.execute(query)

    query = ('DROP TABLE IF EXISTS tokens_count CASCADE;'
             'CREATE TABLE tokens_count('
             'id serial PRIMARY KEY, '
             'tiempo timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
             'id_token int REFERENCES twitter_tokens (id), '
             'simulado boolean DEFAULT false'
             ');'
             )
    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()


def temp_crea_tablas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS app_users CASCADE;'
             'CREATE TABLE app_users ('
             'id serial PRIMARY KEY'
             ', mail varchar(50)'
             ', name varchar(100)'
             ', institution varchar(30)'
             ', role varchar(20)'
             ', username varchar(20)'
             ', pasw varchar(100)'
             ');'
             )
    cur.execute(query)
    
    query = ('DROP TABLE IF EXISTS app_searches CASCADE;'
             'CREATE TABLE app_searches ('
             'id serial PRIMARY KEY'
             ', search_string varchar(200)'
             ', id_user integer REFERENCES app_users(id)'
             ', number_new_tweets integer'
             ', number_recalled_tweets integer'
             ', search_time double precision'
             ');'
             )
    cur.execute(query)
   
    query = ('DROP TABLE IF EXISTS join_search_tweet CASCADE;'
             'CREATE TABLE join_search_tweet ( '
             'id_search int references app_searches(id), '
             'id_tweet int references tweets(id), '
             'primary key (id_search, id_tweet)'
             ');')
    cur.execute(query)
    
    conn.commit()
    cur.close()
    conn.close()

def crea_def_user():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()
    
    query = "INSERT INTO app_users (name,mail,institution,role,username,pasw) VALUES ('dani','garnachod@gmail.com','uam','admin','garnachod','58a543c86d0af40db318dec6c8b47e8a48dac9ea576ed5b944f07ec589e13fc5');"

    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def crea_tareas():
    conSql = ConexionSQL()
    conn = conSql.getConexion()
    cur = conSql.getCursor()

    query = ('DROP TABLE IF EXISTS tareas_programadas CASCADE;'
             'CREATE TABLE tareas_programadas ('
             'id serial PRIMARY KEY'
             ', tipo varchar(30)'
             ', id_search integer REFERENCES app_searches(id)'
             ', tiempo_inicio timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ', tiempo_fin timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP '
             ');'
             )
    cur.execute(query)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    #crea_tablas()
    #temp_crea_tablas()
    #crea_def_user()
    crea_tareas()

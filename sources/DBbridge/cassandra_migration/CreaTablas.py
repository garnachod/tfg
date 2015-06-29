from cassandra.cluster import Cluster

def creaUsersTwitter(session):
    query = (
             'CREATE TABLE users ('
             'id_twitter bigint PRIMARY KEY'
             ', name varchar'
             ', screen_name varchar'
             ', followers int'
             ', location varchar'
             ', created_at timestamp );'
            )
    session.execute(query)

def creaIndexUsersTwitter(session):
    query = "CREATE INDEX indx_screen_name ON users (screen_name);"
    session.execute(query)

def creaTweets(session):
    query = ('CREATE TABLE Tweets ('
             'id_twitter bigint PRIMARY KEY'
             ', status varchar'
             ', created_at timestamp'
             ', lang varchar'
             ', is_retweet boolean'
             ', orig_tweet bigint'
             ', favorite_count int'
             ', retweet_count int'
             ', media_urls set'
             ', lucene TEXT'
             ');'
             
    )
    session.execute(query)

def creaIndexTweet(session):
    ###usa el plugin "https://github.com/Stratio/cassandra-lucene-index" que usa LUCENE

    query = (
        "CREATE CUSTOM INDEX tweets_index ON tweets (lucene)"
        "USING 'com.stratio.cassandra.lucene.Index'"
        "WITH OPTIONS = {"
        "'refresh_seconds' : '1',"
        "'schema' : '{"
        "fields : {"
        "   id    : {type : \"integer\"},"
        "   user  : {type : \"string\"},"
        "   body  : {type : \"text\", analyzer : \"english\"},"
        "   time  : {type : \"date\", pattern : \"yyyy/MM/dd\"},"
        "}"
    "}'"
    "};"
    )
    session.execute(query)


if __name__ == '__main__':
    cluster = Cluster()
    session = cluster.connect('twitter')
    #creaUsersTwitter(session)
    #creaIndexUsersTwitter(session)
    
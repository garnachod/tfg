from cassandra.cluster import Cluster

def creaUsersTwitter(session):
    query = (
             'CREATE TABLE users ('
             'id_twitter bigint PRIMARY KEY'
             ', name varchar'
             ', screen_name varchar'
             ', followers int'
             ', location varchar'
             ', created_at timestamp '
             ', last_tweet_collected bigint);'
            )
    session.execute(query)

def creaIndexUsersTwitter(session):
    query = "CREATE INDEX indx_screen_name ON users (screen_name);"
    session.execute(query)

def getSchemas(session):
    query = "SELECT * FROM system.schema_keyspaces;"
    print session.execute(query)
def getTables(session):
    query = "select columnfamily_name from system.schema_columnfamilies where keyspace_name = 'twitter';"
    print session.execute(query)

def creaTweets(session):
    query = ('CREATE TABLE Tweets ('
             'id_twitter bigint PRIMARY KEY'
             ', status text'
             ', tuser bigint'
             ', created_at timestamp'
             ', lang text'
             ', orig_tweet bigint'
             ', favorite_count int'
             ', retweet_count int'
             ', media_urls map<text, text>'
             ', latitude FLOAT'
    		 ', longitude FLOAT'
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
        "'refresh_seconds' : '60',"
        "'schema' : '{"
        "fields : {"
        "   id_twitter : {type : \"bigint\"},"
        "   tuser  : {type : \"bigint\"},"
        "   status  : {type : \"text\", analyzer : \"english\"},"
        "   created_at  : {type : \"date\", pattern : \"yyyy/MM/dd\"},"
        " place : {type : \"geo_point\", latitude:\"latitude\", longitude:\"longitude\"}"
        "}"
    "}'"
    "};"
    )
    session.execute(query)

    query = "CREATE INDEX indx_tuser ON tweets (tuser);"
    session.execute(query)

def clean(session):
    session.execute("DROP TABLE Tweets;")
    session.execute("DROP TABLE users;")
    
if __name__ == '__main__':
    cluster = Cluster()
    session = cluster.connect('twitter')
    #clean(session)
    creaUsersTwitter(session)
    creaIndexUsersTwitter(session)
    #print "************usuario creado **************"
    creaTweets(session)
    creaIndexTweet(session)
    #print "************tweet creado **************"
    getSchemas(session)
    getTables(session)
    
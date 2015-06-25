from cassandra.cluster import Cluster

def describeTables(session):    
    print session.execute("describe tables;")

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


if __name__ == '__main__':
    cluster = Cluster()
    session = cluster.connect('twitter')
    describeTables(session)
    #creaUsersTwitter(session)
    #creaIndexUsersTwitter(session)
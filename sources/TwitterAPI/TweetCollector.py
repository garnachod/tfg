# -*- coding: iso-8859-15 -*-

__author__ = 'ortigosa'

import twitter
import Utiles

from getAuthorizations import get_twitter_secret


SPAIN_WOE_ID = 23424950
WORD_WOE_ID = 1
US_WOE_ID = 23424977

# Puede usarse tanto para Stream como para Rest
class TweetCollector:
    def __init__(self, recorder, app_num=1):
        API_key, API_secret, access_token, access_token_secret = get_twitter_secret(app_num)
        auth = twitter.oauth.OAuth(access_token, access_token_secret, API_key, API_secret)
        self.twitter_api = twitter.Twitter(auth=auth)
        self.recorder=recorder

        #todo todo el resto
    def get_trends(self):
        spanish_trends = self.twitter_api.trends.place(_id=WORD_WOE_ID)
        spain_trends_set = [trend['name']
                                for trend in spanish_trends[0]['trends']]
        return spain_trends_set

    def print_trends(self):
        spanish_trends = self.twitter_api.trends.place(_id=WORD_WOE_ID)
        spain_trends_set = [trend['name']
                                for trend in spanish_trends[0]['trends']]
        print spain_trends_set

    def searchHashes(self, list_hashes):
        print "lista hashes:", str(list_hashes)
        q = list_hashes[0]
        for hash in list_hashes[1:]:
            q += ' OR ' + hash
        print 'q:', q
        count = 100
        search_results = self.twitter_api.search.tweets(q=q, count=count)
        statuses = search_results['statuses']
        for _ in range(5):
            print "Length of statuses", len(statuses)
            print 'metadata'
            print search_results['search_metadata']
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError, e: # No more results when next_results doesn't exist
                print "No more results"
                break
            # Create a dictionary from next_results, which has the following form:
            #  ?max_id=313519052523986943&q=NCAA&include_entities=1
            kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
            print 'kwargs:' , kwargs
            search_results = self.twitter_api.search.tweets(**kwargs)
            statuses += search_results['statuses']
        # Show one sample search result by slicing the list...
        print "Length of statuses (final)", len(statuses)
        for status in statuses:
            print status['text']

    # def print_public_timeline(self):
    #     statuses = self.twitter_api.GetPublicTimeline()
    #     print [s.user.name for s in statuses]

    def testStream(self):
        #print self.twitter_stream_api.statuses
        stream = self.twitter_stream_api.statuses.filter(track='Anonymous')
        for tweet in stream:
            if 'text' in tweet:
                print tweet['text']

    def get_tweets_user(self, screen_name, newer_than=0):
        """
        Si newer_than > 0, se supone que los tweets más antiguos de este usuario ya se han recuperado y solo pedimos
        los más nuevos. Sino, pedimos todos.
        Retorna el id interno del último tweet recogido.
        """
        try:
            # if newer_than > 0:
            #     cursor = tweepy.Cursor(self.twitter_api.user_timeline, id=screen_name, since_id=newer_than)
            # else:
            #     cursor = tweepy.Cursor(self.twitter_api.user_timeline, id=screen_name)


            for status in self.twitter_api.statuses.user_timeline(id=screen_name):
                print status['text']
                last = self.recorder.record_tweet(status)

        except twitter.api.TwitterError as e:
            if e.message == "Not authorized.":
                Utiles.debug.print_debug("El usuario %s requiere permisos para acceder a sus tweets" % (screen_name,))
                Utiles.debug.write_log("El usuario %s requiere permisos para acceder a sus tweets" % (screen_name,))
            else:
                Utiles.debug.print_debug("Twitter error({0}): {1}".format(e.message, e.args), True)
        else:
            return last

if __name__ == '__main__':
    tc = TweetCollector()
    tc.print_trends()
    #tc.searchHashes(tc.get_trends())
    #tc.searchHashes(['TeDoyUnConsejo', 'AmigosParaTodaLaVidaSonAquellosQue'])
    #tc.print_public_timeline()
    #tc.testStream()
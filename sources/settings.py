# -*- coding: iso-8859-15 -*-
__author__ = 'ortigosa'

#mirar https://dev.twitter.com/docs/platform-objects/users
        #ver 'withheld_in_countries']
user_fields = ['id_str', 'statuses_count', 'friends_count', 'location', 'created_at', 'description',
                      'followers_count', 'name', 'protected', 'screen_name', 'url', 'utc_offset']
tweet_fields = ['id_str', 'text', 'coordinates', 'created_at', 'lang', 'retweeted_status',
                'place', 'favorite_count', 'retweet_count', 'possibly_sensitive',
                'in_reply_to_status_id_str', 'in_reply_to_user_id_str', 'entities'
               ]
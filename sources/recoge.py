#!/usr/bin/env python

import time

from TwitterAPI._oldStreamTweetCollector import oldStreamTweetCollector
from Writers.consoleTweetRecorder import ConsoleTweetRecorder

#parametros al filter
#track=lista claves
#follow= lista personas a seguir (x codigo)

tags = ['UIP', 'antidisturbios', 'manifa', 'acampada', 'LeyMordaza', 'RodeaelCongreso',
        'RodeaMoncloa', '15M', '25S', 'Anonymous', '7J']

usuarios = ['@anonymous']
lugares = [-9, 36, 4, 43.5]
# '-4, 40, 3.3, 41' #Madrid
# '-9, 36, 4, 43.5' #Espana
prefijo = "prueba-1"

log = [prefijo, tags, usuarios, lugares]
if __name__ == "__main__":

    # auth = getAuthorizations.get_tweepy_api_auth(1)
    # api = tweepy.API(auth)
    # listen = SListener(api, prefijo, 20000, True)
    # stream = tweepy.Stream(auth, listen)
    # try:
    #     stream.filter(track=tags, follow=usuarios, locations=lugares)
    #     #stream.sample()
    # except KeyboardInterrupt:
    #     print log
    # except Exception as e:
    #     print "error!" + str(e)
    #     stream.disconnect()

    if True:
        try:
            #recorder = FileTweetRecorder(limit=20000)
            recorder = ConsoleTweetRecorder()
            tc = oldStreamTweetCollector(recorder)
            tc.tags= ['anonymous']
            tc.usuarios = usuarios
            #tc.lugares = [-9, 36, 4, 43.5]
            tc.start()
            time.sleep(6000000) #esta espera es para poder ser interrumpido
        except KeyboardInterrupt:
            tc.finish()
            #break

    # tc = TweetCollector()
    # tc.time_max = 60 # segundos
    # tc.tags=['anonymous']
    # tc.debug=True
    # tc.num_app=2
    # tc.start()
    #
    # tc = TweetCollector()
    # tc.time_max = 60 # segundos
    # tc.tags=['anonymous']
    # tc.debug=True
    # tc.num_app=3
    # tc.start()

    #time.sleep(10)
    #tc.finish()
    print "fin principal"
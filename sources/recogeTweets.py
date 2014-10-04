import time

from twython import Twython
from twython import TwythonStreamer

from DBbridge.PostgresWriter import PostgresWriter


APP_KEY = 'dqxwiv8vVLXmc0aYDY6YwnqLK'
APP_SECRET = 'uVsIsUNVZhl4OvIlCQVMTRum7cV1WPJyFszlfSVpzrhvLz0uQo'

contador = 0


class MyStreamer(TwythonStreamer):
    def set_db(self, database):
        self.db = database

    def on_success(self, data):
        if 'in_reply_to_status_id' in data:
            return self.on_status(data)

        raise Exception("tipo de respuesta no reconocido:", str(data))

    #    	elif 'text' in data:
    #    		#print 'text:' + data['text'].encode('utf-8')
    #    		print str(data)
    #    		return False
    #		if 'user' in data:
    #			print "--- user ---"
    #			for k, v in data['user'].iteritems():
    #				print k, v
    #			print "--- fin user ---"
    #		if 'coordinates' in data:
    #			print 'coordinates:' + str(data['coordinates'])
    #		for k, v in data.iteritems():
    #			if k not in ['user', 'text','coordinates']:
    #				print k, v

    def on_status(self, data):
        global contador
        contador += 1
        #self.db.store_data(data)
        if 'id_str' in data:
            print "id_str:" + data['id_str']
        print '--------------------------'
        print contador
        print '--------------------------'

    def on_error(self, status_code, data):
        print status_code

    # Want to stop trying to get data because of the error?
    # Uncomment the next line!
    # self.disconnect()


twitter = Twython(APP_KEY, APP_SECRET)
auth = twitter.get_authentication_tokens()
OAUTH_TOKEN = '2430201408-Blx8DvBoIASbdW9IpcBlnEJVGlMqwmmJoDCFc9l'
OAUTH_TOKEN_SECRET = 'wAgvoFmjNGpEW2WDupaBF93D9J0Ihc0Rr2F9xAMDptKsX'
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
conexionBD = PostgresWriter()
stream.set_db(conexionBD)

#twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
#ACCESS_TOKEN = twitter.obtain_access_token()
#stream = MyStreamer(APP_KEY, access_token=ACCESS_TOKEN)

try:
    start = time.time()
#stream.statuses.filter(language="es")
#stream.statuses.filter(locations='-4, 40, 3.3, 41') #Madrid
    stream.statuses.filter(locations='-9, 36, 4, 43.5') #Espana

except KeyboardInterrupt:
    end = time.time()
    print "procesados " + str(contador) + " tweets en" + str(end - start) + " segundos"
    conexionBD.close()

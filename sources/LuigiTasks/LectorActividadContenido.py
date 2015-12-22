
import codecs
import json

if __name__ == '__main__':
	fichero = codecs.open("ficheros/GetActividadPorContenidoTweet(EnCasaDeElisa)", "r", "utf-8")
	dicc = json.loads(fichero.read())
	print dicc
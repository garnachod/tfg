# -*- coding: utf-8 -*-
import string
import re
class PalabrasDeTweet(object):
	"""docstring for PalabrasDeTweet"""
	def __init__(self):
		super(PalabrasDeTweet, self).__init__()
		#self.delimiters = '*|\n|(|)|,|;|.| |?|¿|¡|!|\"|\'|[|]|{|}|-|:|<|>'
		self.delimiters = r' |,|\n|\:|\;|\*|\?|\'|\¡|\¿|\[|\]|\{|\}|\-|\<|\>|\»|\«|\_|\"|\!|\.|&gt|\#|\&|\$|\~|\(|\)|\%|\=|\|'

	def stringToAscii(self, cadena):
		return filter(lambda x: x in string.printable, cadena)
		
	def getPalabrasFromString(self, cadena):
		return re.split(self.delimiters, cadena)

	def removeLinks(self, cadena):
		#r'^https?:\/\/.*[\r\n]*'
		cadena = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', cadena, flags=re.IGNORECASE)
		return cadena

	def removeTwitterUsers(self, cadena):
		cadena = re.sub(r'\@([0-9]|[a-zA-Z]|\_)+', ' ', cadena)
		return cadena

	def removeNumbers(self, cadena):
		cadena = re.sub(r'[0-9]+', ' ', cadena)
		return cadena

	def getPalabrasFromStringNormalized(self, cadena):
		listaPalabrasAux = self.getPalabrasFromString(cadena)

		listaPalabras = []
		for palabra in listaPalabrasAux:
			if len(palabra) < 3:
				continue

			palabra = palabra.lower()
			palabra = palabra.replace("á", "a")
			palabra = palabra.replace("é", "e")
			palabra = palabra.replace("í", "i")
			palabra = palabra.replace("ó", "o")
			palabra = palabra.replace("ú", "u")
			palabra = palabra.replace("Á", "a")
			palabra = palabra.replace("É", "e")
			palabra = palabra.replace("Í", "i")
			palabra = palabra.replace("Ó", "o")
			palabra = palabra.replace("Ú", "u")
			palabra = palabra.replace("Ü", "u")
			palabra = palabra.replace("ü", "u")
			palabra = palabra.replace("Ñ", "n")
			palabra = palabra.replace("ñ", "n")
			palabra = self.stringToAscii(palabra)
			
			listaPalabras.append(palabra)

		return listaPalabras

"""pruebas unitarias

"""
if __name__ == '__main__':
	separador = PalabrasDeTweet()
	#print separador.getPalabrasFromString("Goole Project Zero publica tres 0-days y un exploit de OS X: Project ZeroEl equipo de Google dentro de Zero Pr... http://bit.ly/1yUGqGw")
	print separador.getPalabrasFromStringNormalized("AááÁí sdfdfs SDFDFS")
	print separador.removeLinks("test de link ^^ http://t.co/3OGCCtH93K y un exploit de OS X: Project ZeroEl equipo d")
	print separador.removeNumbers("666 dfsfgdfg 562 sdffg")
	print separador.removeTwitterUsers('dsfsdfd @garnachod garnachod @123g @ 34354')
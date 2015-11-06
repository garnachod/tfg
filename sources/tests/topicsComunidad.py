# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from DBbridge.ConsultasCassandra import ConsultasCassandra
from DBbridge.ConsultasNeo4j import ConsultasNeo4j
import codecs
import re


re_urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
re_hastag = re.compile(r'\#[0-9a-zA-Z]+')
re_tuser = re.compile(r'@[a-zA-Z0-9_]+')

def cleanLine(line):
	line = re_urls.sub(" ", line)
	line = re_hastag.sub(" ", line)
	line = re_tuser.sub(" ", line)
	line = line.replace("?", " ")
	line = line.replace("!", " ")
	line = line.replace("...", " ")
	#line = line.replace(".", " DOT ")
	#line = line.replace(",", " COMMA ")
	line = line.replace(".", " ")
	line = line.replace(",", " ")
	line = line.replace("/", " ")
	line = line.replace("\\", " ")
	line = line.replace("\"", " ")
	line = line.replace("\'", " ")
	line = line.replace("-", " ")
	line = line.replace(")", " ")
	line = line.replace("(", " ")
	line = line.replace("'", " ")
	line = line.replace(":", " ")
	line = line.replace(";", " ")
	line = line.replace(u"¿", " ")
	line = line.replace(u"’", " ")
	line = line.replace(u"‘", " ")
	line = line.replace(u"…", " ")
	line = line.replace("+", " ")
	line = line.replace("_", " ")
	line = line.replace(u"´", " ")
	line = line.replace(u"`", " ")
	line = line.replace(u"", " ")
	line = line.replace(u"", " ")
	line = line.replace(u"", " ")
	line = line.replace(u"", " ")
	line = line.replace(u"«", " ")
	line = line.replace(u"»", " ")
	line = line.replace(u"“", " ")
	line = line.replace(u"”", " ")
	line = line.replace(u"¨", " ")
	line = line.replace(u"á", "a")
	line = line.replace(u"é", "e")
	line = line.replace(u"í", "i")
	line = line.replace(u"ó", "o")
	line = line.replace(u"ú", "u")
	line = line.replace(u"ü", "u")
	line = line.replace(u"ñ", "n")

	return line


if __name__ == '__main__':
	consultas = ConsultasCassandra()
	user_id = consultas.getUserIDByScreenNameCassandra("Braun")

	consultasGrafo = ConsultasNeo4j()
	identificadores = consultasGrafo.getListaIDsSeguidoresByUserID(user_id)

	diccionario = {}


	fout = codecs.open("lowcorpus.txt", "w", "utf-8")
	for identificador in identificadores:
		tweets = consultas.getTweetsUsuarioCassandra(long(identificador), limit=10000)
		if len(tweets) > 1:
			for tweet in tweets:
				texto = tweet.status.replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". ")
				texto = texto.lower()
				palabras = cleanLine(texto).split()
				if len(palabras) > 2:
					for palabra in palabras:
						if palabra in diccionario:
							diccionario[palabra] += 1
						else:
							diccionario[palabra] = 1


	tuples = []
	for palabra in diccionario:
		tuples.append((palabra, diccionario[palabra]))

	tuples = sorted(tuples, key=lambda tupla: tupla[1], reverse=True)

	fout = codecs.open("topics.txt", "w", "utf-8")
	for i in range(1000):
		fout.write(tuples[i][0] + " " + str(tuples[i][1]))
		fout.write("\n")

	fout.close()

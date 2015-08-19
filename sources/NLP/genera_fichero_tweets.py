# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from textblob import TextBlob
from DBbridge.ConsultasCassandra import ConsultasCassandra
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import codecs
import re
import string
#cadena = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', cadena, flags=re.IGNORECASE)
re_urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
re_hastag = re.compile(r'\#[0-9a-zA-Z]+')

def stringToAscii(cadena):
	return filter(lambda x: x in string.printable, cadena)

def cleanLine(line):
	line = re_urls.sub(" URL ", line)
	line = re_hastag.sub(" HASTAG ", line)
	line = line.replace("?", " QUESTION ")
	line = line.replace("!", " EXCLAMATION ")
	line = line.replace("...", " DOTDOTDOT ")
	line = line.replace("\n", " ")
	#line = line.replace(".", " DOT ")
	#line = line.replace(",", " COMMA ")
	line = line.replace(".", " ")
	line = line.replace(",", " ")
	line = line.replace("/", " ")
	line = line.replace("\\", " ")
	line = line.replace("-", " ")
	line = line.replace("'", " ")
	line = line.replace(":", " ")
	line = line.replace(u"’", " ")
	line = line.replace(u"‘", " ")
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
	line = stringToAscii(line)

	return line


if __name__ == '__main__':
	consultas = ConsultasCassandra()
	print "buscando tweets"
	tweets = consultas.getAllTweetsNoRtStatusCassandra()
	print "tweets buscados"
	fOut = codecs.open("tweets_clean.txt", "w", "utf-8")
	stemmer = SnowballStemmer("spanish")
	lemma = WordNetLemmatizer()
	for tweet in tweets:
		status = tweet[0]
		status = status.lower()
		status = cleanLine(status)
		textB = TextBlob(status)
		for palabra in textB.words:
			#palabra = stemmer.stem(palabra)
			#palabra = lemma.lemmatize(palabra)
			if len(palabra) <= 1:
				pass
			else:
				fOut.write(palabra + " ")

		fOut.write("\n")


	fOut.close()

	
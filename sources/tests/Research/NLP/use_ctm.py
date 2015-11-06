# -*- coding: utf-8 -*-
# gensim modules
from gensim import utils
from gensim.models.ctmmodel import CtmModel
from gensim.corpora.dictionary import Dictionary
from gensim import corpora
from textblob import TextBlob
import codecs
import re


re_urls = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
re_hastag = re.compile(r'\#[0-9a-zA-Z]+')
re_tuser = re.compile(r'^@[a-zA-Z0-9_]+')

def cleanLine(line):
	line = re_urls.sub(" URL ", line)
	line = re_hastag.sub(" HASTAG ", line)
	line = re_tuser.sub(" USER ", line)
	line = line.replace("?", " QUESTION ")
	line = line.replace("!", " EXCLAMATION ")
	line = line.replace("...", " DOTDOTDOT ")
	line = line.replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". ")
	#line = line.replace(".", " DOT ")
	#line = line.replace(",", " COMMA ")
	line = line.replace(".", " ")
	line = line.replace(",", " ")
	line = line.replace("/", " ")
	line = line.replace("\\", " ")
	line = line.replace("-", " ")
	line = line.replace(")", " ")
	line = line.replace("(", " ")
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

	return line

def read_file(location):
	cadena = ''
	fin = codecs.open(location, "r", "utf-8")
	for line in fin:
		line = line.lower()
		cadena += cleanLine(line) + ' '

	return cadena

if __name__ == '__main__':
	root_files = "/media/dani/data/ficherosPrueba_plsa/"
	filenames = ['AlexMonthy.txt', 'Gameloft_Spain.txt', 'PlayStationES.txt', 'WillyrexYT.txt', 'Alvaro845.txt', 'mangelrogel.txt', 'steam_games.txt','Xodaaaa.txt', 'AudazCarlos.txt', 'Nestle_es.txt', 'Thetoretegg.txt', 'xPekeLoL.txt', 'bysTaXx.txt', 'NexxuzHD.txt', 'vegetta777.txt', 'yuyacst.txt', 'Fernanfloo.txt', 'Outconsumer.txt', 'Wigetta.txt']

	textos = []
	for filename in filenames:
		texto = read_file(root_files+filename)
		textB = TextBlob(texto)
		textoFinal = []
		for palabra in textB.words:
			textoFinal.append(palabra)

		textos.append(textoFinal)

	fout = codecs.open("/media/dani/data/ficherosPrueba_plsa/test_r.csv", "w", "utf-8")
	for texto in textos:
		for palabra in texto:
			fout.write(palabra + " ")
		fout.write("\n")

	fout.close()
	#dictionary = Dictionary(textos)
	#corpus = [dictionary.doc2bow(text) for text in textos]
	#corpora.MmCorpus.serialize('/media/dani/data/ficherosPrueba_plsa/corpus.mm', corpus)
	#corpus = corpora.MmCorpus('/media/dani/data/ficherosPrueba_plsa/corpus.mm')
	#ctm = CtmModel(corpus)
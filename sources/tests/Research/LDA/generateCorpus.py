# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../../')
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
	line = line.replace(u"¿", " ")
	line = line.replace(u"¡", " ")
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

	stopwords = {"http":True, "a":True, "about":True, "above":True, "after":True, "again":True, "against":True, "all":True, "am":True, "an":True, "and":True, "any":True, "are":True, "aren't":True, "as":True, "at":True, "be":True, "because":True, "been":True, "before":True, "being":True, "below":True, "between":True, "both":True, "but":True, "by":True, "can't":True, "cannot":True, "could":True, "couldn't":True, "did":True, "didn't":True, "do":True, "does":True, "doesn't":True, "doing":True, "don't":True, "down":True, "during":True, "each":True, "few":True, "for":True, "from":True, "further":True, "had":True, "hadn't":True, "has":True, "hasn't":True, "have":True, "haven't":True, "having":True, "he":True, "he'd":True, "he'll":True, "he's":True, "her":True, "here":True, "here's":True, "hers":True, "herself":True, "him":True, "himself":True, "his":True, "how":True, "how's":True, "i":True, "i'd":True, "i'll":True, "i'm":True, "i've":True, "if":True, "in":True, "into":True, "is":True, "isn't":True, "it":True, "it's":True, "its":True, "itself":True, "let's":True, "me":True, "more":True, "most":True, "mustn't":True, "my":True, "myself":True, "no":True, "nor":True, "not":True, "of":True, "off":True, "on":True, "once":True, "only":True, "or":True, "other":True, "ought":True, "our":True, "ours 	ourselves":True, "out":True, "over":True, "own":True, "same":True, "shan't":True, "she":True, "she'd":True, "she'll":True, "she's":True, "should":True, "shouldn't":True, "so":True, "some":True, "such":True, "than":True, "that":True, "that's":True, "the":True, "their":True, "theirs":True, "them":True, "themselves":True, "then":True, "there":True, "there's":True, "these":True, "they":True, "they'd":True, "they'll":True, "they're":True, "they've":True, "this":True, "those":True, "through":True, "to":True, "too":True, "under":True, "until":True, "up":True, "very":True, "was":True, "wasn't":True, "we":True, "we'd":True, "we'll":True, "we're":True, "we've":True, "were":True, "weren't":True, "what":True, "what's":True, "when":True, "when's":True, "where":True, "where's":True, "which":True, "while":True, "who":True, "who's":True, "whom":True, "why":True, "why's":True, "with":True, "won't":True, "would":True, "wouldn't":True, "you":True, "you'd":True, "you'll":True, "you're":True, "you've":True, "your": True, "yours":True, "yourself":True, "yourselves" :True}


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
						if palabra not in stopwords:
							if len(palabra) > 2:
								fout.write(palabra)
								fout.write(" ")
			fout.write("\n")

	fout.close()
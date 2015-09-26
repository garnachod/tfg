# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandra import ConsultasCassandra
import pickle
import codecs
import re

""" \r u'\u000D'"""
""" NEXT LINE: U+0085"""
""" Line Separator: U+2028 """
""" Paragraph Separator, U+2029 """

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

if __name__ == '__main__':
	namefile = "/media/dani/tweetsBin.b"
	tweets = pickle.load(open(namefile, "rb"))
	usuariosDic = {}

	for tweet in tweets:
		tuser = tweet.tuser
		status = tweet.status
		if tuser in usuariosDic:
			usuariosDic[tuser].append(status)
		else:
			usuariosDic[tuser] = [status]

	fout = codecs.open("/media/dani/tweetsByUser.txt", "w", "utf-8")
	for tuser in usuariosDic:
		fout.write(str(tuser))
		fout.write("\n")
		
		for tweet in usuariosDic[tuser]:
			texto = tweet.replace("\n", ". ").replace("\r", ". ").replace(u"\u0085", ". ").replace(u"\u2028", ". ").replace(u"\u2029", ". ")
			fout.write(cleanLine(texto))
			fout.write(" ")

		fout.write("\n")

	fout.close()

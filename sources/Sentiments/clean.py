import codecs

if __name__ == '__main__':
	ficheros = ['tweets_pos.txt', 'tweets_neg.txt', 'tweets_es.txt']
	diccionario = {}

	for i, nombre_fichero in enumerate(ficheros):
		f_in = codecs.open(nombre_fichero, "r", "utf-8")
		for line in f_in:
			if line in diccionario:
				pass
			else:
				diccionario[line] = i

		f_in.close()

	fout_pos = codecs.open('tweets_pos_clean.txt', "w", "utf-8")
	fout_neg = codecs.open('tweets_neg_clean.txt', "w", "utf-8")
	fout = codecs.open('tweets_clean.txt', "w", "utf-8")
	for key in diccionario:
		if diccionario[key] == 0:
			fout_pos.write(key)
		elif diccionario[key] == 1:
			fout_neg.write(key)
		else:
			fout.write(key)

	fout_pos.close()
	fout_neg.close()
	fout.close()
import codecs

if __name__ == '__main__':
	entrada = codecs.open("i18n", "r", "utf-8")
	salida = codecs.open("i18n_compiled", "w", "utf-8")

	last_identif = None
	for line in entrada.readlines():
		#comentario
		if line[0] == '#':
			pass
		elif line[0] == '[':
			#identificador
			if last_identif == None:
				salida.write('item = i18n_item()\n')
			else:
				salida.write('self.diccionario["'+last_identif+'"] = item\n')

			line = line.replace("[","")
			line = line.replace("]","")
			line = line.replace("\n","")
			last_identif = str(line)
		else:
			keyAndText = line.split("|")
			keyAndText[1] = keyAndText[1].replace("\n","")
			salida.write('item["'+keyAndText[0]+'"] = "'+keyAndText[1] + '"\n')

	salida.write('self.diccionario["'+last_identif+'"] = item\n')
	salida.close()
	entrada.close()
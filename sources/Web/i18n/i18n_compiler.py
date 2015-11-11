import codecs

def traduceTuplaAString(tupla):
	cadena = ''
	for item in tupla:
		cadena += item + "\n"

	return cadena

if __name__ == '__main__':
	entrada = codecs.open("i18n", "r", "utf-8")
	salida = codecs.open("i18n.py", "w", "utf-8")

	last_identif = None
	cadenas = ('# -*- coding: utf-8 -*-',
			  'from i18n_item import i18n_item',
			  'class i18n(object):',
			  '\t#Codigo autogenerado', 
			  '\tclass __impl:',
			  '\t\t# implementacion del singleton',
			  '\t\tdef __init__(self):',
			  '\t\t\tself.diccionario = {}',
			  '\t\t\tself.inicializa()',
			  '\t\tdef __getitem__(self, index):',
			  '\t\t\treturn self.diccionario[index]',
			  '\t\tdef inicializa(self):'
	)
	cadena = traduceTuplaAString(cadenas)
	salida.write(cadena)
	for line in entrada.readlines():
		#comentario
		if line[0] == '#':
			pass
		elif line[0] == '[':
			#identificador
			if last_identif == None:
				salida.write('\t\t\titem = i18n_item()\n')
			else:
				salida.write('\t\t\tself.diccionario["'+last_identif+'"] = item\n')

			line = line.replace("[","")
			line = line.replace("]","")
			line = line.replace("\n","")
			last_identif = str(line)
		else:
			keyAndText = line.split("|")
			keyAndText[1] = keyAndText[1].replace("\n","")
			salida.write('\t\t\titem["'+keyAndText[0]+'"] = "'+keyAndText[1] + '"\n')

	salida.write('\t\t\tself.diccionario["'+last_identif+'"] = item\n')

	cadenas = (
		'\t# storage for the instance reference',
		'\t__instance = None',
		'\tdef __init__(self):',
		'\t\tif i18n.__instance is None:',
		'\t\t\ti18n.__instance = i18n.__impl()',
		'\tdef __getattr__(self, attr):',
		'\t\t# Delegate access to implementation',
		'\t\treturn getattr(self.__instance, attr)',
		'\tdef __getitem__(self, index):',
		'\t\treturn self.__instance[index]',
		'\tdef __setattr__(self, attr, value):',
		'\t\t#Delegate access to implementation',
		'\t\treturn setattr(self.__instance, attr, value)',
		'#pruebas unitarias',
		'if __name__ == \'__main__\':',
		'\tinternationatization = i18n()',
		'\tprint internationatization["session_info_login"]["es"]'
	)
	cadena = traduceTuplaAString(cadenas)
	salida.write(cadena)
	salida.close()
	entrada.close()
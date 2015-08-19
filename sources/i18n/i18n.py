# -*- coding: utf-8 -*-
from i18n_item import i18n_item
class i18n(object):
	#Codigo autogenerado
	class __impl:
		# implementacion del singleton
		def __init__(self):
			self.diccionario = {}
			self.inicializa()
		def __getitem__(self, index):
			return self.diccionario[index]
		def inicializa(self):
			item = i18n_item()
			item["en"] = "You must log in to the application"
			item["es"] = "Debes iniciar sesión en la aplicación"
			self.diccionario["session_info_login"] = item
	# storage for the instance reference
	__instance = None
	def __init__(self):
		if i18n.__instance is None:
			i18n.__instance = i18n.__impl()
	def __getattr__(self, attr):
		# Delegate access to implementation
		return getattr(self.__instance, attr)
	def __getitem__(self, index):
		return self.__instance[index]
	def __setattr__(self, attr, value):
		#Delegate access to implementation
		return setattr(self.__instance, attr, value)
#pruebas unitarias
if __name__ == '__main__':
	internationatization = i18n()
	print internationatization["session_info_login"]["es"]

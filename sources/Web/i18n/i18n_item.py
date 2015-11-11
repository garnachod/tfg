import re
class i18n_item(object):
	"""docstring for i18n_item"""
	h = re.compile(r',|;')

	def __init__(self):
		super(i18n_item, self).__init__()
		self.langs = {}

	def parseHeaderHTML(self, header):
		elements = i18n_item.h.split(header)
		if len(elements) == 1:
			return i18n_item.h.split(header)[0]
		return i18n_item.h.split(header)[1]

	def __getitem__(self, key):
		key = self.parseHeaderHTML(key)
		if key in self.langs:
			return self.langs[key]
		else:
			return self.langs['en']

	def __setitem__(self, index, value):
		self.langs[index] = value
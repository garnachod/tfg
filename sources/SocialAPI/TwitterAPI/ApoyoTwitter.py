from DBbridge.ConsultasGeneral import ConsultasGeneral

class ApoyoTwitter(object):
	"""docstring for ApoyoTwitter"""
	def __init__(self):
		super(ApoyoTwitter, self).__init__()
		self.consultas = ConsultasGeneral()

	def getLastTweetCollected(self, screen_name):
		return self.consultas.getLastTweetCollectedScreenName(screen_name)
		

	def setLastUserTweet(self, screen_name, maximo):
		return self.consultas.setLastTweetCollectedScreenName(screen_name, maximo)
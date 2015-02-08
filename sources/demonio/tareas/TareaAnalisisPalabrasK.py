from TareaProgramadaBusquedaKeywords import TareaProgramadaBusquedaKeywords
from DBbridge.ConsultasGeneral import ConsultasGeneral
from MachineLearning.ClasificadorTweets import ClasificadorTweets


class TareaAnalisisPalabrasK(TareaProgramadaBusquedaKeywords):
	"""docstring for TareaAnalisisPalabrasK"""
	def __init__(self):
		super(TareaAnalisisPalabrasK, self).__init__()
		self.tipo = "AnalisisPalabrasKeywords"
		
	def doPostProc(self):
		tweets_id = self.consultas.getTweetsIdBusquedaNoAnalizada(self.search_id)
		clasificaTweet = ClasificadorTweets()

		for row in tweets_id:

			clase = clasificaTweet.clasificaTweetById(row[0])
			self.consultas.insertTweetAnalizado(row[0], clase)

		return True

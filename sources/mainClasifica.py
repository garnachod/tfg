from MachineLearning.ClasificaTweet import ClasificaTweet
from DBbridge.ConsultasGeneral import ConsultasGeneral
import time

if __name__ == '__main__':
	clasificaTweet = ClasificaTweet()
	consultas = ConsultasGeneral()


	start = time.time()
	status = consultas.getTweetStatus(7922)
	for i in range(0, 1000):
		print clasificaTweet.clasificaTweetByStatus(status)

	end = time.time()
	print end - start

	print clasificaTweet.clasificaTweetById(46303)
	
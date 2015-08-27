# -*- coding: utf-8 -*-
import os
import sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from DBbridge.ConsultasCassandra import ConsultasCassandra

if __name__ == '__main__':
	consultas = ConsultasCassandra()
	ids = consultas.getAllIDsTweets()

	particiones = []
	n_particiones = 8

	ids = sorted(ids)
	ntweets = len(ids)
	print ntweets
	tweets_particion = ntweets / n_particiones

	last_partition_last_id = 0
	particion_count = 0

	for identificador in ids:
		particion_count += 1
		if particion_count > tweets_particion:
			particiones.append((last_partition_last_id, identificador))
			last_partition_last_id = identificador
			particion_count = 0

	print particiones


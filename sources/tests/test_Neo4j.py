from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSeguidoresNeo4j import EscritorSeguidoresNeo4j
from SocialAPI.TwitterAPI.RecolectorSeguidoresShort import RecolectorSeguidoresShort
import time

if __name__ == '__main__':
	consultas = ConsultasWeb()
	#usuario = "@p_molins"
	usuario = "@Dowrow"
	searchID = consultas.setAppSearchAndGetId(usuario, 1)
	

	inicio = time.time()

	escritores = [EscritorSeguidoresNeo4j(searchID)]
	recolector = RecolectorSeguidoresShort(escritores)
	recolector.recolecta(usuario)

	fin = time.time()
	consultas.setAppSearchTime(searchID, fin - inicio)
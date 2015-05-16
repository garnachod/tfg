from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSeguidores import EscritorSeguidores
from SocialAPI.TwitterAPI.RecolectorSeguidores import RecolectorSeguidores
from DBbridge.ConexionSQL import ConexionSQL
import time

if __name__ == '__main__':
	consultas = ConsultasWeb()
	usuario = "@garnachod"
	searchID = consultas.setAppSearchAndGetId(usuario, 1)
	

	inicio = time.time()

	escritor = EscritorSeguidores(ConexionSQL(), searchID)
	recolector = RecolectorSeguidores(escritor)
	recolector.recolecta(usuario)

	fin = time.time()
	consultas.setAppSearchTime(searchID, fin - inicio)
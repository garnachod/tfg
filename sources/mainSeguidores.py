from DBbridge.ConsultasWeb import ConsultasWeb
from DBbridge.EscritorSeguidores import EscritorSeguidores
from SocialAPI.TwitterAPI.RecolectorSeguidores import RecolectorSeguidores
from DBbridge.ConexionSQL import ConexionSQL
import time

if __name__ == '__main__':
	consultas = ConsultasWeb()
	searchID = consultas.setAppSearchAndGetId(texto, 1)
	usuario = "@garnachod"

	inicio = time.time()

	escritor = EscritorSeguidores(ConexionSQL(), self.searchID)
	recolector = RecolectorSeguidores(escritor)
	recolector.recolecta(usuario)

	fin = time.time()
	consultas.setAppSearchTime(searchID, fin - inicio)
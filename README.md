#TFG
===
Aplicación web:
* Recolección de Tweets
* Clasificación Automática
* Estadisticas sencillas

#TFM
===
##Posibles puntos (más probables):
* Migración a Cassandra (índices de texto no tan completos como en mongo) o MongoDB
	* Si se usa Cassandra hay que tener en cuenta la posible utilización de un gestor de indices externo
* Spark (si se usa, la base de datos debe ser Cassandra)
	* Tiene análisis de grafos
	* pagerank <- https://github.com/apache/spark/blob/master/examples/src/main/python/pagerank.py
* Neo4j <- base de datos, centrada en grafos
	* interesante si no se desea crear o usar una herramienta de visualización de grafos(Brown Dispatching)

* visualización de grafos:
	* por ejemplo...
	* http://arborjs.org/
	* http://sigmajs.org/

* Mejores clasificadores para texto:
	* (es lo mismo que uso +o-, pero añadiendo TF-IDF) https://en.wikipedia.org/wiki/Bag-of-words_model (la red neuronal se encarga de crear los pesos, pero se puede ayudar)

* Clasificación de lenguaje natural
	* doctorado <- https://www.cl.cam.ac.uk/techreports/UCAM-CL-TR-721.pdf
	* investigación de stanford <- http://nlp.stanford.edu/software/classifier.shtml
	* redes neuronales recurrentes?

##Posibles puntos (menos probables o al menos complicados de integrar):
*clasificación de imágenes <- CAFFE
*clasificación de sentimientos <- http://nlp.stanford.edu/sentiment/code.html



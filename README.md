#TFG
===
Aplicación web:
* Recolección de Tweets
* Clasificación Automática
* Estadisticas sencillas

##### Arrancar el sistema
* Cambiar la información de conexión en DBbrige/ConexionSQL.py
* Ejecutar DBbrige/CreaTablas.py se crea un usuario por defecto, se puede cambiar si no se conoce la contraseña
	* En test hay un fichero para crear la hash de la contraseña
* Arrancar la aplicación con runserver.py
* Poner en el navegador localhost:5000
* Iniciar sesión con el usuario por defecto
* En la interfaz de administrador, introducir una apiKey de twitter


#TFM
===
##Posibles puntos (más probables):
* Migración a Cassandra (FINALIZADO, 20 Agosto)
	* https://github.com/Stratio/cassandra-lucene-index

* Spark (EN USO 20 Agosto) mejora las consultas de Cassandra complejas en un 50% de tiempo (Hay que hacer casi todo a mano, pero va jodidamente rápido)
	* Tiene análisis de grafos
	* pagerank <- https://github.com/apache/spark/blob/master/examples/src/main/python/pagerank.py

* Neo4j <- base de datos, centrada en grafos (SIGUENTE PASO)
	* interesante si no se desea crear o usar una herramienta de visualización de grafos(Brown Dispatching)

* visualización de grafos:
	* por ejemplo...
	* http://arborjs.org/
	* http://sigmajs.org/

* Mejores clasificadores para texto:
	* Que le follen a tf-idf, Paragraph vector (doc2vec) + lo que sea


* Búsquedas en tiempo real al estilo TweetDeck pero con clasificación automática.(MUY IMPORTANTE)


##Posibles puntos (menos probables o al menos complicados de integrar):
* clasificación de imágenes <- CAFFE
* clasificación de sentimientos <- http://nlp.stanford.edu/sentiment/code.html
* clasificación de sentimientos <- https://github.com/nltk/nltk/wiki/Sentiment-Analysis
* clasificación de sentimientos <- http://textblob.readthedocs.org/en/dev/quickstart.html#sentiment-analysis



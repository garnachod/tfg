#TFG
===
Aplicación web:
* Recolección de Tweets
* Clasificación Automática
* Estadisticas sencillas

#### Arrancar el sistema
##### Actualizado (23 Agosto)
* Cambiar la información de conexiones en Config/Conf.py
* Ejecutar DBbrige/PostgreSQL/CreaTablas.py se crea un usuario por defecto (que hay que editar)
	* En test hay un fichero para crear la hash de la contraseña
* Ejecutar DBbrige/Cassandra/CreaTablas.py
* Ejecutar Neo4j/CreaRelaciones.py
* Arrancar la aplicación con runserver.py
* Poner en el navegador localhost:5000
* Iniciar sesión con el usuario por defecto
* En la interfaz de administrador, introducir una apiKey de twitter
* Ir a demonio si se necesita el Daemon de tareas en segundo plano para más info


#TFM
===
##Posibles puntos (más probables):
* Migración a Cassandra (FINALIZADO, 20 Agosto)
	* https://github.com/Stratio/cassandra-lucene-index

* Spark (EN USO 20 Agosto) mejora las consultas de Cassandra complejas en un 50% de tiempo (Hay que hacer casi todo a mano, pero va jodidamente rápido)
	* Tiene análisis de grafos
	* pagerank <- https://github.com/apache/spark/blob/master/examples/src/main/python/pagerank.py

* Neo4j <- base de datos, centrada en grafos (Funcionando 22 Agosto)
	* Se va a usar una libreria de visualización de grafos JS
		* por ejemplo...
		* http://arborjs.org/
		* http://sigmajs.org/
	* Va algo lento en las inserciones

* Algoritmos de grafos (EN USO 3 Octubre) :
	* Librería: networkx

* Mejores clasificadores para texto:
	* Que le follen a tf-idf, Paragraph vector (doc2vec) + lo que sea


* Búsquedas en tiempo real al estilo TweetDeck pero con clasificación automática.(MUY IMPORTANTE) (Siguente paso :-( JavaScriptCaca)

##Posibles puntos (Poco a poco...):
* clasificación de imágenes <- CAFFE
* clasificación de sentimientos <- http://nlp.stanford.edu/sentiment/code.html
* clasificación de sentimientos <- https://github.com/nltk/nltk/wiki/Sentiment-Analysis
* clasificación de sentimientos <- http://textblob.readthedocs.org/en/dev/quickstart.html#sentiment-analysis



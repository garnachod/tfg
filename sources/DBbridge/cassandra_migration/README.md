##### instalar
http://docs.datastax.com/en/getting_started/doc/getting_started/gettingStartedDeb_t.html

##### instalar blist y cassandra-driver para python
* sudo pip install blist
* sudo pip install cassandra-driver

##### arrancar la interfaz de cassandra para crear el keyspace
```
 cd /usr/bin/
 ./cqlsh
 CREATE KEYSPACE twitter WITH REPLICATION = { "class" : "SimpleStrategy", "replication_factor" : 1 };
```

##### ya se pueden crear las "tablas"
* utilizar el fichero CreaTablas.py

#### Pruebas de Rendimiento
* 5 Nodos Raspberry Pi 2, 2103 ops/s
* 1 Hilo AMD Phenom(tm) II X6 1055T / 8G Ram, 3127 ops/s
* 6 Hilo AMD Phenom(tm) II X6 1055T / 8G Ram, 17408 ops/s

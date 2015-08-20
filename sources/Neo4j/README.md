# Instalación (La una de la mañana)
* sudo su
* wget -O - http://debian.neo4j.org/neotechnology.gpg.key| apt-key add -
* echo 'deb http://debian.neo4j.org/repo stable/' > /etc/apt/sources.list.d/neo4j.list
* apt-get update -y
* apt-get install install neo4j
* pip install py2neo


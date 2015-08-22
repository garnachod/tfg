# DAEMON
El demonio es un proceso residente. Arranca automáticamente, si se desea instalar, leer instruccionesDaemon.txt

# Librería Python
sudo pip install python-daemon

## Diseño de clases UML
Si se desea crear una nueva tarea en segundo plano (otro tipo)
* Extender Tarea Programada
* Añadir el nombre que se haya definido como identificador del tipo de tarea al Factory Method
![Alt text](../DesignImages/DiagramadeclaseDemonio.png?raw=true "Diseño de clases")
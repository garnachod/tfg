# Módulo Machine Learning 

Este módulo se encarga de la funcionalidad de clasificar automáticamente tweets, útiliza clasificadores genéricos que pueden se utilizados para cualquier tarea de clasificación.

## Diagrama de clases UML de clasificadores
* Si se desea hacer o encapsular un clasificador sólo ha de extender de la clase Clasificador
* Los ficheros de datos se guardan en un array de "Instance"
	* En la última posición está la clase
* Los clasificadores guardan la información del entrenamiento en un JSON
	* Pueden no ser sólo los peso, si no que puedes guardar la localización externa del modelo

![Alt text](../DesignImages/DiagramadeclaseMachineAPR.png?raw=true "Diseño de clases")

## Diagrama de clases UML de generadores ficheros de entrenamiento desde tweets
Estas clases se encargan de generar los ficheros de entrenamiento, generan un .ARFF. En posteriores iteraciones se eliminarán para simplificar el diseño usando librerias de procesamiento de lenguaje natural.

![Alt text](../DesignImages/DiagramadeclaseMachineText.png?raw=true "Diseño de clases")
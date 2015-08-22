# -*- coding: utf-8 -*-

import logging
import os
import time
import random


#de python-daemon import runner

from daemon import runner
from demonio.tareas.GeneraTareasDesdeDB import GeneraTareasDesdeDB
from demonio.tareas.TareaProgramada import TareaProgramada


class App():

    def __init__(self):

        #Se define unos path estándar en linux

        self.stdin_path = '/dev/null'

        #self.stdout_path = '/dev/tty'

        #self.stderr_path = '/dev/tty'
        self.stdout_path = '/dev/null'

        self.stderr_path = '/dev/null'

        #Se define la ruta del archivo pid del demonio.

        self.pidfile_path = '/var/run/demonioTareasTwitter.pid'

        self.pidfile_timeout = 5


    def run(self):

        i = 0

        while True:
            time.sleep(1)
            #codigo principal
            generador = GeneraTareasDesdeDB()
            tareas = generador.genera()
            random.shuffle(tareas)
            logger.info("Numero de tareas %s" %len(tareas))
            if tareas is None:
                pass
            else:
                for tarea in tareas:
                    try:
                        tarea.doSearch()
                    except Exception, e:
                        logger.error("%s" %str(e))

                time.sleep(100)

                for tarea in tareas:
                    try:
                        tarea.doPostProc()
                    except Exception, e:
                        logger.error("%s" %str(e))
                        
            #fin de codigo principal

            i += 1

            #Diferentes niveles de registro de bitacora

            #logger.debug("Debug message %s" %i)

            logger.info("Iteraciones desde arrancado %s" %i)
            #logger.warn("Warning message %s" %i)

            #logger.error("Error message %s" %i)

            


#Se crea la instancia de la clase

app = App()

#define la instancia de la clase logging para generar la bitacora

logger = logging.getLogger("demonioTareasTwitter log")

logger.setLevel(logging.INFO)

#Se define el forma del log

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.FileHandler("/var/log/demonioTareasTwitter/demonioTareasTwitter.log")

handler.setFormatter(formatter)

logger.addHandler(handler)


#Se ejecuta el demonio llamando al objeto app

daemon_runner = runner.DaemonRunner(app)

#Esto evita que el archivo log no se cierre durante la ejecución del demonio

daemon_runner.daemon_context.files_preserve=[handler.stream]

#Ejecuta el método run del objeto app

daemon_runner.do_action()

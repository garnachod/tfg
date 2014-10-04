# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'


DEBUG = False
TEXTO = True


def print_debug(string, forced=False):
    if forced or DEBUG:
        print(string)


def print_if_text(string):
    if TEXTO:
        print string

def abstract_function(fun_name, class_name):
    print_debug("Función %s debe ser especializada por subclases de %s" % (fun_name, class_name))



if __name__ == "__main__":
    logger = Logger()
    logger.insert_log("ejemp_evento", "ejemplo de mensaje")
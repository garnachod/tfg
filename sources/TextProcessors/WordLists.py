# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

from collections import Counter

class WordLists():

    def __init__(self):
        # no si si debo hacer algo
        self.preposiciones = ["a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en",
                              "entre", "hacia", "hasta", "mediante", "para", "por", "pro", "segun", "sin",
                              "sobre", "tras", "via"]

        self.articulos= ["el", "la", "las", "los", "lo", "al", "del", "una", "un"]

        self.adverbios = ["aquí", "allí", "ahí", "allá", "acá", "arriba", "abajo", "cerca", "lejos", "delante",
                          "detrás", "encima", "debajo", "enfrente", "atrás", "alrededor"]
        self.otras_comunes = ["y", "es", "se", "un", "como", "que", "o", "q"]

    def more_frequents(self, word_list, limit=10):
        clean_list = [word.lower() for word in word_list]
        clean_list = self.clean_list(clean_list)
        clean_list = self.remove_symbols(clean_list)
        c = Counter(clean_list)
        return c.most_common(limit)

    def remove_symbols(self, word_list):
        first_out = "#@"
        last_out = "!:"
        word_list = [word[1:] if word[0] in first_out else word for word in word_list]
        retorno = []
        for word in word_list:
            if word != "":
                if word[-1] in last_out:
                    retorno.append(word[:-1])
                else:
                    retorno.append(word)
        return retorno


    def clean_list(self, word_list):
        #quitar stop words
        word_list = filter(lambda a: a not in self.preposiciones, word_list)
        word_list = filter(lambda a: a not in self.articulos, word_list)
        word_list = filter(lambda a: a not in self.adverbios, word_list)
        word_list = filter(lambda a: a not in self.otras_comunes, word_list)
        return word_list
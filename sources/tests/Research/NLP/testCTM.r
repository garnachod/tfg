###ABRIENDO LOS DATOS EN R###
library(NLP)
library(tm)
library(RColorBrewer)
library(wordcloud)
library(topicmodels)
file_loc <- "/media/dani/data/ficherosPrueba_plsa/test_r.csv"
x <- read.csv(file_loc, header = F)
require(tm)
corpusA <- Corpus(DataframeSource(x))
summary(corpusA)
corpusA

## LIMPIA DEL CORPUS ##
corpusA <- tm_map(corpusA, stripWhitespace)
corpusA <- tm_map(corpusA, tolower)
corpusA <- tm_map(corpusA, removeWords, stopwords("spanish"))
corpusA <- tm_map(corpusA,removeNumbers)
corpusA <- tm_map(corpusA,removePunctuation)
corpusA <- tm_map(corpusA, stemDocument)
corpusA <- Corpus(VectorSource(corpusA))

## (te dejo aquí las funciones que utilizo para la limipa por si te sirven de algo)

###CREACIÓN MATRIZ TERMINOS-DOCUMENTOS###
matriz_termosA<- DocumentTermMatrix(corpusA, control=list(minDocFreq=2, minWordLength=2))
rowTotals <- apply(matriz_termosA , 1, sum) 
matriz_termosA <- matriz_termosA[rowTotals> 0, ]


########### Modelo CTM Arboles ################

k<-250

####Esto es un control para la generación del modelo CTM####
Control_CTM_250F<- list(estimate.beta=T, 
                        verbose = 0, prefix = tempfile(), save = 0, keep = 0, 
                        seed = as.integer(Sys.time()), nstart = 1L, best = TRUE, 
                        var = list(iter.max = 500, tol = 10^-6), 
                        em = list(iter.max = -1, tol = 10^-4), 
                        initialize = "random", 
                        cg = list(iter.max = 1000, tol = 10^-5))

###estimación del modelo mediante CTM###
Modelo_CTM_250F<-CTM(matriz_termosA, k, method = "VEM", control = Control_CTM_250F)

####Resultados de la Estimación####
logLik(Modelo_CTM_250F)
perplexity(Modelo_CTM_250F)

## (lo que nos interesa es ver si la “logLik” y la “perplexity” es igual con R y Python y el tiempo de estimación) ##
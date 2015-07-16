# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from DBbridge.ConsultasWeb import ConsultasWeb
import json

class APIGetSearchTweetsDB(object):
   """docstring for APIGetSearchTweetsDB"""
   def __init__(self):
      super(APIGetSearchTweetsDB, self).__init__()
      self.consultas = ConsultasWeb()

   def toString(self):
      if 'user_id' not in session:
         return self.error()

      search_id = request.form['search_id']
      usr_id = session['user_id']
      num_tweets = request.form['num_tweets']
      print num_tweets
      tipo_busqueda = request.form['tipo_busqueda']

      
      if 'max_id' in request.form:
         max_id = request.form['max_id']
      else:

          max_id = None
      
      usr_id = session['user_id']
      

      #test de entradas
      if search_id is None or usr_id is None or num_tweets is None or tipo_busqueda is None:
         return self.error()
      if search_id == "" or usr_id == "" or num_tweets == "" or tipo_busqueda == "":
         return self.error()
      #test de parametros numericos
      #puede que no se busque por maxID
      if max_id is not None:
         try:
            max_id = long(max_id)
            useMaxID = True
         except Exception, e:
            return self.error()
      else:
         useMaxID = False

      if num_tweets is not None:
         try:
            num_tweets = int(num_tweets)
         except Exception, e:
            return self.error()

      #consulta a la base de datos
      #esa consulta es de ese usuario?
      search_string, id_user = self.consultas.getBusquedaFromIdBusqueda(search_id)
      if search_string == False or id_user == False:
         return self.error()
      if id_user != usr_id:
         return self.error()
      #si llegamos aqui podemos asegurar que si que es de ese usuario y se pueden recuperar los tweets
      if tipo_busqueda == 'suser':
         arrayTweets = self.consultas.getTweetsUsuario(search_string, use_max_id=useMaxID, max_id=max_id, limit=num_tweets)
      elif tipo_busqueda == 'topic':
         arrayTweets = self.consultas.getTweetsUsuario(search_string, use_max_id=useMaxID, max_id=max_id, limit=num_tweets)
      else:
         return self.error()

      #se recorren las filas para generar un json fantastico
      retorno = {"status":"true", "tweets" : []}
      for row in arrayTweets:
         tweet = {}
         tweet['text'] = str(row[0])
         tweet['fav'] = str(row[1])
         tweet['rt'] = str(row[2])
         tweet['is_rt'] = str(row[3])
         tweet['media'] = str(row[4])
         tweet['tuser'] = str(row[5])

         retorno['tweets'].append(tweet)
            

      return json.dumps(retorno)

   def error(self):
      retorno = {"status":"false"}
      return json.dumps(retorno)

      
      
# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Web.Index import Index
from Web.Login import Login
from Web.Error import Error
#from Web.Admin import Admin
from Web.Success import Success
from Web.Busqueda import Busqueda
from Web.BusquedaAsinc import BusquedaAsinc
from Web.Contacto import Contacto
from Web.PlanificarTareas import PlanificarTareas
from Web.AltaTarea import AltaTarea
from Web.VisualizarListaTareas import VisualizarListaTareas
from Web.EntrenamientoTweets import EntrenamientoTweets
from Web.ListarTweetsEntrenamiento import ListarTweetsEntrenamiento
from Web.LanzarEntrenamiento import LanzarEntrenamiento
from Web.ResumenTarea import ResumenTarea
from Web.NuevaListaEntrenamiento import NuevaListaEntrenamiento
from DBbridge.ConsultasWeb import ConsultasWeb



#test
from Web.EntrenamientoTweet import EntrenamientoTweet
####
import os
import time


app = Flask(__name__)
consultasWeb = ConsultasWeb()
#vistas de la seccion admin
import sources.views_admin
#vistas JSON esto es, api
import sources.views_api

index_web = Index()
login_web = Login()
error_web = Error()


success_web = Success()
busqueda_web = Busqueda()
planificartarea_web = PlanificarTareas()
busquedaAsinc_web = BusquedaAsinc()
altaTarea_web = AltaTarea()
contacto_web = Contacto()
entrena_tweets_web = EntrenamientoTweets()
listaTareas_web = VisualizarListaTareas()
listaTweetTrain_web = ListarTweetsEntrenamiento()
lanzarEntrenamiento_web = LanzarEntrenamiento()
resumenTarea_web = ResumenTarea()
nlistaEntrena_web = NuevaListaEntrenamiento()

#simulacion de index
@app.route('/')
def index():
	if 'username' in session:
		return index_web.toString(session['username'])
	else:
		return index_web.toString()
		
#inicio de sesion
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		retorno = login_web.doLogin()
		if retorno == 'OK':
			return redirect('/')
		else:
			return redirect('/err?code=1')
	else:
		return login_web.toString()

#cerrar sesion
@app.route('/cerrar_sesion')
def cerrar_sesion():
	session.clear()
	return redirect('/') 
	

#ruta generica de error con diferentes codigos de error
@app.route('/err')
def error():
	if request.args['code'] is None:
		return error_web.toString('2')
	else:
		return error_web.toString(request.args['code'])
#igual que error pero cuando se realiza una transaccion con éxito
@app.route('/success')
def success():
	if request.args['code'] is None:
		return success_web.toString('1')
	else:
		return success_web.toString(request.args['code'])

#aqui se realiza el post de la busqueda
@app.route('/busqueda', methods=['GET', 'POST'])
def busqueda():
	if 'username' in session:
		if request.method == 'POST':
			if request.form['tipoBusqueda'] is None or request.form['search'] is None:
				return redirect('/err?code=2')
			else:
				searchID = busqueda_web.doBusqueda(request.form['tipoBusqueda'], request.form['search'])
				session['searchID'] = searchID

				retorno = busqueda_web.toString(request.form['tipoBusqueda'], request.form['search'])
				
				return retorno
		else:
			return 'err'
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')


@app.route('/busqueda_asinc', methods=['GET', 'POST'])
def busquedaAsinc():
	if request.method == 'POST':
		return busquedaAsinc_web.toJsonSearch()
	else:
		return redirect('/err?code=2')

				
		#return redirect('/err?code=2')


@app.route('/contacto')
def contacto():
	if 'username' in session:
		return contacto_web.toString()
	else:
		return redirect('/err?code=5')
#************************Tareas***********************************
@app.route('/planificartarea')
def planificartarea():
	if 'username' in session:
		return planificartarea_web.toString()
	else:
		return redirect('/err?code=5')

@app.route('/alta_tarea', methods=['GET', 'POST'])
def altatarea():
	if 'username' in session:
		if request.method == 'POST':
			altaTarea_web.alta()
			return redirect('/success?code=3')
		else:
			return redirect('/err?code=2')
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')

@app.route('/ver_tareas_pendientes')
def verTareasPendientes():
	if 'username' in session:
		return listaTareas_web.toString(False)
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')

@app.route('/ver_tareas_finalizadas')
def verTareasFinalizadas():
	if 'username' in session:
		return listaTareas_web.toString(True)
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')

@app.route('/resumen_tarea', methods=['GET'])
def resumenTarea():
	if 'username' in session:
		try:
			identificadorTarea = request.args['identificador']
			try:
				analizar = request.args['analizar']
				if analizar == 't':
					return resumenTarea_web.volverAnalizarTweets(identificadorTarea)
				else:
					return resumenTarea_web.toString(identificadorTarea)
			except Exception, e:
				print e
				return resumenTarea_web.toString(identificadorTarea)
		except Exception, e:
			print e
			return redirect('/')
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')

#******************fin de tareas*************************************
#************************Estadisticas********************************

#******************fin de Estadisticas*******************************

#************************entrenamiento********************************
@app.route('/entrena_tweets')
def entrenamientoTweets():
	if 'username' in session:
		return entrena_tweets_web.toString()
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')


@app.route('/ver_entrena_tweets', methods=['GET'])
def listaEntrenamientoTweets():
	if 'username' in session:
		try:
			if request.args['id_lista'] is None:
				return listaTweetTrain_web.toString()
			else:
				return listaTweetTrain_web.toString(int(request.args['id_lista']))
		except Exception, e:
			return listaTweetTrain_web.toString()
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')
		
@app.route('/change_tweet_train' , methods=['GET', 'POST'])
def changeTweetTrain():
	if 'username' in session:
		if request.method == 'POST':
			return setTweetTrain_web.toStringChange()
		else:
			return redirect('/err?code=2')
	else:
		return 'err'

@app.route('/lanzar_entrenamientos', methods=['GET'])
def lanzarEntrenamientos():
	if 'username' in session:
		try:
			if request.args['id_entr'] is None:
				return lanzarEntrenamiento_web.toString()
			else:
				lanzarEntrenamiento_web.generaEntrenamientoTweets(request.args['id_entr'])
				return redirect('/success?code=4')
		except Exception, e:
			return lanzarEntrenamiento_web.toString()
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')

@app.route('/lista_entrena_tweets' , methods=['GET', 'POST'])
def listaTweetTrain():
	if 'username' in session:
		if request.method == 'POST':
			nlistaEntrena_web.creaLista()
			return redirect('/success?code=3')
		else:
			try:
				if request.args['borrar_id'] is None:
					return nlistaEntrena_web.toString()
				else:
					nlistaEntrena_web.borrar(int(request.args['borrar_id']))
					return redirect('/lista_entrena_tweets')
					
			except Exception, e:
				return nlistaEntrena_web.toString()
	else:
		#si no se ha iniciado sesion redirige a la pagina principal
		return redirect('/')
		
@app.route('/test')
def test():
	test = EntrenamientoTweet()
	return test.toString()

#******************fin de entrenamiento*******************************

#@app.route('/login')
#def login():


if __name__ == '__main__':
	#app.secret_key = '\xe8ysa\xfaAI\x0629\xd4\x11\x0e\xd2\xae\xcf+y2\xeed\x1a\xe1?'
	app.secret_key = os.urandom(24)
	#app.run(host='0.0.0.0')
	app.run(host='0.0.0.0',debug=True)
   
    #app.url_for('static', filename='/css/general.css')
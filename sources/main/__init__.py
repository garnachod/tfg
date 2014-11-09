# -*- coding: utf-8 -*-
from flask import Flask, session, request, redirect
from Web.Index import Index
from Web.Login import Login
from Web.Error import Error
from Web.Admin import Admin
from Web.Success import Success
from Web.Busqueda import Busqueda
from Web.BusquedaAsinc import BusquedaAsinc
from Web.AdminNewUser import AdminNewUser
from Web.AdminNewApiKey import AdminNewApiKey
from DBbridge.ConsultasWeb import ConsultasWeb
import os
import time


app = Flask(__name__)
index_web = Index()
login_web = Login()
error_web = Error()
admin_web = Admin()
success_web = Success()
busqueda_web = Busqueda()
consultasWeb = ConsultasWeb()
admin_new_usr = AdminNewUser()
admin_new_apik = AdminNewApiKey()
busquedaAsinc_web = BusquedaAsinc()


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

#*****rutas de aministrador*************************************
@app.route('/admin')
def admin():
	if 'username' in session:
		if consultasWeb.isAdministrator(session['user_id']):
			return admin_web.toString()
		else:
			return redirect('/err?code=3')
	else:
		return redirect('/login');

@app.route('/admin_new_user', methods=['GET', 'POST'])
def admin_new_user():
	if 'username' in session:
		if request.method == 'POST':
			if admin_new_usr.add():
				return redirect('/success?code=1')
			else:
				return redirect('/err?code=6')
		else:
			return redirect('/err?code=4')
	else:
		return redirect('/err?code=5')

@app.route('/admin_new_apikey', methods=['GET', 'POST'])
def admin_new_apikey():
	if 'username' in session:
		if request.method == 'POST':
			if admin_new_apik.add():
				return redirect('/success?code=2')
			else:
				return redirect('/err?code=6')
		else:
			return redirect('/err?code=4')
	else:
		return redirect('/err?code=5')

#*****fin de rutas de aministrador********************************

#@app.route('/login')
#def login():


if __name__ == '__main__':
	#app.secret_key = '\xe8ysa\xfaAI\x0629\xd4\x11\x0e\xd2\xae\xcf+y2\xeed\x1a\xe1?'
	app.secret_key = os.urandom(24)
	#app.run(host='0.0.0.0')
	app.run(host='0.0.0.0',debug=True)
   
    #app.url_for('static', filename='/css/general.css')

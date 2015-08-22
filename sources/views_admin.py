# -*- coding: utf-8 -*-
from flask import session, request, redirect
from Web.Admin.NuevoUsuarioAdmin import NuevoUsuarioAdmin
from Web.Admin.NuevaApiKeyAdmin import NuevaApiKeyAdmin
from Web.Admin.EstadisticasAdmin import EstadisticasAdmin
from Web.Admin.AdminNewUser import AdminNewUser
from Web.Admin.AdminNewApiKey import AdminNewApiKey
from sources import app,consultasWeb

##ADMIN
admin_vista_newuser = NuevoUsuarioAdmin()
admin_vista_newapikey = NuevaApiKeyAdmin()
admin_new_usr = AdminNewUser()
admin_new_apik = AdminNewApiKey()
admin_estadisticas = EstadisticasAdmin()
##Fin de ADMIN

#*****rutas de aministrador*************************************
@app.route('/admin/usuario_nuevo')
def admin_user():
	if 'username' in session:
		if consultasWeb.isAdministrator(session['user_id']):
			return admin_vista_newuser.toString()
		else:
			return redirect('/err?code=3')
	else:
		return redirect('/login')

@app.route('/admin/nueva_apikey')
def admin_key():
	if 'username' in session:
		if consultasWeb.isAdministrator(session['user_id']):
			return admin_vista_newapikey.toString()
		else:
			return redirect('/err?code=3')
	else:
		return redirect('/login')

@app.route('/admin/estadisticas')
def admin_stats():
	if 'username' in session:
		if consultasWeb.isAdministrator(session['user_id']):
			return admin_estadisticas.toString()
		else:
			return redirect('/err?code=3')
	else:
		return redirect('/login')

@app.route('/admin/new_user', methods=['GET', 'POST'])
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

@app.route('/admin/new_apikey', methods=['GET', 'POST'])
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
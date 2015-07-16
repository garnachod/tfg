# -*- coding: utf-8 -*-
from flask import Flask, session, request
from DBbridge.ConsultasWeb import ConsultasWeb
import json

class APIGetTweetsTrainList(object):
    """docstring for APIGetTweetsTrainList"""
    def __init__(self):
        super(APIGetTweetsTrainList, self).__init__()

    def toString():
        if 'user_id' not in session:
            return self.error()

        if 'list_id' not in request.form:
            return self.error()

        list_id = request.form['list_id']
        if list_id == '':
            return self.error()

        isUser = self.consultas.isListasEntrenamientoFromUser(session['user_id'], list_id)
        if isUser == False:
            return self.error()

        #ya estan todos los controles de seguridad pasados
        

    def error():
        retorno = {"status":"false"}
        return json.dumps(retorno)
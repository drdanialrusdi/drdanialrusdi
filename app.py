# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:14:08 2018

@author: 00130161
"""
from  flask import Flask, request, url_for, redirect, render_template
from datetime import datetime
from oc_prediction import *
import pyodbc
import time

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=server_name;"
                      "Database=db_name;"
                      "Trusted_Connection=yes;")


cursor = cnxn.cursor()
cursor.execute('SELECT * FROM Table')

#Function to retrieve data from database

app = Flask(__name__)

@app.route('/')
def index():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        
        return redirect('/EFTB')

@app.route('/EFTB')
def EFTB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        oc_predict_simulation(data,new_data,model_select='EFTB')
        return render_template()

@app.route('/EGTB')
def EGTB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        oc_predict_simulation(data,new_data,model_select='EGTB')
        return render_template()

@app.route('/EGIB')
def EGIB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        oc_predict_simulation(data,new_data,model_select='EGIB')
        return render_template()

@app.route('/ELIB')
def ELIB():
    if currentday()==6:
        return render_template('predictionnotavailable.html')
    else:
        oc_predict_simulation(data,new_data,model_select='ELIB')
        return render_template()

@app.route('/ELBB')
def ELBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        oc_predict_simulation(data,new_data,model_select='ELBB')
        return render_template()

@app.route('/EGBB')
def EGBB():
    if currentday()==6 | currentday()==5:
        return render_template('predictionnotavailable.html')
    else:
        oc_predict_simulation(data,new_data,model_select='EGBB')
        return render_template()

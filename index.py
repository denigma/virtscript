#!/usr/bin/python
# -*- coding: utf8 -*-

from flask import Flask, render_template, request,  jsonify, session, escape, redirect, url_for
from proxmox.exceptions import *

app = Flask(__name__)

import os
# set the secret key.  keep this really secret:
app.secret_key = os.urandom(24)

from jinja2 import Environment, FileSystemLoader

from wtforms import Form, BooleanField, IntegerField, StringField, PasswordField, validators
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = StringField("username", default="root")
    password = StringField("password", default="")
    host = StringField("host",default="46.4.31.24")



class ContainerForm(Form):
    id = IntegerField('CTID', default=101, validators=[DataRequired()]) # VEID контейнера
    name = StringField("CTNAME", default="semantic", validators=[DataRequired()])   # IP адрес контейнера
    ip = StringField("CTIP", default="192.168.1.104", validators=[DataRequired()])  # hostname контейнера
    banned = StringField("BANNED", default="") # IP адрес контейнера
    allow2ct = StringField("ALLOW2CT", default="")# Разрешаем соединения между DMZ контейнером и этими подсетями
    verelay = StringField("VERELAY", default="yes")# Можно ли контейнеру спамить?
    DNAT4PORTS_TCP = StringField("DNAT4PORTS_TCP", default="4569 9000 7070 5000")   # Пробрасываем указанный внешний порт на контейнер
    DNAT2PORTS_TCP= StringField("DNAT2PORTS_TCP", default="22 80 7070 5000") # Пробрасываем на указанный порт контейнера внешний порт
    DNAT4PORTS_UDP = StringField("DNAT4PORTS_UDP", default="") # Пробрасываем указанный внешний порт на контейнер
    DNAT2PORTS_UDP=StringField("DNAT2PORTS_UDP", default="") # Пробрасываем на указанный порт контейнера внешний порт
    DMZSTATUS = StringField(" DMZSTATUS", default="no")  # В DMZ ли данный контейнер?


#def isLoggedIn():
#    return 'username' in session and 'password' in session


@app.route("/", methods=['GET', 'POST'])
def index():
    #if(isLoggedIn()):
    if(True):
        form = LoginForm(request.form)
        return render_template('login.html',login = form)
    else:
        username = escape(session['username'])
        password = escape(session['password'])
        return ports()

@app.route("/ports", methods=['GET', 'POST'])
def ports():
    form = ContainerForm(request.form)
    return render_template('ports.html',form = form, result = "")


@app.route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


def connect(host,port = 8006 ):
    from proxmox import Connector, Proxmox
    #PROXMOX_HOST = "46.4.31.24"  # can also be an IP or the FQDN of the host
    return Connector(host, port)


def auth(connection,username,password):
    return connection.get_auth_token(username+'@pam', password)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


def save(form,path = "./firewall/"):
    env = Environment(loader=FileSystemLoader('templates'))
    filename = path+form.name.data+".dmz.inc"
    template = env.get_template('file_to_save.txt')
    f = open(filename,'w')
    f.write(template.render(form=form))
    f.close()

@app.route('/register', methods=['GET','POST'])
def register():

    lg = LoginForm(request.form)
    username = session['username'] = lg.username.data
    password = session['password'] = lg.password.data
    host = session['host'] = lg.host.data
    result = "registration! is of for "+lg.username.data+" with host "+lg.host.data
    connection = connect(host)
    try:
        token = auth(connection,username,password)
        form = ContainerForm(request.form)
        return render_template('ports.html', form=form)
    except:
        pass
        return render_template('error.html', title = "AUTH FAILURE",message = "username/password do not much")


@app.route('/save', methods=['GET', 'POST'])
def save():
    form = ContainerForm(request.form)
    save(form)
    return render_template('ports.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('username', None)
    session.pop('username', None)
    return redirect(url_for('index'))


from __future__ import annotations

from os import listdir
from os.path import join, dirname, abspath
from importlib import import_module


from constructors import elements
BASEDIR = abspath(dirname(__file__))
APPLETDIR = join(BASEDIR, 'applets')

applets = [f[:-3] for f in listdir(APPLETDIR) if f.endswith('.py')]
#import all applets
for applet in applets:
    import_module(f'applets.{applet}')

#make a dictionary of all applets's attributes
applets_attr = {applet: getattr(import_module(f'applets.{applet}'), applet) for applet in applets}


from flask import Flask, render_template, request, url_for, session, Response, g, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.local import LocalProxy
from waitress import serve

from datetime import datetime as dt
from time import sleep as wait

import secrets

basedir = abspath(dirname(__file__))

app = Flask(__name__, template_folder='templates', static_folder='static')

app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + join(basedir, 'databases/core.db') 
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///' + join(basedir, 'databases/users.db')
    }

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
ALLOWED_DATA_EXTENSIONS = {'csv', 'db', 'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["DEBUG"] = True

db = SQLAlchemy(app)

@app.route('/<applet>', methods = ['GET', 'POST', 'PUT'])
def core(applet = None):

    try:
        elem = session['elem']

    except:
        elem = elements(applets = applets_attr.keys(), authors = "Florent Maisse")
        elem = elem()
        session['elem'] = elem

    try:
        #try to call the applet and pass the elem object and the methods
        elem = applets_attr[applet](elem, request.method, request.form, request.args)
        session['elem'] = elem
    
    except:
        return redirect(url_for('core', applet = 'home'), code=302)

    #check if all the attributes are present
    if not all([attr in elem.keys() for attr in ['head', 'header', 'menu', 'content', 'side_content', 'search', 'side_footer', 'scripts']]):
        #if not, return the home page
        elem = applets_attr['home'](elem, request.method, request.form, request.args)
        session['elem'] = elem

    return render_template('base.html',
        head = elem['head'],
        header =elem['header'],
        menu = elem['menu'],
        content =elem['content'],
        side_content = elem['side_content'],
        search = elem['search'] ,
        side_footer = elem['side_footer'] ,
        scripts = elem['scripts']

    )

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('core', applet = 'home'), code=302)


#serve(app, host="0.0.0.0", port=8080)
app.run()
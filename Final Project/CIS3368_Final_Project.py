import hashlib
import flask
from flask import jsonify
from flask import request, make_response

import mysql.connector
from mysql.connector import Error
import creds

from sql import create_connection
from sql import execute_read_query
from sql import execute_query

#create connection to mysql database
myCreds = creds.Creds()
connection = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)

#setting up an application name
app = flask.Flask(__name__)
app.config["DEBUG"] = True #show errors

masterPassword = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
masterUsername = 'username'

@app.route('/api/login', methods = ['GET'])
def login_api():
    if request.authorization:
        encoded = request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> Authorized user access </h1>'
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

app.run()
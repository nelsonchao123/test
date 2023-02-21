import flask
from flask import jsonify
from flask import request

import mysql.connector
from mysql.connector import Error
import creds

from sql import create_connection
from sql import execute_read_query
from sql import execute_query

#create connection to mysql database
myCreds = creds.Creds()
connection = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)






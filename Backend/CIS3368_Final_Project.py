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

#get api for captain table
@app.route('/api/captain', methods = ['GET'])
def get_captain():
    sql = "select * from captain"
    user = execute_read_query(connection,sql)

    return jsonify(user)

#get api for spaceship table
@app.route('/api/spaceship', methods = ['GET'])
def get_spaceship():
    sql = "select * from spaceship"
    user = execute_read_query(connection,sql)

    return jsonify(user)

#get api for cargo table
@app.route('/api/cargo', methods = ['GET'])
def get_cargo():
    sql = "select * from cargo"
    user = execute_read_query(connection,sql)

    return jsonify(user)

#post api for captain table
@app.route('/api/captain', methods = ['POST'])
def post_captain():
    request_data = request.get_json()
    newfirstname = request_data['firstname']
    newlastname = request_data['lastname']
    newrank = request_data['rank']
    newhome = request_data['homeplanet']

    sql = "insert into captain(firstname, lastname, `rank`, homeplanet) VALUES ('%s', '%s', '%s', '%s')" % (newfirstname, newlastname, newrank, newhome)
    execute_query(connection, sql)

    return 'Add Request Successful'

#post api for spaceship table
@app.route('/api/spaceship', methods = ['POST'])
def post_spaceship():
    request_data = request.get_json()
    newweight = request_data['maxweight']
    newcapid = request_data['captainid']

    sql = "insert into spaceship(maxweight, captainid) VALUES ('%s', '%s')" % (newweight, newcapid)
    execute_query(connection, sql)

    return 'Add Request Successful'

#post api for cargo table
@app.route('/api/cargo', methods = ['POST'])
def post_cargo():
    checkweight = 0

    request_data = request.get_json()

    checkshipid = request_data['shipid']

    newweightcarg = request_data['weight']
    newcargtype = request_data['cargotype']
    newdepart = request_data['departure']
    newarrival = request_data['arrival']
    newshipid = request_data['shipid']

    sql = "select maxweight from spaceship where id = '%s'" % (checkshipid)
    weinum = execute_read_query(connection, sql)
    weighnum = weinum[0]
    weightnum = weighnum["maxweight"]

    sql = "select weight from cargo where shipid = '%s'" % (checkshipid)
    cargwei = execute_read_query(connection, sql)
    for i in cargwei:
        checkweight += i["weight"]

    if checkweight + newweightcarg <= weightnum:
        sql = "insert into cargo(weight, cargotype, departure, arrival, shipid) VALUES ('%s', '%s', '%s', '%s', '%s')" % (newweightcarg, newcargtype, newdepart, newarrival, newshipid)
        execute_query(connection, sql)

        return 'Add Request Successful'
    else:
        return 'Cargo weight exceeds ship weight'

#delete api for captain table
@app.route('/api/captain', methods = ['DELETE'])
def del_captain():
    request_data = request.get_json()
    deletedID = request_data['id']

    sql = "set foreign_key_checks = 0;"
    execute_query(connection, sql)
    sql = "delete from captain where id = '%s'" % (deletedID)
    execute_query(connection, sql)
    sql = "set foreign_key_checks = 1;"
    execute_query(connection, sql)

    return "Delete Request Successful"

#delete api for spaceship table
@app.route('/api/spaceship', methods = ['DELETE'])
def del_spaceship():
    request_data = request.get_json()
    deletedID = request_data['id']

    sql = "set foreign_key_checks = 0;"
    execute_query(connection, sql)
    sql = "delete from spaceship where id = '%s'" % (deletedID)
    execute_query(connection, sql)
    sql = "set foreign_key_checks = 1;"
    execute_query(connection, sql)

    return "Delete Request Successful"

#delete api for cargo table
@app.route('/api/cargo', methods = ['DELETE'])
def del_cargo():
    request_data = request.get_json()
    deletedID = request_data['id']

    sql = "set foreign_key_checks = 0;"
    execute_query(connection, sql)
    sql = "delete from cargo where id = '%s'" % (deletedID)
    execute_query(connection, sql)
    sql = "set foreign_key_checks = 1;"
    execute_query(connection, sql)

    return "Delete Request Successful"

#put api for captain table
@app.route('/api/captain', methods = ['PUT'])
def put_captain():
    request_data = request.get_json()
    changedID = request_data['id']
    changedFN = request_data['firstname']
    changedLN = request_data['lastname']
    changedrank = request_data['rank']
    changedHP = request_data['homeplanet']

    sql = "set foreign_key_checks = 0;" #so that I am able to change a table with a foreign key
    execute_query(connection, sql)
    sql = "replace into captain SET id = '%s', firstname = '%s', lastname = '%s', `rank` = '%s', homeplanet = '%s';" % (changedID, changedFN, changedLN, changedrank, changedHP)
    execute_query(connection, sql)
    sql = "set foreign_key_checks = 1;" #set foreign_key_checks back to true
    execute_query(connection,sql)

    return "Put Request Successful"

#put api for spaceship table
@app.route('/api/spaceship', methods = ['PUT'])
def put_spaceship():
    request_data = request.get_json()
    changedID = request_data['id']
    changedMW = request_data['maxweight']
    changedCID = request_data['captainid']

    sql = "set foreign_key_checks = 0;"
    execute_query(connection, sql)
    sql = "replace into spaceship SET id = '%s', maxweight = '%s', captainid = '%s';" % (changedID, changedMW, changedCID)
    execute_query(connection, sql)
    sql = "set foreign_key_checks = 1;"
    execute_query(connection, sql)

    return "Put Request Successful"

#put api for cargo table
@app.route('/api/cargo', methods = ['PUT'])
def put_cargo():
    checkweight = 0

    request_data = request.get_json()

    checkshipid = request_data["shipid"]

    changedID = request_data['id']
    changedweight = request_data['weight']
    changedCT = request_data['cargotype']
    changeddepart = request_data['departure']
    changedarrival = request_data['arrival']
    changedSID = request_data['shipid']

    sql = "select maxweight from spaceship where id = '%s'" % (checkshipid)
    weinum = execute_read_query(connection, sql)
    weighnum = weinum[0]
    weightnum = weighnum["maxweight"]

    sql = "select weight from cargo where shipid = '%s'" % (checkshipid)
    cargwei = execute_read_query(connection, sql)
    for i in cargwei:
        checkweight += i["weight"]

    sql = "select weight from cargo where id = '%s'" % (changedID)
    subwei = execute_read_query(connection, sql)
    subweigh = subwei[0]
    subweight = subweigh["weight"]

    checkweight -= subweight

    if checkweight + changedweight <= weightnum:
        sql = "set foreign_key_checks = 0;"
        execute_query(connection, sql)
        sql = "replace into cargo SET id = '%s', weight = '%s', cargotype = '%s', departure = '%s', arrival = '%s', shipid = '%s';" % (changedID, changedweight, changedCT, changeddepart, changedarrival, changedSID)
        execute_query(connection, sql)
        sql = "set foreign_key_checks = 1;"
        execute_query(connection, sql)

        return "Put Request Successful"
    else:
        return 'Cargo weight exceeds ship weight'


app.run()

#testing commit 2
#testing how to commit to github


import mysql.connector
from mysql.connector import Error

#define connection
def create_con(hostname, uname, pwd, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = uname,
            password = pwd,
            database = dbname
        )
    except Error as e:
        print("error is : ", e)
    return connection

con = create_con('cis3368spring.cot5hldu0unp.us-east-1.rds.amazonaws.com', 'admin', 'cis3368spring', 'cis3368database')

cursor = con.cursor(dictionary=True)

#create menu function
def menu():
    print("\nMENU\n")
    print("a - Add cases\n")
    print("o - Output all cases in console\n")
    print("q- Quit\n")

#output menu first time
menu()
option = input()

#loop to keep outputting menu until 'q' is taken as an input
while option != "q":
    if option == "a":
        countryname = input("Enter country name: ")
        year = input("Enter year: ")
        totalcases = input("Enter total cases: ")
        deaths = input("Enter deaths: ")
        recovered = input("Enter number recovered: ")

        #used to test if inputs are taken correctly
        #print(countryname, year, totalcases, deaths, recovered)

        #insert entry into table
        cursor.execute("INSERT INTO covidcases (countryname, year, totalcases, deaths, recovered) VALUES (%s,%s,%s,%s,%s)", (countryname, year, totalcases, deaths, recovered))
        con.commit()

    elif option == "o":
        #test if entry was commited
        sql = 'select * from covidcases'
        cursor.execute(sql)
        rows = cursor.fetchall()

        for user in rows:
            print(user)

    else:
        print("Invalid Option\n")

    menu()
    option = input()
    
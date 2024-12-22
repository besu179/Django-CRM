import mysql.connector

database = mysql.connector.connect(

    host = 'localhost',
    user = 'root',
    passwd = 'Loop12$$'

)

#prepare cursor object 

cursorObject = database.cursor()

#Create database

cursorObject.execute("CREATE DATABASE elderco")

print('All done!')
# Authors: Duncan McConnell and Jack Bonatakis
# Created at Hack CU IV - 2.24.2018

# Imports
import mysql.connector
import re
import math
import sys
import shutil
import os
import urllib

# Function to run SQL scripts stored on EC2 instance
def executeScriptsFromFile(filename, server, cursor):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split('\n')
    
    cursor.execute("USE blackbla_" + server + ";")
    
    for i, command in enumerate(sqlCommands):
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError, msg:
            print "Command skipped: ", msg
        if(filename == '/home/pi/serverTracking/' + server + '/map.sql'):
            temp = math.floor(i/(len(sqlCommands) * 1.0) * 100)
            sys.stdout.write("\r[%-20s] %d%%" % ('|'* int(temp/5), int(temp)))
            sys.stdout.flush()
    if(filename == '/home/pi/serverTracking/' + server + '/map.sql'):
        sys.stdout.write("\r[||||||||||||||||||||] 100%")
        sys.stdout.flush()

#Function to set up MySQL DB connetion and choose which scripts to run per server
def perServerWork(server, link):
    temp = 'blackbla_' + server
    cnx = mysql.connector.connect(
        user='USERNAME',
        password='PASSWORD',
        host='HOST_IP',
        database=temp)
    cursor = cnx.cursor()

    if os.path.exists("/home/pi/serverTracking/" + server) == False:
        os.makedirs("/home/pi/serverTracking/" + server)
        executeScriptsFromFile('/home/pi/serverTracking/server-creation.sql', server, cursor)

    # Download map.sql file 
    urllib.urlretrieve(link, '/home/pi/serverTracking/' + server + '/map.sql')

    # Function calls to run SQL scripts
    executeScriptsFromFile('/home/pi/serverTracking/pre-map.sql', server, cursor)
    executeScriptsFromFile('/home/pi/serverTracking/' + server + '/map.sql', server, cursor)
    executeScriptsFromFile('/home/pi/serverTracking/post-map.sql', server, cursor)
    print(" " + server)
    cnx.commit()

#Imports raw server data from server.txt
serverFile = open('servers.txt', 'r')
serversRaw = serverFile.read()
serverFile.close()

#Formats data into a workable list system
servers = serversRaw.split('\n')

for groups in servers:

    #Formats data into two parts to work with rest of program
    groups = groups.split(',')

    try:
        perServerWork(groups[0], groups[1])
    except:
        print(groups[0] + " has failed.")

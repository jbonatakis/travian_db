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

servers = [ ['ae19', 'https://ts19.travian.ae/map.sql'],

            ['au3', 'https://ts3.travian.com.au/map.sql'],

            ['bgx', 'https://tx3.travian.bg/map.sql'],

            ['br5', 'https://ts5.travian.com.br/map.sql'],
            ['brx', 'https://tx3.travian.com.br/map.sql'],

            ['cl1', 'https://ts1.travian.cl/map.sql'],
            ['clx', 'https://tx3.travian.cl/map.sql'],

            ['com1', 'https://ts1.travian.com/map.sql'],
            ['com5', 'https://ts5.travian.com/map.sql'],
            ['com19', 'https://ts19.travian.com/map.sql'],
            ['com83', 'https://ts83.travian.com/map.sql'],

            ['cz2', 'https://ts2.travian.cz/map.sql'],
            ['cz19', 'https://ts19.travian.cz/map.sql'],
            ['czx', 'https://tx3.travian.cz/map.sql'],

            ['de2', 'https://ts2.travian.de/map.sql'],
            ['de19', 'http://ts19.travian.de/map.sql'],
            ['dex', 'https://tx3.travian.de/map.sql'],

            ['dkx', 'https://tx3.travian.dk/map.sql'],

            ['eg19', 'https://ts19.travian.com.eg/map.sql'],
            ['egx', 'https://tx3.travian.com.eg/map.sql'],

            ['fix', 'https://tx3.travian.fi/map.sql'],

            ['fr1', 'https://ts1.travian.fr/map.sql'],
            ['fr19', 'https://ts19.travian.fr/map.sql'],

            ['hkx', 'https://tx3.travian.hk/map.sql'],

            ['hu19', 'https://ts19.travian.hu/map.sql'],
            ['hux', 'https://tx3.travian.hu/map.sql'],
            
            ['id5', 'https://ts5.travian.co.id/map.sql'],
            ['id19', 'https://ts19.travian.co.id/map.sql'],

            ['il19', 'https://ts19.travian.co.il/map.sql'],
            ['ilx', 'https://tx3.travian.co.il/map.sql'],

            ['ir19', 'https://ts19.travian.ir/map.sql'],
            ['irx', 'https://tx3.travian.ir/map.sql'],

            ['it1', 'https://ts1.travian.it/map.sql'],
            ['it19', 'https://ts19.travian.it/map.sql'],
            ['itx', 'https://tx3.travian.it/map.sql'],

            ['jp19', 'https://ts19.travian.jp/map.sql'],

            ['lt19', 'https://ts19.travian.lt/map.sql'],

            ['my19', 'https://ts19.travian.com.my/map.sql'],

            ['net1', 'https://ts1.travian.net/map.sql'],
            ['netx', 'https://tx3.travian.net/map.sql'],

            ['nl1', 'https://ts1.travian.nl/map.sql'],
            ['nl19', 'https://ts19.travian.nl/map.sql'],
            ['nlx', 'https://tx3.travian.nl/map.sql'],

            ['nox', 'https://tx3.travian.no/map.sql'],

            ['pl2', 'http://ts2.travian.pl/map.sql'],
            ['pl19', 'http://ts19.travian.pl/map.sql'],
            ['plx', 'http://tx3.travian.pl/map.sql'],

            ['pt4', 'https://ts4.travian.pt/map.sql'],

            ['ro3', 'https://ts3.travian.ro/map.sql'],
            ['ro19', 'https://ts19.travian.ro/map.sql'],
            ['rox', 'https://tx3.travian.ro/map.sql'],

            ['rsx', 'https://tx3.travian.rs/map.sql'],

            ['ru1', 'https://ts1.travian.ru/map.sql'],
            ['ru19', 'https://ts19.travian.ru/map.sql'],
            ['rux', 'https://tx3.travian.ru/map.sql'],

            ['sa19', 'https://ts19.travian.com.sa/map.sql'],

            ['sex', 'https://tx3.travian.se/map.sql'],

            ['six', 'https://tx3.travian.si/map.sql'],

            ['sk19', 'https://ts19.travian.sk/map.sql'],

            ['th3', 'https://ts3.travian.asia/map.sql'],
            ['th19', 'https://ts19.travian.asia/map.sql'],
            ['thx', 'https://tx3.travian.asia/map.sql'],

            ['tr5', 'https://ts5.travian.com.tr/map.sql'],
            ['tr19', 'https://ts19.travian.com.tr/map.sql'],
            ['trx', 'https://tx3.travian.com.tr/map.sql'],
            
            ['tw1', 'https://ts1.travian.tw/map.sql'],
            ['tw19', 'https://ts19.travian.tw/map.sql'],
            ['twx', 'https://tx3.travian.tw/map.sql'],

            ['uk2', 'https://ts2.travian.co.uk/map.sql'],
            ['uk3', 'https://ts3.travian.co.uk/map.sql'],
            ['ukx', 'https://tx3.travian.co.uk/map.sql'],

            ['us1', 'https://ts1.travian.us/map.sql'],
            ['us3', 'https://ts3.travian.us/map.sql'],
            
            ['vn1', 'https://ts1.travian.com.vn/map.sql'],
            ['vn19', 'https://ts19.travian.com.vn/map.sql'],
            ['vnx', 'https://tx3.travian.com.vn/map.sql'],
            
            ['bk19', 'https://ts19.balkan.travian.com/map.sql'],
            ['engb', 'https://ts19.english.travian.com/map.sql'],
            ['hisp', 'https://ts19.hispano.travian.com/map.sql'],
            ['itar', 'https://arabiats19.travian.com/map.sql'],
            ['luso', 'https://ts19.lusobrasileiro.travian.com/map.sql'],
            ['nord', 'https://ts19.nordics.travian.com/map.sql']]

# Adds new directory for a new server if currently does not exist
def checkServerDir(server):
    if os.path.exists("/home/pi/serverTracking/" + server) == False:
        os.makedirs("/home/pi/serverTracking/" + server)
        
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

def perServerWork(server, link):
    temp = 'blackbla_' + server
    cnx = mysql.connector.connect(
        user='USERNAME',
        password='PASSWORD',
        host='HOST_IP',
        database=temp)
    cursor = cnx.cursor()

    # Download map.sql file 
    urllib.urlretrieve(link, '/home/pi/serverTracking/' + server + '/map.sql')

    # Function calls to run SQL scripts
    executeScriptsFromFile('/home/pi/serverTracking/pre-map.sql', server, cursor)
    executeScriptsFromFile('/home/pi/serverTracking/' + server + '/map.sql', server, cursor)
    executeScriptsFromFile('/home/pi/serverTracking/post-map.sql', server, cursor)
    print

for groups in servers:
    try:
        checkServerDir(groups[0])
        perServerWork(groups[0], groups[1])
    except:
        print(groups[0] + " has failed.")

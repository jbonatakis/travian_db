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
import pandas as pd
import matplotlib
matplotlib.use('agg',warn=False,force=True)
from matplotlib import pyplot as plt
from datetime import datetime

#Removes old directory if present and creates a new clean directory
if os.path.exists("Alliance_Maps") :
    shutil.rmtree("Alliance_Maps")
os.makedirs("Alliance_Maps")

# Connect to AWS RDS Database
cnx = mysql.connector.connect(
	user='root', 
	password='rootroot',
	host='traviandb2.czwnxyxfgmoy.us-west-2.rds.amazonaws.com',
	database='traviandb2')

cursor = cnx.cursor()

# Function to run SQL scripts stored on EC2 instance
def executeScriptsFromFile(filename):
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split('\n')
    
    cursor.execute("USE traviandb2;")
    
    for i, command in enumerate(sqlCommands):
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError, msg:
            print "Command skipped: ", msg
        if(filename == 'map.sql'):
            temp = math.floor(i/(len(sqlCommands) * 1.0) * 100)
            sys.stdout.write("\r[%-20s] %d%%" % ('|'* int(temp/5), int(temp)))
            sys.stdout.flush()
    if(filename == 'map.sql'):
        sys.stdout.write("\r[||||||||||||||||||||] 100%")
        sys.stdout.flush()

# Download map.sql file 
urllib.urlretrieve('https://ts3.travian.us/map.sql', 'map.sql')

# Function calls to run SQL scripts
executeScriptsFromFile('pre-map.sql')
executeScriptsFromFile('map.sql')
executeScriptsFromFile('post-map.sql')
print

# Create DatFrame for top 10 alliances by population, based on most recent SQL pull
cursor.execute('SELECT aName, SUM(population) FROM total_table WHERE aName != "" AND CreatedTime = (SELECT CreatedTime from total_table ORDER BY CreatedTime DESC LIMIT 1)  GROUP BY aID ORDER BY SUM(population) DESC LIMIT 10;')
top_10_alliances = pd.DataFrame(cursor.fetchall())

# Define column names for select-star DataFrame
cols = ['playerID', 'xCoord', 'yCoord', 'tID', 'vID', 'village', 'userID', 'player', 'aID', 'aName', 'population', 'CreatedTime']

# Select all data from most recent SQL pull, save as a DataFrame 
cursor.execute('SELECT * FROM total_table WHERE CreatedTime = (SELECT CreatedTime from total_table ORDER BY CreatedTime DESC LIMIT 1);')
select_star = pd.DataFrame(cursor.fetchall())
select_star.columns = cols

# Saves top 10 alliances in a list
top10_list = top_10_alliances[0]

today = datetime.today()
# Loops through to create maps for all top 10 alliances
for i in top10_list:

    x = select_star.loc[(select_star.aName == i)]["xCoord"]
    y = select_star.loc[(select_star.aName == i)]["yCoord"] 

    fig = plt.figure()
    ax = plt.scatter(x,y)
    plt.title(i + " Map " + str(today.month) + '-' + str(today.day) + '-' + str(today.year))
    fig.savefig('Alliance_Maps/' + i + ".png")

# Commits 
cnx.commit()


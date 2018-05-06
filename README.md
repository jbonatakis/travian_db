# travian_db
### Authors: Jack Bonatakis and Duncan McConnell

## 1. Once each day, Travian publishes a 'map.sql' file. This can downloaded for each server, and no account is required. Navigate your browser to 'ts3.travian.us/map.sql' for an example (warning: file will automatically begin downloading). The URL can be changed to access the SQL file for your desired server. The script 'run_sql_scripts.py' is set to run each night via cron and automates the execution of the SQL scripts.

## 2. The 'pre-map.sql' script clears the 'x_world' table.

## 3. The 'map.sql' script contains the game data published by Travian, and is insterted into the newly cleared 'x_world' table ('x_world' is the default name given by Travian in their SQL file)

## 4. The 'post-map.sql' script inserts a datetime column into x_world, and then inserts the new data into the table 'total_table'. This table contains the published game data for each day of the game world. 

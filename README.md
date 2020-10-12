# Project1: Data Modeling with Postgres

> In this project, you'll apply what you've learned on data modeling with Postgres and build an ETL pipeline using Python. To complete the project, you will need to define > fact and dimension tables for a star schema for a particular analytic focus, and write an ETL pipeline that transfers data from files in two local directories into these > tables in Postgres using Python and SQL. 
> 
---------------
####  Song Dataset
> song_data/A/B/C/TRABCEI128F424C983.json
> song_data/A/A/B/TRAABJL12903CDCF1A.json


####  Log Dataset
 > log_data/2018/11/2018-11-12-events.json
 > log_data/2018/11/2018-11-13-events.json


---------------

#### Schema for Song Play Analysis
##### Fact Table

1.    **songplays** - records in log data associated with song plays i.e. records with page NextSong
       - songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

##### Dimension Tables


1.    **users** - users in the app
       - user_id, first_name, last_name, gender, level
 2.   **songs** - songs in music database
       - song_id, title, artist_id, year, duration
 3.   **artists** - artists in music database
       - artist_id, name, location, latitude, longitude
  4.  **time** - timestamps of records in songplays broken down into specific units
       - start_time, hour, day, week, month, year, weekday
       
---------------

## Scripts

### Create database

**create_tables.py** contains Python functions that connects to Postgres database using “psycopg2” run this file to reset your tables before each time you run your eti.ipynb scripts.

**sql_queries.py** contains SQL code for all your sql queries Create table ...
### Build ETL pipeline

**etl.ipynb** reads and processes a single file from song_data and log_data and loads the data into the tables.

**etl.py** contains Python functions that processes data from JSON formatted files, reads and processes files from song_data and log_data and loads them into the tables.

### Testing
**test.ipynb** displays the first 5 rows of each table to check the database.

---------------

## Requirements

1. Python 3.x
2. PostgreSQL

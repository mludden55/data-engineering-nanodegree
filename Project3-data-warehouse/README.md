# Data Warehouse Project
## Project Summary
The purpose of this project is to create a data warehouse for Sparkify that can be used for analyzing various attributes of songs and artists contained in the warehouse. We will build an ETL pipeline that extracts data from existing JSON logs, stages the data in Redshift and then transforms the data into a set of tables that the analytics team can use.

The following steps were taken to complete this project:

1. Create table schemas.

    A. Modify sql_queries.py to drop, create and insert to tables.

    B. Modify logic in create_tables.py for connecting to the database.

    C. Launch a Redshift cluster and connect to the database.

    D. Test the create statements by executing create_tables.py. 


2. Build an ETL Pipeline.

    A. Modify etl.py with logic for loading data from S3 to the staging tables.

    B. Modify etl.py with logic to load data from staging tables to analytics tables.

    C. Test by executing etl.py.

    D. Compare results with the expected results.

    E. Delete the redshift cluster.



## Description of database schema design:
The data warehouse includes 1 fact table, 4 dimension tables and 2 staging tables. A star schema is used to relate the fact table to the dimension tables.  The following foreign keys are included in the songplays fact table:


    start_time REFERENCES time(start_time),
    user_id REFERENCES users(user_id),
    song_id REFERENCES songs(song_id),
    artist_id REFERENCES artists(artist_id),

## Table Definitions
Fact table:  
songplays 

CREATE TABLE songplays(  
    songplay_id INT IDENTITY(0,1),  
    start_time TIMESTAMP REFERENCES time(start_time),  
    user_id VARCHAR(100) REFERENCES users(user_id),  
    level VARCHAR(100),  
    song_id VARCHAR(100) REFERENCES songs(song_id),  
    artist_id VARCHAR(100) REFERENCES artists(artist_id),  
    session_id BIGINT,  
    location VARCHAR(255),  
    user_agent TEXT,  
    PRIMARY KEY (songplay_id))

Dimension tables:  
artists  

CREATE TABLE artists(  
    artist_id VARCHAR(100),  
    name VARCHAR(255),  
    location VARCHAR(255),  
    latitude DOUBLE PRECISION,  
    longitude DOUBLE PRECISION,  
    PRIMARY KEY (artist_id))  


songs

CREATE TABLE songs(  
    song_id VARCHAR(100),  
    title VARCHAR(255),  
    artist_id VARCHAR(100) NOT NULL,  
    year INT,  
    duration DOUBLE PRECISION,  
    PRIMARY KEY (song_id))

users

CREATE TABLE users(  
    user_id VARCHAR(100),  
    first_name VARCHAR(100),  
    last_name VARCHAR(100),  
    gender CHAR(1),  
    level VARCHAR(100),  
    PRIMARY KEY (user_id))

time

CREATE TABLE time(  
    start_time TIMESTAMP,  
    hour INT,  
    day INT,  
    week INT,  
    month INT,  
    year INT,  
    weekday INT,  
    PRIMARY KEY (start_time))

Staging tables:

staging_events  
CREATE TABLE staging_events(  
    event_id INT IDENTITY(0,1),  
    artist_name VARCHAR(255),  
    auth VARCHAR(50),  
    user_first_name VARCHAR(100),  
    user_gender  CHAR(1),  
    item_in_session	INT,  
    user_last_name VARCHAR(100),  
    song_length	DOUBLE PRECISION,   
    user_level VARCHAR(50),  
    location VARCHAR(255),	  
    method VARCHAR(25),  
    page VARCHAR(35),  	
    registration VARCHAR(50),  	
    session_id	BIGINT,  
    song_title VARCHAR(255),  
    status INT,  
    ts VARCHAR(50),  
    user_agent TEXT,  	
    user_id VARCHAR(100),  
    PRIMARY KEY (event_id))

staging_songs  
CREATE TABLE staging_songs(  
    song_id VARCHAR(100),  
    num_songs INT,  
    artist_id VARCHAR(100),  
    artist_latitude DOUBLE PRECISION,  
    artist_longitude DOUBLE PRECISION,  
    artist_location VARCHAR(255),  
    artist_name VARCHAR(255),  
    title VARCHAR(255),  
    duration DOUBLE PRECISION,  
    year INT,  
    PRIMARY KEY (song_id))

## File Details  
1. dwh.cfg -  configuration file that contains database information.
2. create_tables.py -  python file to execute to create tables.
3. sql_queries.py - sql queries for adding, dropping, inserting and copying tables.  
4. etl.py -python file to execute to populate tables.





## How to Run
1. Create an Amazon Redshift cluster (see below).
2. Install Python3.
3. Create project folder and copy in all files from this project.  
4. Modify dwh.cfg with Redshift cluster information.
5. Run the following Python scripts from within a Python terminal:

	A. create_tables.py

        B. python etl.py

## Creating a Redshift cluster  
1. Login to Amazon Redshift: https://console.aws.amazon.com/redshift/
2. Create an IAM role that has read access to S3. Name the role myRedshiftRole. 
3. Click Clusters from left side.
4. Click Launch Cluster. 
5. For Cluster Details enter the following:  
        A. Cluster identifier: dwhcluster  
        B. Database name: dwh    
        C. Database port: 5439  
        D. Master user name: awsuser    
        E. Master user password: <your password>

6. For Cluster Details accept all defaults.
7. For Additional Configuration select:  
	A. VPC security groups: redshift_security_group  
	B. Available IAM roles: myRedshiftRole (role created in step #2)  
8. Go to roles: https://console.aws.amazon.com/iam/home?region=us-west-1
9. Enable AmazonRedshiftQueryEditor



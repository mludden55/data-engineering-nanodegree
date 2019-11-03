# Data Modeling with Postgres  
## Project Summary
This goals of this project are as follows:

1. Create a postGres database.
2. Read song/artist data from JSON files.
3. Massage the data and insert into database.


##Description of files and folders:

1. data - The primary data folder.
	
    A. log_data - Folder that contains log files in JSON format generated by the event simulator based on the songs in the dataset.

     B. song_data - files in JSON format that includes data about a song and the artist of the song.

2. etl.ipynb - Python notebook that runs queries to complete requirements for this project.

3. test.ipynb - Python notebook that runs queries to verify data has been inserted into various tables.

4. create_tables.py - Python script that drops and creates various tables.

5. etl.py - Python script that reads JSON files from "data" folder, parses the data and builds relations though logical process.

6. sql__queries.py - Python script that contains SQL statements used in create_tables.py, along with SQL for inserting and reading data.


##How to Run
1. Install and run a PostgreSQL instance.
2. Create a database named sparkifydb
3. Install Python3
4. Create project folder and copy in all files from this project.
5. Run the following Python scripts from within a Python terminal:

	A. create_tables.py

        B. python etl.py

from sqlalchemy import create_engine, event
import configparser
import psycopg2
import io
import os
import csv
import logging 
from io import StringIO
import pandas as pd
       
# Create and configure logger 
logging.basicConfig(filename="load_immigration_data.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  
# Creating logger object 
logger=logging.getLogger() 
  
# Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

# Read config file
config = configparser.ConfigParser()
config.read('dwh.cfg')

# Create database connections
engine = create_engine(config['CLUSTER']['HOST_POS'])
conn = psycopg2.connect(config['CLUSTER']['HOST_POS'])
conn.set_session(autocommit=True)
cur = conn.cursor()

# Use this to speed up to_sql
@event.listens_for(engine, 'before_cursor_execute')
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if executemany:
        cursor.fast_executemany = True
        cursor.commit()

# Read valid port data from csv and insert to database
port_valid = {}

dim_port_insert = """INSERT INTO dim_port
(abrev, port)
VALUES (%s, %s);"""

# Loop through valid_ports.csv
with open('valid_ports.csv', 'r') as data_csv:
    data = csv.reader(data_csv, delimiter="=")
 
    for row in data:
        port = []
        strLen = len(str(row))
        abrev = str(row)[3:6].strip()
        port_name = str(row)[16:strLen-3].strip()
        port.append(abrev)
        port.append(port_name)
        
        # Insert the port data to database
        cur.execute(dim_port_insert, [abrev, port_name])   
        
        # Create key-value pair for filtering immigration data
        port_valid[port[0]]=[port[1]]

counter = 0

# Loop through monthly immigration data files
for filename in os.listdir('../../data/18-83510-I94-Data-2016'):
    counter += 1

    # Read in data
    df_immigration = pd.read_sas('../../data/18-83510-I94-Data-2016/' + filename, 'sas7bdat', encoding='ISO-8859-1')
    logger.info("Number of rows: {}".format(df_immigration.shape[0]))    
    logger.info("Filtering data")

    # Filter certain columns. This will eliminate the bad columns from the month of June 
    df_immigration = df_immigration[["cicid", "i94yr", "i94mon", "i94cit", "i94res", "i94port", "arrdate", "i94mode", "i94addr", "depdate", "i94bir", "i94visa", "count", "dtadfile", "visapost", "occup", "entdepa", "entdepd", "entdepu", "matflag", "biryear", "dtaddto", "gender", "insnum", "airline", "admnum", "fltno", "visatype"]]
    logger.info("Number of rows after filter #1: {}".format(df_immigration.shape[0]))
    
    # Filter out where cicid and i94yr data is null
    df_immigration = df_immigration[df_immigration.cicid.notnull()]
    df_immigration = df_immigration[df_immigration.i94yr.notnull()]
    logger.info("Number of rows after filter #2: {}".format(df_immigration.shape[0]))

    # Filter so that only valid ports are included
    df_immigration = df_immigration[df_immigration.i94port.isin(list(port_valid.keys()))]
    logger.info("Number of rows after filter #3: {}".format(df_immigration.shape[0]))   
    logger.info("Inserting data")
    
    # Filter to only first 75,000 rows.
    df_immigration = df_immigration.head(75000)
    

    df_immigration.to_sql(name='fact_immigration', con=engine, if_exists = 'append', index=False, method='multi')
    
    # Delete dataframe
    del df_immigration
    
logger.info("Data insert complete!") 

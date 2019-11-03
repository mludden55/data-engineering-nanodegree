import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

""" Function for dropping database tables using drop_table_queries. """
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

""" Function for creating database tables using create_table_queries. """
def create_tables(cur, conn):
    for query in create_table_queries:
        #print(query)
        cur.execute(query)
        conn.commit()

""" Main function that:
1. Reads configuration file.
2. Connects to database.
3. Drops and creates tables.
4. Closes database connection.
"""
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(config['CLUSTER']['HOST'],config['CLUSTER']['DB_NAME'],config['CLUSTER']['DB_USER'],config['CLUSTER']['DB_PASSWORD'],config['CLUSTER']['DB_PORT']))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
    

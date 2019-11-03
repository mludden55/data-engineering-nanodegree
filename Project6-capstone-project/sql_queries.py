import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP STAGING TABLES
fact_immigration_table_drop = "DROP TABLE IF EXISTS fact_immigration"

# DROP DIMENSION TABLES
dim_temperature_table_drop = "DROP TABLE IF EXISTS dim_temperature"
dim_demographics_table_drop = "DROP TABLE IF EXISTS dim_demographics"
dim_airport_table_drop = "DROP TABLE IF EXISTS dim_airport"
dim_port_table_drop = "DROP TABLE IF EXISTS dim_port"

# CREATE STAGING TABLES
fact_immigration_table_create = ("""CREATE TABLE fact_immigration(
    immigration_id int,
    cicid int NOT NULL,
    i94yr int NOT NULL,
    i94mon int NOT NULL,
    i94cit int,
    i94res int,
    i94port char(3),
    arrdate int,
    i94mode int,
    i94addr char(3),
    depdate int,
    i94bir int,
    i94visa int,
    count int,
    dtadfile varchar,
    visapost char(3),
    occup char(3),
    entdepa char(1),
    entdepd char(1),
    entdepu char(1),
    matflag char(1),
    biryear int,
    dtaddto varchar,
    gender char(1),
    insnum varchar,
    airline char(3),
    admnum varchar,
    fltno varchar,
    visatype char(3))
""")

dim_temperature_table_create = ("""CREATE TABLE dim_temperature(
    dt varchar,
    averageTemperature int,
    averageTemperatureUncertainty int,
    city varchar NOT NULL,
    country varchar NOT NULL,
    longitude char(10) NOT NULL,
    latitude char(10) NOT NULL,
    PRIMARY KEY (dt))
""")

dim_demographics_table_create = ("""CREATE TABLE dim_demographics(
    count int NOT NULL,
    city varchar NOT NULL,
    number_of_veterans int NOT NULL,
    male_population int NOT NULL,
    foreign_born int NOT NULL,
    average_household_size int NOT NULL,
    median_age int NOT NULL,
    state varchar NOT NULL,
    race varchar NOT NULL,
    total_population int NOT NULL,
    state_code char(2) NOT NULL,
    female_population int NOT NULL,
    PRIMARY KEY (city, state_code))
""")

dim_airport_table_create = ("""CREATE TABLE dim_airport(
    ident char(10),
    type varchar,
    name varchar,
    elevation_ft int,
    continent char(2),
    iso_country char(2),
    iso_region char(10),
    municipality varchar,
    gps_code char(10),
    iata_code char(3),
    local_code char(10),
    coordinates varchar,
    PRIMARY KEY (ident))
""")

dim_port_table_create = ("""CREATE TABLE dim_port(
    abrev varchar,
    port varchar)
""")

#dim_city_insert = """INSERT INTO dim_city
#(city, state, median_age, male_pop, female_pop, total_pop, num_vets, foreign_born, avg_household_size, state_code,
#race, count)
#VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""



#songplay_table_insert = ("""INSERT INTO immigration_country (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
#    SELECT DISTINCT 
#        TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time, 
#        e.user_id, 
#        e.user_level,
#        s.song_id,
#        s.artist_id,
#        e.session_id,
#        e.location,
#        e.user_agent
#    FROM staging_events e, staging_songs s
#    WHERE e.page = 'NextSong'
#    AND e.song_title = s.title
#    AND user_id NOT IN (SELECT DISTINCT s.user_id FROM songplays s WHERE s.user_id = user_id
#                       AND s.start_time = start_time AND s.session_id = session_id )
#""")


# QUERY LISTS
drop_table_queries = [fact_immigration_table_drop, dim_temperature_table_drop, dim_demographics_table_drop, dim_airport_table_drop, dim_port_table_drop]
create_table_queries = [fact_immigration_table_create, dim_temperature_table_create, dim_demographics_table_create, dim_airport_table_create, dim_port_table_create]


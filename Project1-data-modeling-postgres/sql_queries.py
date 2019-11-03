# DROP TABLES

songplay_table_drop = "DROP table IF EXISTS songplays"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays (songplay_id int, start_time timestamp, user_id int, level varchar(100), song_id varchar(100), artist_id varchar(100), session_id varchar, location varchar, user_agent varchar(1000));")

user_table_create = ("CREATE TABLE IF NOT EXISTS users (user_id int, first_name varchar, last_name varchar, gender char(1), level varchar(100), PRIMARY KEY (user_id))")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs (song_id varchar(100), title varchar, artist_id varchar(100), year char(4), duration float, PRIMARY KEY (song_id));")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists (artist_id varchar(100), name varchar, location varchar, latitude float, longitude float, PRIMARY KEY (artist_id));")

time_table_create = ("CREATE TABLE IF NOT EXISTS time (start_time timestamp, hour int, day int, week int, month int, year char(4), weekday int, PRIMARY KEY (start_time));")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET first_name=users.first_name, last_name=users.last_name, gender=users.gender, level=users.level
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO UPDATE SET title=songs.title, artist_id=songs.artist_id,
year=songs.year, duration=songs.duration
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO UPDATE SET name=artists.name, location=artists.location, latitude=artists.latitude, 
longitude=artists.longitude
""")


time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO UPDATE SET hour=time.hour, day=time.day, week=time.week, month=time.month, 
year=time.year, weekday=time.weekday
""")

# FIND SONGS

song_select = ("""SELECT s.song_id, a.artist_id FROM songs s, artists a
WHERE s.artist_id = a.artist_id  
    AND s.title = %s
    AND a.name = %s
    AND s.duration = %s
""")



# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
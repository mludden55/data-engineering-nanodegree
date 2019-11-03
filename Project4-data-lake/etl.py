import configparser
import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_timestamp
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.functions import monotonically_increasing_id


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']

# create spark session
def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.5") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = os.path.join(input_data, "song_data/A/A/A/*.json")

    # read song data file
    print('path', song_data)
    df = spark.read.json(song_data)
    print("Song data count:" , df.count()) 

    # extract columns to create songs table
    songs_table = df.filter(df.song_id.isNotNull())\
                    .select("song_id", "title", "artist_id", "year", "duration")\
                    .dropDuplicates(subset=['song_id'])
    
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id').parquet(os.path.join(output_data, 'songs.parquet'), 'overwrite')
    print("Song table write complete.") 
    

    # extract columns to create artists table
    artists_table = df.filter(df.artist_id.isNotNull())\
                      .select("artist_id", "artist_name", "artist_location", \
                               "artist_latitude", "artist_longitude")\
                      .dropDuplicates(subset=['artist_id'])

    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists.parquet'), 'overwrite')
    print("Artists table write complete.") 


def process_log_data(spark, input_data, output_data):
	# get filepath to song data file
    log_data = os.path.join(input_data, "log_data/*/*/*.json")

    # read log data file
    df = spark.read.json(log_data)
    print("Log data count:" , df.count()) 
    
    # filter by actions for song plays
    songplays_table = df['ts', 'userId', 'level','sessionId', 'location', 'userAgent']


    # extract columns for users table    
    users_table = df['userId', 'firstName', 'lastName', 'gender', 'level']
    users_table = users_table.dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users.parquet'), 'overwrite')
    print("Users table write complete.") 

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: str(int(int(x)/1000)))
    df = df.withColumn("timestamp", get_timestamp(df.ts))

    
    # create datetime column from original timestamp column
    get_datetime = udf(lambda x: str(datetime.fromtimestamp(int(x) / 1000.0)))
    df = df.withColumn("start_time", get_timestamp(df.ts))
    
    # extract columns to create time table
    time_table = df.filter(df.timestamp.isNotNull())\
                   .select(df.timestamp.alias("start_time"),\
                       hour(df.timestamp).alias("hour"),\
                       dayofmonth(df.timestamp).alias("day"),\
                       weekofyear(df.timestamp).alias("week"),\
                       month(df.timestamp).alias("month"),\
                       year(df.timestamp).alias("year"),\
                       date_format(df.timestamp, 'E').alias("weekday"))\
                   .dropDuplicates(subset=['start_time'])

    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'time.parquet'), 'overwrite')
    print("Time table write complete.") 

    # read in song data to use for songplays table
    song_df = spark.read.parquet(output_data + 'songs.parquet/*/*/*')

    # read in artists data to use for songplays table    
    artists_df = spark.read.parquet(output_data + 'artists.parquet/*')

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = df.join(song_df, (df.song==song_df.title) & (df.length==song_df.duration), how='inner')\
                        .select(monotonically_increasing_id().alias('songplay_id'), \
                                df.timestamp.alias('start_time'),\
                                df.userId.alias('user_id'),\
                                month(df.timestamp).alias('month'), 
                                year(df.timestamp).alias('year'),
                                df.level,\
                                song_df.song_id,\
                                df.artist,\
                                df.sessionId.alias('session_id'),\
                                df.location,\
                                df.userAgent.alias('user_agent'))

    # extract columns from joined artists and songplays_table to create songplays_table2    
    songplays_table2 = songplays_table.join(artists_df, songplays_table.artist==artists_df.artist_name, how='inner')\
                          .select(monotonically_increasing_id().alias('songplay_id'), \
                                songplays_table.start_time,\
                                songplays_table.user_id,\
                                songplays_table.month, 
                                songplays_table.year,
                                songplays_table.level,\
                                songplays_table.song_id,\
                                songplays_table.artist,\
                                songplays_table.session_id,\
                                songplays_table.location,\
                                songplays_table.user_agent)
        

    # write songplays table to parquet files partitioned by year and month
    songplays_output = os.path.join(output_data, "songplays_table.parquet")
    songplays_table2.write.partitionBy('year', 'month').parquet(songplays_output, mode="overwrite")
    print("Songplays table write complete.") 


def main():
    # create spark session and initialize input/output data
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://mludden-bucket-demo/"

    # process the song and log data
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
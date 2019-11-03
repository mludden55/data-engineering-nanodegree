# Data Lake Project
## Project Summary
Sparkify is a music streaming startup that has grown their user base and song database who wish to move their data warehouse to a data lake.

The goal of this project is to create an ETL pipeline to copy data from JSON logs to a data lake hosted on Amazon S3.  In order to achieve this we read data maintained on Amazon S3, transform the data into fact and dimension tables and then load the tables back onto S3.  The data is then written to partitioned parquet tables that are maintained in an S3 bucket.



##Code Overview:
1. Read song data and log data from S3 on Amazon.
2. Create temporary tables that filter out duplicate data.
3. Write the tables to parquet files on Amazon S3 with specified partitions.

##File Details  
1. dl.cfg -  configuration file that contains aws information.
2. unzip.py -  python file to execute to extract test data in project workspace.
3. etl.py - python file to execute to read data and then write to tables hosted on Amazon S3.





##How to Run
1. Create a cluster on Amazon EMR.
2. Create a bucket for maintaining data on Amazon S3.
3. Update AWS IAM credentials in dl.cfg file.
4. Run the following python command in a terminal: python etl.py

##Creating an EMR cluster  
1. Services > EC2 > Keypairs (from left nav)
2. Create keypair named spark-cluster
3. Download, save to folder.
4. Services > search for EMR Service
5. Create Cluster  
	A. Name: spark-udacity  
	B. S3 folder: default  
	C. Launch Mode: Cluster  
	D. Applications: Spark: Spark 2.4.0  
	E. EMP Options: emr-5.20.0  
	F. Instance Type: m5.xlarge  
	G. Number of Instances: 4  
	H. EC2 key pair: select one you created in Step #2  
	I. Remaining default options  
6. Click Create Cluster

##Creating an Amazon Bucket
1. Services > S3
2. Buckets

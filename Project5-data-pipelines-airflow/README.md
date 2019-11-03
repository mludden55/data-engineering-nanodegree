# Data Warehouse Project
## Project Summary
The purpose of this project is to automate the ETL pipelines for the music streaming company Sparkify.  Apache Airflow will be used to load and transform the data, along with adding data integrity checks to the table loads.

The following steps were taken to complete this project:

1. Create a Redshift Cluster in Amazon AWS.

2. Create tables for use in Amazon Redshift Cluster database.

3. Modify sample DAG and related python files provided to run in Apache Airflow.

4. Start Apache Airflow.

5. Create appropriate connections in Apache Airflow.

6. Run the DAG from step #3.


##Creating a Redshift cluster  
1. Login to Amazon Redshift: https://console.aws.amazon.com/redshift/
2. Create a security group for Redshift. Name it: redshift___security___group.
3. Create an IAM role that has read access to S3. Name the role myRedshiftRole. 
4. Click Clusters from left side.
5. Click Launch Cluster. 
6. For Cluster Details enter the following:  
        A. Cluster identifier: redshift-cluster-1  
        B. Database name: dev    
        C. Database port: 5439  
        D. Master user name: awsuser    
        E. Master user password: <your password>

7. For Cluster Details accept all defaults.
8. For Additional Configuration select:  
	A. VPC security groups: redshift_security_group  
	B. Available IAM roles: myRedshiftRole (role created in step #2)  

##Creating tables
1. From Redshift Dashboard, click "Query Editor" from left navigation.
2. Select the dev database. 
3. Change schema to "public".
4. Run each of the create tables queries from create_tables.sql in the project repository.

##DAG, SQL and Python File Details  
1. etl_dag.py-  DAG that is run from within Apache Airflow to load data.
2. create_tables.py -  sql that is to be run in Query Editor to create appropriate tables.
3. stage_redshift.py - Read files from S3 and load into Redshift tables.
4. data_quality.py - runs data quality checks on data that is inserted into tables.  
5. load_dimension.py - read from staging tables and populate dimension tables.
6. load_fact.py - read data and populate fact tables.


##Start Apache Airflow
1. From workspace command prompt run the following: /opt/airflow/start.sh
2. Click "Access Airflow" from workspace. 

##Create appropriate connections in Apache Airflow
1. From Apache Airflow Click Admin > Connections.
2. Click "Create". 
3. Configure connection as follows:  
	A. Conn Id: aws_credentials.  
	B. Conn Type: Amazon Web Services  
	C. Login: Access Key ID from IAM users  
	D. Password: Secret Access Key from IAM users  
	E. Remaining fields blank  
4. Click "Save and Add Another".
5. Configure connections as follows:  
	A. Conn ID: redshift  
	B. Conn Type: Postgres  
	C. Host: Endpoint of Redshift Cluster created above  
	D. Schema: dev  
	E. Login: awsuser  
	F. Password: password from Redshift Cluster created above  
	G. Port: 5439  

##Run the DAG
1. From Airflow click "DAGs" from top navigation.
2. You shoud see DAG named etl_dag.
3. Click the Play button.



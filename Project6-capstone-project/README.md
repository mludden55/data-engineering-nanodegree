# Capstone Project
## Project Summary

The following steps were taken to complete this project:

1. Create a Redshift Cluster in Amazon AWS.

2. Run the Capstone Project Template notebook.


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

7. On Node Configuration tab select the following:  
        A. Node type: dc2.large   
        B. Cluster type: Multi Node  
        C. Number of compute nodes: 8  
         
8. On Additional Configuration tab select the following:  
	A. VPC security groups: redshift_security_group (group created in step #2)   
	B. Available IAM roles: myRedshiftRole (role created in step #3)  



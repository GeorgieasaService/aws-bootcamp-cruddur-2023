# Week 5 — DynamoDB 
 
## Non-Relational Databases
DynamoDB is a NoQL Public Database-as-a-service (DBaaS) product.
Ideally, a non-relational database will allow for the consistent performance of internet scale applications when dealing with a variable workload
 
### Non-Relational Database Solutions on AWS
DynamoDB is a non-relational database solution for AWS and is used for high performance applications at any scale. 

NOTE: A Partition Key and a Sort Key are used to organise items in a table. To make it easier to understand, think of table as Hogwarts, and the 4 houses each represent a Partition Key inside of the table, the Sort Key can be used to represent the classes of the students. 
![image](https://user-images.githubusercontent.com/67550608/235657472-4ed2f8f2-69d0-415e-8a0a-6afc048fda51.png)
 
## Security Considerations
###  AWS Security Considerations
- Use a VPC Endpoint to connect the application inside of your vpc directlky to DynamoDB. This will prevent unauthorized access to your instance from the public internet.
- Compliance standard is what your business requires. Dynamo DB should only be used in the AWS region that you're legally allowed to be holding user data in.
- Use Amazon Organisations Service Control Policy (SCP) - to manage DynamoDB table deletion, creation, region-lock etc.
- AWS CloudTrail is enabled and monitored to trigger alerts on malicious DynamoDB behaviour by an identity in AWS.
- As of April 2023 Amazon GuardDuty does not support DynamoDB as per the AWS Documentation. So, consider AWS Config Rules in the region the DynamoDB table is running.

### Application Security Best Practices
 - DynamoDB to use appropriate Authentication - IAM Roles and AWS Cognito Identity pool (Temporary Access). Avoid IAM Groups and Users (Permanent Access).
 - DynamoDB User Lifecycle Management - Create, Modify, Delete Users. 
 - AWS IAM Role instead of individual users to access and manage DynamoDB. DAX Service IAM Role to allow Read-Only Access to DynamoDB.

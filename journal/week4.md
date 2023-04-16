# Week 4 — Relational Databases

## Relational Database Solutions on AWS
 - Aurora:
 - RDS:
 
 ![image](https://user-images.githubusercontent.com/67550608/232323190-415537c0-0e52-4323-add9-f8c3c73e55b8.png)


## Why RDS
It offers different dbs engines such as Aurora(both MySQL or PostgreSQL compatible version), Mysql, PostgreSQL, Oracle

## Security Considerations
There is a need for sensitive info(such as: credit card info & passwords) in databases to be used and stored in a secure manner
Here are some security consideration:
 - Create your database in the region the data originates from. (data sovereignty concerns)
 - Enabling deletion protection is a good idea
 - The dbs should always be encrypted.
 - The dbs shouldn't be publically accessible
 - configure the Security Group of the dbs instance to ONLY allow access from the IP of the admin 


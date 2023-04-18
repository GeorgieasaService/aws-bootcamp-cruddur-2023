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
 - The dbs shouldn't be publicly accessible
 - You can configure an outbound rule of the Security Group of the dbs instance to 0.0.0.0 but configure the inbound rules to ONLY allow access from the IP of the admin
 - Ensure that CloudTrail is enabled and configured to monitor alerts on malicious RDS behaviour by an identity in AWS

 # Instructions
 You could use the console but we'll use the aws-cli

### Creating the RDS instance
 from your terminal use the following code to create your RDS instance
 
```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username cruddurroot \
  --master-user-password insert-your-password \
  --allocated-storage 20 \
  --availability-zone insert-your-region-and-az(eg. us-east-1a) \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp3 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
```

from your terminal use the following command to connect to psql via the psql client cli tool
```
psql -U postgres --host localhost
```

### Some psql commands to remember
```
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```

### Creating a local database
Use this command to create a dbs within the psql client
```
create database cruddur;
```
From the backend-flask dir, create a new dir called db and inside a file called schema.sql
Once created, add the following sql command into the schema.sql file
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

Exit psql using this command
```
\q
```

While in your backend-flask dir and enter the following command into your terminal and afterwards you'll be prompted to your password
```
psql cruddur < db/schema.sql -h localhost -U postgres
```

Postgres Connection URL's are in the following syntax
```
postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
```

Now create the following CONNECTION_URL env var for the local dbs
```
export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
gp env CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
```

Do the same for the RDS dbs instance
```
export PROD_CONNECTION_URL="postgresql://[user[:password]@][endpoint][:port][/dbname]"
gp env PROD_CONNECTION_URL="postgresql://[user[:password]@][endpoint][:port][/dbname]"

```

From the backend-flask dir, create a new dir called bin and inside 3 files called "db-create", "db-drop" and "db-schema-load". 

NOTE: Because they're in the bin dir they don't need file extensions to execute.

Once created, add the following shebang on the first line of each of the 3 files
```
#! /usr/bin/bash
```
NOTE: we used the "whereis bash" command to find bash for the distro we're using


To change the executable of the file created before, insert the following lines of code
```
chmod u+x bin/db-create
chmod u+x bin/db-drop
chmod u+x bin/db-schema-load
```

Add the following lines of code into the db-drop file
```
echo "db-drop"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
```

In db-create add the following lines of code
```
echo "db-create"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "create database cruddur;"

```









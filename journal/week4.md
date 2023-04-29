# Week 4 — Relational Databases

## Relational Database Solutions on AWS
 - RDS: Amazon RDS is a managed service that makes it simple to set up, operate, and scale databases in the cloud. 
 - Aurora: Aurora extends RDS beyond the capabilities of RDS and allows for higher availability of database instances spanning more than a single region, automatic buck-ups and failover to read replicas.
 
 ![image](https://user-images.githubusercontent.com/67550608/232323190-415537c0-0e52-4323-add9-f8c3c73e55b8.png)


## Why RDS
It offers different dbs engines such as Aurora(both MySQL or PostgreSQL compatible version), Mysql, PostgreSQL, Oracle. And lastly, the scale of our application makes RDS ideal for a smaller workload.

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

NOTE: Because they're in the bin/ dir they don't need file extensions to execute.

Once created, add the following shebang on the first line of each of the 3 files
```
#! /usr/bin/bash
```
NOTE: we used the "whereis bash" command to find bash for the distro we're using


To change the executable of the file created before, insert the following lines of code
```
chmod u+x bin/db-create db-drop db-schema-load
```

Add the following lines of code into the db-drop file
```
echo "db-drop"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "DROP DATABASE IF EXISTS cruddur;"
```

In db-create add the following lines of code
```
echo "db-create"
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "create database cruddur;"

```

In db-schema-load add the following lines of code
```
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

schema_path="$(realpath .)/db/schema.sql"

echo $schema_path
# This if statement checks the connection URL to see what db we're using
if [ "$1" = "prod" ]; then
  echo "Running in production mode"
  URL=$PROD_CONNECTION_URL
else
  URL=$CONNECTION_URL
  echo "Running in local mode"
fi

psql $URL cruddur < $schema_path
```

In the schema.sql file, add the following lines of code
```
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;

CREATE TABLE public.users (
 uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
 display_name text,
 handle text,
 cognito_user_id text,
 created_at TIMESTAMP default current_timestamp NOT NULL
);

CREATE TABLE public.activities (
 uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
 user_uuid UUID not null,
 message text NOT NULL,
 replies_count integer DEFAULT 0,
 reposts_count integer DEFAULT 0,
 likes_count integer DEFAULT 0,
 reply_to_activity_uuid integer,
 expires_at TIMESTAMP,
 created_at TIMESTAMP default current_timestamp NOT NULL
);
```

create a file inside the bin/ dir called "db-connect" and add the insert following lines of code into it
```
#! /usr/bin/bash
psql $CONNECTION_URL
```

Add permissions to this file
```
chmod u+x db-connect
```

create another file inside the bin/ dir called "db-seed" and add the insert following lines of code into it
```
#! /usr/bin/bash
#echo "== db-seed-load"
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

seed_path="$(realpath .)/db/seed.sql"

echo $seed_path

if [ "$1" = "prod" ]; then
 echo "Running in production mode"
 URL=$PROD_CONNECTION_URL
else
 URL=$CONNECTION_URL
fi

psql $URL cruddur < $seed_path
```

In the db/ dir create a new file called seed.sql and insert the following lines of code into it
```
-- this file was manually created
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
```

# connecting to RDS

If you've stopped and started or re-created your gitpod/codespace enviroment, make sure to rerun the db-create, db-schema-load and db-seed scripts in that exact order before running the db-connect script. Those docker containers need to be running before making the connection

To see the connections to the db create a file called db-sessions in the backend-flask/bin dir 
```
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
psql $NO_DB_CONNECTION_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```

Change the permission of the db-sessions file
```
 chmod u+x ./db-sessions
```

Create a file called db-setup in the backend-flask/bin dir
This will be used to create and setup the local database
```
#! /usr/bin/bash

-e # stop if it fails at any point
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}==== ${LABEL}${NO_COLOR}\n"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"

```

Change the permission of the db-setup file
```
 chmod u+x ./db-setup
```

## Installing the driver for psql

Add the following libraries into the requirements.txt in the backend-flask/ dir
```
psycopg[binary]
psycopg[pool]
```

and run this command to install the dependencies
```
pip install -r requirements.txt
```


and run the for this time the following command:
```
pip install -r requirements.txt
```

create a file under lib called db.py. this will be the connection for your backend
```
from psycopg_pool import ConnectionPool
import os

def query_wrap_object(template):
  sql = f"""
  (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
  {template}
  ) object_row);
  """
  return sql

def query_wrap_array(template):
  sql = f"""
  (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
  {template}
  ) array_row);
  """
  return sql

connection_url = os.getenv("CONNECTION_URL")
pool = ConnectionPool(connection_url)
```

and insert the library into home_activities.py
```
from lib.db import pool,query_wrap_array
```

and add the following code
```
sql = """
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC
      """
      print(sql)
      span.set_attribute("app.result_length", len(results))
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)
          # this will return a tuple
          # the first field being the data
          json = cur.fetchall()
      return json[0]
```

from the docker-compose file change change the CONNECTIONS_URL to the following
```
      CONNECTION_URL: "postgresql://postgres:password@db:5432/cruddur"
```

From the console start the RDS instance if it isn't running

Edit this PROD_CONNECTION_URL with the details of your RDS instance, it should point to your RDS database.
```
postgresql://userofthedb:masterpassword@endpointofthedb:5432/cruddur
```
create the local env var and on gitpod or codespace
```
export PROD_CONNECTION_URL="postgresql://userofthedb:masterpassword@endpointofthedb:5432/cruddur"
gp env PROD_CONNECTION_URL="postgresql://userofthedb:masterpassword@endpointofthedb:5432/cruddur"
```

To connect to the RDS instance we need to provide our Gitpod IP.
```
export ipshowaddr=$(curl ifconfig.me)
gp env ipshowaddr=$(curl ifconfig.me)
```

From your AWS console edit the RDS instance SG to allow for inbound traffic on port 5432.

Create the following env vars for the RDS Security Group and the Security Group rule
```
export DB_SG_ID="sg-sdfsdf"
gp env DB_SG_ID="sg-sdfsdf"
export DB_SG_RULE_ID="sgr-sdfsdfsdf"
gp env DB_SG_RULE_ID="sgr-sdfsdfsdf"
```

Since the ip address of GITPOD changes every time we restart the environment, we need to automatically update the RDS SG Rule for the gitpod to access the rds instance. Below, is the script for this action. Add it to a new file called rds-update-sg-rule under bin/
```
aws ec2 modify-security-group-rules \
    --group-id $DB_SG_ID \
    --security-group-rules "SecurityGroupRuleId=$DB_SG_RULE_ID,SecurityGroupRule={Description=GITPOD,IpProtocol=tcp,FromPort=5432,ToPort=5432,CidrIpv4=$ipaddrshow/32}"
```

In the file .gitpod.yml add this line of code so it will get the ip of the instance
```
    command: |
      export ipaddrshow=$(curl ifconfig.me)
      source  "$THEIA_WORKSPACE_ROOT/backend-flask/bin/rds-update-sg-rule"
```

# Creating a Lambda Function
Create a lambda function in the same region as the rest of the services in this project.
Add the code to a new file called cruddur-post-confirmation.py in aws/lambdas. (create aws/lambdas if it doesn't already exist)

```
import json
import psycopg

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print('userAttributes')
    print(user)
    user_display_name = user['name']
    user_email        = user['email']
    user_handle       = user['preferred_username']
    user_cognito_id   = user['sub']
    try:
        conn = psycopg.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        sql = f"""
            "INSERT INTO users (
                display_name,
                email,
                handle,
                cognito_user_id
            ) 
            VALUES(
                {user_display_name},
                {user_email},
                {user_handle},
                {user_cognito_id}
            )"
        """            
        cur.execute(sql)
        conn.commit() 

    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event
```

The env var which our lambda function will use is CONNECTION_URL. This has the variable of the PROD_CONNECTION_URL set in gitpod or codespace (eg: PROD_CONNECTION_URL="postgresql://userofthedb:masterpassword@endpointofthedb:5432/cruddur)

Once you've create the env var. From your AWS console create a Lambda Layer for the lambda function we created. 
layer>add layers> select specify arn
```
arn:aws:lambda:us-east-1:898466741470:layer:psycopg2-py38:2
```

Make sure to attach the AWSLambdaVPCAccessExecutionRole policy the lambda role by going to configuration>permission> link under the Role name.

Once the policy is attached, in Lambda>Configurations go to VPC and select the VPC where  the RDS instance resides,
select the subnet mask and the same SG of the RDS instance.

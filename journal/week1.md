# Week 1 — App Containerization

# Summary
This week we launched our application using two docker containers, one hosting the frontend and an additional one for hosting the backend.

# The importance of Containerisation
Containerisation offers quicker performance in a dev/test environment in the sense that we can quickly kill and restart containers

### **Why is containerisation popular?**
It is a agnostic way to run application.
Most engineers started developing apps on containers due to the simplicity to pass the package without considering requirements. Containerisation offers quicker performance in a dev/test environment in the sense that we can quickly kill and restart containers


**Managed Vs Unmanaged Container**

Managed Containers means that the Provider (eg. AWS) manages the underlying services of the container (ECS or EKS). In this case Cloud provider will also be managing the security prospective.

Unmanaged Containers means you are running your container on your servers and you have to manage the entire system. In this case you will be in charged of applying security patches.




### **Docker Components**


- Client is local installation of docker on your system (build, pull, run features)
- Server is the location where is running the container

Registry is a location of the images available on internet (an exampple is docker hub). you could have a private registry inside of your organisation.

### **What is Container Security?**
Container Security is the practice of protecting your application hosted on compute service like containers.

#### **Security Best Practice**
- Keep Host & Docker Updated to latest security patches.
- Docker Daemon & containers should run in non root user mode
- Image Vulnerability Scanning
- Trust a Private vs Public Image Registry
- No Sensitive Data in Docker Files or Images
- Use Secret Management Services to share secrets.
- Read only file system and volume for dockers
- Separate databases for long term storage
- Use DevSecOps practices while building application security
- Ensure all code is tested for vulnerabilities before production use


#### **Docker Compose** 
It is a tool for defining and running multi container Docker Applications (It's a .yml file).

### Tool to identify vulnerabilities in your Docker Compose
Snyk OpenSource Security

### Tools to Store and Manage Secrets
- AWS Secret Manager
- Hashicorp Vault

### Tools to scan Image Vulnerability
- AWS Inspector
- Clair
- Snyk Container Security

### Running Containers in AWS
Problem with docker compose and Docker Containers: If you need to change, you need to stop the machine update the file and restart.

For the Managed Containers you can use the following AWS service
- AWS ECS
- AWS EKS
- AWS Fargate

Reason to run containers on the cloud
- Integration with AWS Services
- Using automation to provision containers at sale with speed and security


## Docker

### Creating docker backend
To create the docker configuration for the backend-flask, create a file called **Dockerfile** and copy the following code

```
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```

from the project directory type the following code to build the image
```
docker build -t backend-flask ./backend-flask
```

typing this command to run the image of the container
```
docker run --rm -p 4567:4567 -it backend-flask
```


this code creates 2 environment variables and are run in the container

```
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```

#### Creating docker frontend
move to the frontend folder and install npm
this command will be execute every time you launch the gitpod session
```
cd frontend-react-js
npm i
```

To create the docker configuration for the frontend-react-js, create a file called **Dockerfile** and copy the following code
```
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```

### Create docker compose

Create the file called docker-compose.yml from the main root and copy the following code.
```
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur
```


to run the docker compose, go to the docker compose and click ***docker up***

add this code on the docker compose yml to prepare the image for dyanodb and postgres

```
 dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal
  db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
```

on docker compose file, add this code after networks
```
volumes:
  db:
    driver: local    
```

to check the if postgres, check the command in the section troubleshooting.
to check the if dyanodb works, check the command in the section troubleshooting.

### Troubleshooting commands

This command check the images on the local machine
```
docker images
```

this  command check the status of the container. good to see if it is not running
```
docker ps
```


from docker extention, click the container image and go to  **attach shell** this open the shell on the contianer. use this tool for troubleshooting



I got problem commiting as I did some changes on github and the same time on gitpod. to solve 

```
git pull --rebase
git push
```

To test postgres, enter to postgres on container type the following command
```
psql -Upostgres --host localhost
```

to test dynabodb locally you can check using the following command

## ***Create a local table***
```
aws dynamodb create-table \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --table-class STANDARD
```
## ***Create an Item***
```aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}}' \
    --return-consumed-capacity TOTAL  
```

## ***List Tables***
```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

## ***Get Records***
```
aws dynamodb scan --table-name Music --query "Items" --endpoint-url http://localhost:8000

```

# Backend

![image](https://user-images.githubusercontent.com/67550608/221628517-4195f341-ab5e-4958-9962-5df38cd5d579.png)


# Frontend

![image](https://user-images.githubusercontent.com/67550608/221628001-500297ee-0e69-46c8-95d0-01558e5c23f7.png)

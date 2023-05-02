# Week 5 — DynamoDB 
 
## Non-Relational Databases
DynamoDB is a NoQL Public Database-as-a-service (DBaaS) product.
Ideally, a non-relational database will allow for the consistent performance of internet scale applications when dealing with a variable workload
 
### Non-Relational Database Solutions on AWS
DynamoDB is a non-relational database solution for AWS and is used for high performance applications at any scale. 
 
## Security Considerations
###  AWS 
- Use a VPC Endpoint to connect the application inside of your vpc directlky to DynamoDB. This will prevent unauthorized access to your instance from the public internet.
- Compliance standard is what your business requires. Dynamo DB should only be used in the AWS region that you're legally allowed to be holding user data in.
- Use Amazon Organisations Service Control Policy (SCP) - to manage DynamoDB table deletion, creation, region-lock etc.
- AWS CloudTrail is enabled and monitored to trigger alerts on malicious DynamoDB behaviour by an identity in AWS.
- As of April 2023 Amazon GuardDuty does not support DynamoDB as per the AWS Documentation. So, consider AWS Config Rules in the region the DynamoDB table is running.

### Application Security Considerations
 

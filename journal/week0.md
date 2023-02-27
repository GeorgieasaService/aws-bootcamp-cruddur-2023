# Week 0 — Billing and Architecture

# Introduction 
During Week 0 of Andrew Brown's Cloud Bootcamp the I and the rest of my cohort were introduced to the project as well as it's requirements and planning that needed to be done. There were practical tasks that had to be done such as setting up the aws-cli as well as configuring billing alarms on my AWS account. 

# Case study and Gathering Requirements
We started by learning about the importance of gathering requirements before starting any project. This involves understanding the user's needs, business objectives, and the constraints of the project. It helps to ask questions, there was emphasis on asking dumb questions to determine the risks, assumptions and constraints of the client. This helps in creating a solid foundation for the project and ensures that the end product meets the user's expectations.

Enter Cruddur, an upcoming social media platform built in the cloud over a 13-14 week period. What makes Cruddur unique is the expirational time-based nature of it's messages which the user has the option of posting publically while also being in-full control over the time-period in which the message is available to be viewed and interacted with by other users before it expires.

# Conceptual Design
This week we learned about the conceptual design phase, here we used simple sketches or in my case, a diagram to visualise the high-level structure of the project.

![image](https://user-images.githubusercontent.com/67550608/221536821-3dea059b-eae2-4f16-b9b6-b99484518f54.png)

# Logical Design
We learned about the logical design phase. In this phase we created a more detailed blueprint of the project that extends beyond the amount of detail specified in the conceptual design phase. We determined the AWS and third party services to be used in the architecture as well as the relationship of these components.

![image](https://user-images.githubusercontent.com/67550608/221538645-16f5f7b7-d043-466f-b46d-d4cdda5c94b7.png)

# Play be the packet
We discussed the value of playing by the packet and considering the user experience. This involves assuming the role of a packet and by keeping in-mind the OSI model, creating a path for the packet through AWS services to the user. This may help to understand the user's needs and ensure that the architecture and design meet those needs.

# AWS Well-Architected Framework
Finally, we learned about the AWS Well-Architected Framework, which is a set of best practices for reviewing workloads against current best practices in the cloud using the following six pillars.
1. Operational excellence.
2. Security.
3. Reliability.
4. Performance efficiency.
5. Cost optimization.
6. Sustainability.

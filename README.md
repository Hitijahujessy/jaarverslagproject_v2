<div align="center">
    
# AIConvoKit API Documentation
Welcome to the AIConvoKit API! This API allows you to interact with our assistant management system, including user management, and chat functionalities. Below, you'll find detailed information on how to authenticate and use each endpoint.


[![Lang](https://skillicons.dev/icons?i=python)](https://skillicons.dev) [![Lang](https://skillicons.dev/icons?i=django)](https://skillicons.dev)

</div>

## Table of Contents
- [What is AIConvoKit?](#what-is-aiconvokit)
      - [How does it work?](#how-does-it-work)
      - [Why AIConvoKit?]](#why-aiconvokit)
- [Base URL](base-url)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
    - [User Management](#user-management)
      - [Create User](#create-user)
    - [Authentication Token](#authentication-token)
      - [Obtain Token](#obtain-token)
    - [Assistant Management](#assistant-management)
      - [List Assistants](#list-assistants)
      - [Create Assistant](#create-assistant)
      - [View Assistant](#view-assistant)
      - [Update Assistant](#update-assistant)
    - [Chat](#chat)
      - [Create Chat](#create-chat)
      - [Send and Receive Messages](#send-and-receive-messages)
- [Status Codes](#status-codes)
- [Rate Limiting](#rate-limiting)

## What is AIConvoKit?
When you need to find information in an important document, it's likely that you'll be having a hard time with finding the correct information. That's no surprise: a lot of these
documents contain a lot of in-depth information so it might be like you're searching for a needle in a haystack. This is where AIConvoKit comes in!

Our goal is to not only simplify the creation of chatbot assistants, but to push the boundaries of how useful a chatbot can be. Using AIConvoKit, it's as simple as giving the assistant a name, a simple instruction, and a document. AIConvoKit will do the rest. From annual reports to contracts, finding the right information will be a breeze. We will also provide an embeddable chat for you to put on your website.

### How does it work?
- Create an assistant by giving it a name, a simple instruction and, optionally, a document
- Test your assistant in our testing environment
- Put the chat on your website
- Done!

### Why AIConvoKit?
You might be wondering, why use AIConvokit if I can just upload my file to ChatGPT-4 and ask my questions there? There are two main reasons to use AIConvoKit instead.

The first reason is consistensy. The assistants are set up with a specific goal and will always have access to uploaded files. On ChatGPT, you need to reupload your files
every time you start a new conversation.

The second reason is accesibility. Not everyone knows how to use models like ChatGPT. There are still people that don't know it's capabilities, and more importantly, how to get
the best out of the technology. Even if they do, there are lots of people that are willing to pay for ChatGPT-4. AIConvoKit allows everyone to get the right information, without the need of subscriptions and difficult prompting. Not only that, but since AIConvoKit provides an embeddable chat, hardly any web- or development skills are needed to set up a chat on your website. 

## Base URL
All URLs referenced in the documentation have the following base URL:
```https://aiconvokit-api-63d82f4cbf77.herokuapp.com/api/v1/```

## Authentication
This API uses token-based authentication. To obtain a token, send a POST request to the /tokens/ endpoint with your username and password. Include the token in the Authorization header as Token <your_token> for subsequent requests that require authentication.

## Endpoints
### User Management
#### Create User
- URL: /users/
- Method: POST
- Body: username, email, password
- Description: Create a new user.
  
### Authentication Token
#### Obtain Token
- URL: /tokens/
- Method: POST
- Body: username, password
- Description: Returns an authentication token.

### Assistant Management
#### List Assistants
- URL: /assistants/
- Method: GET
- Auth Required: Yes
- Description: Returns a list of all assistants.

#### Create Assistant
- URL: /assistants/
- Method: POST
- Auth Required: Yes
- Body: name, company_name, instructions, files (optional)
- Description: Create a new assistant.

#### View assistant
- URL: /assistants/<int:pk>/
- Method: GET
- Auth Required: Yes
- Description: Returns the data of a specific assistants.

#### Update Assistant
- URL: /assistants/<int:pk>/
- Method: PUT
- Auth Required: Yes
- Body: name, new_name (optional), company_name, instructions, files (optional)
- Description: Update an existing assistant.

### Chat
#### Create Chat
- URL: /chat/
- Method: POST
- Auth Required: Yes
- Body: assistant_id
- Description: Create a chat instance. Returns the chat ID used for the ```/chat/<int:pk>/``` endpoint

#### Send and Receive Messages
URL: /chat/<int:pk>/
- Method: PUT
- Auth Required: Yes
- Body: assistant_id, input
- Description: Send a message to an assistant and returns a response.

### Status Codes
#### The API uses the following status codes:
- 200 OK - The request was successful.
- 201 Created - The request was successful, and a resource was created.
- 400 Bad Request - The server could not understand the request due to invalid syntax.
- 401 Unauthorized - Authentication is needed or has failed.
- 404 Not Found - The server could not find the requested resource.
- 500 Internal Server Error - An error occurred on the server side.

### Rate Limiting
Please note that rate limiting may be applied to ensure fair usage. If you encounter 429 Too Many Requests, you are advised to slow down your request rate.


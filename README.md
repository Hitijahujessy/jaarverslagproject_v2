<div align="center">
    
# AIConvoKit API Documentation
Welcome to the AIConvoKit API! This API allows you to interact with our assistant management system, including user management, and chat functionalities. Below, you'll find detailed information on how to authenticate and use each endpoint.


[![Lang](https://skillicons.dev/icons?i=python)](https://skillicons.dev) [![Lang](https://skillicons.dev/icons?i=django)](https://skillicons.dev)

</div>


## Table of Contents
- [What is AIConvoKit?](#what-is-aiconvokit)
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

## Base URL
All URLs referenced in the documentation have the following base:
```http://<your_domain>/api/v1/```

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


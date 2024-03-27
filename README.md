<div align="center">
    
# Floes API Documentation
Welcome to the AIConvoKit API! This API allows you to interact with our assistant management system, including user management, and chat functionalities. Below, you'll find detailed information on how to authenticate and use each endpoint.


[![Lang](https://skillicons.dev/icons?i=python)](https://skillicons.dev) [![Lang](https://skillicons.dev/icons?i=django)](https://skillicons.dev)

</div>

## Table of Contents
- [What is AIConvoKit?](#what-is-aiconvokit)
    - [How does it work?](#how-does-it-work)
    - [Why AIConvoKit?](#why-aiconvokit)
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
In today's digital age, sifting through extensive documents for specific information can feel like searching for a needle in a haystack. The sheer volume of in-depth material often makes this task daunting and time-consuming. Enter AIConvoKit, your innovative solution designed to revolutionize the way we interact with and extract information from documents.

AIConvoKit aims to radically simplify the creation of chatbot assistants while expanding their capabilities to unprecedented levels. With AIConvoKit, setting up your assistant is as easy as naming it, providing a simple directive, and uploading the document. Our cutting-edge technology takes care of the rest, making the retrieval of information from complex documents, such as annual reports and contracts, effortlessly efficient.

Moreover, AIConvoKit enhances your digital presence by offering an embeddable chat feature for your website. This allows your clients or team members to interact directly with the chatbot, obtaining the information they need in real-time. Transform the way you manage and access information with AIConvoKit, where convenience meets innovation..

### How does it work?
- Create an assistant by giving it a name, a simple instruction and, optionally, a document
- Test your assistant in our testing environment (coming soon...)
- Put the chat on your website (coming soon...)
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

# IMPORTANT
Make sure to add the '/' to each endpoint! Otherwise it won't work. Example: use `/users/` instead of `/users`

## Authentication
This API uses token-based authentication. To obtain a token, send a POST request to the /tokens/ endpoint with your username and password. Include the token in the Authorization header as Token <your_token> for subsequent requests that require authentication.

## Endpoints
### User Management
#### Create User
- URL: /users/
- Method: POST
- Body: username, email, password
- Description: Create a new user.
- Returns: ID, username and email.
  
### Authentication Token
#### Obtain Token
- URL: /tokens/
- Method: POST
- Body: username, password
- Description: Get an authetication token.
- Returns: Authentication token.

### Assistant Management
#### List Assistants
- URL: /assistants/
- Method: GET
- Auth Required: Yes
- Description: Retrieve a list of all assistants in the database.
- Returns: List of all assistants and their ID, openai_id, absolute URL, name, company_name, instructions, created_at, updated_at, query_count (placeholder) and file path.

#### Create Assistant
- URL: /assistants/
- Method: POST
- Auth Required: Yes
- Body: name, company_name, instructions, files (optional)
- Description: Create a new assistant.
- Returns: ID, openai_id, absolute URL, name, company_name, instructions, created_at, updated_at, query_count (placeholder) and file path.

#### View assistant
- URL: /assistants/assistant id/
- Method: GET
- Auth Required: Yes
- Description: Retrieve all information of an assistant.
- Returns: ID, openai_id, absolute URL, name, company_name, instructions, created_at, updated_at, query_count (placeholder) and file path.

#### Update Assistant
- URL: /assistants/assistant id/
- Method: PUT
- Auth Required: Yes
- Body: name, new_name (optional), company_name, instructions, files (optional)
- Description: Update an existing assistant.
- Returns: ID, openai_id, absolute URL, name, company_name, instructions, created_at, updated_at, query_count (placeholder) and file path.

### Chat
#### Create Chat
- URL: /chat/
- Method: POST
- Auth Required: Yes
- Body: assistant_id
- Description: Create a chat instance.
- Returns: ID, absolute_url, thread_id

#### Send and Receive Messages
URL: /chat/chat id/
- Method: PUT
- Auth Required: Yes
- Body: assistant_id, input
- Description: Send and receive messages to and from an assistant.
- Returns: ID, absolute_url, thread_id, input, output

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


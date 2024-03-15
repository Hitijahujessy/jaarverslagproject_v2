# jaarverslagproject_v2 API Documentation
Welcome to the MyProject API! This API allows you to interact with our assistant management system, including user management, and chat functionalities. Below, you'll find detailed information on how to authenticate and use each endpoint.

## Base URL
All URLs referenced in the documentation have the following base:
```http://<your_domain>/api/v1/```

## Authentication
This API uses token-based authentication. To obtain a token, send a POST request to the /tokens/ endpoint with your username and password. Include the token in the Authorization header as Token <your_token> for subsequent requests that require authentication.

## Endpoints
### User Management
Create User
- URL: /users/
- Method: POST
- Body: username, email, password
- Description: Register a new user.
  
### Authentication Token
Obtain Token
- URL: /tokens/
- Method: POST
- Body: username, password
- Description: Obtain an authentication token.

### Assistant Management
List Assistants
- URL: /assistants/
- Method: GET
- Auth Required: Yes
- Description: Retrieve a list of all assistants.

Create Assistant
- URL: /assistants/
- Method: POST
- Auth Required: Yes
- Body: name, company_name, instructions, files (optional)
- Description: Create a new assistant.

Update Assistant
- URL: /assistants/<int:pk>/
- Method: PUT
- Auth Required: Yes
- Body: name, new_name (optional), company_name, instructions, files (optional)
- Description: Update an existing assistant.

### Chat
Create Chat Message
- URL: /chat/
- Method: POST
- Auth Required: Yes
- Body: assistant_name, _input
- Description: Send a message to an assistant and receive a response.

### Status Codes
The API uses the following status codes:
- 200 OK - The request was successful.
- 201 Created - The request was successful, and a resource was created.
- 400 Bad Request - The server could not understand the request due to invalid syntax.
- 401 Unauthorized - Authentication is needed or has failed.
- 404 Not Found - The server could not find the requested resource.
- 500 Internal Server Error - An error occurred on the server side.

### Rate Limiting
Please note that rate limiting may be applied to ensure fair usage. If you encounter 429 Too Many Requests, you are advised to slow down your request rate.

from openai import OpenAI
from django.conf import settings
import time

# Set up OpenAI with API key
client = OpenAI(
    api_key=settings.APIKEY,
)

# Create an assistant using user-given name and description (retrieved from AssistantModel)
def create_new_assistant(name, description):
    print("wompwomp")
    assistant = client.beta.assistants.create(
        name=name,
        description=description,
        model= "gpt-3.5-turbo-0125",
        tools=[{"type": "retrieval"}]
    )
    
    return assistant

# Modify an assistant using user-given name and description (retrieved from AssistantModel)
def modify_assistant(name, description):
    print("miepmiep")
    # Retrieve the list of existing assistants
    existing_assistants = client.beta.assistants.list()

    # Check if the desired assistant exists in the list
    desired_assistant_name = name  # Placeholder, could be something like "desired_assistant.name", 
                                      # "desired_assistant" being an instance of AssistantModel
    assistant = None
    for existing_assistant in existing_assistants.data:
      if existing_assistant.name == desired_assistant_name:
          assistant = existing_assistant
          break
      
    # Retrieve assistant
    assistant = client.beta.assistants.retrieve(assistant.id)
    
    assistant = client.beta.assistants.update(
        assistant.id,
        name=name,
        description=description,
    )
    
    return assistant

# Wait for the connection with the OpenAI API is established before trying to start a conversation
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(.5)

    if run.status == "failed":
        print(run.failed_at)
    return run


# Send/retrieve messages to/from assistant
def send_message_to_assistant(msg):
    # Retrieve the list of existing assistants
    existing_assistants = client.beta.assistants.list()

    # Check if the desired assistant exists in the list
    desired_assistant_name = "Pieter"  # Placeholder, could be something like "desired_assistant.name", 
                                      # "desired_assistant" being an instance of AssistantModel
    assistant = None
    for existing_assistant in existing_assistants.data:
      if existing_assistant.name == desired_assistant_name:
          assistant = existing_assistant
          break
      
    # Retrieve assistant
    assistant = client.beta.assistants.retrieve(assistant.id)
    
    # Create a thread (conversation)
    thread = client.beta.threads.create()

    # Define the user's message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"{assistant.description}. {msg}. {assistant.instructions}")

    # Send the message and pre-given instructions to assistant 
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions=assistant.instructions
    )

    # Wait for connection with the OpenAI API
    wait_on_run(run, thread)


    # Retrieve the conversation messages
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Retrieve and return the response message
    for message in messages.data:
        role = message.role
        content = message.content[0].text.value
        
        return content

def send_code_to_api(code):
    try:
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an experienced developer."},
                {"role": "user", "content": f"Tell me in what language is this code written? {code}"},
            ]
        )
        return res.choices[0].message.content
    except OpenAI.error.APIError as e:
        raise ValueError(f"OpenAI API returned an API Error: {e}")
    except OpenAI.error.APIConnectionError as e:
        raise ValueError(f"Failed to connect to OpenAI API: {e}")
    except OpenAI.error.RateLimitError as e:
        raise ValueError(f"OpenAI API request exceeded rate limit: {e}")
    
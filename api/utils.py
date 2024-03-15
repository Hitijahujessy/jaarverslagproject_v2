
# In this updated version, I've added the `create_thread` function to create a new thread.
# The `send_message_to_assistant` function now has an additional argument `thread_id`, which specifies the ID of the thread to which the message should be sent.
# If `thread_id` is not provided, a new thread is created using the `create_thread` function. Otherwise, the message is added to the existing thread specified by `thread_id`.


from openai import OpenAI
from django.conf import settings
import time

# Set up OpenAI with API key
client = OpenAI(
    api_key=settings.APIKEY,
)

# Function to create a new thread
def create_thread(assistant):
    # Retrieve the assistant object
    assistant = client.beta.assistants.retrieve(assistant.id)
    return client.beta.threads.create()

    
# Create an assistant using user-given name and instructions (retrieved from AssistantModel)
def create_new_assistant(name, company, instructions, uploaded_file=None):
    # Initialize file_ids as an empty list
    file_ids = []
    
    # Only proceed with file handling if uploaded_file is not None
    if uploaded_file is not None:
        # Read the content of the uploaded file into bytes
        file_content = uploaded_file.read()
        
        # Create the file with OpenAI's API
        file = client.files.create(
            file=file_content,  # Pass the file content as bytes
            purpose='assistants'
        )
        
        # Add the created file's ID to the file_ids list
        file_ids.append(file.id)
        
    description_string = f"Your name is {name}, an assistant working for {company}."
    description_string += f"You read and analyse files if possible. "
    description_string += f"You are designed to make customers feel like they're chatting with a real help desk agent. "
    description_string += f"You are trained to communicate naturally and to answer user's questions in a way that mimics human interaction. "
    description_string += f"You can base your answers and refer to preview messages from the user. "
    description_string += f"End your message with a question if more clarity is needed."
    description_string += f"Answer as short as possible, without missing crucial information."

        
    
    # Create the assistant with conditional file_ids
    assistant = client.beta.assistants.create(
        name=name,
        instructions=f"{description_string}. {instructions}",
        model= "gpt-3.5-turbo-0125",
        tools=[{"type": "retrieval"}],
        file_ids=file_ids  # Use the possibly empty file_ids list
    )
    
    return assistant

# Modify an assistant using user-given name and description (retrieved from AssistantModel)
def modify_assistant(name, new_name, company, instructions, uploaded_file):
    print(new_name)
    # Initialize file_ids as an empty list
    file_ids = []
    if uploaded_file:
        file_content = uploaded_file.read()
        
        # Create the file with OpenAI's API
        file = client.files.create(
            file=file_content,  # Pass the file content as bytes
            purpose='assistants'
        )
        
        # Add the created file's ID to the file_ids list
        file_ids.append(file.id)

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
    
    updated_name = new_name if new_name is not None and new_name != name else name

    description_string = f"Your name is {name}, an assistant working for {company}."
    description_string += f"You read and analyse files if possible. "
    description_string += f"You are designed to make customers feel like they're chatting with a real help desk agent. "
    description_string += f"You are trained to communicate naturally and to answer user's questions in a way that mimics human interaction. "
    description_string += f"You can base your answers and refer to preview messages from the user. "
    description_string += f"End your message with a question if more clarity is needed."
    description_string += f"Answer as short as possible, without missing crucial information."


    # Update the assistant
    assistant = client.beta.assistants.update(
        assistant.id,
        name=updated_name,
        instructions=f"{description_string} {instructions}",
        file_ids=file_ids
    )
    
    return assistant

# Wait for the connection with the OpenAI API is established before trying to start a conversation
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(3.5)

    if run.status == "failed":
        print(run.failed_at)
    return run


# Send/retrieve messages to/from assistant
def send_message_to_assistant(name, msg, thread_id=None):
    # Retrieve the list of existing assistants
    existing_assistants = client.beta.assistants.list()

    # Check if the desired assistant exists in the list
    desired_assistant_name = name  # Placeholder, could be something like "desired_assistant.name", 
                                    # "desired_assistant" being an instance

    # of AssistantModel.
    # Should also check credentials before allowing a connection with an Assistant
    assistant = None
    for existing_assistant in existing_assistants.data:
        if existing_assistant.name == desired_assistant_name:
            assistant = existing_assistant
            break
    
    # Retrieve assistant
    assistant = client.beta.assistants.retrieve(assistant.id)

    # Create a thread if thread_id is not provided
    if not thread_id:
        thread = create_thread(assistant)
    else:
        thread = client.beta.threads.retrieve(thread_id)

    # Define the user's message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg)

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
        thread_id=thread.id,
        order="asc",
        after=message.id
    )

    # Retrieve and return the response message
    for message in messages.data:
        role = message.role
        content = message.content[0].text.value
        
        return content
    
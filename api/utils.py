
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

    
# Create an assistant using user-given name and description (retrieved from AssistantModel)
def create_new_assistant(name, company, instructions, uploaded_file):
    # Read the content of the uploaded file into bytes
    file_content = uploaded_file.read()
    
    file = client.files.create(
      file=file_content,  # Pass the file content as bytes
      purpose='assistants'
    )
    

    description_string = f"You read and analyse files if possible. "
    description_string += f"You are designed to make customers feel like they're chatting with a real help desk agent. "
    description_string += f"You are trained to communicate naturally and to answer user's questions in a way that mimics human interaction. "
    description_string += f"You can base your answers and refer to preview messages from the user. "
    description_string += f"End your message with a question if more clarity is needed."
    description_string += f"Answer as short as possible, without missing crucial information."

    assistant = client.beta.assistants.create(
        name=name,
        instructions=description_string,
        model="gpt-3.5-turbo-0125",
        tools=[{"type": "retrieval"}],
        file_ids=[file.id]
    )
    
    return assistant

# Modify an assistant using user-given name and description (retrieved from AssistantModel)
def modify_assistant(name, new_name, company, instructions, uploaded_file):
    if uploaded_file:
        file_content = uploaded_file.read()
        
        file = client.files.create(
            file=file_content,  # Pass the file content as bytes
            purpose='assistants'
        )
    
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
        name=new_name if new_name != name or new_name != None else name,
        instructions=f"Your name is {new_name}, an assistant working for {company}. {instructions}",
        file_ids=[file.id] if uploaded_file else None
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
        content=f"{assistant.instructions}. {msg}.")

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
    
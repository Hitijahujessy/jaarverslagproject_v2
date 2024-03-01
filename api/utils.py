from openai import OpenAI
from django.conf import settings
import time
# openai.api_key = settings.APIKEY
client = OpenAI(
    # This is the default and can be omitted
    api_key=settings.APIKEY,
)

def create_new_assistant(name, description):
    assistant = client.beta.assistants.create(
        name=name,
        description=description,
        model= "gpt-3.5-turbo-0125",
        tools=[{"type": "retrieval"}]
    )
    
    return assistant

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(2.5)

    if run.status == "failed":
        print(run.failed_at)
    return run

def send_message_to_assistant(msg):
    
    # Retrieve the list of existing assistants
    existing_assistants = client.beta.assistants.list()

    # Check if the desired assistant exists in the list
    desired_assistant_name = "Johan"
    assistant = None
    for existing_assistant in existing_assistants.data:
      if existing_assistant.name == desired_assistant_name:
          assistant = existing_assistant
          break
      
    # Retrieve assistant
    assistant = client.beta.assistants.retrieve(assistant.id)
    
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Keep your answers as short as possible."
    )

    wait_on_run(run, thread)

    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

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
    
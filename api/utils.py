from openai import OpenAI
from django.conf import settings
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
    
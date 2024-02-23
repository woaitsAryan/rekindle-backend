from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm_response(emotion: str) -> str:
    client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    )

    gpt_prompt = f"I want you to be very emotionally recpeptive and act as an empathic companion to me. I am going to detail the events and experiences of today as a story. Please give me advice and encouragement on that. My day was: {emotion}"
    
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": gpt_prompt,
            },
        ],
    )

    return chat_completion.choices[0].message.content # type: ignore

from openai import OpenAI

from helpers.envHandler import env_vars

def get_llm_response(text: str) -> str:
    
    client = OpenAI(
        api_key = env_vars['OPENAI_API_KEY']
    )

    gpt_prompt = f"I am going to give you a story of the events I experienced today. Please try to be empathetic, compassionate, and provide advice, encouragement, and a have a chat with me on the same within 150 words. This is my story: {text}"
    
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": gpt_prompt,
            },
        ],
    )
    
    # responsellm = ollama.chat(model='gemma:2b', messages=[
    #     {
    #         'role': 'user',
    #         'content': gpt_prompt
    #     }
    # ])

    return chat_completion.choices[0].message.content # type: ignore
    # return responsellm['message']['content'] # type: ignore

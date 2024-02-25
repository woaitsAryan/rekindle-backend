# from openai import OpenAI
# import os
# from dotenv import load_dotenv
import ollama

# load_dotenv()

def get_llm_response(emotion: str) -> str:
    # client = OpenAI(
    # api_key=os.getenv("OPENAI_API_KEY"),
    # )

    gpt_prompt = f"I am going to give you a story of the events I experienced today. Please try to be empathetic, compassionate, and provide advice, encouragement, and a have a chat with me on the same within 150 words. This is my story: {emotion}"
    
    # chat_completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": gpt_prompt,
    #         },
    #     ],
    # )
    
    responsellm = ollama.chat(model='gemma:2b', messages=[
        {
            'role': 'user',
            'content': gpt_prompt
        }
    ])

    # return chat_completion.choices[0].message.content # type: ignore
    return responsellm['message']['content']

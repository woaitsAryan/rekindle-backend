from typing import Optional, Tuple
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from sqlite3 import Error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv
import threading
from contextlib import contextmanager

load_dotenv()

app = FastAPI()


origins = [
    "http://localhost:3000",  # Allow localhost for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@contextmanager
def get_db():
    conn = sqlite3.connect('storage.db')
    try:
        yield conn
    finally:
        conn.close()

class TextModel(BaseModel):
    text: str

@app.post("/emotion")
def get_emotion_response(body: TextModel, conn = Depends(get_db)):
    response = get_llm_response(body.text)
    
    threading.Thread(target=compute_emotion_and_save, args=(response, body.text)).start()

    return {"response": response}

def determine_emotion(text: str) -> Tuple[str, str, str]:
    from transformers import pipeline
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    outputs = classifier(text)
    return outputs[0][0]['label'], outputs[0][1]['label'], outputs[0][2]['label']  # type: ignore

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


@app.get("/get_emotion")
def get_emotion(emotion: Optional[str] = None, conn = Depends(get_db)):
    if emotion:
        rows = conn.execute("SELECT * FROM MyTable WHERE emotion1 = ? OR emotion2 = ? OR emotion3 = ?", (emotion, emotion, emotion)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM MyTable").fetchall()

    return {"rows": rows}

def compute_emotion_and_save(llm_response: str, body_text: str):
    with get_db() as conn:
        emotion = determine_emotion(body_text)
        try:
            conn.execute("INSERT INTO MyTable (text, emotion1, emotion2, emotion3, response) VALUES (?, ?, ?, ?, ?)", (body_text, emotion[0], emotion[1], emotion[2], llm_response))
            conn.commit()
        except Error as e:
            print(e)
            raise HTTPException(status_code=500, detail="Database error")        

from typing import Union
from enum import Enum
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3
from sqlite3 import Error

app = FastAPI()


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
    emotion = determine_emotion(body.text)
    try:
        response = EmotionResponse[emotion.upper()].value
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid emotion")

    try:
        conn.execute("INSERT INTO MyTable (text, emotion) VALUES (?, ?)", (body.text, emotion))
        conn.commit()
    except Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")        

    return {"response": response}

def determine_emotion(text: str) -> str:
    # Your logic here...
    return "happy"  #


class EmotionResponse(Enum):
    HAPPY = "We're glad you're feeling happy!"
    SAD = "We're sorry to hear you're feeling sad."
    # Add more emotions as needed...
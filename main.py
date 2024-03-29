from typing import Optional
from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schema.input import TextModel
from helpers.emotion_nlp import compute_emotion_and_save
import threading
from helpers.llm import get_llm_response
from helpers.db import get_db

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/journal")
def write_journal(body: TextModel):
    response = get_llm_response(body.text)
    
    threading.Thread(target=compute_emotion_and_save, args=(response, body.text)).start()

    return {"response": response}

@app.get("/journal")
def get_journal(emotion: Optional[str] = None):
    with get_db() as conn:
        if emotion:
            rows = conn.execute("SELECT * FROM MyTable WHERE emotion1 = ? OR emotion2 = ? OR emotion3 = ?", (emotion, emotion, emotion)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM MyTable").fetchall()

    responsearr = []

    for row in rows:
        responsearr.append({
            "text": row[1],
            "emotion1": row[2],
            "emotion2": row[3],
            "emotion3": row[4],
            "response": row[5],
            "date": row[6]
        })
    
    return {"response": responsearr}


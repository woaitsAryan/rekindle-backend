import threading
from fastapi import APIRouter, Depends
from sqlalchemy import text
from typing_extensions import Optional
from sqlalchemy.orm import Session
from helpers.llm import get_llm_response
from helpers.emotion_nlp import compute_emotion_and_save
from helpers.db import get_db
from models.schema import DayInput
from middleware.protect import protect

journalRouter = APIRouter()

@journalRouter.post("/")
def write_journal(body: DayInput, db: Session = Depends(get_db), id: str = Depends(protect)):
    user_id = int(id)

    response = get_llm_response(body.text)
    
    threading.Thread(target=compute_emotion_and_save, args=(response, body.text, db, user_id)).start()

    return {"response": response}

@journalRouter.get("/")
def get_journal(emotion: Optional[str] = None, db: Session = Depends(get_db), id: str = Depends(protect)):
    if emotion:
        query = text("SELECT * FROM days WHERE :emotion = ANY(emotions) AND user_id = :id")
        result = db.execute(query, {"emotion": emotion, "id": id}).fetchall()
    else:
        query = text("SELECT * FROM days WHERE user_id = :id")
        result = db.execute(query, {"id": id}).fetchall()
      
    response = []
    
    for row in result:
        response.append({
            "text": row[1],
            "emotions": row[2],
            "response": row[3],
            "date": row[4]
        })

    
    return {"response": response}

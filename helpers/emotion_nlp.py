from fastapi import HTTPException
from typing_extensions import Tuple
from sqlalchemy.orm import Session

from models.user import Day

def compute_emotion_and_save(llm_response: str, body_text: str, db: Session, user_id: int):
    emotion = determine_emotion(body_text)
    try:
        new_day = Day(
            text = body_text,
            emotions = emotion, 
            response = llm_response,
            user_id = user_id
        )
        db.add(new_day)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")        

def determine_emotion(text: str) -> Tuple[str, str, str]:
    from transformers import pipeline
    classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
    outputs = classifier(text)
    return outputs[0][0]['label'], outputs[0][1]['label'], outputs[0][2]['label']  # type: ignore
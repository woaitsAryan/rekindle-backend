from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import Base
from helpers.envHandler import env_vars

engine = create_engine(env_vars['DATABASE_URL'])
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from rekindle.models.user import Base

url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="pgpass",
    host="localhost",
    port=5432,
    database="postgres"
)

def get_db():
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    
    db = Session()
    try:
        yield db
    finally:
        db.close()
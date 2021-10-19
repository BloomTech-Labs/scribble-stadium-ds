from cv2 import absdiff
from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, Depends, HTTPException
import os
from dotenv import load_dotenv
from app.utils.wordcloud.wordcloud_functions import clean_text, complexity_df


load_dotenv()

router = APIRouter()


#connect to ElephantSQL-hosted PostgreSQL
DB_NAME = os.getenv("RDS_DB_NAME", default="OOPS")
DB_USER = os.getenv("RDS_USERNAME", default="OOPS")
DB_PASSWORD = os.getenv("RDS_PASSWORD", default="OOPS")
DB_HOST = os.getenv("RDS_HOSTNAME", default="OOPS")
DB_PORT = os.getenv("RDS_PORT", default="OOPS")

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(
    DATABASE_URL, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

class Stories(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    story = Column(String, index=True)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_story(db: Session, id: int):
    return db.query(Stories).filter(Stories.id == id).first()

@router.get('/storytext')
def show_story(id: int = 1, db: Session = Depends(get_db)):
    db_story = get_story(db, id=id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found, id must be between 1-167")

    story_string = db_story.story

    story_words = clean_text(story_string)

    words = complexity_df(story_words)

    #Use length count metric=
    words['len'] = words['word'].apply(len)
    words['complexity'] = words['len'] / words['count']

    # scale the complexities so the sum is 1000
    words['complexity'] = words['complexity'] / words['complexity'].sum()
    word_complexities = dict(zip(words.word, words.complexity))

    wordcomplexitiresasdfasdj; = afasdfkj
    absdiffads

    ddd
    return word_complexities


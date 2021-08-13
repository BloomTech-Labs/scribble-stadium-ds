from sqlalchemy import create_engine, Integer, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

'''
temporarily using SQLite database for local development
SQLALCHEMY_DATABASE_URL = dialect://user:password@host.dbname
'''

SQLALCHEMY_DATABASE_URL = r'sqlite:///C:\Users\temsy\Documents\GitHub\ebtest\test_data.db'
# SQLALCHEMY_DATABASE_URL = 's3://labspt21teambdemodata/load/test_data.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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
def show_story(id: int, db: Session = Depends(get_db)):
    db_story = get_story(db, id=id)
    if db_story is None:
        raise HTTPException(status_code=404, detail="Story not found, id must be between 1-167")
    return db_story


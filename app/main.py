from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api import wordcloud_text, wordcloud_cloud, wordcloud_update

application = app = FastAPI(
    title="Labs26-StorySquad-DS-Team B",
    description="A RESTful API for the Story Squad Project",
    version="0.1",
    docs_url="/"
)

app.include_router(wordcloud_text.router, tags=['Word Cloud'])
app.include_router(wordcloud_update.router, tags=['Word Cloud'])
app.include_router(wordcloud_cloud.router, tags=['Word Cloud'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(application)
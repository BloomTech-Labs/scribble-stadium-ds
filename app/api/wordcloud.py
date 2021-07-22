import pandas as pd
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

class Story(BaseModel):
    """The submission entry in string form"""
    Story: str


@router.post('/wordcloud/text')
async def wordcloudtext(story: Story):
    return story


'''NOTES: it doesn't like copy/paste text that contains /n'''

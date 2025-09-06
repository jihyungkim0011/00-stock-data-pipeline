from pydantic import BaseModel
from datetime import datetime

class NewsItem(BaseModel):
    Symbol: str
    Name: str
    title: str
    url: str
    publishedAt: datetime

    class Config:
        from_attributes = True

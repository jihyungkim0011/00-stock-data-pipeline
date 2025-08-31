from fastapi import APIRouter
from typing import List

from app.services.local_news_service import local_news_service
from app.schemas.news import NewsItem

router = APIRouter()

@router.get("/news/{symbol}", response_model=List[NewsItem])
def read_news_by_symbol(symbol: str):
    """
    특정 주식 심볼(Symbol)에 대한 뉴스 기사 목록을 반환합니다.
    - **symbol**: 주식 심볼 (예: AAPL, MSFT)
    """
    news_list = local_news_service.get_news_by_symbol(symbol)
    if not news_list:
        # 주석 처리: 뉴스가 없는 경우 404 대신 빈 목록을 반환하는 것이 더 일반적일 수 있습니다.
        # raise HTTPException(status_code=404, detail=f"News for symbol '{symbol}' not found")
        return []
    return news_list

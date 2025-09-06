from fastapi import APIRouter
from typing import List

from app.services.financials_info_service import FinancialsInfoService
from app.schemas.financial_info import FinancialInfo

router = APIRouter()
financials_service = FinancialsInfoService()

@router.get("/financial-info/{symbol}", response_model=List[FinancialInfo])
def read_financial_info_by_symbol(symbol: str):
    """
    특정 주식 심볼(Symbol)에 대한 재무정보 목록을 반환합니다.
    - **symbol**: 주식 심볼 (예: AAPL, MSFT)
    """
    financial_info_list = financials_service.get_info_by_symbol(symbol)
    if not financial_info_list:
        return []
    return financial_info_list
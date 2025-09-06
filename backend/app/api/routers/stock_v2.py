from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

# --- 스키마 임포트 --- #
from app.schemas.stock import StockPrice, Financials

# --- 서비스 임포트 --- #
from app.services.disclosure_service import DisclosureService
from app.services.stock_service import StockService


# --- 서비스 인스턴스 최적화 --- #
# 애플리케이션 시작 시 서비스 인스턴스를 한 번만 생성합니다.
# API가 호출될 때마다 파일을 새로 읽는 것을 방지하여 성능이 향상됩니다.
stock_service_instance = StockService()
disclosure_service_instance = DisclosureService()

# --- 의존성 주입 --- #
# 의존성 주입 함수는 미리 생성된 인스턴스를 반환하는 역할만 합니다.
def get_stock_service() -> StockService:
    return stock_service_instance

def get_disclosure_service() -> DisclosureService:
    return disclosure_service_instance


# --- 라우터 설정 --- #
router = APIRouter(
    prefix="/stocks",
    tags=["stocks_v2_integrated"], 
)


# --- API 엔드포인트 (DisclosureService 사용) --- #

@router.get("/financials/annual", response_model=List[Financials])
async def get_annual_financials(service: DisclosureService = Depends(get_disclosure_service)):
    """
    **[Disclosure] 연간 재무제표 데이터 조회**

    `nasdaq_financials_annual_all.csv` 파일에서 데이터를 가져와 상위 5개 행을 반환합니다.
    """
    data = service.get_annual_financials()
    if data is None:
        raise HTTPException(status_code=404, detail="연간 재무 데이터를 찾을 수 없거나 로드에 실패했습니다.")
    return data.head().to_dict(orient="records")

@router.get("/financials/quarterly", response_model=List[Financials])
async def get_quarterly_financials(service: DisclosureService = Depends(get_disclosure_service)):
    """
    **[Disclosure] 분기별 재무제표 데이터 조회**

    `nasdaq_financials_quarterly_all.csv` 파일에서 데이터를 가져와 상위 5개 행을 반환합니다.
    """
    data = service.get_quarterly_financials()
    if data is None:
        raise HTTPException(status_code=404, detail="분기별 재무 데이터를 찾을 수 없거나 로드에 실패했습니다.")
    return data.head().to_dict(orient="records")


# --- API 엔드포인트 (StockService 사용) --- #

@router.get("/", response_model=List[StockPrice])
async def get_all_stocks(service: StockService = Depends(get_stock_service)):
    """
    **[Stock] 모든 주식 데이터 조회**

    `nasdaq_all_stocks.csv` 파일의 모든 데이터를 반환합니다.
    """
    stocks = service.get_all_stocks()
    if not stocks:
        raise HTTPException(status_code=404, detail="주식 데이터를 찾을 수 없습니다.")
    return stocks

@router.get("/{ticker}", response_model=List[StockPrice])
async def get_stock_by_ticker(
    ticker: str, 
    service: StockService = Depends(get_stock_service),
    start_date: Optional[str] = Query(None, description="조회 시작일 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="조회 종료일 (YYYY-MM-DD)")
):
    """
    **[Stock] 특정 종목 데이터 조회 (날짜 필터링 가능)**

    - **ticker**: 조회할 주식의 티커 (예: AAPL)
    - **start_date** (선택): 조회 시작 날짜
    - **end_date** (선택): 조회 종료 날짜
    """
    stocks = service.get_stock_by_ticker_and_date_range(ticker, start_date, end_date)
    if not stocks:
        raise HTTPException(status_code=404, detail=f"종목 '{ticker}'에 대한 데이터를 찾을 수 없습니다.")
    return stocks

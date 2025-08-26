from fastapi import FastAPI, HTTPException, Depends
import uvicorn
from typing import Annotated # Python 3.9+ 에서는 list[dict] 등으로 사용 가능
from services.stock_service import StockService # 새로 만든 서비스 클래스 임포트

# FastAPI 애플리케이션 초기화
app = FastAPI()

# StockService 인스턴스를 전역으로 생성합니다.
# 애플리케이션 시작 시 한 번만 CSV 파일을 로드하게 됩니다.
# 현재 파일(main.py)의 디렉토리를 기준으로 data 폴더의 경로를 구성합니다.
# os.path.dirname(__file__)은 현재 파일(main.py)의 디렉토리
# "data/nasdaq_all_stocks.csv"는 project_root의 data 폴더에 직접 접근
# (stock_service.py에서 이미 상대경로 처리했으므로, 여기서는 기본값 사용)
global_stock_service = StockService() 


# 의존성 주입을 위한 헬퍼 함수
# 이 함수는 각 엔드포인트가 호출될 때마다 StockService 인스턴스를 제공합니다.
# 하지만 위에서 global_stock_service를 이미 생성했으므로, 
# FastAPI는 같은 인스턴스를 재사용하게 됩니다.
def get_stock_service() -> StockService:
    return global_stock_service

# 1. 모든 주식 데이터 반환 API
@app.get("/stocks")
def get_all_stocks_api(stock_service: Annotated[StockService, Depends(get_stock_service)]):
    """
    모든 주식 데이터를 JSON 형태로 반환합니다.
    """
    stocks = stock_service.get_all_stocks()
    if not stocks: # 빈 리스트 또는 None 체크
        raise HTTPException(status_code=404, detail="데이터를 찾을 수 없습니다.")
    return stocks

# 2. 특정 종목 데이터 반환 API
@app.get("/stocks/{ticker}")
def get_stock_by_ticker_api(ticker: str, stock_service: Annotated[StockService, Depends(get_stock_service)]):
    """
    특정 주식 종목(ticker)에 해당하는 데이터를 반환합니다.
    예: /stocks/AAPL
    """
    stocks = stock_service.get_stock_by_ticker(ticker)
    if not stocks:
        raise HTTPException(status_code=404, detail=f"종목 '{ticker}'에 대한 데이터를 찾을 수 없습니다.")
    return stocks

# 3. 날짜 및 종목으로 필터링하는 API
@app.get("/stocks/{ticker}/by_date")
def get_stock_by_ticker_and_date_range_api(
    ticker: str, 
    stock_service: Annotated[StockService, Depends(get_stock_service)],
    start_date: str = None, 
    end_date: str = None
):
    """
    특정 종목의 지정된 날짜 범위 데이터를 반환합니다.
    예: /stocks/AAPL/by_date?start_date=2024-01-01&end_date=2024-01-02
    """
    stocks = stock_service.get_stock_by_ticker_and_date_range(ticker, start_date, end_date)
    if not stocks: # 데이터가 없으면 빈 리스트를 반환하므로 404를 발생시키지 않습니다.
        return []
    return stocks


if __name__ == '__main__':
    print("FastAPI 서버를 시작합니다. http://127.0.0.1:8000/docs 로 접속하세요.")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, workers=1)


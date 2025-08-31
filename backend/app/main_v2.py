from fastapi import FastAPI

# api/routers 폴더에 있는 라우터 객체들을 가져옵니다.
from app.api.routers import stock_v2, news

# FastAPI 애플리케이션 인스턴스를 생성합니다.
app = FastAPI(
    title="Stock Project API v2",
    description="라우터 분리 및 서비스 계층을 적용한 API",
    version="2.0.0",
)

# 정의한 라우터들을 애플리케이션에 포함시킵니다.
app.include_router(stock_v2.router)
app.include_router(news.router, prefix="/api", tags=["news"])

@app.get("/", tags=["root"])
async def read_root():
    """
    API 서버의 루트 엔드포인트입니다.
    서버가 정상적으로 실행 중인지 확인하는 용도로 사용할 수 있습니다.
    """
    return {"message": "API v2가 실행 중입니다. API 문서는 /docs 를 참고하세요."}

# --- 서버 실행 방법 ---
# 1. 터미널에서 `backend` 폴더로 이동합니다.
#    cd D:\Windows\0.DEV\python\00-stock-project\backend
#
# 2. uvicorn을 사용하여 서버를 실행합니다.
#    uvicorn app.main_v2:app --reload
#
# 3. 웹 브라우저에서 http://127.0.0.1:8000/docs 로 접속하여 API 문서를 확인합니다.

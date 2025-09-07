from app.core.config import settings

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging

from pathlib import Path
# api/routers 폴더에 있는 라우터 객체들을 가져옵니다.
from app.api.routers import stock_v2, news, financial_info

# FastAPI 애플리케이션 인스턴스를 생성합니다.
app = FastAPI(
    title="Stock Project API v2",
    description="라우터 분리 및 서비스 계층을 적용한 API",
    version="2.0.0",
)

# --- 정적 파일 마운트 ---
def mount_static(app, mounts):
    for url_path, rel_path, opts in mounts:
        dir_path = Path(__file__).parent.parent.parent / rel_path
        if dir_path.exists():
            app.mount(url_path, StaticFiles(directory=dir_path, **opts), name=url_path.strip("/"))
        else:
            logging.warning(f"{url_path} directory not found: {dir_path}. '{url_path}' route will not be mounted.")

mounts = [
    ("/static", "frontend/src/pages", {"html": True}),
    ("/css", "frontend/src/css", {}),
    ("/components", "frontend/src/components", {}),
    ("/stock_chart", "frontend/src/pages", {"html": True}),
]
mount_static(app, mounts)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

# 정의한 라우터들을 애플리케이션에 포함시킵니다.
app.include_router(stock_v2.router)
app.include_router(news.router, prefix="/api", tags=["news"])
app.include_router(financial_info.router, prefix="/api", tags=["financial-info"])

@app.get("/", tags=["root"])
async def read_root():
    """
    API 서버의 루트 엔드포인트입니다.
    서버가 정상적으로 실행 중인지 확인하는 용도로 사용할 수 있습니다.
    """
    return {"message": "API v2가 실행 중입니다. API 문서는 /docs 를 참고하세요."}

# --- 정적 파일 제공을 위한 루트 경로 리디렉션 (선택 사항) ---
# 사용자가 http://localhost:8000/ 에 접속했을 때, 특정 HTML 파일을 보여주고 싶을 경우 사용합니다.
# 예를 들어, index.html을 보여주려면 아래 주석을 해제하세요.
# from fastapi.responses import FileResponse
# @app.get("/", include_in_schema=False)
# async def read_index():
#     return FileResponse(str(Path(__file__).parent.parent.parent / "frontend" / "public" / "index.html"))

# --- 서버 실행 방법 ---
# 1. 터미널에서 `backend` 폴더로 이동합니다.
#    cd backend
#
# 2. uvicorn을 사용하여 서버를 실행합니다.
#    uvicorn app.main_v2:app --reload
#
# 3. 웹 브라우저에서 http://127.0.0.1:8000/docs 로 접속하여 API 문서를 확인합니다.

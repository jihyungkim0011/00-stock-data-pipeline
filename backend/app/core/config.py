import os
from dotenv import load_dotenv

# 현재 파일의 위치를 기준으로 프로젝트 루트에 있는 .env 파일을 찾아 로드합니다.
# backend/app/core/config.py -> backend/app/ -> backend/ -> .env찾기
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    """애플리케이션 설정을 관리하는 클래스"""
    
    # os.getenv를 사용하여 .env 파일의 "DATA_FILE_PATH" 변수를 읽어옵니다.
    # 만약 해당 변수가 없으면 기본값으로 None을 사용합니다.
    DATA_FILE_PATH: str = os.getenv("DATA_FILE_PATH")
    ANNUAL_FINANCIALS_PATH: str = os.getenv("ANNUAL_FINANCIALS_PATH")
    QUARTERLY_FINANCIALS_PATH: str = os.getenv("QUARTERLY_FINANCIALS_PATH")
    NEWS_PATH: str = os.getenv("NEWS_PATH")
    FINANCIALS_INFO_PATH: str = os.getenv("FINANCIALS_INFO_PATH")

# 다른 모듈에서 쉽게 가져다 쓸 수 있도록 설정 객체의 인스턴스를 생성합니다.
settings = Settings()

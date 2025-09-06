import pandas as pd

from app.core.config import settings

class LocalNewsService:
    _df = None
    _csv_path = settings.NEWS_PATH

    @classmethod
    def _load_data(cls):
        """CSV 파일에서 데이터를 로드하여 클래스 변수 _df에 저장합니다."""
        if cls._df is None:
            try:
                cls._df = pd.read_csv(cls._csv_path)
                # 날짜 형식 변환
                cls._df['publishedAt'] = pd.to_datetime(cls._df['publishedAt'])
                print(f"Successfully loaded news data from {cls._csv_path}")
            except FileNotFoundError:
                print(f"Error: News data file not found at {cls._csv_path}")
                # 파일이 없을 경우 빈 데이터프레임 생성
                cls._df = pd.DataFrame(columns=['Symbol', 'Name', 'title', 'url', 'publishedAt'])

    @classmethod
    def get_news_by_symbol(cls, symbol: str) -> list:
        """특정 심볼에 해당하는 뉴스 목록을 반환합니다."""
        cls._load_data() # 데이터가 로드되었는지 확인
        
        if cls._df.empty:
            return []

        # 심볼로 데이터 필터링 (대소문자 구분 없이)
        result_df = cls._df[cls._df['Symbol'].str.lower() == symbol.lower()]
        
        if result_df.empty:
            return []
            
        # DataFrame을 dictionary 리스트로 변환하여 반환
        return result_df.to_dict('records')

# 서비스 인스턴스 생성 (싱글턴처럼 사용)
local_news_service = LocalNewsService()

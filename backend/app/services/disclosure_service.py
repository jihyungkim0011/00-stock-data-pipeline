import pandas as pd
import os
from typing import Optional
from app.core.config import settings

class DisclosureService:
    """
    금융 공시 데이터를 불러오는 서비스를 담당하는 클래스입니다.
    """

    def __init__(self):
        """
        설정(settings)에 명시된 경로를 사용하여 서비스를 초기화합니다.
        """
        self.annual_path = settings.ANNUAL_FINANCIALS_PATH
        self.quarterly_path = settings.QUARTERLY_FINANCIALS_PATH

    def get_annual_financials(self) -> Optional[pd.DataFrame]:
        """
        설정에 정의된 경로에서 연간 재무 데이터를 불러와 반환합니다.

        반환값:
            Optional[pd.DataFrame]: 연간 재무 데이터가 담긴 pandas DataFrame, 
                                     파일을 찾거나 읽을 수 없는 경우 None을 반환합니다.
        """
        try:
            if not self.annual_path or not os.path.exists(self.annual_path):
                print(f"오류: 연간 재무 데이터 파일을 찾을 수 없거나 경로가 설정되지 않았습니다. 경로: {self.annual_path}")
                return None
            df = pd.read_csv(self.annual_path)
            return df
        except Exception as e:
            print(f"연간 재무 CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
            return None

    def get_quarterly_financials(self) -> Optional[pd.DataFrame]:
        """
        설정에 정의된 경로에서 분기별 재무 데이터를 불러와 반환합니다.

        반환값:
            Optional[pd.DataFrame]: 분기별 재무 데이터가 담긴 pandas DataFrame,
                                     파일을 찾거나 읽을 수 없는 경우 None을 반환합니다.
        """
        try:
            if not self.quarterly_path or not os.path.exists(self.quarterly_path):
                print(f"오류: 분기별 재무 데이터 파일을 찾을 수 없거나 경로가 설정되지 않았습니다. 경로: {self.quarterly_path}")
                return None
            df = pd.read_csv(self.quarterly_path)
            return df
        except Exception as e:
            print(f"분기별 재무 CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
            return None

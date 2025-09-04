import pandas as pd
from typing import List, Dict, Any, Optional

from app.core.config import settings

class FinancialsInfoService:
    def __init__(self):
        self.data_path = settings.FINANCIALS_INFO_PATH
        self.df: Optional[pd.DataFrame] = None
    
    def load_csv_data(self) -> pd.DataFrame:
        """CSV 데이터를 로드합니다."""
        if self.df is None:
            if not self.data_path.exists():
                raise FileNotFoundError(f"CSV file not found at: {self.data_path}")
            
            self.df = pd.read_csv(self.data_path)
        
        return self.df
    
    def get_info_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        """심볼에 해당하는 재무정보 목록을 반환합니다."""
        if self.df is None:
            self.load_csv_data()
        
        filtered_data = self.df[self.df['Symbol'] == symbol]
        
        if filtered_data.empty:
            return []
        
        return filtered_data.to_dict('records')
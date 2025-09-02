import pandas as pd
import FinanceDataReader as fdr

def get_nasdaq_companies(limit=None):
    """
    NASDAQ에 상장된 모든 회사의 정보를 DataFrame으로 반환합니다.
    """
    nasdaq_df = fdr.StockListing('NASDAQ')
    
    if nasdaq_df.empty:
        print("NASDAQ 목록을 가져오는 데 실패했습니다.")
        return pd.DataFrame()
    
    if limit:
        nasdaq_df = nasdaq_df.head(limit)

    return nasdaq_df


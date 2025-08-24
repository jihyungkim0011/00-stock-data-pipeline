import FinanceDataReader as fdr
import os
import time
from tqdm import tqdm

def get_nasdaq_companies(limit=1000):
    """
    FinanceDataReader를 사용하여 나스닥 기업 목록을 가져옵니다.
    :param limit: 가져올 기업의 최대 개수
    :return: DataFrame으로 된 나스닥 기업 목록
    """
    df_nasdaq = fdr.StockListing('NASDAQ')
    return df_nasdaq.head(limit)

def fetch_and_save_data(
    stock_list_df, 
    start_date='2020-01-01'\
):
    """
    기업 목록에 대해 주식 데이터를 가져오고 CSV로 저장합니다.
    :param stock_list_df: 기업 목록 DataFrame
    :param start_date: 데이터 시작 날짜
    """
    output_dir = 'data/nasdaq_stocks'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # DataFrame에 시가총액, 거래액, 거래량 컬럼 추가
    # FinanceDataReader의 get_stock_data는 기본적으로 Volume 컬럼을 포함합니다.
    # 시가총액과 거래액은 pandas를 사용하여 계산합니다.
    # Open, High, Low, Close, Volume, Change 컬럼을 가져옵니다.
    print(f"총 {len(stock_list_df)}개 나스닥 기업의 데이터를 수집합니다.")
    
    for _, row in tqdm(
        stock_list_df.iterrows(), 
        total=len(stock_list_df), 
        desc="데이터 수집 중"
        ):
        symbol = row['Symbol']
        name = row['Name']
        
        try:
            # 일별 주식 데이터 가져오기
            df_stock = fdr.DataReader(symbol, start=start_date)

            if df_stock.empty:
                print(f"[{symbol}] {name} 데이터가 존재하지 않습니다. 건너뜁니다.")
                continue

            # 시가총액 계산 (종가 * 상장주식수)
            # FinanceDataReader는 상장주식수 정보를 제공하지 않으므로, 이 부분을 포함하려면 추가적인 데이터 소스가 필요합니다.
            # 이 코드에서는 종가(Close), 거래량(Volume)을 기준으로 시가총액과 거래액을 계산합니다.
            # 시가총액 = 종가 * 발행주식수 (발행주식수 데이터가 없으므로 여기서는 계산하지 않습니다.)
            # 거래액 = 종가 * 거래량
            
            df_stock['거래액'] = df_stock['Close'] * df_stock['Volume']
            df_stock['시가총액'] = None # 발행주식수 데이터가 없어 계산할 수 없음

            # 필요한 컬럼만 선택
            df_stock = df_stock[['Open', 'High', 'Low', 'Close', 'Volume', '거래액', '시가총액']]

            # CSV 파일로 저장
            file_path = os.path.join(output_dir, f'{symbol}.csv')
            df_stock.to_csv(file_path, encoding='utf-8-sig')

            print(f"[{symbol}] {name} 데이터가 {file_path}에 저장되었습니다.")
            
            # API 호출 제한을 피하기 위해 잠시 대기
            time.sleep(1)

        except Exception as e:
            print(f"[{symbol}] {name} 데이터를 가져오는 중 오류 발생: {e}")
            continue

if __name__ == '__main__':
    # 1. 나스닥 기업 1000개 리스트 가져오기
    print("나스닥 기업 목록을 가져오는 중...")
    nasdaq_companies_df = get_nasdaq_companies(limit=1000)
    
    if not nasdaq_companies_df.empty:
        # 2, 3, 4. 주식 데이터 수집 및 CSV로 저장
        fetch_and_save_data(nasdaq_companies_df)
    else:
        print("나스닥 기업 목록을 가져오는 데 실패했습니다.")
    
    print("모든 작업이 완료되었습니다.")
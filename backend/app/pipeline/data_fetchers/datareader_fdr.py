import FinanceDataReader as fdr
import os
import time
from tqdm import tqdm
import pandas as pd

from companiesCollector import get_nasdaq_companies

def fetch_and_save_data(stock_list_df, start_date='2020-01-01'):
    """
    기업 목록에 대해 주식 데이터를 가져오고 단일 CSV로 저장합니다.
    :param stock_list_df: 기업 목록 DataFrame
    :param start_date: 데이터 시작 날짜
    """
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 모든 데이터를 담을 빈 DataFrame을 생성합니다.
    all_stocks_df = pd.DataFrame()

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

            # 거래액 계산
            df_stock['거래액'] = df_stock['Close'] * df_stock['Volume']

            # 종목 코드를 식별하기 위해 'Symbol' 컬럼을 추가합니다.
            df_stock['Symbol'] = symbol

            # 필요한 컬럼만 선택
            df_stock = df_stock[[
                'Symbol', 'Open', 'High', 
                'Low', 'Close', 'Volume', 
                '거래액'
                ]]

            # 가져온 데이터를 all_stocks_df에 추가합니다.
            all_stocks_df = pd.concat([all_stocks_df, df_stock])

            # API 호출 제한을 피하기 위해 잠시 대기
            time.sleep(1)

        except Exception as e:
            print(f"[{symbol}] {name} 데이터를 가져오는 중 오류 발생: {e}")
            continue

    # 모든 데이터 수집이 완료된 후, 하나의 CSV 파일로 저장합니다.
    if not all_stocks_df.empty:
        file_path = os.path.join(output_dir, 'nasdaq_all_stocks.csv')
        all_stocks_df = all_stocks_df.reset_index(names=['Date'])
        all_stocks_df.to_csv(file_path, encoding='utf-8', index=False)
        print(f"\n모든 나스닥 기업의 데이터가 {file_path}에 성공적으로 저장되었습니다.")
    else:
        print("\n데이터를 저장할 내용이 없습니다.")


if __name__ == '__main__':
    print("나스닥 기업 목록을 가져오는 중...")
    nasdaq_companies_df = get_nasdaq_companies(limit=10)
    
    if not nasdaq_companies_df.empty:
        # 2, 3, 4. 주식 데이터 수집 및 CSV로 저장
        fetch_and_save_data(nasdaq_companies_df)
    else:
        print("나스닥 기업 주식목록을 가져오는 데 실패했습니다.")
    
    print("주식목록 데이터의 모든 작업이 완료되었습니다.")
import yfinance as yf
import pandas as pd
import os
from tqdm import tqdm
import time

def get_financial_info(ticker_symbol: str) -> dict:
    """
    yfinance를 사용하여 특정 티커의 주요 재무 지표를 가져옵니다.

    :param ticker_symbol: 주식 티커 심볼 (e.g., 'AAPL')
    :return: 재무 지표를 담은 딕셔너리. 오류 발생 시 None.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info

        # yfinance의 info 딕셔너리에서 필요한 지표를 추출합니다.
        # .get() 메서드를 사용하여 키가 없는 경우에도 오류 없이 None을 반환합니다.
        financial_metrics = {
            'Symbol': ticker_symbol,
            'Name': info.get('shortName'),
            'EPS': info.get('trailingEps'),
            'PER': info.get('trailingPE'),
            'BPS': info.get('bookValue'),
            'PBR': info.get('priceToBook'),
            'ROE': info.get('returnOnEquity'),
            'ROA': info.get('returnOnAssets'),
            'EBITDA': info.get('ebitda'),
            'EV': info.get('enterpriseValue')
        }
        return financial_metrics

    except Exception as e:
        print(f"[{ticker_symbol}] 정보를 가져오는 중 오류 발생: {e}")
        return None

def fetch_and_save_financial_info(ticker_list: list, output_filename: str = 'nasdaq_financial_info.csv'):
    """
    주어진 티커 목록에 대해 재무 정보를 수집하고 CSV 파일로 저장합니다.

    :param ticker_list: 주식 티커 심볼의 리스트
    :param output_filename: 저장할 CSV 파일 이름
    """
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    all_financial_info = []

    print(f"총 {len(ticker_list)}개 기업의 재무 정보를 수집합니다.")
    
    for symbol in tqdm(ticker_list, desc="재무 정보 수집 중"):
        info = get_financial_info(symbol)
        if info:
            all_financial_info.append(info)
        time.sleep(0.5) # To avoid getting blocked

    if not all_financial_info:
        print("수집된 재무 정보가 없습니다.")
        return

    # 리스트를 DataFrame으로 변환
    df = pd.DataFrame(all_financial_info)
    
    # 컬럼 순서 지정
    columns_order = ['Symbol', 'Name', 'EPS', 'PER', 'BPS', 'PBR', 'ROE', 'ROA', 'EBITDA', 'EV']
    df = df[columns_order]

    # CSV 파일로 저장
    file_path = os.path.join(output_dir, output_filename)
    df.to_csv(file_path, index=False, encoding='utf-8')
    print(f"\n모든 재무 정보가 {file_path}에 저장되었습니다.")


if __name__ == '__main__':
    # 테스트를 위한 티커 목록
    # 실제 사용 시에는 FinanceDataReader 등을 통해 동적으로 목록을 가져올 수 있습니다.
    sample_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("주요 재무 정보 수집을 시작합니다.")
    fetch_and_save_financial_info(sample_tickers)
    print("모든 작업이 완료되었습니다.")

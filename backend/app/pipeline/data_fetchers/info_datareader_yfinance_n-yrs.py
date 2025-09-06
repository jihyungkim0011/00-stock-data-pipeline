import yfinance as yf
import pandas as pd
import os
from tqdm import tqdm
import time

def get_historical_financial_summary(ticker_symbol: str) -> pd.DataFrame:
    """
    yfinance를 사용하여 특정 티커의 과거 연간 재무 요약 정보를 가져옵니다.
    yfinance는 보통 4년간의 연간 데이터를 제공합니다.

    :param ticker_symbol: 주식 티커 심볼 (e.g., 'AAPL')
    :return: 과거 재무 지표를 담은 DataFrame. 오류 발생 시 None.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)

        # 연간 재무제표와 대차대조표를 가져옵니다.
        financials = ticker.financials.T
        balance_sheet = ticker.balance_sheet.T

        if financials.empty or balance_sheet.empty:
            print(f"[{ticker_symbol}] 재무 데이터를 찾을 수 없습니다.")
            return None

        # 날짜 인덱스를 설정합니다.
        financials.index.name = 'Date'
        balance_sheet.index.name = 'Date'

        # 필요한 컬럼만 선택하고 이름을 변경합니다.
        summary_df = pd.DataFrame(index=financials.index)
        summary_df['Symbol'] = ticker_symbol
        summary_df['Name'] = ticker.info.get('shortName')
        
        # EPS (주당순이익)
        if 'Basic EPS' in financials.columns:
            summary_df['EPS'] = financials['Basic EPS']
        else:
            summary_df['EPS'] = None
            
        # ROE (자기자본이익률)
        if 'Net Income' in financials.columns and 'Total Stockholder Equity' in balance_sheet.columns:
            summary_df['ROE'] = financials['Net Income'] / balance_sheet['Total Stockholder Equity']
        else:
            summary_df['ROE'] = None

        # ROA (총자산이익률)
        if 'Net Income' in financials.columns and 'Total Assets' in balance_sheet.columns:
            summary_df['ROA'] = financials['Net Income'] / balance_sheet['Total Assets']
        else:
            summary_df['ROA'] = None
            
        # EBITDA
        if 'EBITDA' in financials.columns:
            summary_df['EBITDA'] = financials['EBITDA']
        else:
            summary_df['EBITDA'] = None
            
        # BPS, PBR, PER, EV는 과거 데이터를 정확히 계산하기 복잡하므로 일단 제외합니다.
        # (과거 주가, 과거 발행 주식 수 필요)
        summary_df['BPS'] = None
        summary_df['PBR'] = None
        summary_df['PER'] = None
        summary_df['EV'] = None

        summary_df.reset_index(inplace=True)
        
        # 컬럼 순서 재정렬
        cols = ['Symbol', 'Name', 'Date', 'EPS', 'ROE', 'ROA', 'EBITDA', 'BPS', 'PBR', 'PER', 'EV']
        summary_df = summary_df[cols]

        return summary_df

    except Exception as e:
        print(f"[{ticker_symbol}] 정보를 가져오는 중 오류 발생: {e}")
        return None

def fetch_and_save_historical_summary(ticker_list: list, output_filename: str = 'nasdaq_financial_summary_annual.csv'):
    """
    주어진 티커 목록에 대해 과거 재무 요약 정보를 수집하고 CSV 파일로 저장합니다.

    :param ticker_list: 주식 티커 심볼의 리스트
    :param output_filename: 저장할 CSV 파일 이름
    """
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    all_summaries_df = pd.DataFrame()

    print(f"총 {len(ticker_list)}개 기업의 연간 재무 요약을 수집합니다.")
    
    for symbol in tqdm(ticker_list, desc="재무 요약 수집 중"):
        summary_df = get_historical_financial_summary(symbol)
        if summary_df is not None and not summary_df.empty:
            all_summaries_df = pd.concat([all_summaries_df, summary_df], ignore_index=True)
        time.sleep(0.5)

    if all_summaries_df.empty:
        print("수집된 재무 요약 정보가 없습니다.")
        return

    # CSV 파일로 저장
    file_path = os.path.join(output_dir, output_filename)
    all_summaries_df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"\n모든 재무 요약 정보가 {file_path}에 저장되었습니다.")


if __name__ == '__main__':
    sample_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    print("과거 재무 요약 정보 수집을 시작합니다.")
    fetch_and_save_historical_summary(sample_tickers)
    print("모든 작업이 완료되었습니다.")

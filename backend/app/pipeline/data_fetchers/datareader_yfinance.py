import pandas as pd
import yfinance as yf
import os
import time
from tqdm import tqdm

from companiesCollector import get_nasdaq_companies

def process_all_financials(ticker, period='annual', start_date='2020-01-01'):
    """
    yfinance 티커 객체로부터 연간 또는 분기별 재무제표 전체를 가져와서 합칩니다.
    :param ticker: yfinance.Ticker 객체
    :param period: 'annual' 또는 'quarterly'
    :param start_date: 데이터 시작 날짜 (ISO 8601 형식)
    :return: 가공된 DataFrame 또는 None
    """
    try:
        if period == 'annual':
            financials_df = ticker.financials.T
            balance_sheet_df = ticker.balance_sheet.T
            cash_flow_df = ticker.cashflow.T
        else:
            financials_df = ticker.quarterly_financials.T
            balance_sheet_df = ticker.quarterly_balance_sheet.T
            cash_flow_df = ticker.quarterly_cashflow.T
        
        # 날짜 인덱스를 datetime 형식으로 변환
        financials_df.index = pd.to_datetime(financials_df.index)
        balance_sheet_df.index = pd.to_datetime(balance_sheet_df.index)
        cash_flow_df.index = pd.to_datetime(cash_flow_df.index)
        
        # 시작 날짜 이후의 데이터만 필터링
        financials_filtered = financials_df[financials_df.index >= start_date]
        balance_sheet_filtered = balance_sheet_df[balance_sheet_df.index >= start_date]
        cash_flow_filtered = cash_flow_df[cash_flow_df.index >= start_date]
        
        if financials_filtered.empty and balance_sheet_filtered.empty and cash_flow_filtered.empty:
            return None

        # 데이터 합치기
        combined_df = financials_filtered.join(balance_sheet_filtered, how='outer', lsuffix='_fin', rsuffix='_bal')
        combined_df = combined_df.join(cash_flow_filtered, how='outer', lsuffix='_comb', rsuffix='_cash')
        
        # 'Date', 'Symbol', 'Name' 컬럼 추가
        combined_df['Date'] = combined_df.index
        combined_df['Symbol'] = ticker.info['symbol']
        combined_df['Name'] = ticker.info['shortName']

        # 컬럼 순서 재정렬
        cols = ['Symbol', 'Name', 'Date'] + [col for col in combined_df.columns if col not in ['Symbol', 'Name', 'Date']]
        combined_df = combined_df[cols]
        
        return combined_df

    except Exception as e:
        print(f"[{ticker.info.get('symbol')}] 재무 데이터를 가져오는 중 오류 발생: {e}")
        return None

def fetch_and_save_all_financial_data(stock_list_df, start_date='2020-01-01'):
    """
    모든 기업의 연간 및 분기별 재무 데이터를 수집하고 단일 CSV로 저장합니다.
    :param stock_list_df: 기업 목록 DataFrame
    :param start_date: 데이터 시작 날짜 (ISO 8601 형식)
    """
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    # 모든 연간 데이터를 담을 빈 DataFrame
    all_annual_df = pd.DataFrame()
    # 모든 분기별 데이터를 담을 빈 DataFrame
    all_quarterly_df = pd.DataFrame()

    print(f"총 {len(stock_list_df)}개 나스닥 기업의 재무 데이터를 수집합니다.")
    
    for _, row in tqdm(stock_list_df.iterrows(), total=len(stock_list_df), desc="데이터 수집 중"):
        symbol = row['Symbol']
        
        try:
            ticker = yf.Ticker(symbol)
            
            # 연간 데이터 처리 및 추가
            annual_df = process_all_financials(ticker, period='annual', start_date=start_date)
            if annual_df is not None and not annual_df.empty:
                all_annual_df = pd.concat([all_annual_df, annual_df], ignore_index=True)
                # tqdm 진행률 표시를 위해 print 대신 log를 사용하거나,
                # 별도 로그 파일을 만들어야 합니다. 여기서는 간결성을 위해 생략.

            # 분기별 데이터 처리 및 추가
            quarterly_df = process_all_financials(ticker, period='quarterly', start_date=start_date)
            if quarterly_df is not None and not quarterly_df.empty:
                all_quarterly_df = pd.concat([all_quarterly_df, quarterly_df], ignore_index=True)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"[{symbol}] 데이터 처리 중 오류 발생: {e}")
            continue

    # 모든 데이터 수집 후 CSV 파일로 저장
    if not all_annual_df.empty:
        file_path_annual = os.path.join(output_dir, 'nasdaq_financials_annual_all.csv')
        all_annual_df.to_csv(file_path_annual, index=False, encoding='utf-8-sig')
        print(f"\n모든 연간 재무 데이터가 {file_path_annual}에 저장되었습니다.")
    else:
        print("\n저장할 연간 재무 데이터가 없습니다.")

    if not all_quarterly_df.empty:
        file_path_quarterly = os.path.join(output_dir, 'nasdaq_financials_quarterly_all.csv')
        all_quarterly_df.to_csv(file_path_quarterly, index=False, encoding='utf-8-sig')
        print(f"모든 분기별 재무 데이터가 {file_path_quarterly}에 저장되었습니다.")
    else:
        print("저장할 분기별 재무 데이터가 없습니다.")

if __name__ == '__main__':
    # 1. 나스닥 기업 목록 가져오기
    print("나스닥 기업 목록을 가져오는 중...")
    nasdaq_companies_df = get_nasdaq_companies(limit=5) # 테스트를 위해 5개만 가져옵니다.
    
    if not nasdaq_companies_df.empty:
        # 데이터 수집 및 CSV로 저장
        fetch_and_save_all_financial_data(nasdaq_companies_df, start_date='2020-01-01')
    else:
        print("나스닥 기업 목록을 가져오는 데 실패했습니다.")
    
    print("모든 작업이 완료되었습니다.")
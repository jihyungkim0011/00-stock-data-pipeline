import yfinance as yf
import pandas as pd
import os
from tqdm import tqdm
import time
from companiesCollector import get_nasdaq_companies

def get_historical_financial_info(ticker_symbol: str, years: int) -> list:
    """
    yfinance를 사용하여 특정 티커의 과거 N년간 주요 재무 지표를 가져옵니다.
    :param ticker_symbol: 주식 티커 심볼 (e.g., 'AAPL')
    :param years: 가져올 연도 수
    :return: 각 연도의 재무 지표 딕셔너리를 담은 리스트.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        
        # 연간 재무제표 데이터 가져오기
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        
        if financials.empty or balance_sheet.empty:
            print(f"[{ticker_symbol}] 재무제표 데이터를 찾을 수 없습니다.")
            return []
            
        # 회사 이름 가져오기
        info = ticker.info
        name = info.get('shortName')
        
        # 사용 가능한 연도만큼만 데이터를 가져오도록 제한
        available_years = financials.columns[:years]
        all_yearly_metrics = []
        
        # 주주 자본(Total Stockholder Equity)에 대한 여러 대체 키
        equity_keys = ['Total Stockholder Equity', 'Stockholders Equity', 'Total Equity Gross Minority Interest']

        for year_column in available_years:
            try:
                report_date = year_column.strftime('%Y-%m-%d')
                
                # --- 주요 지표 추출 및 계산 ---
                net_income = financials.loc['Net Income'].get(year_column)
                total_assets = balance_sheet.loc['Total Assets'].get(year_column)
                
                # 여러 키를 시도하여 주주 자본 데이터 가져오기
                total_stockholder_equity = None
                for key in equity_keys:
                    if key in balance_sheet.index:
                        total_stockholder_equity = balance_sheet.loc[key].get(year_column)
                        break
                
                # EBITDA는 없는 경우가 많으므로 안전하게 가져옴
                ebitda = financials.loc['EBITDA'].get(year_column) if 'EBITDA' in financials.index else None
                shares_outstanding = financials.loc['Basic Average Shares'].get(year_column)
                
                # 해당 연도 마지막 거래일의 종가 가져오기
                end_of_year_date = year_column.strftime('%Y-%m-%d')
                hist = ticker.history(start=end_of_year_date, period="1d")
                if hist.empty:
                    next_day = year_column + pd.Timedelta(days=1)
                    hist = ticker.history(start=next_day.strftime('%Y-%m-%d'), period="1d")
                    
                close_price = hist['Close'].iloc[0] if not hist.empty else None
                
                # --- 지표 계산 (0으로 나누기 방지) ---
                eps = (net_income / shares_outstanding) if net_income is not None and shares_outstanding and shares_outstanding != 0 else None
                per = (close_price / eps) if close_price is not None and eps and eps > 0 else None
                
                bps = (total_stockholder_equity / shares_outstanding) if total_stockholder_equity is not None and shares_outstanding and shares_outstanding != 0 else None
                pbr = (close_price / bps) if close_price is not None and bps and bps > 0 else None
                
                roe = (net_income / total_stockholder_equity) if net_income is not None and total_stockholder_equity and total_stockholder_equity != 0 else None
                roa = (net_income / total_assets) if net_income is not None and total_assets and total_assets != 0 else None
                
                ev = None # EV는 과거 데이터를 정확히 계산하기 복잡하므로 일단 제외합니다.
                
                yearly_metrics = {
                    'Date': report_date,
                    'Symbol': ticker_symbol,
                    'Name': name,
                    'EPS': eps,
                    'PER': per,
                    'BPS': bps,
                    'PBR': pbr,
                    'ROE': roe,
                    'ROA': roa,
                    'EBITDA': ebitda,
                    'EV': ev
                }
                all_yearly_metrics.append(yearly_metrics)
                time.sleep(0.1)
                
            except Exception as e:
                # 개별 연도 처리 중 오류가 발생해도 계속 진행
                print(f"[{ticker_symbol}] {year_column.year}년도 데이터 처리 중 오류 발생: {e}")
                continue # 다음 연도로 넘어감
                
        return all_yearly_metrics
        
    except Exception as e:
        print(f"[{ticker_symbol}] 정보를 가져오는 중 오류 발생: {e}")
        return []

def fetch_and_save_historical_info(companies_df: pd.DataFrame, years: int, output_filename: str = 'nasdaq_financial_info_n_yrs.csv'):
    """
    주어진 티커 목록에 대해 과거 N년간의 재무 정보를 수집하고 CSV 파일로 저장합니다.

    :param companies_df: 주식 티커와 산업 정보가 포함된 데이터프레임
    :param years: 수집할 연도 수
    :param output_filename: 저장할 CSV 파일 이름
    """
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    all_financial_info = []

    print(f"총 {len(companies_df)}개 기업의 {years}년간 재무 정보를 수집합니다.")
    
    for index, row in tqdm(companies_df.iterrows(), total=companies_df.shape[0], desc="재무 정보 수집 중"):
        symbol = row['Symbol']
        industry = row.get('Industry')
        industry_code = row.get('IndustryCode')
        
        info_list = get_historical_financial_info(symbol, years)
        if info_list:
            for info in info_list:
                info['Industry'] = industry
                info['IndustryCode'] = industry_code
            all_financial_info.extend(info_list)
        time.sleep(0.5)

    if not all_financial_info:
        print("수집된 재무 정보가 없습니다.")
        return

    df = pd.DataFrame(all_financial_info)
    
    # 컬럼 순서 지정
    columns_order = ['Date', 'Symbol', 'Name', 'EPS', 'PER', 'BPS', 'PBR', 'ROE', 'ROA', 'EBITDA', 'EV']
    df = df.reindex(columns=columns_order)

    file_path = os.path.join(output_dir, output_filename)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"\n모든 재무 정보가 {file_path}에 저장되었습니다.")


if __name__ == '__main__':
    # NASDAQ 회사 목록을 DataFrame으로 가져옵니다.
    nasdaq_companies_df = get_nasdaq_companies(limit=5)
    
    if nasdaq_companies_df.empty:
        print("NASDAQ 회사 목록을 가져오지 못했습니다. 작업을 중단합니다.")
    else:
        YEARS_TO_FETCH = 5
        
        print("과거 재무 정보 수집을 시작합니다.")
        fetch_and_save_historical_info(nasdaq_companies_df, YEARS_TO_FETCH)
        print("모든 작업이 완료되었습니다.")
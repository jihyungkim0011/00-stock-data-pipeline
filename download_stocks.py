import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. 데이터를 가져올 회사들의 티커(Ticker) 목록을 지정합니다.
# 예시: 애플, 마이크로소프트, 구글, 아마존, 엔비디아, 테슬라, 메타, JP모건, 비자, 존슨앤드존슨
# 원하는 회사들의 티커로 이 목록을 수정하세요.
tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 
    'TSLA', 'META', 'JPM', 'V', 'JNJ'
]

# 2. 데이터 조회 기간을 설정합니다 (오늘로부터 3년 전까지).
end_date = datetime.today()
start_date = end_date - timedelta(days=3 * 365)

# 날짜 형식을 'YYYY-MM-DD'로 변환합니다.
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

print(f"{len(tickers)}개 회사의 주식 데이터를 다운로드합니다...")
print(f"조회 기간: {start_date_str} 부터 {end_date_str} 까지")

# 3. yfinance를 사용하여 지정된 기간의 주식 데이터를 다운로드합니다.
# group_by='ticker' 옵션은 데이터를 회사별로 정리해줍니다.
data = yf.download(
    tickers, 
    start=start_date_str, 
    end=end_date_str, 
    group_by='ticker'
)


# 4. 다운로드한 데이터를 회사별로 나누어 하나의 CSV 파일에 저장합니다.
# 각 회사의 데이터는 별도의 시트(Sheet)에 저장됩니다.
output_filename = 'stock_data_last_3_years.xlsx'
with pd.ExcelWriter(output_filename) as writer:
    for ticker in tickers:
        # 특정 티커의 데이터만 선택하여 시트에 저장
        # data[ticker]는 해당 티커의 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume' 컬럼을 포함합니다.
        ticker_data = data[ticker].dropna() # 데이터가 없는 행은 제외
        ticker_data.to_excel(writer, sheet_name=ticker)
        print(f"- '{ticker}' 데이터 저장 완료.")

print(f"\n모든 데이터 다운로드가 완료되었습니다. '{output_filename}' 파일로 저장되었습니다.")


# 각 티커에 대해 재무제표 데이터 불러오기
for ticker_symbol in tickers:
    try:
        print(f"========== {ticker_symbol} 재무 정보 ==========")
        # yfinance Ticker 객체 생성
        stock = yf.Ticker(ticker_symbol)

        # 1. 손익계산서 (Financials)
        print("\n--- 손익계산서 (Annual) ---")
        print(stock.financials)

        # 2. 대차대조표 (Balance Sheet)
        print("\n--- 대차대조표 (Annual) ---")
        print(stock.balance_sheet)

        # 3. 현금흐름표 (Cash Flow)
        print("\n--- 현금흐름표 (Annual) ---")
        print(stock.cashflow)

        print(f"========== {ticker_symbol} 정보 끝 ==========\n")

    except Exception as e:
        print(f"{ticker_symbol} 정보를 가져오는 중 오류가 발생했습니다: {e}")
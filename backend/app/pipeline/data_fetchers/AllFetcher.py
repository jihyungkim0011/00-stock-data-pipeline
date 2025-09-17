from companiesCollector import get_nasdaq_companies
from datareader_fdr import fetch_and_save_data
from datareader_yfinance import fetch_and_save_all_financial_data
from info_datareader_yfinance_NYrs import fetch_and_save_historical_info
from news_crawler import fetch_and_save_news_urls
# from CompanyData import fetch_nasdaq_companies_field

# fetch_nasdaq_companies_field()

print("나스닥 기업 목록을 가져오는 중...")
nasdaq_companies_df = get_nasdaq_companies(limit=10)

if not nasdaq_companies_df.empty:
    fetch_and_save_data(nasdaq_companies_df)
    print("AllFetcher: 주식목록 데이터의 모든 작업이 완료되었습니다.")
    fetch_and_save_all_financial_data(nasdaq_companies_df, start_date='2020-01-01')
    print("AllFetcher: 재무데이터의 모든 작업이 완료되었습니다.")
    fetch_and_save_historical_info(nasdaq_companies_df, years=5)
    print("AllFetcher: 과거 재무지표의 모든 작업이 완료되었습니다.")
else:
    print("AllFetcher: 나스닥 기업목록을 가져오는 데 실패했습니다.")

if not nasdaq_companies_df.empty:
    fetch_and_save_news_urls(nasdaq_companies_df, days=10)
    print("AllFetcher: 과거 뉴스 데이터의 모든 작업이 완료되었습니다.")
else:
    print("AllFetcher: 나스닥 뉴스데이터 목록을 가져오는 데 실패했습니다.")

print("AllFetcher: 모든 작업이 완료되었습니다.")
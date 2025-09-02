import pandas as pd
from newsapi import NewsApiClient
import os
import time
from tqdm import tqdm
from datetime import datetime, timedelta
import configparser

from companiesCollector import get_nasdaq_companies

def load_api_key(section="news_api",config_path='pipeline.conf'):
    """
    설정 파일에서 API 키를 불러옵니다.
    """
    try:
        parser = configparser.ConfigParser()
        parser.read(config_path)
        return parser.get(section, "api_key")
    except Exception as e:
        print(f"API 키를 불러오는 중 오류 발생: {e}")
        return None

def get_news_from_api(query, start_date, end_date):
    """
    NewsAPI를 사용하여 지정된 검색어와 기간의 뉴스를 가져옵니다.
    :param query: 검색어 (기업명)
    :param start_date: 검색 시작 날짜
    :param end_date: 검색 종료 날짜
    :return: 뉴스 기사 리스트 (성공 시), None (오류 발생 시)
    """
    try:
        # NewsAPI 무료 플랜의 최대 검색 기간인 30일로 제한
        days = (end_date - start_date).days
        if days > 30:
            print(f"경고: NewsAPI 무료 플랜은 최대 30일 이내의 뉴스만 제공합니다. 검색 기간을 {days}일에서 30일로 조정합니다.")
            start_date = end_date - timedelta(days=30)
            
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
        all_articles = newsapi.get_everything(
            q=query,
            from_param=start_date.strftime('%Y-%m-%d'),
            to=end_date.strftime('%Y-%m-%d'),
            language='en',
            sort_by='relevancy'
        )
        return all_articles.get('articles', [])
    except Exception as e:
        print(f"NewsAPI 요청 중 오류 발생: {e}")
        return None

def process_and_save_news(symbol, name, articles):
    """
    수집된 뉴스 기사 목록을 DataFrame으로 변환하여 반환합니다.
    이 함수는 더 이상 파일 저장을 담당하지 않습니다.
    """
    if not articles:
        print(f"[{symbol}] {name}에 대한 뉴스가 없습니다.")
        return None
        
    news_list = []
    for article in articles:
        news_list.append({
            'Symbol': symbol,
            'Name': name,
            'title': article.get('title'),
            'url': article.get('url'),
            'publishedAt': article.get('publishedAt')
        })
    
    df_news = pd.DataFrame(news_list)
    return df_news

def fetch_and_save_news_urls(stock_list_df, days=30):
    """
    모든 기업에 대한 뉴스 URL을 수집하고 하나의 CSV로 저장합니다.
    """
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # 모든 뉴스 데이터를 담을 빈 DataFrame을 생성합니다.
    all_news_df = pd.DataFrame()

    print(f"총 {len(stock_list_df)}개 나스닥 기업의 뉴스를 수집합니다. 기간: {days}일")

    for _, row in tqdm(stock_list_df.iterrows(), total=len(stock_list_df), desc="뉴스 URL 수집 중"):
        symbol = row['Symbol']
        name = row['Name']
        
        articles = get_news_from_api(name, start_date, end_date)
        
        if articles is not None:
            df_news = process_and_save_news(symbol, name, articles)
            if df_news is not None:
                # 개별 기업의 뉴스 데이터를 전체 데이터프레임에 추가합니다.
                all_news_df = pd.concat([all_news_df, df_news], ignore_index=True)
        
        time.sleep(1) # API 호출 빈도 제어

    # 모든 데이터 수집 후 하나의 CSV 파일로 저장
    if not all_news_df.empty:
        file_path = os.path.join(output_dir, 'nasdaq_news_all.csv')
        all_news_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"\n모든 나스닥 기업의 뉴스 URL이 {file_path}에 성공적으로 저장되었습니다.")
    else:
        print("\n저장할 뉴스 데이터가 없습니다.")

if __name__ == '__main__':
    NEWS_API_KEY = load_api_key()
    if not NEWS_API_KEY:
        print("API 키를 불러오지 못했습니다. 프로그램을 종료합니다.")
    else:
        print("나스닥 기업 목록을 가져오는 중...")
        nasdaq_companies_df = get_nasdaq_companies(limit=5)
        
        if not nasdaq_companies_df.empty:
            fetch_and_save_news_urls(nasdaq_companies_df, days=5)
        else:
            print("나스닥 기업 목록을 가져오는 데 실패했습니다.")
            
    print("모든 작업이 완료되었습니다.")
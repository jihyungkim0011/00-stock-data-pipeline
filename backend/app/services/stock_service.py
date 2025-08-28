import pandas as pd
import os

class StockService:
    """
    주식 데이터를 로드하고 필터링하는 비즈니스 로직을 처리하는 서비스 클래스입니다.
    """
    df_stocks: pd.DataFrame

    def __init__(self, data_file_path: str = "nasdaq_all_stocks.csv"):
        """
        서비스 초기화 시 CSV 파일을 로드합니다.
        """
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, "..","..","..", "data", data_file_path)
        
        self.df_stocks = pd.DataFrame() # 초기 빈 DataFrame 설정

        try:
            self.df_stocks = pd.read_csv(csv_path)
            # 'Date' 컬럼을 datetime 객체로 변환하여 날짜 기반 필터링에 용이하게 함
            self.df_stocks['Date'] = pd.to_datetime(self.df_stocks['Date'])
            # 'Symbol' 컬럼을 대문자로 통일하여 검색 일관성 유지
            self.df_stocks['Symbol'] = self.df_stocks['Symbol'].str.upper()
            print(f"INFO: {csv_path} 파일 로드 성공. 총 {len(self.df_stocks)}개 데이터.")
        except FileNotFoundError:
            print(f"경고: {csv_path} 파일을 찾을 수 없습니다. 서비스는 데이터 없이 실행됩니다.")
        except KeyError as e:
            print(f"경고: CSV 파일에 필요한 컬럼이 없습니다: {e}. 'Symbol' 또는 'Date' 컬럼 이름을 확인하세요.")
        except Exception as e:
            print(f"경고: CSV 파일을 로드하는 중 오류 발생: {e}. 서비스는 데이터 없이 실행됩니다.")

    def get_all_stocks(self) -> list[dict]:
        """
        모든 주식 데이터를 반환합니다.
        """
        if self.df_stocks.empty:
            return []
        return self.df_stocks.to_dict(orient="records")

    def get_stock_by_ticker(self, ticker: str) -> list[dict]:
        """
        특정 종목(ticker)에 해당하는 모든 데이터를 반환합니다.
        """
        filtered_df = self.df_stocks[self.df_stocks['Symbol'] == ticker.upper()]
        return filtered_df.to_dict(orient="records")

    def get_stock_by_ticker_and_date_range(self, ticker: str, start_date: str = None, end_date: str = None) -> list[dict]:
        """
        특정 종목의 지정된 날짜 범위 데이터를 반환합니다.
        """
        filtered_df = self.df_stocks[self.df_stocks['Symbol'] == ticker.upper()]

        if start_date:
            try:
                start_date_dt = pd.to_datetime(start_date)
                filtered_df = filtered_df[filtered_df['Date'] >= start_date_dt]
            except ValueError:
                # 잘못된 날짜 형식 처리
                pass # 에러를 발생시키는 대신 필터링하지 않고 넘어갑니다.
            
        if end_date:
            try:
                end_date_dt = pd.to_datetime(end_date)
                filtered_df = filtered_df[filtered_df['Date'] <= end_date_dt]
            except ValueError:
                # 잘못된 날짜 형식 처리
                pass # 에러를 발생시키는 대신 필터링하지 않고 넘어갑니다.

        return filtered_df.to_dict(orient="records")


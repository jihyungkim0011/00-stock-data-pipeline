import pandas as pd
import duckdb

from app.core.config import settings

class StockService:
    """
    주식 데이터를 불러오고 필터링하는 비즈니스 로직을 처리하는 서비스 클래스입니다.
    높은 성능을 위해 DuckDB를 사용하여 기술적 지표를 미리 계산합니다.
    """
    df_stocks_enriched: pd.DataFrame

    def __init__(self):
        """
        서비스를 초기화합니다. CSV 파일을 불러온 다음, DuckDB를 사용하여
        모든 주식에 대한 모든 기술적 지표(이동 평균, RSI)를 미리 계산합니다.
        """
        self.df_stocks_enriched = pd.DataFrame()  # 초기 빈 DataFrame
        csv_path = settings.DATA_FILE_PATH

        if not csv_path:
            print("경고: .env 파일에 DATA_FILE_PATH가 설정되지 않았습니다. 서비스가 데이터 없이 실행됩니다.")
            return

        try:
            df_stocks = pd.read_csv(csv_path)
            df_stocks['Date'] = pd.to_datetime(df_stocks['Date'])
            df_stocks['Symbol'] = df_stocks['Symbol'].str.upper()

            # 성능 향상을 위해 SQL과 DuckDB를 사용하여 지표를 효율적으로 계산합니다.
            con = duckdb.connect(database=':memory:', read_only=False)
            con.register('stocks', df_stocks)

            query = """
            WITH PriceDiff AS (
                SELECT
                    *,
                    "Close" - LAG("Close", 1, "Close") OVER (PARTITION BY "Symbol" ORDER BY "Date") AS diff
                FROM stocks
            ),
            GainsAndLosses AS (
                SELECT
                    *,
                    CASE WHEN diff > 0 THEN diff ELSE 0 END AS gain,
                    CASE WHEN diff < 0 THEN -diff ELSE 0 END AS loss
                FROM PriceDiff
            )
            SELECT
                *,
                AVG("Close") OVER (PARTITION BY "Symbol" ORDER BY "Date" ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS MA_5,
                AVG("Close") OVER (PARTITION BY "Symbol" ORDER BY "Date" ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS MA_20,
                AVG("Close") OVER (PARTITION BY "Symbol" ORDER BY "Date" ROWS BETWEEN 59 PRECEDING AND CURRENT ROW) AS MA_60,
                (
                    100 - (100 / (1 + (
                        AVG(gain) OVER (PARTITION BY "Symbol" ORDER BY "Date" ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) /
                        NULLIF(AVG(loss) OVER (PARTITION BY "Symbol" ORDER BY "Date" ROWS BETWEEN 13 PRECEDING AND CURRENT ROW), 0)
                    )))
                ) AS RSI_14
            FROM GainsAndLosses
            """

            self.df_stocks_enriched = con.execute(query).fetchdf()
            con.close()

            print(f"정보: {csv_path} 파일을 성공적으로 불러오고 처리했습니다. 총 행 수: {len(self.df_stocks_enriched)}.")

        except FileNotFoundError:
            print(f"경고: {csv_path} 파일을 찾을 수 없습니다. 서비스가 데이터 없이 실행됩니다.")
        except Exception as e:
            print(f"경고: 데이터를 불러오거나 처리하는 중 오류가 발생했습니다: {e}. 서비스가 데이터 없이 실행됩니다.")

    def get_all_stocks(self) -> list[dict]:
        """
        미리 계산된 지표가 포함된 모든 주식 데이터를 반환합니다.
        """
        if self.df_stocks_enriched.empty:
            return []
        return self.df_stocks_enriched.to_dict(orient="records")

    def get_stock_by_ticker(self, ticker: str) -> list[dict]:
        """
        미리 계산된 지표가 포함된 특정 티커(종목)의 모든 데이터를 반환합니다.
        """
        return self.get_stock_by_ticker_and_date_range(ticker)

    def get_stock_by_ticker_and_date_range(self, ticker: str, start_date: str = None, end_date: str = None) -> list[dict]:
        """
        미리 계산된 데이터에서 지정된 날짜 범위 내의 특정 티커 데이터를 반환합니다.
        """
        if self.df_stocks_enriched.empty:
            return []

        # 이미 처리된 DataFrame에서 필터링
        filtered_df = self.df_stocks_enriched[self.df_stocks_enriched['Symbol'] == ticker.upper()].copy()

        if start_date:
            try:
                start_date_dt = pd.to_datetime(start_date)
                filtered_df = filtered_df[filtered_df['Date'] >= start_date_dt]
            except ValueError:
                pass  # 유효하지 않은 날짜 형식은 무시합니다.

        if end_date:
            try:
                end_date_dt = pd.to_datetime(end_date)
                filtered_df = filtered_df[filtered_df['Date'] <= end_date_dt]
            except ValueError:
                pass  # 유효하지 않은 날짜 형식은 무시합니다.

        return filtered_df.to_dict(orient="records")

import pytest
import pandas as pd
from unittest.mock import patch
from app.services.stock_service import StockService

# 테스트에 사용할 가짜 데이터프레임을 생성합니다.
# 실제 read_csv를 호출하는 대신 이 데이터가 반환될 것입니다.
@pytest.fixture
def mock_stock_data():
    """테스트용 가짜 주식 데이터프레임을 제공하는 Fixture"""
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-01'],
        'Symbol': ['aapl', 'msft', 'aapl'],
        'Open': [150.0, 300.0, 151.0],
        'Close': [152.0, 305.0, 153.0]
    }
    return pd.DataFrame(data)

# patch를 사용하여 pandas.read_csv의 동작을 가로챕니다.
# 이제 StockService가 초기화될 때 실제 파일을 읽지 않고,
# mock_stock_data가 반환하는 데이터프레임을 사용하게 됩니다.
@patch('pandas.read_csv')
def test_service_initialization(mock_read_csv, mock_stock_data):
    """StockService가 정상적으로 초기화되는지 테스트합니다."""
    # mock_read_csv가 mock_stock_data를 반환하도록 설정
    mock_read_csv.return_value = mock_stock_data
    
    service = StockService()

    # CSV 파일 로드 시 Symbol이 대문자로 변환되었는지 확인
    assert service.df_stocks['Symbol'].tolist() == ['AAPL', 'MSFT', 'AAPL']
    # Date 컬럼이 datetime 객체로 변환되었는지 확인
    assert pd.api.types.is_datetime64_any_dtype(service.df_stocks['Date'])
    # mock_read_csv가 한 번 호출되었는지 확인
    mock_read_csv.assert_called_once()

@patch('pandas.read_csv')
def test_get_stock_by_ticker(mock_read_csv, mock_stock_data):
    """특정 티커로 주식 정보를 잘 필터링하는지 테스트합니다."""
    mock_read_csv.return_value = mock_stock_data
    service = StockService()

    # 'aapl' (소문자)로 조회해도 'AAPL' 데이터를 반환해야 함
    result = service.get_stock_by_ticker('aapl')
    assert len(result) == 2
    assert result[0]['Symbol'] == 'AAPL'
    assert result[1]['Symbol'] == 'AAPL'

    # 존재하지 않는 티커 조회 시 빈 리스트를 반환해야 함
    result_empty = service.get_stock_by_ticker('GOOG')
    assert len(result_empty) == 0

@patch('pandas.read_csv')
def test_get_stock_by_ticker_and_date_range(mock_read_csv, mock_stock_data):
    """티커와 날짜 범위로 주식 정보를 잘 필터링하는지 테스트합니다."""
    mock_read_csv.return_value = mock_stock_data
    service = StockService()

    # 시작 날짜로 필터링
    result = service.get_stock_by_ticker_and_date_range('aapl', start_date='2023-01-01')
    assert len(result) == 2

    # 시작/종료 날짜로 필터링
    result = service.get_stock_by_ticker_and_date_range('msft', start_date='2023-01-01', end_date='2023-01-03')
    assert len(result) == 1
    assert result[0]['Symbol'] == 'MSFT'
    assert str(result[0]['Date'].date()) == '2023-01-02'

    # 데이터가 없는 날짜 범위로 필터링
    result = service.get_stock_by_ticker_and_date_range('aapl', start_date='2023-02-01')
    assert len(result) == 0

    # 잘못된 날짜 형식에도 에러 없이 빈 결과를 반환해야 함
    result = service.get_stock_by_ticker_and_date_range('aapl', start_date='invalid-date')
    assert len(result) == 2 # 날짜 필터링이 적용되지 않은 원래 결과

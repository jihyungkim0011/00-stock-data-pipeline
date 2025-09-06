from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class StockPrice(BaseModel):
    """
    Schema for stock price data, including technical indicators.
    """
    Date: date = Field(..., alias="Date")
    symbol: str = Field(..., alias="Symbol")
    open: float = Field(..., alias="Open")
    high: float = Field(..., alias="High")
    low: float = Field(..., alias="Low")
    close: float = Field(..., alias="Close")
    volume: int = Field(..., alias="Volume")
    trading_value: float = Field(..., alias="거래액")

    # Technical Indicators
    ma_5: Optional[float] = Field(None, alias="MA_5")
    ma_20: Optional[float] = Field(None, alias="MA_20")
    ma_60: Optional[float] = Field(None, alias="MA_60")
    rsi_14: Optional[float] = Field(None, alias="RSI_14")

    class Config:
        from_attributes = True
        populate_by_name = True


class Financials(BaseModel):
    """
    Schema for company financials.
    """
    symbol: str = Field(..., alias="Symbol")
    name: str = Field(..., alias="Name")
    Date: date = Field(..., alias="Date")
    total_revenue: Optional[float] = Field(None, alias="Total Revenue")
    cost_of_revenue: Optional[float] = Field(None, alias="Cost Of Revenue")
    gross_profit: Optional[float] = Field(None, alias="Gross Profit")
    operating_income: Optional[float] = Field(None, alias="Operating Income")
    operating_expense: Optional[float] = Field(None, alias="Operating Expense")
    net_income: Optional[float] = Field(None, alias="Net Income")
    diluted_eps: Optional[float] = Field(None, alias="Diluted EPS")
    total_liabilities_net_minority_interest: Optional[float] = Field(None, alias="Total Liabilities Net Minority Interest")
    stockholders_equity: Optional[float] = Field(None, alias="Stockholders Equity")
    working_capital: Optional[float] = Field(None, alias="Working Capital")
    net_debt: Optional[float] = Field(None, alias="Net Debt")

    class Config:
        from_attributes = True
        populate_by_name = True

from pydantic import BaseModel
from typing import Optional

class FinancialInfo(BaseModel):
    Date: str
    Symbol: str
    Name: str
    EPS: Optional[float]
    PER: Optional[float]
    BPS: Optional[float]
    PBR: Optional[float]
    ROE: Optional[float]
    ROA: Optional[float]
    EBITDA: Optional[float]
    EV: Optional[float]

    class Config:
        from_attributes = True
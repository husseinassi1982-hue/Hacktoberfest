from pydantic import BaseModel, Field


class Position(BaseModel):
    symbol: str
    quantity: float = Field(gt=0)
    price: float = Field(gt=0)
    sector: str
    asset_type: str


class Portfolio(BaseModel):
    positions: list[Position] = Field(default_factory=list)
    cash: float = Field(default=0, ge=0)


class StoredPortfolioRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    portfolio: Portfolio

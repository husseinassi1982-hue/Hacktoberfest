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
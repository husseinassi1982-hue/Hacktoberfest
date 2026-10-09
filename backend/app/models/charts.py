from pydantic import BaseModel

from app.models.portfolio import Portfolio
from app.models.scenario import ScenarioInput


class ChartDataRequest(BaseModel):
    portfolio: Portfolio
    scenario: ScenarioInput | None = None

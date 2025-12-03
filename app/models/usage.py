from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class UsageLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    agent_id: str
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model: str
    input_tokens: int
    output_tokens: int
    cost_rub: float = 0.0
    revenue_rub: float = 0.0
    plan_id: str
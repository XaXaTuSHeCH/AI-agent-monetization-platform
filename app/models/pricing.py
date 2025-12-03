from pydantic import BaseModel
from typing import Literal, Optional
from enum import Enum

class PricingType(str, Enum):
    SUBSCRIPTION = "subscription"
    PER_REQUEST = "per_request"
    PAY_PER_RESULT = "pay_per_result"
    HYBRID = "hybrid"

class PayPerResultConfig(BaseModel):
    result_type: Literal["exam_score_improvement", "task_solved", "time_saved"]
    baseline_field: str
    threshold: float
    payment_per_unit: float
    max_payment_per_month: Optional[float] = None

class PricingPlan(BaseModel):
    id: str
    name: str
    pricing_type: PricingType
    subscription_monthly: float = 0.0
    price_per_request: float = 0.0
    pay_per_result: Optional[PayPerResultConfig] = None
    active: bool = True
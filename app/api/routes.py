from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.models.usage import UsageLog
from app.models.pricing import PricingPlan
from app.services.profitability import get_profitability_last_30d
from app.services.billing import calculate_result_payment
from app.services.cost_tracker import calculate_cost
from typing import List, Dict

router = APIRouter()

@router.post("/usage")
def log_usage(usage: UsageLog, session: Session = Depends(get_session)):
    usage.cost_rub = calculate_cost(usage.model, usage.input_tokens, usage.output_tokens)
    session.add(usage)
    session.commit()
    return {"message": "Usage logged"}

@router.get("/profitability/{agent_id}")
def get_profitability(agent_id: str):
    return get_profitability_last_30d(agent_id)

@router.post("/billing/calculate")
def calculate_payment(plan: PricingPlan, user_history: List[Dict]):
    return {"payment": calculate_result_payment(user_history, plan)}
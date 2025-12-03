from typing import List, Dict
from app.models.pricing import PricingPlan, PayPerResultConfig

def calculate_result_payment(user_history: List[Dict], plan: PricingPlan) -> float:
    if not plan.pay_per_result or not user_history:
        return 0.0

    cfg: PayPerResultConfig = plan.pay_per_result
    baseline = None
    for entry in user_history:
        if cfg.baseline_field in entry:
            baseline = entry[cfg.baseline_field]
            break
    if baseline is None:
        return 0.0

    latest_score = user_history[-1].get("mock_exam_score_after", baseline)
    improvement = max(0, latest_score - baseline)
    units = improvement // cfg.threshold
    payment = units * cfg.payment_per_unit

    if cfg.max_payment_per_month:
        payment = min(payment, cfg.max_payment_per_month)

    return round(payment, 2)
import pandas as pd
from app.models.pricing import PricingPlan

def simulate_plan_revenue(df: pd.DataFrame, plan: PricingPlan) -> float:
    total = 0.0
    if plan.pricing_type == "subscription":
        total += plan.subscription_monthly * len(df)
    elif plan.pricing_type == "pay_per_result" and plan.pay_per_result:
        for _, row in df.iterrows():
            improvement = row["mock_exam_score_after"] - row["mock_exam_score_before"]
            units = max(0, improvement // plan.pay_per_result.threshold)
            total += units * plan.pay_per_result.payment_per_unit
    return round(total, 2)
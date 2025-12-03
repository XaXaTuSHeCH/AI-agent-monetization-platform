from sqlmodel import select, func
from app.models.usage import UsageLog
from app.database import engine

def get_profitability_last_30d(agent_id: str = "math-ege-agent"):
    with engine.connect() as conn:
        statement = select(
            func.sum(UsageLog.cost_rub),
            func.sum(UsageLog.revenue_rub)
        ).where(UsageLog.agent_id == agent_id)
        result = conn.execute(statement).first()
        cost, revenue = result if result else (0, 0)

    revenue = revenue or 0.0001
    margin = (revenue - cost) / revenue

    return {
        "cost_rub": round(cost, 2),
        "revenue_rub": round(revenue, 2),
        "margin": round(margin, 3),
        "recommendation": "Маржа <20% — повысьте тариф!" if margin < 0.2 else None
    }
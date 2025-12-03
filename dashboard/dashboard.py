import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from app.services.profitability import get_profitability_last_30d
from app.services.simulator import simulate_plan_revenue
from app.models.pricing import PricingPlan, PricingType, PayPerResultConfig

st.set_page_config(page_title="Монетизация ИИ-агента", layout="wide")

@st.cache_data
def load_data():
    path = Path(__file__).parent.parent / "data" / "synthetic_data.csv"
    return pd.read_csv(path)

df = load_data()

subscription_plan = PricingPlan(
    id="subscription-499",
    name="Подписка 499 руб/мес",
    pricing_type=PricingType.SUBSCRIPTION,
    subscription_monthly=499.0
)

pay_per_result_plan = PricingPlan(
    id="pay-per-result-199",
    name="Оплата за результат (199 руб за +10 баллов)",
    pricing_type=PricingType.PAY_PER_RESULT,
    pay_per_result=PayPerResultConfig(
        result_type="exam_score_improvement",
        baseline_field="mock_exam_score_before",
        threshold=10.0,
        payment_per_unit=199.0
    )
)

def ask_llm(question: str) -> str:
    try:
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": f"Ты финансовый аналитик ИИ-агентов. Ответь коротко и по-русски: {question}",
                "stream": False
            },
            timeout=15
        )
        return resp.json()["response"]
    except Exception as e:
        return f"Ошибка LLM: {str(e)}"

st.title("Платформа монетизации ИИ-агента с оплатой за результат")

prof = get_profitability_last_30d()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Выручка (30 дн)", f"{prof['revenue_rub']:,.0f} ₽")
col2.metric("Расходы на LLM", f"{prof['cost_rub']:,.0f} ₽")
col3.metric("Маржа", f"{prof['margin']:.1%}")
col4.metric("ROI", f"{(prof['revenue_rub']/prof['cost_rub']-1 if prof['cost_rub'] > 0 else 0):.1%}")

if prof['recommendation']:
    st.warning(prof['recommendation'])

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Аналитика", "Сравнение тарифов", "ИИ-ассистент"])

with tab1:
    st.subheader("Доходность по пользователям")
    fig = px.scatter(df, x="requests_count", y="mock_exam_score_after",
                     size="mock_exam_score_before", color="mock_exam_score_after",
                     hover_data=["user_id"])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Симуляция тарифов на исторических данных")
    revenues = {
        "Тариф": ["Подписка 499 руб/мес", "Оплата за результат"],
        "Выручка": [
            simulate_plan_revenue(df, subscription_plan),
            simulate_plan_revenue(df, pay_per_result_plan)
        ]
    }
    fig = px.bar(revenues, x="Тариф", y="Выручка", color="Тариф", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Задайте вопрос аналитику")
    question = st.text_input("Например: Почему маржа упала в октябре?")
    if question:
        with st.spinner("Анализирую..."):
            answer = ask_llm(question)
        st.write(answer)

st.sidebar.subheader("Экспорт отчёта для клиента")
user_id = st.sidebar.selectbox("Выберите пользователя", df['user_id'])
if st.sidebar.button("Генерировать отчёт"):
    row = df[df['user_id'] == user_id].iloc[0]
    time_saved = row['time_spent_hours']
    money_saved = time_saved * 240
    st.sidebar.success(f"Вы сэкономили {time_saved} часов и {money_saved:.0f} ₽ по сравнению с репетитором (240 ₽/час)")
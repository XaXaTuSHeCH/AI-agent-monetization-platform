# DA-1 — Платформа монетизации ИИ-агентов

MVP для монетизации ИИ-агентов с оплатой за результат.

## Установка
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`

## Запуск (после всех этапов)
- Бэкенд: `uvicorn app.main:app --reload`
- Дашборд: `streamlit run dashboard/app.py`
- Ollama (для ИИ-ассистента): Установи отдельно и запусти `ollama serve && ollama pull llama3.2:3b`
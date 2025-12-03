from fastapi import FastAPI
from .database import create_db_and_tables
from .api.routes import router

app = FastAPI(title="Платформа монетизации ИИ-агентов")

app.include_router(router, prefix="/api")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "DA-1 — Платформа монетизации ИИ-агентов готова!"}
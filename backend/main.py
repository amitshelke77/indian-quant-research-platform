from fastapi import FastAPI
from backend.api.health import router as health_router

app = FastAPI(
    title="Indian Quant Research Platform",
    version="1.0.0"
)

app.include_router(health_router)

@app.get("/")
def root():
    return {"status": "running"}
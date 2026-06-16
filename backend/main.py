from fastapi import FastAPI

app = FastAPI(
    title="Indian Quant Research Platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Indian Quant Research Platform"
    }
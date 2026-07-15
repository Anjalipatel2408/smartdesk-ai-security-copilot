from fastapi import FastAPI

app = FastAPI(title="SmartDesk AI — Security Intelligence Copilot")

@app.get("/health")
def health_check():
    return {"status": "OK", "service": "SmartDesk AI"}
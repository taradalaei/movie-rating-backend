from fastapi import FastAPI

app = FastAPI(title="Movie Rating System")

@app.get("/health")
def health():
    return {"status": "ok"}

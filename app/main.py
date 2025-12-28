from app.controller.movies import router as movies_router

from fastapi import FastAPI

app = FastAPI(title="Movie Rating System")

app.include_router(movies_router)

@app.get("/health")
def health():
    return {"status": "ok"}

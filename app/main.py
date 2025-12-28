from app.controller.movies_read import router as movies_read_router

from fastapi import FastAPI

app = FastAPI(title="Movie Rating System")

app.include_router(movies_read_router)

@app.get("/health")
def health():
    return {"status": "ok"}

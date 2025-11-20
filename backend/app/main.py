from fastapi import FastAPI
from app.routers import search, hacks, debug

app = FastAPI(title="Ikea Hacks IR API")

app.include_router(search.router)
app.include_router(hacks.router)
app.include_router(debug.router)

@app.get("/")
def root():
    return {"message": " backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


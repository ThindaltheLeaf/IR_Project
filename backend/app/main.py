from fastapi import FastAPI

from app.routers import search
from app.core.cors import setup_cors

app = FastAPI(title="Ikea Hacks IR API")

setup_cors(app)

app.include_router(search.router)

@app.get("/")
def root():
    return {"message": " backend is running"}




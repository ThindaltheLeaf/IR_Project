# app/core/cors.py
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

def _parse_origins(env_value: str) -> List[str]:
    """Parse comma-separated origins from env."""
    return [o.strip() for o in env_value.split(",") if o.strip()]

def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS for the given FastAPI app.
    Reads allowed origins from CORS_ALLOW_ORIGINS env var.
    """
    origins_env = os.getenv("CORS_ALLOW_ORIGINS")
    origins = _parse_origins(origins_env)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

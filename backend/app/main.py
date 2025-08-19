from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.database import engine
from app import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Force docs + openapi
app = FastAPI(
    docs_url="/docs",
    redoc_url=None,
    openapi_url="/openapi.json"
)

# Allow all origins for now (adjust later for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root redirect → docs
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


# Example healthcheck
@app.get("/health", tags=["System"])
def healthcheck():
    return {"status": "ok"}



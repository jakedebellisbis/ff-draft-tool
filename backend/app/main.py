from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers import leagues, players, adp, keepers, imports, availability, admin

# DB (for creating tables on startup)
from app.database import engine
from app.models import Base

app = FastAPI(
    title="FF Draft Tool API",
    version="1.0.0",
)

# CORS — allow local dev and hosted frontends (Render/Vercel).
# If you later know your exact Vercel URL, add it to allow_origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can tighten this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- ensure DB tables exist at container startup (Render, etc.) ----
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)
# --------------------------------------------------------------------

# Simple health/root endpoints
@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "app": "ff-draft-tool-api"}

@app.get("/healthz", tags=["health"])
def healthz():
    return {"ok": True}

# Attach routers (these files already exist in app/routers/)
app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(adp.router)
app.include_router(keepers.router)
app.include_router(imports.router)
app.include_router(availability.router)
app.include_router(admin.router)



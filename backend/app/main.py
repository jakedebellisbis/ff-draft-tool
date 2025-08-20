from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers import leagues, players, adp, keepers, imports, availability, admin

# DB + models (ensure tables exist)
from app.database import engine
from app.models import Base

# Seeding
from app import seed as seed_module

app = FastAPI()

# CORS for local dev + Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Do NOT add extra prefixes here — routers already have them
app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(adp.router)
app.include_router(keepers.router)
app.include_router(imports.router)
app.include_router(availability.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup_tasks():
    # Make sure DB tables exist on Render (Neon)
    Base.metadata.create_all(bind=engine)
    # Try to seed once (should be idempotent)
    try:
        seed_module.run()
        print("✅ Seeded data on startup (if empty).")
    except Exception as e:
        print(f"⚠️ Seeding skipped or failed: {e}")

# --- Health / root checks for Render ---
@app.get("/", tags=["health"])
def root():
    return {"status": "ok"}

@app.get("/healthz", tags=["health"])
def healthz():
    return {"status": "ok"}





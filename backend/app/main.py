from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers import leagues, players, adp, keepers, imports, availability, admin

# DB + models (to ensure tables exist)
from app.database import engine
from app.models import Base

# Seeding
from app import seed as seed_module

app = FastAPI()

# CORS (add your Vercel domain later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"ok": True}

# Include routers
app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(adp.router)
app.include_router(keepers.router)
app.include_router(imports.router)
app.include_router(availability.router)
app.include_router(admin.router)

# Ensure tables exist + try to seed once on startup
@app.on_event("startup")
def startup_tasks():
    # Make sure DB tables exist on Render (Neon)
    Base.metadata.create_all(bind=engine)

    # Try to seed (seed.run() should be idempotent or handle duplicates gracefully)
    try:
        seed_module.run()
        print("✅ Seeded data on startup (if empty).")
    except Exception as e:
        # Not fatal; just log
        print(f"⚠️ Seeding skipped or failed: {e}")





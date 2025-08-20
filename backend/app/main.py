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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "https://ff-draft-tool-sandy.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leagues.router, prefix="/leagues", tags=["leagues"])
app.include_router(players.router, prefix="/players", tags=["players"])
app.include_router(adp.router, prefix="/adp", tags=["adp"])
app.include_router(keepers.router, prefix="/keepers", tags=["keepers"])
app.include_router(imports.router, prefix="/imports", tags=["imports"])
app.include_router(availability.router, prefix="/availability", tags=["availability"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

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





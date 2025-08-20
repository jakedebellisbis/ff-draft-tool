from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routers import leagues, players, adp, keepers, imports, availability, admin

# DB + models (ensure tables exist on startup)
from app.database import engine
from app.models import Base

# Optional seeding
from app import seed as seed_module

app = FastAPI()

# CORS: local dev + Vercel
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

# Health & root
@app.get("/", include_in_schema=False)
def root():
    return {"ok": True, "message": "ff-draft-tool backend"}

@app.get("/health", include_in_schema=False)
def health():
    return {"ok": True, "service": "backend", "status": "up"}

# Routers
app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(adp.router)
app.include_router(keepers.router)
app.include_router(imports.router)
app.include_router(availability.router)
app.include_router(admin.router)

# Startup tasks: create tables and try to seed once
@app.on_event("startup")
def startup_tasks():
    Base.metadata.create_all(bind=engine)
    try:
        seed_module.run()
        print("✅ Seeded data on startup (if empty).")
    except Exception as e:
        print(f"⚠️ Seeding skipped or failed: {e}")

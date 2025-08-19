from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import leagues, players, adp, keepers, imports, availability, admin

app = FastAPI(title="FF Draft Tool")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# CORS for local dev + later Vercel site (add your Vercel domain when deployed)
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers (no extra prefixes; routers define their own)
app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(adp.router)
app.include_router(keepers.router)
app.include_router(imports.router)
app.include_router(availability.router)
app.include_router(admin.router)



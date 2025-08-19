from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ import all your routers
from app.routers import leagues, players, adp, keepers, imports, availability, admin

app = FastAPI()

# ✅ Allow the Vite dev server to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ register routers so endpoints exist (e.g., GET /leagues)
app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(adp.router)
app.include_router(keepers.router)
app.include_router(imports.router)
app.include_router(availability.router)
app.include_router(admin.router)


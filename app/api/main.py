from fastapi import FastAPI

from app.api.routers import players, teams, organizations
from app.db import engine, Base, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(organizations.router)


@app.get("/")
def root():
    return {"message": "SportCore API is running"}

from fastapi import FastAPI

from app.api.routers import players, teams
from app.db import engine, Base, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)


@app.get("/")
def root():
    return {"message": "SportCore API is running"}

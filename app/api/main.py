from fastapi import FastAPI

from app.api.routers import players, teams, organizations, trainings
from app.db import engine, Base, SessionLocal


app = FastAPI()

app.include_router(players.router)
app.include_router(teams.router)
app.include_router(organizations.router)
app.include_router(trainings.router)


@app.get("/")
def root():
    return {"message": "SportCore API is running"}

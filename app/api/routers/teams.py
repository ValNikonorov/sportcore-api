from fastapi import APIRouter, Depends

from app.api.schemas import TeamCreate, TeamResponse
from app.db import get_db

from app.services.team_service import create_team, get_all_teams, serialize_team

from sqlalchemy.orm import Session

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamResponse])
def get_teams_endpoint(db: Session = Depends(get_db)):
    return get_all_teams(session=db)


@router.post("/", response_model=TeamResponse)
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):

    new_team = create_team(
        session=db,
        name=team.name,
        city=team.city
    )

    return serialize_team(new_team)

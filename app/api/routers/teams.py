from fastapi import APIRouter, Response, HTTPException, Depends

from app.api.schemas import TeamCreate, TeamResponse, TeamPlayersResponse
from app.db import get_db

from app.services.team_service import create_team, get_all_teams, serialize_team, get_team_by_id, delete_team_by_id
from app.services.player_service import serialize_player
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
        city=team.city,
        organization_id=team.organization_id,
        age_group=team.age_group,
        level=team.level,
        gender=team.gender
    )

    return serialize_team(new_team)


@router.get("/{team_id}/players", response_model=TeamPlayersResponse)
def get_players_by_team_id_endpoint(team_id: int, db: Session = Depends(get_db)):

    team = get_team_by_id(db, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return {
        "organization_id": team.organization_id,
        "team_id": team.id,
        "team_name": team.name,
        "players": [
            serialize_player(player)
            for player in team.players
        ]
    }


@router.delete("/{team_id}")
def delete_team_by_id_endpoint(team_id: int, db: Session = Depends(get_db)):
    deleted_team = delete_team_by_id(
        session=db,
        team_id=team_id
    )

    if deleted_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    if deleted_team is False:
        raise HTTPException(
            status_code=400, detail="Cannot delete team with players")

    return Response(status_code=204)

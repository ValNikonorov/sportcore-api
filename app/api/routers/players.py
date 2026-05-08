from datetime import date

from fastapi import APIRouter, Response, HTTPException, Depends

from app.api.schemas import PlayerCreate, PlayerWeightUpdate, PlayerResponse, PlayersListResponse
from app.db import get_db

from app.services.player_service import create_player, get_all_players, get_player_by_id, serialize_player, update_player_weight_by_id, delete_player_by_id

from sqlalchemy.orm import Session

router = APIRouter(prefix="/players", tags=["players"])


@router.get("/", response_model=PlayersListResponse)
def get_players(
    team_id: int | None = None,
    position: str | None = None,
    search: str | None = None,
    sort_by: str | None = None,
    order: str = "asc",
    limit: int = 4,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    players = get_all_players(
        session=db,
        team_id=team_id,
        position=position,
        search=search,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )
    return players


@router.post("/", response_model=PlayerResponse)
def create_player_endpoint(player: PlayerCreate, db: Session = Depends(get_db)):

    new_player = create_player(
        session=db,
        first_name=player.first_name,
        last_name=player.last_name,
        birth_date=date.fromisoformat(player.birth_date),
        team_id=player.team_id,
        position=player.position,
        weight=player.weight,
    )

    return serialize_player(new_player)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player_by_id_endpoint(player_id: int, db: Session = Depends(get_db)):

    found_player_by_id = get_player_by_id(db, player_id)
    if not found_player_by_id:
        raise HTTPException(status_code=404, detail="Player not found")
    return serialize_player(found_player_by_id)


@router.patch("/{player_id}/weight", response_model=PlayerResponse)
def update_player_weight_endpoint(player_id: int, data: PlayerWeightUpdate, db: Session = Depends(get_db)):

    updated_player = update_player_weight_by_id(
        session=db,
        player_id=player_id,
        weight=data.weight,
    )

    if not updated_player:
        raise HTTPException(status_code=404, detail="Player not found")

    return serialize_player(updated_player)


@router.delete("/{player_id}")
def delete_player_by_id_endpoint(player_id: int, db: Session = Depends(get_db)):

    deleted_player = delete_player_by_id(
        session=db,
        player_id=player_id
    )
    if not deleted_player:
        raise HTTPException(status_code=404, detail="Player not found")
    return Response(status_code=204)

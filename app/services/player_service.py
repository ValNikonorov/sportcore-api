from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.player import Player
from app.models.team import Team
from app.models.organization import Organization


def get_player_by_identity_fields(
    session: Session,
    first_name: str,
    last_name: str,
    birth_date: date,
    team_id: int,
):
    return (
        session.query(Player)
        .filter_by(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            team_id=team_id,
        )
        .first()
    )


def create_player(
        session: Session,
        first_name: str,
        last_name: str,
        birth_date: date,
        team_id: int,
        weight: float | None = None,
        position: str | None = None):
    existing = get_player_by_identity_fields(
        session=session,
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        team_id=team_id,
    )

    if existing:
        return existing
    else:
        new_player = Player(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            team_id=team_id,
            weight=weight,
            position=position
        )
        session.add(new_player)
        session.commit()

        return new_player


def serialize_player(player: Player) -> dict:
    return {
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "birth_date": str(player.birth_date),
        "team_id": player.team_id,
        "weight": player.weight,
        "height": player.height,
        "position": player.position
    }


def serialize_player_detail(player: Player) -> dict:
    return {
        "id": player.id,
        "first_name": player.first_name,
        "last_name": player.last_name,
        "birth_date": str(player.birth_date),
        "weight": player.weight,
        "height": player.height,
        "position": player.position,
        "team_id": player.team_id,
        "team_name": player.team.name if player.team else None,
        "organization_id": player.team.organization_id if player.team else None,
        "organization_name":  (
            player.team.organization.name
            if player.team and player.team.organization
            else None
        )
    }


def get_all_players(
        session: Session,
        team_id: int | None = None,
        position: str | None = None,
        limit: int = 4,
        offset: int = 0,
        sort_by: str | None = None,
        order: str = "asc",
        search: str | None = None,
):
    query = session.query(Player)

    if team_id is not None:
        query = query.filter(Player.team_id == team_id)

    if position is not None:
        query = query.filter(Player.position == position)

    total = query.count()

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Player.first_name.ilike(search_pattern),
                Player.last_name.ilike(search_pattern),
            )
        )

    allowed_sort_fields = {
        "first_name": Player.first_name,
        "last_name": Player.last_name,
        "weight": Player.weight,
        "birth_date": Player.birth_date,
    }

    if sort_by is not None:
        if sort_by in allowed_sort_fields:
            sort_column = allowed_sort_fields[sort_by]
            if order == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())

    query = query.limit(limit).offset(offset)

    players = query.all()

    return {
        "total": total,
        "items": [serialize_player(player) for player in players]
    }


def get_player_by_id(
    session: Session,
    player_id: int
):
    return session.query(Player).filter(Player.id == player_id).first()


def update_player_weight_by_id(
        session: Session,
        player_id: int,
        weight: float,
):
    player = get_player_by_id(session, player_id)
    if not player:
        return None

    player.weight = weight
    session.commit()

    return player


def delete_player_by_id(session, player_id):
    player = get_player_by_id(session, player_id)
    if not player:
        return None

    session.delete(player)
    session.commit()
    return player

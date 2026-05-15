from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.team import Team


def get_team_by_identity_fields(
    session: Session,
    name: str,
    city: str
):
    return (
        session.query(Team)
        .filter_by(
            name=name,
            city=city
        )
        .first()
    )


def serialize_team(team: Team):
    return {
        "id": team.id,
        "name": team.name,
        "city": team.city,
    }


def create_team(
    session: Session,
    name: str,
    city: str
):
    existing = get_team_by_identity_fields(
        session=session,
        name=name,
        city=city
    )
    if existing:
        return existing
    else:
        new_team = Team(
            name=name,
            city=city
        )
        session.add(new_team)
        session.commit()
        session.refresh(new_team)

        return new_team


def get_all_teams(
        session: Session,
):
    query = session.query(Team)
    teams = query.all()

    return [serialize_team(team) for team in teams]


def get_team_by_id(
        session: Session,
        team_id: int
):
    return session.query(Team).filter(Team.id == team_id).first()


def delete_team_by_id(session, team_id):
    team = get_team_by_id(session, team_id)
    if not team:
        return None

    if team.players:
        return False

    session.delete(team)
    session.commit()
    return team

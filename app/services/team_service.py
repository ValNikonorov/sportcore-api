from sqlalchemy.orm import Session


from app.models.team import Team
from app.services.organization_service import get_organization_by_id


def get_team_by_identity_fields(
    session: Session,
    name: str,
    organization_id: int
):
    return (
        session.query(Team)
        .filter_by(
            name=name,
            organization_id=organization_id
        )
        .first()
    )


def serialize_team(team: Team):
    return {
        "id": team.id,
        "name": team.name,
        "city": team.city,
        "gender": team.gender,
        "organization_id": team.organization_id,
        "organization_name": team.organization.name if team.organization else None,
        "age_group": team.age_group,
        "level": team.level
    }


def create_team(
    session: Session,
    name: str,
    city: str,
    age_group: str,
    level: str,
    organization_id: int,
    gender: str
):
    organization = get_organization_by_id(session, organization_id)

    if not organization:
        return False

    existing = get_team_by_identity_fields(
        session=session,
        name=name,
        organization_id=organization_id
    )

    if existing:
        return existing
    else:
        new_team = Team(
            name=name,
            city=city,
            age_group=age_group,
            level=level,
            organization_id=organization_id,
            gender=gender
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

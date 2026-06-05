from sqlalchemy.orm import Session

from app.models.organization import Organization

from app.services.player_service import serialize_player


def get_organization_by_identify_fields(
        session: Session,
        name: str,
        city: str,
        organization_type: str
):
    return (
        session.query(Organization)
        .filter_by(
            name=name,
            city=city,
            organization_type=organization_type
        )
        .first()
    )


def serialize_organization(organization: Organization):
    return {
        "id": organization.id,
        "name": organization.name,
        "city": organization.city,
        "organization_type": organization.organization_type
    }


def create_organization(
        session: Session,
        name: str,
        city: str,
        organization_type: str
):
    existing = get_organization_by_identify_fields(
        session=session,
        name=name,
        city=city,
        organization_type=organization_type
    )

    if existing:
        return existing
    else:
        new_organization = Organization(
            name=name,
            city=city,
            organization_type=organization_type
        )
        session.add(new_organization)
        session.commit()
        session.refresh(new_organization)

        return new_organization


def get_all_organizations(
        session: Session,
):
    query = session.query(Organization)
    organizations = query.all()

    return [serialize_organization(organization) for organization in organizations]


def get_organization_by_id(
        session: Session,
        organization_id: int
):
    return session.query(Organization).filter(Organization.id == organization_id).first()


def delete_organization_by_id(session, organization_id):
    pass


def get_organization_players(session: Session, organization_id: int):
    organization = get_organization_by_id(session, organization_id)

    if not organization:
        return None

    players = []

    for team in organization.teams:
        players.extend(team.players)

    return {
        "organization_id": organization.id,
        "organization_name": organization.name,
        "organization_type": organization.organization_type,
        "city": organization.city,
        "players": [
            serialize_player(player)
            for player in players
        ]
    }

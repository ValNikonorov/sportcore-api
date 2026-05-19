from fastapi import APIRouter, Response, HTTPException, Depends

from app.api.schemas import OrganizationCreate, OrganizationResponse, OrganizationTeamsResponse

from app.db import get_db

from app.services.organization_service import create_organization, get_all_organizations, serialize_organization, get_organization_by_id

from app.services.team_service import serialize_team

from sqlalchemy.orm import Session

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/", response_model=list[OrganizationResponse])
def get_organizations_endpoint(db: Session = Depends(get_db)):
    return get_all_organizations(session=db)


@router.post("/", response_model=OrganizationResponse)
def create_organization_endpoint(organization: OrganizationCreate, db: Session = Depends(get_db)):

    new_organization = create_organization(
        session=db,
        name=organization.name,
        city=organization.city,
        organization_type=organization.organization_type
    )

    return serialize_organization(new_organization)


@router.get("/{organization_id}/teams", response_model=OrganizationTeamsResponse)
def get_teams_by_organization_id_endpoint(organization_id: int, db: Session = Depends(get_db)):
    organization = get_organization_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return {
        "organization_id": organization.id,
        "organization_name": organization.name,
        "organization_type": organization.organization_type,
        "city": organization.city,
        "teams": [
            serialize_team(team)
            for team in organization.teams
        ]
    }

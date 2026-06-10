from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    birth_date: str
    team_id: int = Field(gt=0)
    weight: float = Field(gt=0)
    height: float = Field(gt=0)
    position: str | None = None


class PlayerWeightUpdate(BaseModel):
    weight: float = Field(gt=0)


class PlayerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: str
    team_id: int
    weight: float | None = None
    height: float | None = None
    position: str | None = None


class PlayersListResponse(BaseModel):
    total: int
    items: list[PlayerResponse]


class PlayerDetailResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: str
    position: str | None = None
    weight: float | None = None
    height: float | None = None
    team_id: int
    team_name: str | None = None
    organization_id: int | None = None
    organization_name: str | None = None


class TeamCreate(BaseModel):
    name: str = Field(min_length=1)
    organization_id: int
    gender: str
    age_group: str | None = None
    level: str | None = None
    city: str | None = None
    gender: str | None = None


class TeamResponse(BaseModel):
    id: int
    name: str
    city: str | None = None
    gender: str
    organization_id: int
    organization_name: str
    age_group: str | None = None
    level: str | None = None


class TeamPlayersResponse(BaseModel):
    team_id: int
    team_name: str
    players: list[PlayerResponse]


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1)
    city: str = Field(min_length=1)
    organization_type: str = Field(min_length=1)


class OrganizationResponse(BaseModel):
    id: int
    name: str
    city: str
    organization_type: str


class OrganizationTeamsResponse(BaseModel):
    organization_id: int
    organization_name: str
    organization_type: str
    city: str
    teams: list[TeamResponse]


class OrganizationPlayersResponse(BaseModel):
    organization_id: int
    organization_name: str
    organization_type: str
    city: str
    players: list[PlayerResponse]

from pydantic import BaseModel, Field


class PlayerCreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    birth_date: str
    team_id: int = Field(gt=0)
    weight: float = Field(gt=0)
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
    position: str | None = None


class PlayersListResponse(BaseModel):
    total: int
    items: list[PlayerResponse]


class TeamCreate(BaseModel):
    name: str = Field(min_length=1)
    city: str = Field(min_length=1)


class TeamResponse(BaseModel):
    id: int
    name: str
    city: str


class TeamPlayersResponse(BaseModel):
    team_id: int
    team_name: str
    players: list[PlayerResponse]

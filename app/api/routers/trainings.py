from fastapi import APIRouter, HTTPException, Depends

from app.api.schemas import TrainingCreate, TrainingResponse, TeamTrainingsResponse

from app.db import get_db

from app.services.training_service import create_training, get_all_trainings, get_team_trainings, serialize_training

from sqlalchemy.orm import Session

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.get("/", response_model=list[TrainingResponse])
def get_trainings_endpoint(db: Session = Depends(get_db)):
    return get_all_trainings(session=db)


@router.post("/", response_model=TrainingResponse)
def create_training_endpoint(training: TrainingCreate, db: Session = Depends(get_db)):

    new_training = create_training(
        session=db,
        team_ids=training.team_ids,
        title=training.title,
        training_type=training.training_type,
        start_time=training.start_time,
        end_time=training.end_time,
        location=training.location,
    )
    if new_training == "invalid_time":
        raise HTTPException(status_code=400, detail="Invalid training time")
    if new_training == "team_not_found":
        raise HTTPException(
            status_code=404, detail="One or more of the teams were not found")
    if new_training == "time_conflict":
        raise HTTPException(
            status_code=400, detail="Training have time conflict with other training")

    return serialize_training(new_training)


@router.get("/teams/{team_id}/trainings", response_model=TeamTrainingsResponse)
def get_team_trainings_by_team_id(team_id: int, db: Session = Depends(get_db)):
    result = get_team_trainings(db, team_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Team not found")

    team, trainings = result
    return {
        "team_id": team.id,
        "team_name": team.name,
        "trainings": [
            serialize_training(training)
            for training in trainings
        ]
    }

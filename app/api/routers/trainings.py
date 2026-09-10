from fastapi import APIRouter, HTTPException, Depends

from app.api.schemas import TrainingCreate, TrainingResponse, TeamTrainingsResponse, TrainingUpdate

from app.db import get_db

from app.services.training_service import create_training, get_all_trainings, get_team_trainings, serialize_training, update_training_by_id, delete_training_by_id

from sqlalchemy.orm import Session

router = APIRouter(prefix="/trainings", tags=["trainings"])


@router.get("/", response_model=list[TrainingResponse])
def get_trainings_endpoint(db: Session = Depends(get_db)):
    return get_all_trainings(session=db)


@router.post("/", response_model=TrainingResponse)
def create_training_endpoint(training: TrainingCreate, db: Session = Depends(get_db)):

    updated_training = create_training(
        session=db,
        team_ids=training.team_ids,
        title=training.title,
        training_type=training.training_type,
        start_time=training.start_time,
        end_time=training.end_time,
        location=training.location,
    )
    if updated_training == "invalid_time":
        raise HTTPException(status_code=400, detail="Invalid training time")
    if updated_training == "team_not_found":
        raise HTTPException(
            status_code=404, detail="One or more of the teams were not found")
    if updated_training == "time_conflict":
        raise HTTPException(
            status_code=400, detail="Training have time conflict with other training")

    return serialize_training(updated_training)


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


@router.patch("/{training_id}", response_model=TrainingResponse)
def update_training_by_training_id(training_id: int, training: TrainingUpdate, db: Session = Depends(get_db)):
    updated_training = update_training_by_id(
        session=db,
        training_id=training_id,
        team_ids=training.team_ids,
        title=training.title,
        training_type=training.training_type,
        location=training.location,
        start_time=training.start_time,
        end_time=training.end_time,
    )

    if updated_training is None:
        raise HTTPException(status_code=404, detail="Training not found")
    if updated_training == "invalid_time":
        raise HTTPException(status_code=400, detail="Invalid training time")
    if updated_training == "team_not_found":
        raise HTTPException(
            status_code=404, detail="One or more of the teams were not found")
    if updated_training == "time_conflict":
        raise HTTPException(
            status_code=400, detail="Training have time conflict with other training")
    if updated_training == "location_conflict":
        raise HTTPException(
            status_code=400, detail="Training location is already occupied at this time")

    return serialize_training(updated_training)


@router.delete("/{training_id}")
def delete_training_by_id_endpoint(training_id: int, db: Session = Depends(get_db)):
    deleted_training = delete_training_by_id(
        session=db,
        training_id=training_id
    )
    if deleted_training is None:
        raise HTTPException(
            status_code=404, detail="Training not found")

    return {
        "detail": "Training deleted"
    }

from datetime import datetime
from sqlalchemy.orm import Session

from app.models.training import Training
from app.models.team import Team

from app.services.team_service import serialize_team


def get_overlapping_training(
    session: Session,
    team_ids: list[int],
    start_time: datetime,
    end_time: datetime,
):
    return (
        session.query(Training)

        .filter(
            Team.id.in_(team_ids),
            Training.start_time < end_time,
            Training.end_time > start_time,
        )
        .first()
    )


def create_training(
        session: Session,
        team_ids: list[int],
        title: str,
        training_type: str,
        start_time: datetime,
        end_time: datetime,
        location: str | None = None,

):
    if end_time <= start_time:
        return "invalid_time"

    teams = (
        session.query(Team)
        .filter(Team.id.in_(team_ids))
        .all()
    )

    if len(teams) != len(set(team_ids)):
        return "team_not_found"

    overlapping = get_overlapping_training(
        session=session,
        team_ids=team_ids,
        start_time=start_time,
        end_time=end_time,
    )

    if overlapping:
        return "time_conflict"

    new_training = Training(
        title=title,
        training_type=training_type,
        location=location,
        start_time=start_time,
        end_time=end_time,
    )

    new_training.teams = teams

    session.add(new_training)
    session.commit()
    session.refresh(new_training)

    return new_training


def get_all_trainings(
        session: Session,
):
    query = session.query(Training)
    trainings = query.all()

    return [serialize_training(training) for training in trainings]


def get_team_trainings(
    session: Session,
    team_id: int,
):
    team = session.query(Team).filter(Team.id == team_id).first()

    if not team:
        return None

    trainings = session.query(Training).join(Training.teams).filter(
        Team.id == team_id).order_by(Training.start_time).all()

    return team, trainings


def serialize_training(training: Training):
    return {
        "id": training.id,
        "team_ids": [team.id for team in training.teams],
        "teams": [serialize_team(team) for team in training.teams],
        "title": training.title,
        "training_type": training.training_type,
        "location": training.location,
        "start_time": training.start_time,
        "end_time": training.end_time
    }

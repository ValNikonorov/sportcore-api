from datetime import date, datetime, time, timedelta
from sqlalchemy.orm import Session

from app.models.training import Training
from app.models.team import Team

from app.services.team_service import serialize_team

from datetime import date


def get_overlapping_training(
    session: Session,
    team_ids: list[int],
    start_time: datetime,
    end_time: datetime,
    exclude_training_id: int | None = None,
):

    query = (
        session.query(Training)
        .join(Training.teams)
        .filter(
            Team.id.in_(team_ids),
            Training.start_time < end_time,
            Training.end_time > start_time,
        )
    )
    if exclude_training_id is not None:
        query = query.filter(
            Training.id != exclude_training_id
        )

    return query.first()


def get_overlapping_training_by_location(
    session: Session,
    location: str,
    start_time: datetime,
    end_time: datetime,
    exclude_training_id: int | None = None,
):
    query = (
        session.query(Training)
        .filter(
            Training.location == location,
            Training.start_time < end_time,
            Training.end_time > start_time,
        )
    )

    if exclude_training_id is not None:
        query = query.filter(
            Training.id != exclude_training_id
        )

    return query.first()


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

    if location is not None:

        location_conflict = get_overlapping_training_by_location(
            session=session,
            location=location,
            start_time=start_time,
            end_time=end_time,
        )

        if location_conflict:
            return "location_conflict"

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


def update_training_by_id(
    session: Session,
    training_id: int,
    team_ids: list[int] | None = None,
    title: str | None = None,
    training_type: str | None = None,
    location: str | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,

):
    training = (
        session.query(Training)
        .filter(Training.id == training_id)
        .first()
    )

    if not training:
        return None

    new_start_time = start_time if start_time is not None else training.start_time

    new_end_time = end_time if end_time is not None else training.end_time

    if new_end_time <= new_start_time:
        return "invalid_time"

    if team_ids is not None:

        teams = (session.query(Team)
                 .filter(Team.id.in_(team_ids))
                 .all()
                 )
        if len(teams) != len(set(team_ids)):
            return "team_not_found"

        new_teams = teams
    else:
        new_teams = training.teams

    overlapping = get_overlapping_training(
        session=session,
        team_ids=[team.id for team in new_teams],
        start_time=new_start_time,
        end_time=new_end_time,
        exclude_training_id=training_id,
    )

    if overlapping:
        return "time_conflict"

    location_conflict = get_overlapping_training_by_location(
        session=session,
        location=location if location is not None else training.location,
        start_time=new_start_time,
        end_time=new_end_time,
        exclude_training_id=training_id,
    )

    if location_conflict:
        return "location_conflict"

    training.start_time = new_start_time
    training.end_time = new_end_time
    training.teams = new_teams
    if title is not None:
        training.title = title

    if training_type is not None:
        training.training_type = training_type

    if location is not None:
        training.location = location

    session.commit()
    session.refresh(training)

    return training


def delete_training_by_id(
    session: Session,
    training_id: int,
):
    training = (
        session.query(Training)
        .filter(Training.id == training_id)
        .first()
    )

    if not training:
        return None

    session.delete(training)
    session.commit()
    return training


def get_trainings_by_date(
    session: Session,
    training_date: date,
):
    day_start = datetime.combine(training_date, time.min)
    next_day_start = day_start + timedelta(days=1)

    day_schedule = (
        session.query(Training)
        .filter(
            Training.start_time >= day_start,
            Training.start_time < next_day_start,
        )
        .order_by(Training.start_time)
        .all()
    )

    return day_schedule

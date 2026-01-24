from flask_login import current_user
from project import db
from project.models import ActivityLog

def log_event(
    *,
    action: str,
    target_type: str,
    target_id: int,
    actor=None,
    details: dict | None = None
):
    """
    Records an immutable system event.
    Does NOT commit — caller controls the transaction.
    """

    if actor is None:
        actor = current_user

    event = ActivityLog(
        actor_id=actor.id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details
    )

    db.session.add(event)